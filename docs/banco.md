# Banco (Supabase)

Projeto "Open Rpg" (`riltokltdqpccckpqmal`). Postgres + RLS + Realtime + Storage. **Quem protege é o RLS**; o cliente usa só a chave publishable.

## Ordem dos SQL (rodar no SQL Editor; todos re-executáveis)
1. `schema.sql` 2. `schema_etapa2.sql` 3. `schema_etapa2b.sql` 4. `schema_etapa3.sql` 5. `schema_etapa3b_musica.sql` 6. `schema_etapa4.sql` 7. `schema_etapa5.sql` 8. `schema_etapa6_livro.sql` 9. `schema_etapa6b_rituais.sql` 10. `schema_etapa6c_origens.sql` 11. `schema_etapa6d_itens.sql` 12. `schema_etapa7_quadro.sql`
**Pendente no projeto do usuário:** 5, 6, 7, 8 e 9. Confirmar com ele se já rodou. As páginas funcionam sem o 7 (sem loja/dinheiro/sistema; mostram aviso).

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

## Etapa 6 (habilidades do livro)
- `livro_habilidades` (ref PK, sistema, fonte, classe, grupo `classe|poder|trilha`, trilha, nex, ordem, nome, `dados` jsonb já no formato de poder da ficha: tipo, desc, pe, ef[]). **Global e só leitura** para `authenticated` (sem policy de escrita; quem altera é o dono rodando SQL). Rituais e outros livros entram na mesma tabela (coluna `fonte`).
- O SQL é GERADO por `python3 tools/livro/gerar_op_basico.py` (edite os dados lá, não o `.sql`). Textos são resumos da mecânica (livro v1.2), não cópia.
- Rituais (`schema_etapa6b_rituais.sql`, gerado por `tools/livro/gerar_op_rituais.py`): 82 linhas `grupo='ritual'`, `classe` null, colunas `circulo` (1–4) e `elemento` (null = Amaldiçoar Arma, escolhe ao aprender); `dados` = `{tipo:'ritual', circ, el, pe (custo do círculo 1/3/6/10), desc (parâmetros + efeito + formas discente/verdadeira), ef:[]}`. Sem efeito automático.
- Origens e poderes paranormais (`schema_etapa6c_origens.sql`, gerado por `tools/livro/gerar_op_origens.py`): 26 linhas `grupo='origem'` (dados: `pericias[]`, `origem`, `desc`, `ef`) e 22 `grupo='paranormal'` (coluna `elemento`; dados: `pre`, `desc`, `ef`). `classe` null. Rode depois do 6b (o 6c só troca o check de `grupo`).
- Itens e armas (`schema_etapa6d_itens.sql`, gerado por `tools/livro/gerar_op_itens.py`): tabela nova `livro_itens` (global, só leitura, mesmo RLS). 110 linhas: 35 armas, 6 munições, 3 proteções, 3 acessórios, 5 explosivos, 19 operacionais, 16 paranormais, 23 modificações. `dados` já no formato do item da ficha (`tipo, catg, esp, arma{dano,crit,alc,td,per}, def, sub, ef, luz, desc`); `mc` = classe para modificações (corpo/disparo/fogo/municao/protecao/acessorio); modificações têm `aplica[]` e `mod{catg,esp,def}`. Sem dependência dos outros SQLs.

## Etapa 7 (quadro de investigação)
- `quadro_itens` (campanha_id, autor, tipo nota|documento|foto, titulo, texto, imagem = data URL reduzida ≤ 900 mil caracteres, cor, x, y, rot, `so_mestre`) e `quadro_ligacoes` (de, para = fios). RLS: membro da campanha vê e cria; só o autor ou mestre/admin edita/apaga; `so_mestre` esconde do jogador. Trigger trava `autor`/`campanha_id`. Realtime ligado. Página `quadro.html?camp=ID` (botão "Quadro de investigação" na tela da campanha). Teste t21.
- Efeito automático (`ef`) só onde a regra é exata: Reflexos Defensivos, Casca Grossa (PV × nível), Iniciativa Aprimorada, Gatuno. O resto fica na descrição.

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
