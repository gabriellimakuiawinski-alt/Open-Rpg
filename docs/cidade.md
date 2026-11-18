# Mapa da cidade (cidade.html)

Mapa 3D de uma cidade (HTML único, three.js embutido) ligado à campanha: `cidade.html?camp=<id>`. Botão "Mapa da cidade" no menu da campanha (`index.html`). Funciona como mapa de jogo: o jogador vê só o que o grupo já explorou e onde o grupo está agora.

## Quem vê o quê
- **Mestre/admin** (`campanha_membros.papel`): edita tudo (bairros, locais, zonas, rumores, clima, hora, névoa, régua), vê segredos e locais escondidos. Grava em `cidade_mapa` (completo) e publica em `cidade_jogador` a versão sem segredos (`ORpublico` em `cidade.html`): sem `segredo`, rumores, encontros, locais/zonas `mestre`, link de battlemap; bairros não explorados saem sem descrição.
- **Jogador**: só leitura. Lê `cidade_jogador` + `cidade_grupo`. Atualiza sozinho (realtime) quando o mestre muda algo ou move o grupo.
- Primeiro acesso do mestre: nasce com o mapa padrão, névoa ligada e todos os bairros "não explorados".

## Grupo (marcador)
`cidade_grupo`: posição `px,py` (plano do mapa, 1 px = 4 m na horizontal e 5 m na vertical), nome e `trilha` (pontos a cada ~90 m, até 1500). Mestre: botão "Mover grupo" e toque no mapa. Ao mover, revela a névoa ao redor (raio ajustável) ao longo do caminho, então o mapa guarda por onde o grupo já passou. Todos: "Ir ao grupo" e liga/desliga trilha.

## Interior = cena da mesa
No editor de um local (mestre) o campo "Interior (cena da mesa)" lista as cenas das mesas da campanha. O local guarda `cena`, `mesa`, `cenaNome`. Botão no local: mestre chama a RPC `ativar_cena` e vai para `mesa.html?mesa=<id>` (troca a cena dos jogadores); jogador só vai para a mesa. A imagem de battlemap local (IndexedDB) foi removida aqui: use as cenas da mesa.

## Como é gerado
`cidade.html` é o mapa original (sfl2-mapa-cidade) + trechos do Open RPG (dados em `ORinit/save`, grupo, interiores, realtime). Não há gerador no repositório: edite o `cidade.html` direto (blocos marcados com "Open RPG"). Mudou? Teste com mestre e jogador (o mapa leva ~10 s para montar).

## Pacote v8 (18/11/2026)
- **Linha do tempo**: `DATA.dia`, `DATA.eventos` `{id,dia,titulo,desc,clima,revela,esconde,mestre,feito}`. Avançar o dia aplica os eventos (clima, mostrar/esconder zona). Voltar o dia não desfaz. Teclas `[` `]`. Jogador vê só eventos já ocorridos e não secretos (filtro em `ORpublico`). `DATA.diario` `{id,dia,texto}`: notas da sessão.
- **NPCs**: `DATA.npcs` `{id,nome,fac,px,py,desc,segredo,mestre}`; nascem escondidos. Rótulos HTML (`.nlabel`).
- **Rotas**: `DATA.rotas` `{id,nome,tipo,pts:[[px,py]],risco,desc,segredo,mestre}`; tipos em `ROTA_T` (velocidade para o tempo). Tubo 3D sempre visível + rótulo.
- **Comércio**: `local.com` `{on,fac,agua,comida,comb,mun,rem,preco}`; filtro "Comércio" na busca. `local.visitado`: marcado à mão ou quando o grupo passa a menos de 130 m.
- **Anotações pessoais**: `localStorage['or-cidade-notas-<camp>']` (só no aparelho, para qualquer papel).
- **Clima e hora** da campanha vão em `DATA.clima/DATA.hora` e o jogador recebe.
- **Imagem**: baixa a vista em 2x/4x; mestre envia para a biblioteca de mapas de uma mesa (`arquivos` + bucket `mesa-arquivos`, tipo `mapa`). Rótulos HTML não saem na imagem.
- **Cenários**: tabela `cidade_cenarios` (`schema_etapa19_cidade_cenarios.sql`, só mestre).
- **Som ambiente**: Web Audio gerado (vento, chuva, sirene, corvos, fogueira, cães à noite). Desligado por padrão.
- **Atalhos**: `?` mostra a lista. Celular: barra inferior Grupo/Buscar/Painel/Campanha.
- **Locais novos** (`V8_POIS`, migração `locaisV8`) com adereços 3D em `genV8()`; o marcador é movido para onde o adereço coube (`v8Fx.sitios`). `genV8` também faz acampamentos, gente, hordas, poças, vidro, passarelas caídas, canais bloqueados, entulho por bairro e corvos.
- Fonte: `cidade.html` é montado fora do repo (v7 + camadas Open RPG + v8). Para mudanças pequenas, editar o `cidade.html` direto.
