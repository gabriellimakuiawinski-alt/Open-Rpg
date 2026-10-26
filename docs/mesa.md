# Tabletop (mesa.html)

Mapa com cenas, tokens, fog/escuridão, paredes e luzes, biblioteca de arquivos, log, anotações do mestre. Base: `tools/build/original/mesa-paranormal-v10.html` + camada de nuvem (`tools/build/nuvem.js`).

## Módulos (carregados por `?v=N` injetado em `build.py`)
- `mesa-fx.js` — canvas `#fx` por cima do mapa: `MesaFX.onda/burst`, anel de seleção, poeira, cortina ao trocar de cena, overlay do resultado de dado (lê o 1º segmento antes do `<br>` em `#log`). Desligado com `prefers-reduced-motion`.
- `mesa-ficha.js` — ficha e inventário no tabletop: no menu do token ligado a ficha (campanha OP), dono e mestre rolam perícia, atacam/rolam dano, equipam e usam itens (grava `personagens.dados` lendo o mais recente antes). Usa `SIS` (mesmos números da ficha). `PERS` agora guarda o `dados` completo.
- Sem emojis nos botões: texto puro em todas as telas (não reintroduzir). Roda do mouse com um token sendo arrastado gira o token em passos de 15 graus.
- `mesa-musica.js` — mestre: botão `#mtx` (transmitir); jogadores: pílula `#mx-musica`; efeitos sonoros compartilhados (sobrescreve `fx`). Expõe `MusicaSync.conectou()`.
- `mesa-dados.js` — `DadoHook/DadoRx`: rolagens compartilhadas no canal; checkbox `#dsec` = rolagem secreta (só o mestre vê).
- `mesa-notas.js` — "Meu caderno" (para quem não é DONO), `upsert` em `notas_jogador` com `onConflict:'mesa_id,user_id'`.
- `mesa-exportar.js` — botão "Exportar mesa" (DONO).

## Sincronização PV/PE/SAN
Token ↔ ficha por triggers no banco (`dados` do token ↔ `stats` da ficha). Barras no token: `hp/pv`, `mn/mm` (PE), `sn/sm` (SAN), `lo/lz` (luz).

## Luz pelo inventário (campanha Ordem Paranormal)
Token ligado a ficha: botões Lanterna/Lampião só ligam se a ficha tem item com `luz` do tipo; alcance = melhor item (`luzInv`, metros ÷ `S.gm`). Sem campo de alcance para ninguém nesse caso. O banco garante (`token_luz_auto`). Menu mostra o inventário (mestre e dono). `SISM` = sistema da campanha; `PERS` traz `inv`; `rtPers` atualiza ao vivo.

## Fog e luz
Escuro/escuridão/névoa por cena; `lightsData` gera luz dos tokens; `cena_visivel` decide o que o jogador recebe. Testado para mestre e jogador (`tools/tests/e/fog.py`).

## Tema
`tema-mesa.css`: painéis escuros, interruptores com carimbo, chips, aba ativa em papel, campos numéricos; animações `painel/sobe/pulso/chacoalha`. No celular `#rm` não pode cobrir os botões do topo (`#dcb,#mpb` ficam `position:fixed` — **não** pôr `position:relative` neles).

## Armadilhas já vividas
- `DONO` falso no load → iniciar só em `conectou()`.
- `upsert` sem `onConflict` assume PK `id`.
- Dado recebido: overlay deve usar só o texto do 1º `<br>`.

## Desempenho (não desfazer)
- `mip(im,w)` (build.py): mapas e tokens grandes são desenhados a partir de cópias reduzidas (metade, um quarto…), criadas aos poucos (uma por quadro).
- `camada()` (build.py): névoa e escuridão ficam em cache com margem de 25% em volta da tela; arrastar só move a imagem. Redesenha quando muda a névoa/luz (`WV`, `FK`/`DK`), sai da margem ou o zoom muda mais de 25% (e 200 ms depois de parar o zoom, para ficar nítido).
- Só desenha mapa/token que está na tela.
- `mesa-fx.js`: o laço só roda com efeito ativo; parado = 0% de CPU. Canvas de efeitos em 1x. No modo Leve (`S.q=='l'`): sem poeira e anel de seleção parado. É acordado pelo `render` (embrulhado no fim do arquivo).
- Token enviado é reduzido para no máximo 512px (`reduzTok`). Mapas não (o tamanho do mapa define a grade).
- Animações CSS infinitas: só `transform`/`opacity` (nunca `height`, que recalcula a página a cada quadro).
