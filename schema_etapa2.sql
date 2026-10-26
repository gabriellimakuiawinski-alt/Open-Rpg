-- =====================================================================
-- MESA RPG — ETAPA 2 (parte 1): papéis, permissões, tabletop e arquivos
--
-- COMO USAR: rode DEPOIS do schema.sql (etapa 1). No Supabase: SQL Editor →
-- New query → cole TUDO isto → Run. Pode rodar de novo sem quebrar nada.
--
-- PAPÉIS NA MESA
--   mestre  : controla tudo. Único que promove/rebaixa admin e muda as opções da mesa.
--   admin   : um jogador promovido. Gerencia cenas, mapas, névoa, paredes, tokens e a
--             biblioteca. NÃO vê as coisas pessoais do mestre (fichas de NPC, notas,
--             playlists) e não mexe em músicas.
--   jogador : move os tokens que o mestre não travou e pode enviar imagens de token
--             (se a mesa permitir). Só vê a cena ativa.
--
-- FICHAS: as fichas dos jogadores da mesma mesa são públicas para a mesa, a não ser
-- que o dono ou o mestre marque como "privada". Ficha de NPC só o mestre vê.
-- =====================================================================

-- ---------- Ajustes em tabelas da etapa 1 ----------

alter table public.membros drop constraint if exists membros_papel_check;
alter table public.membros add constraint membros_papel_check
  check (papel in ('mestre', 'admin', 'jogador'));

alter table public.mesas add column if not exists jogadores_adicionam boolean not null default true;
alter table public.mesas add column if not exists jogadores_movem boolean not null default true;

alter table public.personagens add column if not exists privada boolean not null default false;
alter table public.personagens add column if not exists npc boolean not null default false;

-- ---------- Novas tabelas ----------

create table if not exists public.cenas (
  id uuid primary key default gen_random_uuid(),
  mesa_id uuid not null references public.mesas(id) on delete cascade,
  nome text not null default 'Nova cena',
  ordem int not null default 0,
  escuro boolean not null default false,
  escuridao numeric not null default 0.92,
  grade_px numeric not null default 50,
  grade_m numeric not null default 1.5,
  grade_visivel boolean not null default true,
  nevoa jsonb not null default '[]'::jsonb,
  nevoa_cor text not null default '#000000',
  nevoa_opacidade numeric not null default 0.6,
  paredes jsonb not null default '[]'::jsonb,
  versao int not null default 0,  -- sobe quando um token some/aparece para os jogadores
  criado_em timestamptz not null default now()
);
create index if not exists cenas_mesa_idx on public.cenas(mesa_id);

-- Cena que os jogadores estão vendo agora
alter table public.mesas add column if not exists cena_ativa uuid references public.cenas(id) on delete set null;

create table if not exists public.pastas (
  id uuid primary key default gen_random_uuid(),
  mesa_id uuid not null references public.mesas(id) on delete cascade,
  tipo text not null check (tipo in ('mapa', 'chr', 'prop', 'mnt')),
  nome text not null
);

-- Biblioteca: cada linha descreve um arquivo guardado no Storage (bucket "mesa-arquivos")
create table if not exists public.arquivos (
  id uuid primary key default gen_random_uuid(),
  mesa_id uuid not null references public.mesas(id) on delete cascade,
  tipo text not null check (tipo in ('mapa', 'chr', 'prop', 'mnt', 'aud')),
  nome text not null default '',
  pasta_id uuid references public.pastas(id) on delete set null,
  path text not null unique,
  mime text not null default '',
  tamanho bigint not null default 0,
  efeito boolean not null default false,
  atalho text not null default '',
  criado_por uuid references public.profiles(id) on delete set null,
  criado_em timestamptz not null default now(),
  constraint arquivos_path_ok check (path like mesa_id::text || '/%')
);
create index if not exists arquivos_mesa_idx on public.arquivos(mesa_id);

