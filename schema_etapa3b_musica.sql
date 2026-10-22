-- =====================================================================
-- OPEN RPG — MÚSICA COMPARTILHADA
-- Rode no SQL Editor do Supabase (New query -> colar tudo -> Run).
-- Pode rodar de novo sem quebrar nada.
--
-- O QUE FAZ: quando o mestre toca uma música, os jogadores da mesa passam a
-- ouvir também. Os jogadores só conseguem abrir O ARQUIVO DA FAIXA QUE ESTÁ
-- TOCANDO — o resto da biblioteca de músicas continua só do mestre.
-- =====================================================================
alter table public.mesas
  add column if not exists musica_id uuid references public.arquivos(id) on delete set null;

create or replace function public.musica_em_uso(a uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.mesas m
                 where m.musica_id = a and public.eh_membro(m.id));
$$;

drop policy if exists arquivos_ver on public.arquivos;
create policy arquivos_ver on public.arquivos for select to authenticated
  using ((tipo = 'aud' and public.eh_mestre(mesa_id))
         or (tipo <> 'aud' and public.pode_gerir(mesa_id))
         or (criado_por = auth.uid() and public.eh_membro(mesa_id))
         or (tipo <> 'aud' and public.arquivo_em_uso(id))
         or (tipo = 'aud' and public.musica_em_uso(id)));
