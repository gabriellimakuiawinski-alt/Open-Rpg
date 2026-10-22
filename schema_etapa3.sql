-- =====================================================================
-- OPEN RPG — ETAPA 3: campanhas, mesas avulsas e página inicial
--
-- COMO USAR: rode DEPOIS do schema_etapa2b.sql, no SQL Editor do Supabase
-- (New query -> colar tudo -> Run). Pode rodar de novo sem quebrar nada.
--
-- O QUE MUDA
--   CAMPANHA = um grupo de pessoas + as fichas delas (e um código de convite).
--   MESA     = o tabletop (cenas, tokens, biblioteca). Pode pertencer a uma
--              campanha ou ser avulsa.
--   * Mesa de campanha: todo mundo da campanha entra sozinho nela, com o mesmo
--     papel (mestre / admin / jogador), e as fichas da campanha ficam
--     disponíveis para ligar aos tokens.
--   * Mesa avulsa (sem campanha): NÃO tem fichas. Entra-se pelo código da mesa.
--   * Suas mesas atuais viram campanhas automaticamente (mesmo nome, mesmo
--     código de convite, mesmos membros, mesmas fichas). Nada se perde.
--   * "Última mesa": cada pessoa passa a ter a data do último acesso a cada mesa.
-- =====================================================================

-- ---------- Tabelas novas ----------

create table if not exists public.campanhas (
  id uuid primary key default gen_random_uuid(),
  nome text not null,
  mestre_id uuid not null references public.profiles(id) on delete cascade,
  codigo text not null unique default public.gerar_codigo(),
  criado_em timestamptz not null default now()
);

create table if not exists public.campanha_membros (
  campanha_id uuid not null references public.campanhas(id) on delete cascade,
  user_id uuid not null references public.profiles(id) on delete cascade,
  papel text not null default 'jogador' check (papel in ('mestre', 'admin', 'jogador')),
  entrou_em timestamptz not null default now(),
  primary key (campanha_id, user_id)
);
create index if not exists campanha_membros_user_idx on public.campanha_membros(user_id);

alter table public.membros add column if not exists ultimo_acesso timestamptz;

-- ---------- Migração (roda uma única vez): cada mesa antiga vira uma campanha ----------
do $$
begin
  if not exists (select 1 from information_schema.columns
                 where table_schema = 'public' and table_name = 'mesas' and column_name = 'campanha_id') then
    alter table public.mesas add column campanha_id uuid references public.campanhas(id) on delete set null;
    alter table public.personagens add column campanha_id uuid references public.campanhas(id) on delete set null;

    insert into public.campanhas (id, nome, mestre_id, codigo, criado_em)
      select id, nome, mestre_id, codigo, criado_em from public.mesas
      on conflict (id) do nothing;
    insert into public.campanha_membros (campanha_id, user_id, papel, entrou_em)
      select mesa_id, user_id, papel, entrou_em from public.membros
      on conflict do nothing;
    update public.mesas set campanha_id = id;
    update public.personagens set campanha_id = mesa_id where mesa_id is not null;
  end if;
end $$;
create index if not exists mesas_campanha_idx on public.mesas(campanha_id);
create index if not exists personagens_campanha_idx on public.personagens(campanha_id);

-- ---------- Funções de permissão ----------

create or replace function public.c_membro(c uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.campanha_membros where campanha_id = c and user_id = auth.uid());
$$;

create or replace function public.c_mestre(c uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.campanhas where id = c and mestre_id = auth.uid());
$$;

create or replace function public.c_gerir(c uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.campanha_membros
                 where campanha_id = c and user_id = auth.uid() and papel in ('mestre', 'admin'));
$$;

create or replace function public.c_usuario(c uuid, u uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.campanha_membros where campanha_id = c and user_id = u);
$$;