create table if not exists public.mapas_cena (
  id uuid primary key default gen_random_uuid(),
  cena_id uuid not null references public.cenas(id) on delete cascade,
  arquivo_id uuid not null references public.arquivos(id) on delete cascade,
  x numeric not null default 0,
  y numeric not null default 0,
  escala numeric not null default 1,
  travado boolean not null default true,
  ordem int not null default 0
);
create index if not exists mapas_cena_idx on public.mapas_cena(cena_id);

create table if not exists public.tokens (
  id uuid primary key default gen_random_uuid(),
  cena_id uuid not null references public.cenas(id) on delete cascade,
  nome text not null default '',
  categoria text not null default 'chr' check (categoria in ('chr', 'prop', 'mnt')),
  imagem_id uuid references public.arquivos(id) on delete set null,
  imagem_caido_id uuid references public.arquivos(id) on delete set null,
  alts uuid[] not null default '{}',
  x numeric not null default 0,
  y numeric not null default 0,
  tam numeric not null default 1,
  rot numeric not null default 0,
  travado boolean not null default false,  -- travado pelo mestre: jogador não move
  oculto boolean not null default false,   -- oculto: nem chega ao aparelho do jogador
  caido boolean not null default false,
  personagem_id uuid references public.personagens(id) on delete set null,
  rol int,                                 -- iniciativa rolada
  dados jsonb not null default '{}'::jsonb, -- vida, mana, luz, barras... (formato livre)
  criado_por uuid references public.profiles(id) on delete set null,
  criado_em timestamptz not null default now()
);
create index if not exists tokens_cena_idx on public.tokens(cena_id);

-- Só do mestre
create table if not exists public.playlists (
  id uuid primary key default gen_random_uuid(),
  mesa_id uuid not null references public.mesas(id) on delete cascade,
  nome text not null,
  faixas uuid[] not null default '{}'
);
create table if not exists public.notas (
  mesa_id uuid primary key references public.mesas(id) on delete cascade,
  texto text not null default ''
);

-- ---------- Funções de permissão ----------

create or replace function public.pode_gerir(m uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.membros
                 where mesa_id = m and user_id = auth.uid() and papel in ('mestre', 'admin'));
$$;

create or replace function public.mesa_da_cena(c uuid) returns uuid
language sql stable security definer set search_path = public as $$
  select mesa_id from public.cenas where id = c;
$$;

