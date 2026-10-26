# Som (som.js)

Tudo sintetizado com Web Audio, **sem arquivos de áudio**.
- `window.Som`: `fx(nome)`, `musica(on)`, `efeitos(on)`, `volume(v)`, `estado()`.
- Efeitos: `pasta carimbo tachinha papel lapis dado aba abre fecha postit cracha tecla` (ruído filtrado, reverb por convolução).
- Trilha ambiente gerada (`Motor()`): acordes Am, F, Dm, E, Bb; notas de caixinha de música; pulso grave.
- Só começa após o 1º `pointerdown/keydown/touchstart` (regra dos navegadores); pausa com a aba oculta.
- No `index.html`, cliques são mapeados para efeitos por elemento. Teste: `tools/tests/e/t14.py` (todos os `fx` sem erro).
- No tabletop, música/efeitos compartilhados são outra coisa: `mesa-musica.js` (docs/mesa.md).
