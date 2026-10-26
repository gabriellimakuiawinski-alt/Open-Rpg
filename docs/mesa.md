# Tabletop (mesa.html)

Mapa com cenas, tokens, fog/escuridão, paredes e luzes, biblioteca de arquivos, log, anotações do mestre. Base: `tools/build/original/mesa-paranormal-v10.html` + camada de nuvem (`tools/build/nuvem.js`).

## Módulos (carregados por `?v=N` injetado em `build.py`)
- `mesa-fx.js` — canvas `#fx` por cima do mapa: `MesaFX.onda/burst`, anel de seleção, poeira, cortina ao trocar de cena, overlay do resultado de dado (lê o 1º segmento antes do `<br>` em `#log`). Desligado com `prefers-reduced-motion`.
- `mesa-icones.js` — troca emojis por SVG (`.ie`) e injeta o CSS de tamanho.
- `mesa-musica.js` — mestre: botão `#mtx` (transmitir); jogadores: pílula `#mx-musica`; efeitos sonoros compartilhados (sobrescreve `fx`). Expõe `MusicaSync.conectou()`.
- `mesa-dados.js` — `DadoHook/DadoRx`: rolagens compartilhadas no canal; checkbox `#dsec` = rolagem secreta (só o mestre vê).
- `mesa-notas.js` — "Meu caderno" (para quem não é DONO), `upsert` em `notas_jogador` com `onConflict:'mesa_id,user_id'`.
- `mesa-exportar.js` — botão "Exportar mesa" (DONO).

## Sincronização PV/PE/SAN
Token ↔ ficha por triggers no banco (`dados` do token ↔ `stats` da ficha). Barras no token: `hp/pv`, `mn/mm` (PE), `sn/sm` (SAN), `lo/lz` (luz).

## Fog e luz
Escuro/escuridão/névoa por cena; `lightsData` gera luz dos tokens; `cena_visivel` decide o que o jogador recebe. Testado para mestre e jogador (`tools/tests/e/fog.py`).

## Tema
`tema-mesa.css`: painéis escuros, interruptores com carimbo, chips, aba ativa em papel, campos numéricos; animações `painel/sobe/pulso/chacoalha`. No celular `#rm` não pode cobrir os botões do topo (`#dcb,#mpb` ficam `position:fixed` — **não** pôr `position:relative` neles).

## Armadilhas já vividas
- `DONO` falso no load → iniciar só em `conectou()`.
- `upsert` sem `onConflict` assume PK `id`.
- Dado recebido: overlay deve usar só o texto do 1º `<br>`.