-- Jogadores só enxergam a cena ativa; mestre e admin enxergam todas
create or replace function public.cena_visivel(c uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (
    select 1 from public.cenas s join public.mesas m on m.id = s.mesa_id
    where s.id = c and (public.pode_gerir(s.mesa_id)
                        or (public.eh_membro(s.mesa_id) and m.cena_ativa = s.id)));
$$;

-- Um arquivo "em uso" (mapa ou token que o jogador pode ver) pode ser lido por ele
create or replace function public.arquivo_em_uso(a uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (
      select 1 from public.tokens t
      where (t.imagem_id = a or t.imagem_caido_id = a or a = any(t.alts))
        and public.cena_visivel(t.cena_id)
        and (not t.oculto or public.pode_gerir(public.mesa_da_cena(t.cena_id))))
    or exists (
      select 1 from public.mapas_cena mc
      where mc.arquivo_id = a and public.cena_visivel(mc.cena_id));
$$;

-- Trocar a cena que os jogadores veem (mestre e admin)
create or replace function public.ativar_cena(p_cena uuid) returns void
language plpgsql security definer set search_path = public as $$
declare m uuid;
begin
  select mesa_id into m from public.cenas where id = p_cena;
  if m is null or not public.pode_gerir(m) then
    raise exception 'Sem permissão para trocar a cena';
  end if;
  update public.mesas set cena_ativa = p_cena where id = m;
end $$;

-- Mover um token. É o único jeito de um jogador comum mover token (ele não edita a tabela direto).
create or replace function public.mover_token(p_id uuid, p_x numeric, p_y numeric) returns void
language plpgsql security definer set search_path = public as $$
declare t public.tokens; m public.mesas;
begin
  select * into t from public.tokens where id = p_id;
  if not found then raise exception 'Token não encontrado'; end if;
  select * into m from public.mesas where id = public.mesa_da_cena(t.cena_id);
  if not public.eh_membro(m.id) then raise exception 'Você não faz parte desta mesa'; end if;
  if not public.pode_gerir(m.id) then
    if m.cena_ativa is distinct from t.cena_id then raise exception 'Esta cena não está ativa'; end if;
    if t.oculto then raise exception 'Sem permissão'; end if;
    if t.travado then raise exception 'Token travado pelo mestre'; end if;
    if not m.jogadores_movem then raise exception 'O mestre travou o movimento dos jogadores'; end if;
  end if;
  update public.tokens set x = p_x, y = p_y where id = p_id;
end $$;

revoke all on function public.ativar_cena(uuid) from public, anon;
revoke all on function public.mover_token(uuid, numeric, numeric) from public, anon;
grant execute on function public.ativar_cena(uuid) to authenticated;
grant execute on function public.mover_token(uuid, numeric, numeric) to authenticated;

-- ---------- Gatilhos ----------

-- Ficha: só o dono ou o mestre muda "privada", "npc" e a mesa; ninguém troca o dono
create or replace function public.personagem_antes_de_salvar() returns trigger
language plpgsql security definer set search_path = public as $$
declare dono_ou_mestre boolean;
begin
  new.atualizado_em := now();
  if tg_op = 'UPDATE' then
    if new.user_id is distinct from old.user_id then
      raise exception 'Não é permitido trocar o dono do personagem';
    end if;
    if auth.uid() is not null and pg_trigger_depth() = 1 then  -- depth > 1: limpeza automática (ex.: mesa excluída)
      dono_ou_mestre := old.user_id = auth.uid() or public.eh_mestre(old.mesa_id);
      if not dono_ou_mestre and (new.privada is distinct from old.privada
                                 or new.npc is distinct from old.npc
                                 or new.mesa_id is distinct from old.mesa_id) then
        raise exception 'Só o dono da ficha ou o mestre pode mudar isso';
      end if;
    end if;
  end if;
  return new;
end $$;

-- Token: quem não é mestre/admin não destrava, não esconde e não move token travado
create or replace function public.token_antes_de_salvar() returns trigger
language plpgsql security definer set search_path = public as $$
declare m uuid; mm public.mesas;
begin
  if tg_op = 'INSERT' or auth.uid() is null or pg_trigger_depth() > 1 then return new; end if;  -- depth > 1: limpeza automática
  m := public.mesa_da_cena(old.cena_id);
  if public.pode_gerir(m) then return new; end if;
  if new.cena_id is distinct from old.cena_id or new.travado is distinct from old.travado
     or new.oculto is distinct from old.oculto or new.criado_por is distinct from old.criado_por
     or new.personagem_id is distinct from old.personagem_id then
    raise exception 'Só o mestre ou o admin pode mudar isso';
  end if;
  if new.x is distinct from old.x or new.y is distinct from old.y then
    select * into mm from public.mesas where id = m;
    if old.travado then raise exception 'Token travado pelo mestre'; end if;
    if not mm.jogadores_movem then raise exception 'O mestre travou o movimento dos jogadores'; end if;
  end if;
  return new;
end $$;
drop trigger if exists antes_de_salvar_token on public.tokens;
create trigger antes_de_salvar_token before update on public.tokens
  for each row execute function public.token_antes_de_salvar();

-- Quando um token aparece/some para os jogadores, a cena sobe de versão (eles recarregam a cena)
create or replace function public.token_mudou_visibilidade() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  if tg_op = 'DELETE' then
    update public.cenas set versao = versao + 1 where id = old.cena_id;
    return old;
  end if;
  if new.oculto is distinct from old.oculto then
    update public.cenas set versao = versao + 1 where id = new.cena_id;
  end if;
  return new;
end $$;
drop trigger if exists apos_mudar_token on public.tokens;
create trigger apos_mudar_token after update on public.tokens
  for each row execute function public.token_mudou_visibilidade();
drop trigger if exists apos_apagar_token on public.tokens;
create trigger apos_apagar_token after delete on public.tokens
  for each row execute function public.token_mudou_visibilidade();

-- Arquivo: dono, mesa, tipo e caminho não mudam depois de criados
create or replace function public.arquivo_imutavel() returns trigger
language plpgsql as $$
begin
  if pg_trigger_depth() > 1 then return new; end if;  -- limpeza automática (ex.: conta excluída)
  if new.mesa_id is distinct from old.mesa_id or new.tipo is distinct from old.tipo
     or new.path is distinct from old.path or new.criado_por is distinct from old.criado_por then
    raise exception 'Não é permitido mudar mesa, tipo ou caminho do arquivo';
  end if;
  return new;
end $$;
drop trigger if exists arquivo_nao_muda on public.arquivos;
create trigger arquivo_nao_muda before update on public.arquivos
  for each row execute function public.arquivo_imutavel();

-- ---------- Regras de segurança (RLS) ----------

alter table public.cenas     enable row level security;
alter table public.pastas    enable row level security;
alter table public.arquivos  enable row level security;
alter table public.mapas_cena enable row level security;
alter table public.tokens    enable row level security;
alter table public.playlists enable row level security;
alter table public.notas     enable row level security;

-- membros: o mestre promove/rebaixa (jogador <-> admin)
grant update (papel) on public.membros to authenticated;
drop policy if exists membros_papel on public.membros;
create policy membros_papel on public.membros for update to authenticated
  using (papel <> 'mestre' and public.eh_mestre(mesa_id))
  with check (papel in ('admin', 'jogador') and public.eh_mestre(mesa_id));

-- personagens: públicas para a mesa, exceto privadas e NPCs
drop policy if exists personagens_ver on public.personagens;
create policy personagens_ver on public.personagens for select to authenticated
  using (user_id = auth.uid()
         or public.eh_mestre(mesa_id)
         or (mesa_id is not null and public.eh_membro(mesa_id) and not privada and not npc));
drop policy if exists personagens_editar on public.personagens;
create policy personagens_editar on public.personagens for update to authenticated
  using (user_id = auth.uid()
         or public.eh_mestre(mesa_id)
         or (mesa_id is not null and public.pode_gerir(mesa_id) and not privada and not npc))
  with check ((user_id = auth.uid()
               or public.eh_mestre(mesa_id)
               or (mesa_id is not null and public.pode_gerir(mesa_id) and not privada and not npc))
              and (mesa_id is null or public.usuario_na_mesa(mesa_id, user_id)));

-- cenas
drop policy if exists cenas_ver on public.cenas;
create policy cenas_ver on public.cenas for select to authenticated
  using (public.pode_gerir(mesa_id)
         or (public.eh_membro(mesa_id) and id = (select m.cena_ativa from public.mesas m where m.id = mesa_id)));
drop policy if exists cenas_criar on public.cenas;
create policy cenas_criar on public.cenas for insert to authenticated
  with check (public.pode_gerir(mesa_id));
drop policy if exists cenas_editar on public.cenas;
create policy cenas_editar on public.cenas for update to authenticated
  using (public.pode_gerir(mesa_id)) with check (public.pode_gerir(mesa_id));
drop policy if exists cenas_excluir on public.cenas;
create policy cenas_excluir on public.cenas for delete to authenticated
  using (public.pode_gerir(mesa_id));

-- mapas na cena
drop policy if exists mapas_ver on public.mapas_cena;
create policy mapas_ver on public.mapas_cena for select to authenticated
  using (public.cena_visivel(cena_id));
drop policy if exists mapas_criar on public.mapas_cena;
create policy mapas_criar on public.mapas_cena for insert to authenticated
  with check (public.pode_gerir(public.mesa_da_cena(cena_id)));
drop policy if exists mapas_editar on public.mapas_cena;
create policy mapas_editar on public.mapas_cena for update to authenticated
  using (public.pode_gerir(public.mesa_da_cena(cena_id)))
  with check (public.pode_gerir(public.mesa_da_cena(cena_id)));
drop policy if exists mapas_excluir on public.mapas_cena;
create policy mapas_excluir on public.mapas_cena for delete to authenticated
  using (public.pode_gerir(public.mesa_da_cena(cena_id)));

-- tokens
drop policy if exists tokens_ver on public.tokens;
create policy tokens_ver on public.tokens for select to authenticated
  using (public.cena_visivel(cena_id)
         and (not oculto or public.pode_gerir(public.mesa_da_cena(cena_id))));
drop policy if exists tokens_criar on public.tokens;
create policy tokens_criar on public.tokens for insert to authenticated
  with check (criado_por = auth.uid()
              and (public.pode_gerir(public.mesa_da_cena(cena_id))
                   or (public.cena_visivel(cena_id) and not oculto and personagem_id is null
                       and (select m.jogadores_adicionam from public.mesas m
                            where m.id = public.mesa_da_cena(cena_id)))));
drop policy if exists tokens_editar on public.tokens;
create policy tokens_editar on public.tokens for update to authenticated
  using (public.pode_gerir(public.mesa_da_cena(cena_id))
         or (public.cena_visivel(cena_id)
             and (criado_por = auth.uid()
                  or exists (select 1 from public.personagens p
                             where p.id = personagem_id and p.user_id = auth.uid()))))
  with check (public.pode_gerir(public.mesa_da_cena(cena_id))
              or (public.cena_visivel(cena_id)
                  and (criado_por = auth.uid()
                       or exists (select 1 from public.personagens p
                                  where p.id = personagem_id and p.user_id = auth.uid()))));
drop policy if exists tokens_excluir on public.tokens;
create policy tokens_excluir on public.tokens for delete to authenticated
  using (public.pode_gerir(public.mesa_da_cena(cena_id))
         or (public.cena_visivel(cena_id) and criado_por = auth.uid()));

-- pastas da biblioteca
drop policy if exists pastas_todas on public.pastas;
create policy pastas_todas on public.pastas for all to authenticated
  using (public.pode_gerir(mesa_id)) with check (public.pode_gerir(mesa_id));

-- arquivos da biblioteca
drop policy if exists arquivos_ver on public.arquivos;
create policy arquivos_ver on public.arquivos for select to authenticated
  using ((tipo = 'aud' and public.eh_mestre(mesa_id))
         or (tipo <> 'aud' and public.pode_gerir(mesa_id))
         or (criado_por = auth.uid() and public.eh_membro(mesa_id))
         or (tipo <> 'aud' and public.arquivo_em_uso(id)));
drop policy if exists arquivos_criar on public.arquivos;
create policy arquivos_criar on public.arquivos for insert to authenticated
  with check (criado_por = auth.uid() and public.eh_membro(mesa_id)
              and ((tipo = 'aud' and public.eh_mestre(mesa_id))
                   or (tipo = 'mapa' and public.pode_gerir(mesa_id))
                   or (tipo in ('chr', 'prop', 'mnt')
                       and (public.pode_gerir(mesa_id)
                            or (select m.jogadores_adicionam from public.mesas m where m.id = mesa_id)))));
drop policy if exists arquivos_editar on public.arquivos;
create policy arquivos_editar on public.arquivos for update to authenticated
  using ((tipo = 'aud' and public.eh_mestre(mesa_id))
         or (tipo <> 'aud' and public.pode_gerir(mesa_id))
         or (criado_por = auth.uid() and public.eh_membro(mesa_id)))
  with check ((tipo = 'aud' and public.eh_mestre(mesa_id))
              or (tipo <> 'aud' and public.pode_gerir(mesa_id))
              or (criado_por = auth.uid() and public.eh_membro(mesa_id)));
drop policy if exists arquivos_excluir on public.arquivos;
create policy arquivos_excluir on public.arquivos for delete to authenticated
  using ((tipo = 'aud' and public.eh_mestre(mesa_id))
         or (tipo <> 'aud' and public.pode_gerir(mesa_id))
         or (criado_por = auth.uid() and public.eh_membro(mesa_id)));

-- playlists e notas: só o mestre
drop policy if exists playlists_mestre on public.playlists;
create policy playlists_mestre on public.playlists for all to authenticated
  using (public.eh_mestre(mesa_id)) with check (public.eh_mestre(mesa_id));
drop policy if exists notas_mestre on public.notas;
create policy notas_mestre on public.notas for all to authenticated
  using (public.eh_mestre(mesa_id)) with check (public.eh_mestre(mesa_id));

-- ---------- Permissões de acesso às tabelas ----------
grant select, insert, update, delete on public.cenas, public.pastas, public.arquivos,
  public.mapas_cena, public.tokens, public.playlists, public.notas to authenticated;

-- ---------- Armazenamento de arquivos (Storage) ----------
-- Bucket privado. Caminho de cada arquivo: <id da mesa>/<id do arquivo>-<nome>
-- Fluxo do app: 1) cria a linha em "arquivos"  2) envia o arquivo  (apagar: 1) arquivo  2) linha)
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('mesa-arquivos', 'mesa-arquivos', false, 52428800, array[
  'image/png', 'image/jpeg', 'image/webp', 'image/gif', 'image/avif',
  'audio/mpeg', 'audio/mp3', 'audio/mp4', 'audio/x-m4a', 'audio/aac', 'audio/ogg',
  'audio/wav', 'audio/x-wav', 'audio/wave', 'audio/webm', 'audio/flac', 'audio/opus',
  'video/mp4', 'application/ogg'])
