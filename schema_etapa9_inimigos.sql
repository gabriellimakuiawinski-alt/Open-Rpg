-- =====================================================================
-- OPEN RPG — ETAPA 9: inimigos (bestiário) salvos no perfil de cada usuário
--
-- COMO USAR: rode no SQL Editor do Supabase (New query -> colar tudo -> Run). Pode rodar de novo.
-- Não depende de outras etapas. Cada pessoa só vê e mexe nos inimigos que ela mesma criou
-- (ficam no perfil, valem para qualquer campanha). Os inimigos prontos do livro vêm numa etapa à parte.
-- =====================================================================

create table if not exists public.inimigos (
  id          uuid primary key default gen_random_uuid(),
  dono        uuid not null default auth.uid(),
  nome        text not null default 'Novo inimigo',
  elemento    text not null default '',
  vd          text not null default '',
  dados       jsonb not null default '{}'::jsonb,
  criado_em   timestamptz not null default now(),
  atualizado_em timestamptz not null default now(),
  constraint inimigos_tamanho check (length(nome) <= 200 and length(dados::text) <= 60000)
);
create index if not exists inimigos_dono_idx on public.inimigos(dono);

create or replace function public.inimigos_travas() returns trigger
language plpgsql set search_path = public as $$
begin
  new.dono := old.dono; new.criado_em := old.criado_em; new.atualizado_em := now();
  return new;
end $$;
drop trigger if exists inimigos_travas on public.inimigos;
create trigger inimigos_travas before update on public.inimigos
  for each row execute function public.inimigos_travas();

alter table public.inimigos enable row level security;

drop policy if exists inimigos_ver on public.inimigos;
create policy inimigos_ver on public.inimigos for select to authenticated using (dono = auth.uid());
drop policy if exists inimigos_criar on public.inimigos;
create policy inimigos_criar on public.inimigos for insert to authenticated with check (dono = auth.uid());
drop policy if exists inimigos_editar on public.inimigos;
create policy inimigos_editar on public.inimigos for update to authenticated using (dono = auth.uid()) with check (dono = auth.uid());
drop policy if exists inimigos_apagar on public.inimigos;
create policy inimigos_apagar on public.inimigos for delete to authenticated using (dono = auth.uid());

revoke all on public.inimigos from anon, authenticated;
grant select, insert, update, delete on public.inimigos to authenticated;
