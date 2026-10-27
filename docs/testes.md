# Testes e gerador

Tudo em `tools/`. Precisa de Postgres 16 local (porta 54329, socket `/tmp/pgtest`), Playwright (Chromium) e `psql`.

## Preparar (cada sessão nova)
```
# iniciar o cluster de teste (se ainda não existir, criar: initdb em /tmp/pgtest/data)
pg_isready -h /tmp/pgtest -p 54329 || su postgres -c "/usr/lib/postgresql/16/bin/pg_ctl -D /tmp/pgtest/data -o '-p 54329 -k /tmp/pgtest' -l /tmp/pgtest/log start"
# cluster novo: criar os papéis uma vez
psql -h /tmp/pgtest -p 54329 -U postgres -c "create role authenticated nologin" -c "create role anon nologin" -c "create role service_role nologin bypassrls"
bash tools/tests/t/mkdb.sh        # recria o banco e2e com os schemas reais
```
## Rodar
- E2E (Playwright com cliente Supabase simulado `mock2.js` + banco real via `pgx.py`): `cd tools/tests/e && python3 t1.py` … `t14.py`, `fx.py`, `fog.py`. Cada arquivo termina com `report()` (imprime `FALHOU: n`). Capturas vão para `/tmp/open-rpg-shots/`.
- SQL de permissões: `bash tools/tests/m/run3.sh` (66 ok esperado); `perm4.sql`/`perm5.sql` rodam com `psql -d e2e -f` depois do `mkdb.sh`; `m/mig.sh` testa a migração da etapa 3.
- `lib.py` = harness do tabletop; `lib2.py` = harness de index/ficha.

## Quando rodar
Antes de publicar: `python3 tools/build/build.py` (mesa.html), e as suítes da área mexida (mesa → t1–t6, t9–t12, t15, fx, fog; início/ficha/loja → t7, t8, t13, t14, t15, t16, t17, t18, t19 e t20 (habilidades, avisos de NEX, rituais, origens, poderes paranormais e itens do livro), t21 (quadro de investigação), t23 (aba Criadas), t24 (modificações na arma), t25 (pedido ao mestre), t26 (botão Modificar), t27 (mestre livre em NPC), t28 (excluir), t29 (inimigos), t30 (bestiário do livro), t31 (ficha de monstro), t32 (calculador de VD), t33 (aba Combate), t34 (treino de perícias) e t22 (giro do token com a roda + ficha no menu do token); banco → m/*, inclusive `perm6.sql` da etapa 5).
Teste novo: copie um `tN.py`, use `chk()` e termine com `report()`.

Falhas `ERR_TUNNEL_CONNECTION_FAILED` são as fontes do Google bloqueadas no ambiente, não erro do código.

## Limites
O mock não prova o realtime real nem multi-dispositivo. Validar no site com 2 contas depois de rodar os SQL.
- t35 (treino por grau: 2/5/3 + Int, NEX 70) e t36 (editar monstro na ficha + token ao usar inimigo) em `tools/tests/e`.
- t37 (itens amaldiçoados), t38 (ritual por NEX do ocultista), t39 (condições e página de regras). Ao rodar vários testes, recrie o banco com `tools/tests/t/mkdb.sh` (t29 espera zero inimigos; o t30 cria um).
- t41 (complementos SaH no catálogo, Equipar, aliado, Bateria Potente) e t42 (escolha de complementos na campanha). `mkdb.sh` agora roda também a etapa 13. Num `pg.evaluate` de função que abre janela (ex. `novaCamp`) use `setTimeout(fn,0)`, senão o teste trava esperando a janela fechar.
