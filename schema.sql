-- =====================================================================
-- MESA RPG — ETAPA 1: contas, mesas, membros e personagens (fichas)
--
-- COMO USAR: no painel do Supabase abra "SQL Editor", clique em "New query",
-- cole TUDO isto e clique em "Run". Pode rodar de novo sem quebrar nada.
--
-- Ideia central: a ficha mora em "personagens.dados" (jsonb, formato livre),
-- então você pode mudar o sistema de regras sem mexer no banco.
-- Quem pode o quê:
--   * cada pessoa vê e edita as PRÓPRIAS fichas;
--   * o MESTRE de uma mesa vê e edita as fichas ligadas à mesa dele;
--   * jogadores entram numa mesa pelo código de convite;
--   * ninguém além do dono exclui uma ficha.
-- =====================================================================

-- ---------- Funções auxiliares ----------

-- Gera um código de convite único (8 caracteres)
create or replace function public.gerar_codigo() returns text
language plpgsql as $$
declare c text;
begin
  loop
    c := upper(substr(md5(random()::text || clock_timestamp()::text), 1, 8));
    exit when not exists (select 1 from public.mesas where codigo = c);
  end loop;
  return c;
end $$;

-- ---------- Tabelas ----------

create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  nome text not null default '',
  criado_em timestamptz not null default now()
);

create table if not exists public.mesas (
  id uuid primary key default gen_random_uuid(),
  nome text not null,
  mestre_id uuid not null references public.profiles(id) on delete cascade,
  codigo text not null unique default public.gerar_codigo(),
  criado_em timestamptz not null default now()
);

create table if not exists public.membros (
  mesa_id uuid not null references public.mesas(id) on delete cascade,
  user_id uuid not null references public.profiles(id) on delete cascade,
  papel text not null default 'jogador' check (papel in ('mestre', 'jogador')),
  entrou_em timestamptz not null default now(),
  primary key (mesa_id, user_id)
);

create table if not exists public.personagens (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.profiles(id) on delete cascade,
  mesa_id uuid references public.mesas(id) on delete set null,
  nome text not null default '',
  dados jsonb not null default '{}'::jsonb,
  criado_em timestamptz not null default now(),
  atualizado_em timestamptz not null default now()
);
create index if not exists personagens_user_idx on public.personagens(user_id);
create index if not exists personagens_mesa_idx on public.personagens(mesa_id);

-- ---------- Funções de permissão (usadas nas regras abaixo) ----------
-- "security definer" evita que as regras de segurança fiquem em loop.

create or replace function public.eh_membro(m uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.membros where mesa_id = m and user_id = auth.uid());
$$;

create or replace function public.eh_mestre(m uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.mesas where id = m and mestre_id = auth.uid());
$$;

create or replace function public.usuario_na_mesa(m uuid, u uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.membros where mesa_id = m and user_id = u);
$$;

