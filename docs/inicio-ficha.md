# Início e ficha

## index.html
- Splash "ABERTO" (carimbo), herói com polaroid, abas (`.divisorias`), pastas de campanha, faixas de mesa, cartões de ficha.
- Formulários como papel: `perguntar/pedir`; confirmações com `carimbar`; avisos com `aviso`.
- Campanha: aba **Grupo** com "Exportar campanha" e "Exportar minhas fichas" (`exportarCamp`/`baixar`).
- `vivo()`: revelar ao rolar (IntersectionObserver `.rv/.vis`), contadores, inclinação do herói; poeira em `#poeira`; luminária `.luz`.
- Som: botão `.radio` + painel `#som-pop` (ver docs/som.md). `sessionStorage open_rpg_abertura` evita repetir a abertura.
- Mesa pode ser avulsa (sem campanha) ou dentro de campanha.

## Sistemas
- A campanha escolhe o sistema (criar campanha / botão "Sistema e regras" do mestre). Ficha sem campanha escolhe o próprio (`dados.sistema`).
- **Ordem Paranormal** (`ficha-op.js`): `dados.op = {classe, nex|estagio, origem, trilha, pp, bonus{}, avisos[], visto, ult{}}`. `SIS.aplicar` recalcula PV/PE/SAN máx. (sobe o atual junto), Defesa (10+AGI+proteção equipada+escudo+efeitos−sobrecarga), carga, deslocamento, PE/turno, patente e limites, DT de rituais. Subir NEX gera `avisos` (trilha, poder, atributo, grau…). Itens: `tipo, catg, esp, qtd, eq, sub/def, arma{dano,crit,per}, luz{t,m}, ef[]`. Regras do item só o mestre edita. Habilidades: `tipo` (poder/ritual/…/homebrew), `pe`, `circ`, `ef[{a,v,nv}]` (efeito automático). Homebrew → `catalogo` (mestre aprova). Determinação (config) troca PE+SAN por PD (stat id `pe`, nome PD).
- Habilidades do livro: aba Habilidades → **＋ Do livro** (`doLivro` em `ficha-op.js`) lê `livro_habilidades` (classe/poder/trilha de combatente, especialista e ocultista), copia para `f.poderes` com `ref:'livro:<ref>'` (sem duplicar) e preenche `op.trilha` se estiver vazio.
- **Modular**: a ficha antiga, tudo editável, mais `secoes` livres.
- Não renderize sem `OP.calc` antes; `OP.depois(f)` diz se precisa redesenhar (redesenha no `change` para não perder o foco).

## ficha.html
- Seções: info, atributos, stats (PV/PE/SAN…), perícias, inventário, poderes, **Documentos** (imagens comprimidas por `comprime()`, `verDoc()`, sem peso), notas.
- `completa()` garante os campos novos em fichas antigas (ex.: `docs`).
- Dados em `personagens.dados` (jsonb). Ver docs/banco.md.
- Mesma linguagem visual do `tema.css`.
