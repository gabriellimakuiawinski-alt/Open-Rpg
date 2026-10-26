# Testes e gerador

Tudo em `tools/`. Precisa de Postgres 16 local (porta 54329, socket `/tmp/pgtest`), Playwright (Chromium) e `psql`.

## Preparar (cada sessão nova)
```
# iniciar o cluster de teste (se ainda não existir, criar: initdb em /tmp/pgtest/data)
pg_isready -h /tmp/pgtest -p 54329 || su postgres -c "/usr/lib/postgresql/16/bin/pg_ctl -D /tmp/pgtest/data -o '-p 54329 -k /tmp/pgtest' -l /tmp/pgtest/log start"
bash tools/tests/t/mkdb.sh        # recria o banco e2e com os schemas reais
```
## Rodar
- E2E (Playwright com cliente Supabase simulado `mock2.js` + banco real via `pgx.py`): `cd tools/tests/e && python3 t1.py` … `t14.py`, `fx.py`, `fog.py`. Cada arquivo termina com `report()` (imprime `FALHOU: n`). Capturas vão para `/tmp/open-rpg-shots/`.
- SQL de permissões: `bash tools/tests/m/run3.sh` (66 ok esperado); `perm4.sql`/`perm5.sql` rodam com `psql -d e2e -f` depois do `mkdb.sh`; `m/mig.sh` testa a migração da etapa 3.
- `lib.py` = harness do tabletop; `lib2.py` = harness de index/ficha.

## Quando rodar
Antes de publicar: `python3 tools/build/build.py` (mesa.html), e as suítes da área mexida (mesa → t1–t6, t9–t12, fx, fog; início/ficha → t7, t8, t13, t14; banco → m/*).
Teste novo: copie um `tN.py`, use `chk()` e termine com `report()`.

## Limites
O mock não prova o realtime real nem multi-dispositivo. Validar no site com 2 contas depois de rodar os SQL.
