-- OPEN RPG — ETAPA 14: sistema Search For Light (SFL 2)
-- Libera 'sfl' como sistema da campanha. Re-executável. Rodar depois da etapa 5.
alter table public.campanhas drop constraint if exists campanhas_sistema_ok;
alter table public.campanhas add constraint campanhas_sistema_ok check (sistema in ('op', 'sfl', 'modular'));
