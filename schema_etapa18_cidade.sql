-- =====================================================================
-- OPEN RPG — ETAPA 18: mapa da cidade (cidade.html), integrado à campanha
--
-- COMO USAR: rode no SQL Editor do Supabase (New query -> colar tudo -> Run).
-- Depende só do schema_etapa3.sql (funções c_membro / c_gerir). Pode rodar de novo.
--   cidade_mapa    : o mapa COMPLETO (segredos, locais escondidos, rumores). Só o mestre/admin lê e grava.
--   cidade_jogador : a versão pública que o mestre publica (sem segredos) + a névoa (o que já foi explorado). Todo membro lê.
--   cidade_grupo   : onde o grupo está agora e por onde passou. Todo membro lê; só o mestre/admin muda.
-- =====================================================================

create table if not exists public.cidade_mapa (
  campanha_id   uuid primary key references public.campanhas(id) on delete cascade,
  dados         jsonb not null default '{}'::jsonb,
  atualizado_em timestamptz not null default now(),
  constraint cidade_mapa_tamanho check (length(dados::text) <= 4000000)
);

create table if not exists public.cidade_jogador (
  campanha_id   uuid primary key references public.campanhas(id) on delete cascade,
  dados         jsonb not null default '{}'::jsonb,
  nevoa         text,                              -- PNG (data URL) do que já foi revelado
  atualizado_em timestamptz not null default now(),
  constraint cidade_jogador_tamanho check (length(dados::text) <= 4000000 and coalesce(length(nevoa), 0) <= 600000)
);

create table if not exists public.cidade_grupo (
  campanha_id   uuid primary key references public.campanhas(id) on delete cascade,
  px            numeric,                           -- posição no plano do mapa (null = sem marcador)
  py            numeric,
  nome          text not null default 'Grupo',
  trilha        jsonb not null default '[]'::jsonb, -- [[px,py],...] por onde passou
  atualizado_em timestamptz not null default now(),
  constraint cidade_grupo_trilha check (jsonb_typeof(trilha) = 'array' and jsonb_array_length(trilha) <= 1500)
);

alter table public.cidade_mapa enable row level security;
alter table public.cidade_jogador enable row level security;
alter table public.cidade_grupo enable row level security;

drop policy if exists cidade_mapa_mestre on public.cidade_mapa;
create policy cidade_mapa_mestre on public.cidade_mapa for all to authenticated
  using (public.c_gerir(campanha_id)) with check (public.c_gerir(campanha_id));

drop policy if exists cidade_jogador_ver on public.cidade_jogador;
create policy cidade_jogador_ver on public.cidade_jogador for select to authenticated
  using (public.c_membro(campanha_id));
drop policy if exists cidade_jogador_mestre on public.cidade_jogador;
create policy cidade_jogador_mestre on public.cidade_jogador for all to authenticated
  using (public.c_gerir(campanha_id)) with check (public.c_gerir(campanha_id));

drop policy if exists cidade_grupo_ver on public.cidade_grupo;
create policy cidade_grupo_ver on public.cidade_grupo for select to authenticated
  using (public.c_membro(campanha_id));
drop policy if exists cidade_grupo_mestre on public.cidade_grupo;
create policy cidade_grupo_mestre on public.cidade_grupo for all to authenticated
  using (public.c_gerir(campanha_id)) with check (public.c_gerir(campanha_id));

revoke all on public.cidade_mapa, public.cidade_jogador, public.cidade_grupo from anon, authenticated;
grant select, insert, update, delete on public.cidade_mapa, public.cidade_jogador, public.cidade_grupo to authenticated;

do $$ begin alter publication supabase_realtime add table public.cidade_jogador;
exception when duplicate_object then null; when undefined_object then null; end $$;
do $$ begin alter publication supabase_realtime add table public.cidade_grupo;
exception when duplicate_object then null; when undefined_object then null; end $$;
