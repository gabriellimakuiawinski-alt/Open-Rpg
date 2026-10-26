# Banco (Supabase)

Projeto "Open Rpg" (`riltokltdqpccckpqmal`). Postgres + RLS + Realtime + Storage. **Quem protege é o RLS**; o cliente usa só a chave publishable.

## Ordem dos SQL (rodar no SQL Editor; todos re-executáveis)
1. `schema.sql` 2. `schema_etapa2.sql` 3. `schema_etapa2b.sql` 4. `schema_etapa3.sql` 5. `schema_etapa3b_musica.sql` 6. `schema_etapa4.sql` 7. `schema_etapa5.sql`
**Pendente no projeto do usuário:** 5, 6 e 7. Confirmar com ele se já rodou. As páginas funcionam sem o 7 (sem loja/dinheiro/sistema; mostram aviso).

## Tabelas
`profiles, campanhas, campanha_membros, mesas (campanha_id opcional, musica_id), membros, cenas, mapas_cena, tokens, personagens, pastas, arquivos, playlists, notas (do mestre), notas_jogador (PK mesa_id+user_id, só o dono lê/escreve)`.
- `cenas`: escuro, escuridao, nevoa, paredes, versao. `tokens`: personagem_id, `dados` jsonb (hp, pv, mn, mm, sn, sm, lo, lz…).
- `personagens.dados` jsonb: info, attrs, stats `[{id,n,cur,max,c}]`, skills, inv, poderes, docs, notas.
- `arquivos`: tipo (aud/mapa/chr/prop/mnt), efeito, atalho, path `<mesa>/<id>-nome`. Storage privado `mesa-arquivos`, acesso por URL assinada.

## Etapa 5 (sistema, dinheiro, lojas, homebrew, luz)
- `campanhas.sistema` ('op' | 'modular', padrão 'op') e `campanhas.config` jsonb (`moeda`, `determinacao`, `catalogoLivre`).
- `personagens.dinheiro`: só o mestre da campanha muda (trigger `ficha_dinheiro_protegido`); ficha nova nasce com 0. A RPC `comprar(p_item,p_ficha,p_qtd)` é a única outra via (liga `openrpg.compra`).
- `lojas` (aberta = jogadores veem), `loja_itens` (item jsonb como vai para o inventário, preço, estoque null = ∞), `loja_compras` (histórico; só `comprar()` grava).
- `catalogo` (homebrews/itens da campanha): jogador cria pendente; só o mestre aprova.
- Luz: `luz_da_ficha(dados)` → melhor `{c,l}` em metros dos itens com `luz:{t:'c'|'l',m}`. Trigger `token_luz_auto` (tokens ligados a ficha em campanha 'op') força `lz = m / grade_m` e apaga se não houver fonte. `ficha_luz_tokens` recalcula ao mudar o inventário.

## Funções-chave (security definer)
Permissão: `eh_membro, eh_mestre, pode_gerir, c_membro, c_mestre, c_gerir, c_usuario, usuario_na_mesa, cena_visivel, arquivo_em_uso, musica_em_uso`.
RPCs usadas pelo site: `entrar_na_campanha, entrar_na_mesa, marcar_acesso_mesa, ativar_cena, mover_token`.
Sincronia ficha↔token: `token_para_ficha, ficha_para_tokens, stats_aplica, barras_da_ficha` + triggers (cuidado com laço: usa `pg_trigger_depth`).

## Realtime
- `postgres_changes` nas tabelas da mesa.
- Broadcast no canal `mesa:<id>`: eventos `musica` (mestre→jogadores) e `dado` (rolagens, inclusive secretas).

## Regras de ouro
- Toda tabela nova: `enable row level security` + policies; testar no `tools/tests/m/`.
- Nunca confiar em checagem só no cliente.
