-- =====================================================================
-- OPEN RPG — ETAPA 7: quadro de investigação da campanha
--
-- COMO USAR: rode no SQL Editor do Supabase (New query -> colar tudo -> Run).
-- Depende só do schema_etapa3.sql (funções c_membro / c_gerir). Pode rodar de novo.
-- Quem é da campanha vê e põe documentos no quadro; só o autor (ou mestre/admin) edita ou apaga os seus.
-- Itens "só mestre" ficam escondidos dos jogadores até o mestre revelar.
-- =====================================================================

create table if not exists public.quadro_itens (
  id          uuid primary key default gen_random_uuid(),
  campanha_id uuid not null references public.campanhas(id) on delete cascade,
  autor       uuid not null default auth.uid(),
  tipo        text not null default 'nota' check (tipo in ('nota', 'documento', 'foto')),
  titulo      text not null default '',
  texto       text not null default '',
  imagem      text,                                   -- foto reduzida (data URL)
  cor         text not null default 'amarelo',
  x           numeric not null default 60,
  y           numeric not null default 60,
  rot         numeric not null default 0,
  so_mestre   boolean not null default false,
  criado_em   timestamptz not null default now(),
  constraint quadro_itens_tamanho check (coalesce(length(imagem), 0) <= 900000 and length(texto) <= 20000)
);
create index if not exists quadro_itens_camp_idx on public.quadro_itens(campanha_id);

create table if not exists public.quadro_ligacoes (
  id          uuid primary key default gen_random_uuid(),
  campanha_id uuid not null references public.campanhas(id) on delete cascade,
  autor       uuid not null default auth.uid(),
  de          uuid not null references public.quadro_itens(id) on delete cascade,
  para        uuid not null references public.quadro_itens(id) on delete cascade,
  criado_em   timestamptz not null default now(),
  constraint quadro_ligacoes_distintas check (de <> para),
  constraint quadro_ligacoes_unica unique (de, para)
);
create index if not exists quadro_ligacoes_camp_idx on public.quadro_ligacoes(campanha_id);

-- não deixa trocar de dono nem de campanha
create or replace function public.quadro_itens_travas() returns trigger
language plpgsql set search_path = public as $$
begin
  new.autor := old.autor; new.campanha_id := old.campanha_id;
  return new;
end $$;
drop trigger if exists quadro_itens_travas on public.quadro_itens;
create trigger quadro_itens_travas before update on public.quadro_itens
  for each row execute function public.quadro_itens_travas();

-- a ligação só vale entre itens da mesma campanha
create or replace function public.quadro_ligacao_valida() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  if (select count(*) from public.quadro_itens where id in (new.de, new.para) and campanha_id = new.campanha_id) <> 2 then
    raise exception 'Os dois documentos precisam ser desta campanha';
  end if;
  return new;
end $$;
drop trigger if exists quadro_ligacao_valida on public.quadro_ligacoes;
create trigger quadro_ligacao_valida before insert on public.quadro_ligacoes
  for each row execute function public.quadro_ligacao_valida();

alter table public.quadro_itens enable row level security;
alter table public.quadro_ligacoes enable row level security;

drop policy if exists quadro_itens_ver on public.quadro_itens;
create policy quadro_itens_ver on public.quadro_itens for select to authenticated
  using (public.c_membro(campanha_id) and (not so_mestre or autor = auth.uid() or public.c_gerir(campanha_id)));
drop policy if exists quadro_itens_criar on public.quadro_itens;
create policy quadro_itens_criar on public.quadro_itens for insert to authenticated
  with check (public.c_membro(campanha_id) and autor = auth.uid() and (not so_mestre or public.c_gerir(campanha_id)));
drop policy if exists quadro_itens_editar on public.quadro_itens;
create policy quadro_itens_editar on public.quadro_itens for update to authenticated
  using (public.c_membro(campanha_id) and (autor = auth.uid() or public.c_gerir(campanha_id)))
  with check (public.c_membro(campanha_id) and (not so_mestre or public.c_gerir(campanha_id)));
drop policy if exists quadro_itens_apagar on public.quadro_itens;
create policy quadro_itens_apagar on public.quadro_itens for delete to authenticated
  using (public.c_membro(campanha_id) and (autor = auth.uid() or public.c_gerir(campanha_id)));

drop policy if exists quadro_lig_ver on public.quadro_ligacoes;
create policy quadro_lig_ver on public.quadro_ligacoes for select to authenticated
  using (public.c_membro(campanha_id)
         and exists (select 1 from public.quadro_itens i where i.id = de)
         and exists (select 1 from public.quadro_itens i where i.id = para));
drop policy if exists quadro_lig_criar on public.quadro_ligacoes;
create policy quadro_lig_criar on public.quadro_ligacoes for insert to authenticated
  with check (public.c_membro(campanha_id) and autor = auth.uid());
drop policy if exists quadro_lig_apagar on public.quadro_ligacoes;
create policy quadro_lig_apagar on public.quadro_ligacoes for delete to authenticated
  using (public.c_membro(campanha_id) and (autor = auth.uid() or public.c_gerir(campanha_id)));

revoke all on public.quadro_itens, public.quadro_ligacoes from anon, authenticated;
grant select, insert, update, delete on public.quadro_itens, public.quadro_ligacoes to authenticated;

do $$ begin alter publication supabase_realtime add table public.quadro_itens;
exception when duplicate_object then null; when undefined_object then null; end $$;
do $$ begin alter publication supabase_realtime add table public.quadro_ligacoes;
exception when duplicate_object then null; when undefined_object then null; end $$;
