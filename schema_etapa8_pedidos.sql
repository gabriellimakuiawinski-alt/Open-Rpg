-- =====================================================================
-- OPEN RPG — ETAPA 8: pedidos ao mestre (ex.: modificação que a patente não permite)
--
-- COMO USAR: rode no SQL Editor do Supabase (New query -> colar tudo -> Run).
-- Depende só do schema_etapa3.sql (c_membro / c_gerir) e da tabela personagens. Pode rodar de novo.
-- O jogador envia o pedido; o mestre/admin aprova ou recusa na aba "Pedidos" da campanha;
-- se aprovado, a própria ficha do jogador aplica o item e marca o pedido como "aplicado".
-- =====================================================================

create table if not exists public.pedidos (
  id            uuid primary key default gen_random_uuid(),
  campanha_id   uuid not null references public.campanhas(id) on delete cascade,
  personagem_id uuid not null references public.personagens(id) on delete cascade,
  autor         uuid not null default auth.uid(),
  tipo          text not null default 'modificacao' check (tipo in ('modificacao')),
  titulo        text not null default '',
  detalhe       text not null default '',
  dados         jsonb not null default '{}'::jsonb,
  estado        text not null default 'pendente' check (estado in ('pendente', 'aprovado', 'recusado', 'aplicado')),
  resposta      text not null default '',
  criado_em     timestamptz not null default now(),
  decidido_em   timestamptz,
  constraint pedidos_tamanho check (length(titulo) <= 300 and length(detalhe) <= 2000 and length(resposta) <= 2000 and length(dados::text) <= 20000)
);
create index if not exists pedidos_camp_idx on public.pedidos(campanha_id, estado);
create index if not exists pedidos_pers_idx on public.pedidos(personagem_id);

-- quem pode mudar o quê: mestre/admin decide (pendente -> aprovado/recusado, com resposta);
-- o autor só confirma que aplicou (aprovado -> aplicado). O resto fica travado.
create or replace function public.pedidos_travas() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  new.autor := old.autor; new.campanha_id := old.campanha_id; new.personagem_id := old.personagem_id;
  new.tipo := old.tipo; new.titulo := old.titulo; new.detalhe := old.detalhe; new.dados := old.dados; new.criado_em := old.criado_em;
  if new.estado is not distinct from old.estado and new.resposta is not distinct from old.resposta then return new; end if;
  if old.estado = 'aprovado' and new.estado = 'aplicado' and old.autor = auth.uid() then
    new.resposta := old.resposta; new.decidido_em := old.decidido_em; return new;
  end if;
  if public.c_gerir(old.campanha_id) and old.estado = 'pendente' and new.estado in ('aprovado', 'recusado') then
    new.decidido_em := now(); return new;
  end if;
  raise exception 'Mudança de pedido não permitida';
end $$;
drop trigger if exists pedidos_travas on public.pedidos;
create trigger pedidos_travas before update on public.pedidos
  for each row execute function public.pedidos_travas();

alter table public.pedidos enable row level security;

drop policy if exists pedidos_ver on public.pedidos;
create policy pedidos_ver on public.pedidos for select to authenticated
  using (public.c_membro(campanha_id) and (autor = auth.uid() or public.c_gerir(campanha_id)));
drop policy if exists pedidos_criar on public.pedidos;
create policy pedidos_criar on public.pedidos for insert to authenticated
  with check (public.c_membro(campanha_id) and autor = auth.uid() and estado = 'pendente'
    and exists (select 1 from public.personagens p where p.id = personagem_id and p.user_id = auth.uid() and p.campanha_id = pedidos.campanha_id));
drop policy if exists pedidos_editar on public.pedidos;
create policy pedidos_editar on public.pedidos for update to authenticated
  using (public.c_membro(campanha_id) and (autor = auth.uid() or public.c_gerir(campanha_id)))
  with check (public.c_membro(campanha_id) and (autor = auth.uid() or public.c_gerir(campanha_id)));
drop policy if exists pedidos_apagar on public.pedidos;
create policy pedidos_apagar on public.pedidos for delete to authenticated
  using (public.c_membro(campanha_id) and (autor = auth.uid() or public.c_gerir(campanha_id)));

revoke all on public.pedidos from anon, authenticated;
grant select, insert, update, delete on public.pedidos to authenticated;

do $$ begin alter publication supabase_realtime add table public.pedidos;
exception when duplicate_object then null; when undefined_object then null; end $$;
