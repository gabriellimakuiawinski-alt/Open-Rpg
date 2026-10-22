-- =====================================================================
-- OPEN RPG — ETAPA 4: efeitos sonoros para todos, PV/PE/SAN sincronizados
--             entre token e ficha, notas do jogador
--
-- COMO USAR: rode DEPOIS do schema_etapa3b_musica.sql, no SQL Editor do
-- Supabase (New query -> colar tudo -> Run). Pode rodar de novo sem quebrar nada.
-- =====================================================================

-- ---------- 1. Efeitos sonoros: os jogadores da mesa podem abrir os EFEITOS ----------
-- (as músicas da biblioteca continuam só do mestre, exceto a que está tocando)
drop policy if exists arquivos_ver on public.arquivos;
create policy arquivos_ver on public.arquivos for select to authenticated
  using ((tipo = 'aud' and public.eh_mestre(mesa_id))
         or (tipo <> 'aud' and public.pode_gerir(mesa_id))
         or (criado_por = auth.uid() and public.eh_membro(mesa_id))
         or (tipo <> 'aud' and public.arquivo_em_uso(id))
         or (tipo = 'aud' and efeito and public.eh_membro(mesa_id))
         or (tipo = 'aud' and public.musica_em_uso(id)));

-- ---------- 2. PV / PE / SAN: token <-> ficha ----------
-- Na ficha as barras são os itens de "stats" com id/nome pv, pe, san.
-- No token ficam em dados: hp/pv (vida atual/máx), mn/mm (PE), sn/sm (SAN).

create or replace function public.stats_aplica(d jsonb, k text, cur jsonb, mx jsonb)
returns jsonb language plpgsql immutable as $$
declare r jsonb := coalesce(d->'stats','[]'::jsonb); e jsonb; i int := 0; idx int := null;
begin
  if jsonb_typeof(r) <> 'array' then return d; end if;
  for e in select jsonb_array_elements(r) loop
    if lower(coalesce(e->>'id','')) = k or lower(coalesce(e->>'n','')) = k then idx := i; exit; end if;
    i := i + 1;
  end loop;
  if idx is null then return d; end if;
  if cur is not null and jsonb_typeof(cur) = 'number' then r := jsonb_set(r, array[idx::text,'cur'], cur); end if;
  if mx  is not null and jsonb_typeof(mx)  = 'number' then r := jsonb_set(r, array[idx::text,'max'], mx);  end if;
  return jsonb_set(coalesce(d,'{}'::jsonb), '{stats}', r);
end $$;

create or replace function public.stat_de(d jsonb, k text)
returns jsonb language sql immutable as $$
  select e from jsonb_array_elements(case when jsonb_typeof(d->'stats')='array' then d->'stats' else '[]'::jsonb end) e
  where lower(coalesce(e->>'id','')) = k or lower(coalesce(e->>'n','')) = k limit 1
$$;

-- valores da ficha no formato do token (só o que existe na ficha)
create or replace function public.barras_da_ficha(d jsonb) returns jsonb
language sql immutable as $$
  select jsonb_strip_nulls(jsonb_build_object(
    'hp', public.stat_de(d,'pv')->'cur',  'pv', public.stat_de(d,'pv')->'max',
    'mn', public.stat_de(d,'pe')->'cur',  'mm', public.stat_de(d,'pe')->'max',
    'sn', public.stat_de(d,'san')->'cur', 'sm', public.stat_de(d,'san')->'max'))
$$;

-- (a) ao ligar um token a uma ficha, o token assume as barras da ficha
create or replace function public.token_adota_ficha() returns trigger
language plpgsql security definer set search_path = public as $$
declare f jsonb;
begin
  if new.personagem_id is null then return new; end if;
  if tg_op = 'UPDATE' and old.personagem_id is not distinct from new.personagem_id then return new; end if;
  select dados into f from public.personagens where id = new.personagem_id;
  if f is not null then new.dados := coalesce(new.dados,'{}'::jsonb) || public.barras_da_ficha(f); end if;
  return new;
end $$;
drop trigger if exists token_adota_ficha on public.tokens;
create trigger token_adota_ficha before insert or update of personagem_id on public.tokens
  for each row execute function public.token_adota_ficha();

-- (b) token mudou -> atualiza a ficha (só se quem mexeu pode editar aquela ficha)
create or replace function public.token_para_ficha() returns trigger
language plpgsql security definer set search_path = public as $$
declare p public.personagens%rowtype; nd jsonb;
begin
  if new.personagem_id is null then return new; end if;
  if tg_op = 'UPDATE' and old.personagem_id is not distinct from new.personagem_id
     and (new.dados->'hp', new.dados->'pv', new.dados->'mn', new.dados->'mm', new.dados->'sn', new.dados->'sm')
         is not distinct from
         (old.dados->'hp', old.dados->'pv', old.dados->'mn', old.dados->'mm', old.dados->'sn', old.dados->'sm')
  then return new; end if;
  if tg_op = 'UPDATE' and old.personagem_id is distinct from new.personagem_id then return new; end if; -- ligação nova: a ficha manda
  select * into p from public.personagens where id = new.personagem_id;
  if not found then return new; end if;
  if auth.uid() is not null and not (p.user_id = auth.uid() or public.c_mestre(p.campanha_id)
       or (p.campanha_id is not null and public.c_gerir(p.campanha_id) and not p.privada and not p.npc)) then
    return new;
  end if;
  nd := p.dados;
  nd := public.stats_aplica(nd,'pv',  new.dados->'hp', new.dados->'pv');
  nd := public.stats_aplica(nd,'pe',  new.dados->'mn', new.dados->'mm');
  nd := public.stats_aplica(nd,'san', new.dados->'sn', new.dados->'sm');
  if nd is distinct from p.dados then update public.personagens set dados = nd where id = p.id; end if;
  return new;
end $$;
drop trigger if exists token_para_ficha on public.tokens;
create trigger token_para_ficha after insert or update of dados, personagem_id on public.tokens
  for each row execute function public.token_para_ficha();

-- (c) ficha mudou -> atualiza todos os tokens ligados a ela
create or replace function public.ficha_para_tokens() returns trigger
language plpgsql security definer set search_path = public as $$
declare b jsonb := public.barras_da_ficha(new.dados);
begin
  if b = '{}'::jsonb then return new; end if;
  if public.barras_da_ficha(old.dados) is not distinct from b then return new; end if;
  update public.tokens t set dados = coalesce(t.dados,'{}'::jsonb) || b
   where t.personagem_id = new.id and (coalesce(t.dados,'{}'::jsonb) || b) is distinct from t.dados;
  return new;
end $$;
drop trigger if exists ficha_para_tokens on public.personagens;
create trigger ficha_para_tokens after update of dados on public.personagens
  for each row execute function public.ficha_para_tokens();

-- ---------- 3. Notas do jogador (privadas, uma por pessoa em cada mesa) ----------
create table if not exists public.notas_jogador (
  mesa_id uuid not null references public.mesas(id) on delete cascade,
  user_id uuid not null references auth.users(id) on delete cascade,
  texto text not null default '',
  atualizado_em timestamptz not null default now(),
  primary key (mesa_id, user_id)
);
alter table public.notas_jogador enable row level security;
drop policy if exists notas_jogador_minhas on public.notas_jogador;
create policy notas_jogador_minhas on public.notas_jogador for all to authenticated
  using (user_id = auth.uid() and public.eh_membro(mesa_id))
  with check (user_id = auth.uid() and public.eh_membro(mesa_id));
grant select, insert, update, delete on public.notas_jogador to authenticated;
