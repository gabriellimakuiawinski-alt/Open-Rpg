-- =====================================================================
-- OPEN RPG — ETAPA 5: sistema por campanha, dinheiro, lojas, homebrews
--             e luz do token automática pelo inventário
--
-- COMO USAR: rode DEPOIS do schema_etapa4.sql, no SQL Editor do Supabase
-- (New query -> colar tudo -> Run). Pode rodar de novo sem quebrar nada.
-- =====================================================================

-- ---------- 1. Sistema da campanha ----------
-- sistema: 'op' (Ordem Paranormal, ficha automática) ou 'modular' (ficha 100% editável)
-- config: opções do sistema, ex.: {"moeda":"R$","determinacao":false}
alter table public.campanhas add column if not exists sistema text not null default 'op';
alter table public.campanhas add column if not exists config jsonb not null default '{}'::jsonb;
do $$ begin
  alter table public.campanhas add constraint campanhas_sistema_ok check (sistema in ('op', 'modular'));
exception when duplicate_object then null; end $$;

-- ---------- 2. Dinheiro do personagem (só o mestre ou uma compra mexe) ----------
alter table public.personagens add column if not exists dinheiro numeric not null default 0;

create or replace function public.ficha_dinheiro_protegido() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  if new.dinheiro is distinct from old.dinheiro and auth.uid() is not null
     and coalesce(current_setting('openrpg.compra', true), '') <> '1'
     and not public.c_mestre(old.campanha_id) then
    raise exception 'Só o mestre da campanha muda o dinheiro';
  end if;
  if new.dinheiro < 0 then raise exception 'Dinheiro não pode ficar negativo'; end if;
  return new;
end $$;
drop trigger if exists ficha_dinheiro_protegido on public.personagens;
create trigger ficha_dinheiro_protegido before update of dinheiro on public.personagens
  for each row execute function public.ficha_dinheiro_protegido();

-- ficha nova começa sem dinheiro (só o mestre dá)
create or replace function public.ficha_nova_sem_dinheiro() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  if auth.uid() is not null and not public.c_mestre(new.campanha_id) then new.dinheiro := 0; end if;
  return new;
end $$;
drop trigger if exists ficha_nova_sem_dinheiro on public.personagens;
create trigger ficha_nova_sem_dinheiro before insert on public.personagens
  for each row execute function public.ficha_nova_sem_dinheiro();

-- ---------- 3. Lojas ----------
create table if not exists public.lojas (
  id uuid primary key default gen_random_uuid(),
  campanha_id uuid not null references public.campanhas(id) on delete cascade,
  nome text not null default 'Loja',
  descricao text not null default '',
  aberta boolean not null default false,   -- só lojas abertas aparecem para os jogadores
  ordem int not null default 0,
  criado_em timestamptz not null default now()
);
create index if not exists lojas_campanha_idx on public.lojas(campanha_id);

create table if not exists public.loja_itens (
  id uuid primary key default gen_random_uuid(),
  loja_id uuid not null references public.lojas(id) on delete cascade,
  item jsonb not null default '{}'::jsonb,  -- o item como vai para o inventário (nome, tipo, espaços, defesa, luz...)
  preco numeric not null default 0 check (preco >= 0),
  estoque int check (estoque is null or estoque >= 0),  -- null = ilimitado
  ordem int not null default 0,
  criado_em timestamptz not null default now()
);
create index if not exists loja_itens_loja_idx on public.loja_itens(loja_id);

create table if not exists public.loja_compras (
  id uuid primary key default gen_random_uuid(),
  campanha_id uuid not null references public.campanhas(id) on delete cascade,
  loja_id uuid references public.lojas(id) on delete set null,
  personagem_id uuid references public.personagens(id) on delete set null,
  user_id uuid references public.profiles(id) on delete set null,
  item_nome text not null default '',
  qtd int not null default 1,
  total numeric not null default 0,
  em timestamptz not null default now()
);
create index if not exists loja_compras_campanha_idx on public.loja_compras(campanha_id);

create or replace function public.loja_campanha(l uuid) returns uuid
language sql stable security definer set search_path = public as $$
  select campanha_id from public.lojas where id = l;
