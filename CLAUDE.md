# Open RPG — guia para o Claude

Mesa virtual de RPG própria (inspirada no Owlbear Rodeo) com contas na nuvem. O dono é o **mestre** do grupo, fala **pt-BR**, usa **celular**: respostas curtas, sem jargão.
Site: https://gabriellimakuiawinski-alt.github.io/Open-Rpg/ (GitHub Pages, branch `main`). Supabase: projeto "Open Rpg" (`riltokltdqpccckpqmal`).

## Leia só o que precisar (um arquivo por assunto)
| Vou mexer em… | Leia |
|---|---|
| estrutura, cache, como gerar `mesa.html` | docs/arquitetura.md |
| tabelas, permissões, SQL | docs/banco.md |
| tabletop (mapa, tokens, fog, música, dados, caderno) | docs/mesa.md |
| tela inicial, ficha, sistemas e loja | docs/inicio-ficha.md |
| sons e trilha | docs/som.md |
| testes | docs/testes.md |
| dados do livro (habilidades, rituais) | tools/livro/ + docs/banco.md |
| o que falta / ideias | docs/pendencias.md |

## Regras que não mudam
- **Nunca** chave `secret`/`service_role` nem senha de banco no código. Só a chave *publishable* (em `comum.js`). Quem protege os dados é o RLS.
- **`mesa.html` é GERADO** por `python3 tools/build/build.py` (a partir de `tools/build/original/` + `nuvem.js`). Não edite o `mesa.html` à mão: mude `build.py`/`nuvem.js` ou os módulos `mesa-*.js` e regenere.
- Mudou CSS/JS? Suba o `?v=N` nas tags (no `index.html`, `ficha.html` e nas injeções do `build.py`), senão o celular fica com cache antigo.
- Arquivos que o usuário enviar são originais: trabalhe numa cópia.
- SQL novo: arquivo `schema_etapaN*.sql` **re-executável** (`if not exists`, `create or replace`, `drop policy if exists`). O MCP do Supabase costuma dar "cancelled": o usuário roda o SQL manualmente no SQL Editor. Diga a ordem exata.
- Não contorne o proxy do ambiente.

## Publicar (o usuário quer que o Claude faça sozinho)
```
git fetch origin main; git checkout main; git reset --hard FETCH_HEAD
git checkout -b <branch>; (alterar/copiar arquivos); git add -A; git commit
git push -u origin <branch>
gh api -X POST repos/gabriellimakuiawinski-alt/Open-Rpg/pulls -f title=… -f head=<branch> -f base=main -f body=…
sleep 3; gh api -X PUT repos/…/pulls/N/merge -f merge_method=squash   # 405 "Base branch was modified": esperar e repetir
git checkout main; git fetch origin main; git reset --hard FETCH_HEAD; git branch -D <branch>
```
Não dá para conferir o deploy do Pages daqui; avise o usuário para abrir em aba anônima.
Antes de publicar: `python3 tools/build/build.py` e rode os testes (docs/testes.md).

## Estado atual
Ver docs/pendencias.md. **Pendente do usuário:** rodar no Supabase `schema_etapa3b_musica.sql`, depois `schema_etapa4.sql`, depois `schema_etapa5.sql`, depois `schema_etapa6_livro.sql`.
