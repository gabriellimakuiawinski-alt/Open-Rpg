-- =====================================================================
-- OPEN RPG — ETAPA 19: cenários salvos do mapa da cidade
--
-- COMO USAR: rode no SQL Editor do Supabase DEPOIS da etapa 18. Pode rodar de novo.
-- O mestre guarda "fotos" do mapa (névoa, zonas, NPCs, dia) e volta a elas depois.
-- Só o mestre/admin da campanha vê e mexe.
-- =====================================================================
create table if not exists public.cidade_cenarios (
  id          uuid primary key default gen_random_uuid(),
  campanha_id uuid not null references public.campanhas(id) on delete cascade,
  nome        text not null default 'Cenário',
  dados       jsonb not null default '{}'::jsonb,
  criado_em   timestamptz not null default now(),
  constraint cidade_cenarios_tamanho check (length(dados::text) <= 4500000)
);
create index if not exists cidade_cenarios_camp_idx on public.cidade_cenarios(campanha_id);
alter table public.cidade_cenarios enable row level security;
drop policy if exists cidade_cenarios_mestre on public.cidade_cenarios;
create policy cidade_cenarios_mestre on public.cidade_cenarios for all to authenticated
  using (public.c_gerir(campanha_id)) with check (public.c_gerir(campanha_id));
revoke all on public.cidade_cenarios from anon, authenticated;
grant select, insert, update, delete on public.cidade_cenarios to authenticated;
