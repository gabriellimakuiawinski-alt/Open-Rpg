-- Etapa 17: luzes fixas coloridas na cena escura. Cada cena guarda a lista:
-- [{id, x, y, R (quadrados), c (cor), a (intensidade 0.2 a 1), t ('l' lampião, 'c' lanterna em cone), la (abertura), d (direção em graus)}]. Re-executável.
alter table public.cenas add column if not exists luzes jsonb not null default '[]'::jsonb;
do $$ begin
  if not exists (select 1 from pg_constraint where conname = 'cenas_luzes_array') then
    alter table public.cenas add constraint cenas_luzes_array check (jsonb_typeof(luzes) = 'array');
  end if;
end $$;