create or replace function public.divide_mesa(u uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (
    select 1 from public.membros a join public.membros b on a.mesa_id = b.mesa_id
    where a.user_id = auth.uid() and b.user_id = u
  );
$$;

-- Entrar numa mesa pelo código de convite
create or replace function public.entrar_na_mesa(p_codigo text) returns uuid
language plpgsql security definer set search_path = public as $$
declare m uuid;
begin
  if auth.uid() is null then raise exception 'Faça login primeiro'; end if;
  select id into m from public.mesas where codigo = upper(trim(p_codigo));
  if m is null then raise exception 'Código de mesa inválido'; end if;
  insert into public.membros (mesa_id, user_id, papel) values (m, auth.uid(), 'jogador')
    on conflict do nothing;
  return m;
end $$;
revoke all on function public.entrar_na_mesa(text) from public, anon;
grant execute on function public.entrar_na_mesa(text) to authenticated;

-- ---------- Gatilhos (automações) ----------

-- Ao criar uma conta, cria o perfil com o nome
create or replace function public.novo_usuario() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  insert into public.profiles (id, nome)
  values (new.id, coalesce(nullif(new.raw_user_meta_data->>'nome', ''), split_part(new.email, '@', 1)))
  on conflict (id) do nothing;
  return new;
end $$;
drop trigger if exists ao_criar_usuario on auth.users;
create trigger ao_criar_usuario after insert on auth.users
  for each row execute function public.novo_usuario();

-- Contas que já existiam antes deste script ganham perfil também
insert into public.profiles (id, nome)
select id, coalesce(nullif(raw_user_meta_data->>'nome', ''), split_part(email, '@', 1))
from auth.users on conflict (id) do nothing;

-- Quem cria a mesa vira membro com papel de mestre
create or replace function public.mesa_criada() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  insert into public.membros (mesa_id, user_id, papel) values (new.id, new.mestre_id, 'mestre')
    on conflict do nothing;
  return new;
end $$;
drop trigger if exists ao_criar_mesa on public.mesas;
create trigger ao_criar_mesa after insert on public.mesas
  for each row execute function public.mesa_criada();

-- Quem sai (ou é removido) da mesa tem as fichas desvinculadas dela
create or replace function public.membro_saiu() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  update public.personagens set mesa_id = null
  where mesa_id = old.mesa_id and user_id = old.user_id;
  return old;
end $$;
drop trigger if exists ao_sair_da_mesa on public.membros;
create trigger ao_sair_da_mesa after delete on public.membros
  for each row execute function public.membro_saiu();

-- Atualiza a data de modificação e impede trocar o dono da ficha
create or replace function public.personagem_antes_de_salvar() returns trigger
language plpgsql as $$
begin
  new.atualizado_em := now();
  if tg_op = 'UPDATE' and new.user_id is distinct from old.user_id then
    raise exception 'Não é permitido trocar o dono do personagem';
  end if;
  return new;
end $$;
drop trigger if exists antes_de_salvar_personagem on public.personagens;
create trigger antes_de_salvar_personagem before update on public.personagens
  for each row execute function public.personagem_antes_de_salvar();

-- ---------- Regras de segurança (RLS) ----------

alter table public.profiles    enable row level security;
alter table public.mesas       enable row level security;
alter table public.membros     enable row level security;
alter table public.personagens enable row level security;

-- profiles: vê o próprio e o de quem divide mesa com você
drop policy if exists profiles_ver on public.profiles;
create policy profiles_ver on public.profiles for select to authenticated
  using (id = auth.uid() or public.divide_mesa(id));
drop policy if exists profiles_criar on public.profiles;
create policy profiles_criar on public.profiles for insert to authenticated
  with check (id = auth.uid());
drop policy if exists profiles_editar on public.profiles;
create policy profiles_editar on public.profiles for update to authenticated
  using (id = auth.uid()) with check (id = auth.uid());

-- mesas: membros veem; qualquer pessoa logada cria a sua; só o mestre altera/exclui
drop policy if exists mesas_ver on public.mesas;
create policy mesas_ver on public.mesas for select to authenticated
  using (mestre_id = auth.uid() or public.eh_membro(id));
drop policy if exists mesas_criar on public.mesas;
create policy mesas_criar on public.mesas for insert to authenticated
  with check (mestre_id = auth.uid());
drop policy if exists mesas_editar on public.mesas;
create policy mesas_editar on public.mesas for update to authenticated
  using (public.eh_mestre(id)) with check (mestre_id = auth.uid());
drop policy if exists mesas_excluir on public.mesas;
create policy mesas_excluir on public.mesas for delete to authenticated
  using (public.eh_mestre(id));

-- membros: só quem é da mesa vê. Entrar é feito pela função entrar_na_mesa().
-- Sair: o próprio jogador, ou o mestre removendo um jogador (o mestre não sai da própria mesa).
drop policy if exists membros_ver on public.membros;
create policy membros_ver on public.membros for select to authenticated
  using (public.eh_membro(mesa_id));
drop policy if exists membros_sair on public.membros;
create policy membros_sair on public.membros for delete to authenticated
  using (papel <> 'mestre' and (user_id = auth.uid() or public.eh_mestre(mesa_id)));

-- personagens: o dono e o mestre da mesa veem e editam; só o dono cria e exclui.
-- A ficha só pode ser ligada a uma mesa da qual o dono faz parte.
drop policy if exists personagens_ver on public.personagens;
create policy personagens_ver on public.personagens for select to authenticated
  using (user_id = auth.uid() or public.eh_mestre(mesa_id));
drop policy if exists personagens_criar on public.personagens;
create policy personagens_criar on public.personagens for insert to authenticated
  with check (user_id = auth.uid() and (mesa_id is null or public.usuario_na_mesa(mesa_id, user_id)));
drop policy if exists personagens_editar on public.personagens;
create policy personagens_editar on public.personagens for update to authenticated
  using (user_id = auth.uid() or public.eh_mestre(mesa_id))
  with check ((user_id = auth.uid() or public.eh_mestre(mesa_id))
              and (mesa_id is null or public.usuario_na_mesa(mesa_id, user_id)));
drop policy if exists personagens_excluir on public.personagens;
create policy personagens_excluir on public.personagens for delete to authenticated
  using (user_id = auth.uid());

-- ---------- Permissões de acesso às tabelas ----------
grant usage on schema public to authenticated;
grant select, insert, update on public.profiles to authenticated;
grant select, insert, update, delete on public.mesas to authenticated;
grant select, delete on public.membros to authenticated;
grant select, insert, update, delete on public.personagens to authenticated;

-- ---------- Tempo real: mudanças nas fichas chegam ao vivo ----------
do $$
begin
  alter publication supabase_realtime add table public.personagens;
exception when duplicate_object then null;
end $$;
