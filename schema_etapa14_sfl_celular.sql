alter table public.campanhas drop constraint if exists campanhas_sistema_ok; alter table public.campanhas add constraint campanhas_sistema_ok check (sistema in ('op', 'sfl', 'modular'));
