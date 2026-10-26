# Início e ficha

## index.html
- Splash "ABERTO" (carimbo), herói com polaroid, abas (`.divisorias`), pastas de campanha, faixas de mesa, cartões de ficha.
- Formulários como papel: `perguntar/pedir`; confirmações com `carimbar`; avisos com `aviso`.
- Campanha: aba **Grupo** com "Exportar campanha" e "Exportar minhas fichas" (`exportarCamp`/`baixar`).
- `vivo()`: revelar ao rolar (IntersectionObserver `.rv/.vis`), contadores, inclinação do herói; poeira em `#poeira`; luminária `.luz`.
- Som: botão `.radio` + painel `#som-pop` (ver docs/som.md). `sessionStorage open_rpg_abertura` evita repetir a abertura.
- Mesa pode ser avulsa (sem campanha) ou dentro de campanha.

## ficha.html
- Seções: info, atributos, stats (PV/PE/SAN…), perícias, inventário, poderes, **Documentos** (imagens comprimidas por `comprime()`, `verDoc()`, sem peso), notas.
- `completa()` garante os campos novos em fichas antigas (ex.: `docs`).
- Dados em `personagens.dados` (jsonb). Ver docs/banco.md.
- Mesma linguagem visual do `tema.css`.