create or replace function public.c_divide(u uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (
    select 1 from public.campanha_membros a join public.campanha_membros b on a.campanha_id = b.campanha_id
    where a.user_id = auth.uid() and b.user_id = u
  );
$$;

create or replace function public.mesa_em_campanha(m uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select coalesce((select campanha_id is not null from public.mesas where id = m), false);
$$;

-- ---------- Entrar por código ----------

-- Mesa avulsa: entra pelo código da mesa. Mesa de campanha: tem que entrar pela campanha.
create or replace function public.entrar_na_mesa(p_codigo text) returns uuid
language plpgsql security definer set search_path = public as $$
declare m public.mesas;
begin
  if auth.uid() is null then raise exception 'Faça login primeiro'; end if;
  select * into m from public.mesas where codigo = upper(trim(p_codigo));
  if m.id is null then raise exception 'Código de mesa inválido'; end if;
  if m.campanha_id is not null then
    raise exception 'Esta mesa pertence a uma campanha. Entre usando o código da campanha.';
  end if;
  insert into public.membros (mesa_id, user_id, papel) values (m.id, auth.uid(), 'jogador')
    on conflict do nothing;
  return m.id;
end $$;

create or replace function public.entrar_na_campanha(p_codigo text) returns uuid
language plpgsql security definer set search_path = public as $$
declare c uuid;
begin
  if auth.uid() is null then raise exception 'Faça login primeiro'; end if;
  select id into c from public.campanhas where codigo = upper(trim(p_codigo));
  if c is null then raise exception 'Código inválido'; end if;
  insert into public.campanha_membros (campanha_id, user_id, papel) values (c, auth.uid(), 'jogador')
    on conflict do nothing;
  return c;
end $$;

-- Anota que a pessoa abriu a mesa agora ("última mesa" da página inicial)
create or replace function public.marcar_acesso_mesa(p_mesa uuid) returns void
language sql security definer set search_path = public as $$
  update public.membros set ultimo_acesso = now() where mesa_id = p_mesa and user_id = auth.uid();
$$;

revoke all on function public.entrar_na_mesa(text), public.entrar_na_campanha(text),
  public.marcar_acesso_mesa(uuid) from public, anon;
grant execute on function public.entrar_na_mesa(text), public.entrar_na_campanha(text),
  public.marcar_acesso_mesa(uuid) to authenticated;

-- ---------- Gatilhos ----------

-- Quem cria a campanha vira o mestre dela
create or replace function public.campanha_criada() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  insert into public.campanha_membros (campanha_id, user_id, papel) values (new.id, new.mestre_id, 'mestre')
    on conflict do nothing;
  return new;
end $$;
drop trigger if exists ao_criar_campanha on public.campanhas;
create trigger ao_criar_campanha after insert on public.campanhas
  for each row execute function public.campanha_criada();

-- Quem cria a mesa vira mestre dela; numa campanha, o grupo todo entra junto
create or replace function public.mesa_criada() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  insert into public.membros (mesa_id, user_id, papel) values (new.id, new.mestre_id, 'mestre')
    on conflict do nothing;
  if new.campanha_id is not null then
    insert into public.membros (mesa_id, user_id, papel)
      select new.id, user_id, papel from public.campanha_membros
      where campanha_id = new.campanha_id and user_id <> new.mestre_id
      on conflict do nothing;
  end if;
  return new;
end $$;

-- A campanha de uma mesa não muda depois de criada
create or replace function public.mesa_antes_de_salvar() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  if pg_trigger_depth() > 1 then return new; end if;  -- limpeza automática (campanha excluída)
  if new.campanha_id is distinct from old.campanha_id then
    raise exception 'A campanha de uma mesa não pode ser trocada';
  end if;
  return new;
end $$;
drop trigger if exists antes_de_salvar_mesa on public.mesas;
create trigger antes_de_salvar_mesa before update on public.mesas
  for each row execute function public.mesa_antes_de_salvar();

-- Entrou / mudou de papel / saiu da campanha -> o mesmo acontece nas mesas dela
create or replace function public.cmembro_entrou() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  insert into public.membros (mesa_id, user_id, papel)
    select id, new.user_id, new.papel from public.mesas where campanha_id = new.campanha_id
    on conflict do nothing;
  return new;
end $$;
drop trigger if exists ao_entrar_campanha on public.campanha_membros;
create trigger ao_entrar_campanha after insert on public.campanha_membros
  for each row execute function public.cmembro_entrou();

create or replace function public.cmembro_mudou() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  if new.papel is distinct from old.papel then
    update public.membros set papel = new.papel
    where user_id = new.user_id and papel <> 'mestre'
      and mesa_id in (select id from public.mesas where campanha_id = new.campanha_id);
  end if;
  return new;
end $$;
drop trigger if exists ao_mudar_papel_campanha on public.campanha_membros;
create trigger ao_mudar_papel_campanha after update on public.campanha_membros
  for each row execute function public.cmembro_mudou();

create or replace function public.cmembro_saiu() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  if pg_trigger_depth() > 1 then return old; end if;  -- exclusão em cascata (conta/campanha apagada)
  delete from public.membros
   where user_id = old.user_id
     and mesa_id in (select id from public.mesas where campanha_id = old.campanha_id);
  update public.personagens set campanha_id = null
   where user_id = old.user_id and campanha_id = old.campanha_id;
  return old;
end $$;
drop trigger if exists ao_sair_campanha on public.campanha_membros;
create trigger ao_sair_campanha after delete on public.campanha_membros
  for each row execute function public.cmembro_saiu();

-- (a regra antiga "sair da mesa solta as fichas" não existe mais: ficha é da campanha)
drop trigger if exists ao_sair_da_mesa on public.membros;

-- Ficha: só o dono ou o mestre da campanha muda "privada", "npc" e a campanha
create or replace function public.personagem_antes_de_salvar() returns trigger
language plpgsql security definer set search_path = public as $$
declare dono_ou_mestre boolean;
begin
  new.atualizado_em := now();
  if tg_op = 'UPDATE' then
    if new.user_id is distinct from old.user_id then
      raise exception 'Não é permitido trocar o dono do personagem';
    end if;
    if auth.uid() is not null and pg_trigger_depth() = 1 then
      dono_ou_mestre := old.user_id = auth.uid() or public.c_mestre(old.campanha_id);
      if not dono_ou_mestre and (new.privada is distinct from old.privada
                                 or new.npc is distinct from old.npc
                                 or new.campanha_id is distinct from old.campanha_id) then
        raise exception 'Só o dono da ficha ou o mestre pode mudar isso';
      end if;
    end if;
  end if;
  return new;
end $$;

-- Token só liga a ficha da própria campanha da mesa (mesa avulsa não tem fichas)
create or replace function public.token_ficha_valida() returns trigger
language plpgsql security definer set search_path = public as $$
declare c uuid;
begin
  if new.personagem_id is null then return new; end if;
  if tg_op = 'UPDATE' and new.personagem_id is not distinct from old.personagem_id then return new; end if;
  select campanha_id into c from public.mesas where id = public.mesa_da_cena(new.cena_id);
  if c is null or not exists (select 1 from public.personagens where id = new.personagem_id and campanha_id = c) then
    raise exception 'Esta ficha não pertence à campanha desta mesa';
  end if;
  return new;
end $$;
drop trigger if exists antes_ligar_ficha on public.tokens;
create trigger antes_ligar_ficha before insert or update on public.tokens
  for each row execute function public.token_ficha_valida();

-- Ficha que sai da campanha desliga dos tokens
create or replace function public.ficha_mudou_campanha() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  if new.campanha_id is distinct from old.campanha_id then
    update public.tokens set personagem_id = null where personagem_id = new.id;
  end if;
  return new;
end $$;
drop trigger if exists apos_mudar_campanha_ficha on public.personagens;
create trigger apos_mudar_campanha_ficha after update on public.personagens
  for each row execute function public.ficha_mudou_campanha();

-- ---------- Regras de segurança (RLS) ----------

alter table public.campanhas        enable row level security;
alter table public.campanha_membros enable row level security;

-- perfis: vê o próprio, quem divide mesa e quem divide campanha
drop policy if exists profiles_ver on public.profiles;
create policy profiles_ver on public.profiles for select to authenticated
  using (id = auth.uid() or public.divide_mesa(id) or public.c_divide(id));

-- campanhas: membros veem; qualquer pessoa cria a sua; só o mestre altera / exclui
drop policy if exists campanhas_ver on public.campanhas;
create policy campanhas_ver on public.campanhas for select to authenticated
  using (mestre_id = auth.uid() or public.c_membro(id));
drop policy if exists campanhas_criar on public.campanhas;
create policy campanhas_criar on public.campanhas for insert to authenticated
  with check (mestre_id = auth.uid());
drop policy if exists campanhas_editar on public.campanhas;
create policy campanhas_editar on public.campanhas for update to authenticated
  using (public.c_mestre(id)) with check (mestre_id = auth.uid());
drop policy if exists campanhas_excluir on public.campanhas;
create policy campanhas_excluir on public.campanhas for delete to authenticated
  using (public.c_mestre(id));

-- membros da campanha: quem é da campanha vê. Entrar = entrar_na_campanha().
-- Sair: o próprio jogador, ou o mestre removendo alguém. Só o mestre promove/rebaixa.
drop policy if exists cmembros_ver on public.campanha_membros;
create policy cmembros_ver on public.campanha_membros for select to authenticated
  using (public.c_membro(campanha_id));
drop policy if exists cmembros_sair on public.campanha_membros;
create policy cmembros_sair on public.campanha_membros for delete to authenticated
  using (papel <> 'mestre' and (user_id = auth.uid() or public.c_mestre(campanha_id)));
drop policy if exists cmembros_papel on public.campanha_membros;
create policy cmembros_papel on public.campanha_membros for update to authenticated
  using (papel <> 'mestre' and public.c_mestre(campanha_id))
  with check (papel in ('admin', 'jogador') and public.c_mestre(campanha_id));

-- mesas: numa campanha, só o mestre dela cria a mesa
drop policy if exists mesas_criar on public.mesas;
create policy mesas_criar on public.mesas for insert to authenticated
  with check (mestre_id = auth.uid() and (campanha_id is null or public.c_mestre(campanha_id)));

-- membros da mesa: numa mesa de campanha, entrar/sair/papel acontecem pela campanha
drop policy if exists membros_sair on public.membros;
create policy membros_sair on public.membros for delete to authenticated
  using (papel <> 'mestre' and (user_id = auth.uid() or public.eh_mestre(mesa_id))
         and not public.mesa_em_campanha(mesa_id));
drop policy if exists membros_papel on public.membros;
create policy membros_papel on public.membros for update to authenticated
  using (papel <> 'mestre' and public.eh_mestre(mesa_id) and not public.mesa_em_campanha(mesa_id))
  with check (papel in ('admin', 'jogador') and public.eh_mestre(mesa_id) and not public.mesa_em_campanha(mesa_id));

-- fichas: públicas para a campanha, exceto privadas e NPCs
drop policy if exists personagens_ver on public.personagens;
create policy personagens_ver on public.personagens for select to authenticated
  using (user_id = auth.uid()
         or public.c_mestre(campanha_id)
         or (campanha_id is not null and public.c_membro(campanha_id) and not privada and not npc));
drop policy if exists personagens_criar on public.personagens;
create policy personagens_criar on public.personagens for insert to authenticated
  with check (user_id = auth.uid() and (campanha_id is null or public.c_usuario(campanha_id, user_id)));
drop policy if exists personagens_editar on public.personagens;
create policy personagens_editar on public.personagens for update to authenticated
  using (user_id = auth.uid()
         or public.c_mestre(campanha_id)
         or (campanha_id is not null and public.c_gerir(campanha_id) and not privada and not npc))
  with check ((user_id = auth.uid()
               or public.c_mestre(campanha_id)
               or (campanha_id is not null and public.c_gerir(campanha_id) and not privada and not npc))
              and (campanha_id is null or public.c_usuario(campanha_id, user_id)));

-- ---------- Permissões e tempo real ----------
grant select, insert, update, delete on public.campanhas to authenticated;
grant select, delete on public.campanha_membros to authenticated;
grant update (papel) on public.campanha_membros to authenticated;

do $$ begin alter publication supabase_realtime add table public.campanhas;
exception when duplicate_object then null; end $$;
do $$ begin alter publication supabase_realtime add table public.campanha_membros;
exception when duplicate_object then null; end $$;
do $$ begin alter publication supabase_realtime add table public.membros;
exception when duplicate_object then null; end $$;
