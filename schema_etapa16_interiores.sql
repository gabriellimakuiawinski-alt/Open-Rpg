-- Etapa 16: mapas de interior (um mapa dentro de um local marcado em outro mapa).
-- Cada cena guarda a lista de interiores: [{id, i (arquivo do mapa), x, y, w, h, t (1 = telhado ligado, interior escondido), p (1 = manter proporção)}].
-- Re-executável.
alter table public.cenas add column if not exists interiores jsonb not null default '[]'::jsonb;
do $$ begin
  if not exists (select 1 from pg_constraint where conname = 'cenas_interiores_array') then
    alter table public.cenas add constraint cenas_interiores_array check (jsonb_typeof(interiores) = 'array');
  end if;
end $$;

-- O jogador precisa poder ler a imagem do mapa de interior de uma cena que ele vê
create or replace function public.arquivo_em_uso(a uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (
      select 1 from public.tokens t
      where (t.imagem_id = a or t.imagem_caido_id = a or a = any(t.alts))
        and public.cena_visivel(t.cena_id)
        and (not t.oculto or public.pode_gerir(public.mesa_da_cena(t.cena_id))))
    or exists (
      select 1 from public.mapas_cena mc
      where mc.arquivo_id = a and public.cena_visivel(mc.cena_id))
    or exists (
      select 1 from public.cenas c, jsonb_array_elements(c.interiores) e
      where e->>'i' = a::text and public.cena_visivel(c.id));
$$;