on conflict (id) do update set public = false,
  file_size_limit = excluded.file_size_limit, allowed_mime_types = excluded.allowed_mime_types;

drop policy if exists mesa_arquivos_ler on storage.objects;
create policy mesa_arquivos_ler on storage.objects for select to authenticated
  using (bucket_id = 'mesa-arquivos'
         and exists (select 1 from public.arquivos a where a.path = name));
drop policy if exists mesa_arquivos_enviar on storage.objects;
create policy mesa_arquivos_enviar on storage.objects for insert to authenticated
  with check (bucket_id = 'mesa-arquivos'
              and exists (select 1 from public.arquivos a where a.path = name and a.criado_por = auth.uid()));
drop policy if exists mesa_arquivos_apagar on storage.objects;
create policy mesa_arquivos_apagar on storage.objects for delete to authenticated
  using (bucket_id = 'mesa-arquivos'
         and exists (select 1 from public.arquivos a
                     where a.path = name and (a.criado_por = auth.uid() or public.pode_gerir(a.mesa_id))));

-- ---------- Tempo real ----------
do $$ begin alter publication supabase_realtime add table public.tokens;
exception when duplicate_object then null; end $$;
do $$ begin alter publication supabase_realtime add table public.cenas;
exception when duplicate_object then null; end $$;
do $$ begin alter publication supabase_realtime add table public.mapas_cena;
exception when duplicate_object then null; end $$;
do $$ begin alter publication supabase_realtime add table public.mesas;
exception when duplicate_object then null; end $$;
do $$ begin alter publication supabase_realtime add table public.membros;
exception when duplicate_object then null; end $$;
