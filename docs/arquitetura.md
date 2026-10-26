# Arquitetura

Páginas estáticas, sem framework, sem build para o resto (só `mesa.html` é gerado).

## Arquivos
- `index.html` — início: splash, campanhas, mesas, fichas, abas, exportar. Roteamento por hash (`#/c/<uuid>`). Carrega `som.js`.
- `ficha.html` — ficha de personagem (seção Documentos, sem peso).
- `mesa.html` — tabletop. **Gerado** (ver abaixo).
- `comum.js` — define `window.LEVE` e a classe `html.leve` (celular/aparelho fraco/economia de dados/menos movimento: as páginas desligam enfeites pesados); `window.Mesa = {db, exigirLogin, sair}`; cria o cliente Supabase e a tela de login (papel com carimbo).
- `tema.css` — tokens e classes do visual "dossiê" (`--tabua --papel --pasta --tinta --carimbo --fita`, fontes Special Elite / Caveat / Hanken Grotesk). `tema-mesa.css` — tema do tabletop.
- `som.js` — ver docs/som.md.
- Módulos do tabletop: `mesa-fx.js mesa-icones.js mesa-musica.js mesa-dados.js mesa-notas.js mesa-exportar.js` (ver docs/mesa.md).
- `schema*.sql` — banco (docs/banco.md).
- `tools/` — gerador e testes (docs/testes.md).

## Como o `mesa.html` é feito
`tools/build/build.py` lê `tools/build/original/mesa-paranormal-v10.html` (tabletop original, local/IndexedDB), corta trechos por número de linha (com asserts de assinatura), troca o armazenamento por `tools/build/nuvem.js` (camada Supabase) e aplica `rep()` (substituições de texto) e injeta `<link>`/`<script>` com `?v=N`. Saída: `mesa.html` na raiz.
- Para mudar comportamento do tabletop: `rep()` no `build.py`, trecho em `nuvem.js`, ou um módulo `mesa-*.js`. Preferir módulo novo quando possível.
- Se um `rep()` falhar, o texto original não bate: leia o trecho no original antes de ajustar.

## Cache
Supabase JS fixado em versão exata (`@2.118.0/dist/umd/supabase.js`) nas 3 páginas: cache longo no celular. Para atualizar, troque o número nas 3 (no `build.py` para a mesa).
Todo CSS/JS tem `?v=N`. Ao mudar um arquivo, subir o N dele (e checar se `index.html`/`ficha.html`/`build.py` usam o mesmo número para o mesmo arquivo). Já houve tela "bugada" no celular por CSS novo com JS antigo em cache.

## Escopo léxico no tabletop
Os scripts extras são *classic scripts* e enxergam as variáveis do script principal: `sb, MESA, ME, GER, DONO, VIEW, S, sel, selM, AU, Q, qi, LIB, fx, logm, toast, RC, lightsData, draw`. `GER/DONO` são definidos de forma **assíncrona**; módulos devem esperar (`MusicaSync.conectou()` é chamado quando o canal realtime entra em SUBSCRIBED) em vez de ler no carregamento.