$$;
create or replace function public.loja_aberta(l uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select coalesce((select aberta from public.lojas where id = l), false);
$$;

-- Comprar: confere loja aberta, estoque, dono da ficha e saldo; desconta e põe no inventário
create or replace function public.comprar(p_item uuid, p_ficha uuid, p_qtd int default 1) returns void
language plpgsql security definer set search_path = public as $$
declare li public.loja_itens; lj public.lojas; p public.personagens; total numeric; it jsonb; itens jsonb; i int; achou boolean := false;
begin
  if auth.uid() is null then raise exception 'Faça login'; end if;
  if p_qtd is null or p_qtd < 1 or p_qtd > 999 then raise exception 'Quantidade inválida'; end if;
  select * into li from public.loja_itens where id = p_item for update;
  if not found then raise exception 'Item não encontrado'; end if;
  select * into lj from public.lojas where id = li.loja_id;
  if not lj.aberta and not public.c_mestre(lj.campanha_id) then raise exception 'Esta loja está fechada'; end if;
  select * into p from public.personagens where id = p_ficha for update;
  if not found then raise exception 'Ficha não encontrada'; end if;
  if p.campanha_id is distinct from lj.campanha_id then raise exception 'Esta ficha não é desta campanha'; end if;
  if p.user_id <> auth.uid() and not public.c_mestre(lj.campanha_id) then raise exception 'Só o dono da ficha compra para ela'; end if;
  if li.estoque is not null and li.estoque < p_qtd then raise exception 'Estoque insuficiente'; end if;
  total := li.preco * p_qtd;
  if p.dinheiro < total then raise exception 'Dinheiro insuficiente'; end if;

  itens := case when jsonb_typeof(p.dados->'inv'->'items') = 'array' then p.dados->'inv'->'items' else '[]'::jsonb end;
  -- mesmo item da mesma loja já no inventário: soma a quantidade
  for i in 0 .. jsonb_array_length(itens) - 1 loop
    if itens->i->>'ref' = li.id::text then
      itens := jsonb_set(itens, array[i::text, 'qtd'],
                 to_jsonb(coalesce(case when (itens->i->>'qtd') ~ '^[0-9.]+$' then (itens->i->>'qtd')::numeric end, 0) + p_qtd));
      achou := true; exit;
    end if;
  end loop;
  if not achou then
    it := coalesce(li.item, '{}'::jsonb) || jsonb_build_object('id', substr(md5(random()::text), 1, 8), 'qtd', p_qtd, 'ref', li.id::text, 'eq', false);
    itens := itens || jsonb_build_array(it);
  end if;

  if li.estoque is not null then update public.loja_itens set estoque = estoque - p_qtd where id = li.id; end if;
  perform set_config('openrpg.compra', '1', true);
  update public.personagens
     set dinheiro = dinheiro - total,
         dados = jsonb_set(case when jsonb_typeof(coalesce(dados->'inv', 'null')) = 'object' then dados
                                else jsonb_set(coalesce(dados, '{}'::jsonb), '{inv}', '{"items":[]}'::jsonb) end,
                           '{inv,items}', itens)
   where id = p.id;
  perform set_config('openrpg.compra', '', true);
  insert into public.loja_compras(campanha_id, loja_id, personagem_id, user_id, item_nome, qtd, total)
    values (lj.campanha_id, lj.id, p.id, auth.uid(), coalesce(li.item->>'n', ''), p_qtd, total);
end $$;
grant execute on function public.comprar(uuid, uuid, int) to authenticated;

-- ---------- 4. Catálogo da campanha (homebrews e itens próprios) ----------
create table if not exists public.catalogo (
  id uuid primary key default gen_random_uuid(),
  campanha_id uuid not null references public.campanhas(id) on delete cascade,
  tipo text not null default 'habilidade' check (tipo in ('habilidade', 'item')),
  nome text not null default '',
  dados jsonb not null default '{}'::jsonb,
  aprovado boolean not null default false,   -- homebrew de jogador precisa do ok do mestre
  criado_por uuid references public.profiles(id) on delete set null,
  criado_em timestamptz not null default now()
);
create index if not exists catalogo_campanha_idx on public.catalogo(campanha_id);

-- ---------- 5. Luz do token pelo inventário (Ordem Paranormal) ----------
-- No inventário, um item com "luz": {"t":"c","m":9} é lanterna (cone de 9 m);
-- {"t":"l","m":6} é lampião (raio de 6 m). O token usa a MELHOR fonte que a ficha tem.
-- Sem fonte do tipo escolhido, a luz não liga. O jogador não escolhe o alcance.
create or replace function public.num_ou(t text, d numeric) returns numeric
language sql immutable as $$
  select case when t ~ '^\s*-?[0-9]+(\.[0-9]+)?\s*$' then t::numeric else d end
$$;

create or replace function public.luz_da_ficha(d jsonb) returns jsonb
language sql immutable as $$
  select jsonb_build_object(
    'c', coalesce(max(case when it->'luz'->>'t' = 'c' then public.num_ou(it->'luz'->>'m', 0) end), 0),
    'l', coalesce(max(case when it->'luz'->>'t' = 'l' then public.num_ou(it->'luz'->>'m', 0) end), 0))
  from jsonb_array_elements(case when jsonb_typeof(d->'inv'->'items') = 'array' then d->'inv'->'items' else '[]'::jsonb end) it
  where jsonb_typeof(it) = 'object' and jsonb_typeof(it->'luz') = 'object' and public.num_ou(it->>'qtd', 1) > 0
$$;

create or replace function public.token_luz_auto() returns trigger
language plpgsql security definer set search_path = public as $$
declare sis text; gm numeric; f jsonb; l jsonb; modo text; m numeric; ligada boolean;
begin
  if new.personagem_id is null then return new; end if;
  select c.sistema, ce.grade_m into sis, gm
    from public.cenas ce join public.mesas me on me.id = ce.mesa_id
    left join public.campanhas c on c.id = me.campanha_id
   where ce.id = new.cena_id;
  if coalesce(sis, '') <> 'op' then return new; end if;
  select dados into f from public.personagens where id = new.personagem_id;
  l := public.luz_da_ficha(f);
  modo := case when coalesce(new.dados->>'lm', '') = 'c' then 'c' else 'l' end;
  m := public.num_ou(l->>modo, 0);
  ligada := coalesce(new.dados->>'lo', '0') in ('1', 'true');
  if gm is null or gm <= 0 then gm := 1.5; end if;
  new.dados := coalesce(new.dados, '{}'::jsonb)
    || jsonb_build_object('lz', round(m / gm * 2) / 2, 'lo', case when ligada and m > 0 then 1 else 0 end);
  return new;
end $$;
drop trigger if exists token_luz_auto on public.tokens;
create trigger token_luz_auto before insert or update on public.tokens
  for each row execute function public.token_luz_auto();

-- inventário mudou -> tokens ligados à ficha recalculam a luz
create or replace function public.ficha_luz_tokens() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  if public.luz_da_ficha(new.dados) is not distinct from public.luz_da_ficha(old.dados) then return new; end if;
  update public.tokens set dados = dados where personagem_id = new.id;
  return new;
end $$;
drop trigger if exists ficha_luz_tokens on public.personagens;
create trigger ficha_luz_tokens after update of dados on public.personagens
  for each row execute function public.ficha_luz_tokens();

-- ---------- 6. Regras de segurança (RLS) ----------
alter table public.lojas        enable row level security;
alter table public.loja_itens   enable row level security;
alter table public.loja_compras enable row level security;
alter table public.catalogo     enable row level security;

drop policy if exists lojas_ver on public.lojas;
create policy lojas_ver on public.lojas for select to authenticated
  using (public.c_mestre(campanha_id) or (aberta and public.c_membro(campanha_id)));
drop policy if exists lojas_mestre on public.lojas;
create policy lojas_mestre on public.lojas for all to authenticated
  using (public.c_mestre(campanha_id)) with check (public.c_mestre(campanha_id));

drop policy if exists loja_itens_ver on public.loja_itens;
create policy loja_itens_ver on public.loja_itens for select to authenticated
  using (public.c_mestre(public.loja_campanha(loja_id))
         or (public.loja_aberta(loja_id) and public.c_membro(public.loja_campanha(loja_id))));
drop policy if exists loja_itens_mestre on public.loja_itens;
create policy loja_itens_mestre on public.loja_itens for all to authenticated
  using (public.c_mestre(public.loja_campanha(loja_id))) with check (public.c_mestre(public.loja_campanha(loja_id)));

-- histórico: o mestre vê tudo; o jogador vê as próprias compras. Só a função comprar() grava.
drop policy if exists loja_compras_ver on public.loja_compras;
create policy loja_compras_ver on public.loja_compras for select to authenticated
  using (public.c_mestre(campanha_id) or user_id = auth.uid());

drop policy if exists catalogo_ver on public.catalogo;
create policy catalogo_ver on public.catalogo for select to authenticated
  using (public.c_mestre(campanha_id) or (public.c_membro(campanha_id) and (aprovado or criado_por = auth.uid())));
drop policy if exists catalogo_criar on public.catalogo;
create policy catalogo_criar on public.catalogo for insert to authenticated
  with check (public.c_membro(campanha_id) and criado_por = auth.uid() and (not aprovado or public.c_mestre(campanha_id)));
drop policy if exists catalogo_editar on public.catalogo;
create policy catalogo_editar on public.catalogo for update to authenticated
  using (public.c_mestre(campanha_id) or (criado_por = auth.uid() and not aprovado))
  with check (public.c_mestre(campanha_id) or (criado_por = auth.uid() and not aprovado));
drop policy if exists catalogo_excluir on public.catalogo;
create policy catalogo_excluir on public.catalogo for delete to authenticated
  using (public.c_mestre(campanha_id) or (criado_por = auth.uid() and not aprovado));

-- ---------- 7. Permissões e tempo real ----------
grant select, insert, update, delete on public.lojas, public.loja_itens, public.catalogo to authenticated;
grant select on public.loja_compras to authenticated;

do $$ begin alter publication supabase_realtime add table public.lojas;
exception when duplicate_object then null; end $$;
do $$ begin alter publication supabase_realtime add table public.loja_itens;
exception when duplicate_object then null; end $$;
do $$ begin alter publication supabase_realtime add table public.catalogo;
exception when duplicate_object then null; end $$;
