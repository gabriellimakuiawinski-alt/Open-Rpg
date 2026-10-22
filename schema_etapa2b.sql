-- =====================================================================
-- MESA RPG — ETAPA 2 (parte 2): ajustes para o tabletop na nuvem
--
-- COMO USAR: rode DEPOIS do schema_etapa2.sql, no SQL Editor do Supabase
-- (New query -> colar tudo -> Run). Pode rodar de novo sem quebrar nada.
--
-- O que muda:
--   * "miniatura": cada imagem da biblioteca guarda uma versão minúscula,
--     para a lista de assets abrir rápido sem baixar mapas inteiros;
--   * trocar a categoria de um arquivo (personagem <-> prop <-> montaria);
--   * mudanças na biblioteca chegam ao vivo para quem está na mesa.
-- =====================================================================

alter table public.arquivos add column if not exists miniatura text;

-- Categoria pode mudar apenas entre personagem / prop / montaria.
-- (Mapas e áudios continuam fixos, senão um jogador poderia transformar a
-- própria imagem em "mapa" e fugir das regras.)
create or replace function public.arquivo_imutavel() returns trigger
language plpgsql as $$
begin
  if pg_trigger_depth() > 1 then return new; end if;  -- limpeza automática (ex.: conta excluída)
  if new.mesa_id is distinct from old.mesa_id
     or new.path is distinct from old.path
     or new.criado_por is distinct from old.criado_por then
    raise exception 'Não é permitido mudar mesa, dono ou caminho do arquivo';
  end if;
  if new.tipo is distinct from old.tipo
     and not (old.tipo in ('chr', 'prop', 'mnt') and new.tipo in ('chr', 'prop', 'mnt')) then
    raise exception 'Só é possível trocar entre personagem, prop e montaria';
  end if;
  return new;
end $$;

do $$
begin
  alter publication supabase_realtime add table public.arquivos;
exception when duplicate_object then null;
end $$;
