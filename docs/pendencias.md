# Pendências e ideias

## Do usuário
- Rodar `schema_etapa3b_musica.sql`, depois `schema_etapa4.sql`, depois `schema_etapa5.sql` no Supabase (SQL Editor). Não confirmado.
- Testar com 2 contas/dispositivos: música, dados, PV/PE/SAN, caderno.

## Já publicado
Visual dossiê, animações do mapa, ícones SVG, música e efeitos compartilhados, PV/PE/SAN sincronizados, rolagens compartilhadas/secretas, Documentos na ficha, caderno do jogador, exportações, sons e trilha na página inicial.

## Etapa 5 (publicada)
Sistema por campanha (Ordem Paranormal automática / Modular), loja e dinheiro, homebrews com efeito automático, luz do token pelo inventário.
## Etapa 6 (em andamento)
Feito: habilidades de classe, poderes de classe e trilhas do livro básico (130 linhas) + botão "Do livro". **Pendente do usuário:** rodar `schema_etapa6_livro.sql` (depois do etapa5).
Rituais do livro básico: FEITO (82, `schema_etapa6b_rituais.sql`; pendente do usuário rodar). Ideia: aviso de "aprender ritual" a cada NEX do ocultista (hoje ele escolhe em "Do livro").
Origens (26) e poderes paranormais (22) do livro básico: FEITO (`schema_etapa6c_origens.sql`; pendente do usuário rodar). Itens e armas do livro básico (110): FEITO (`schema_etapa6d_itens.sql`; pendente do usuário rodar). Falta: itens amaldiçoados (livro p.144), rituais do Sobrevivendo ao Horror; trilhas/poderes dos outros livros.

Próximos passos possíveis: origens com efeitos prontos, munição gasta ao atacar, rolagens da ficha no log da mesa.

## Ideias (não feitas)
- Rolagens da ficha no log da mesa; imagem do personagem compartilhada ficha↔token; abrir a ficha pelo token.
- Handouts, iniciativa na tela, ping no mapa, backup, PWA.
- Pacote de sistema **Ordem Paranormal** (escolher sistema muda a ficha; rituais em poderes; catálogo de itens/armas). Dados ficam no Supabase atrás de login, não no repositório. Precisa do PDF do usuário.
- Loja de créditos, bot do Discord, quadro de investigação.
- Tokens PNG: já funcionam (imagens da biblioteca).
Quadro de investigação (PR do quadro): FEITO (`schema_etapa7_quadro.sql`; pendente do usuário rodar). Ideias: mover papéis de outros jogadores, anexar PDF, texto sobre os fios, revelar um papel a um jogador só.
Feito em 27/10/2026: itens amaldiçoados, ritual por NEX, Ameaças da Realidade (18), condições, perigos e cálculos. Ainda não catalogado do livro: descrição das perícias (cap. 2), ações e manobras de combate (cap. 4), Aliados (p.170), regras opcionais (p.171), gerador de missões, sanidade/exposição, entidades do Outro Lado e o mundo de OP (lore). Rituais do Sobrevivendo ao Horror: fora de escopo por ora.

## Complementos (27/10/2026, em andamento)
Feito: estrutura (escolha na campanha, etiqueta SaH, filtro) e os 91 itens do SaH (armas, munição, modificações, acessórios, explosivos, operacionais, medicamentos, paranormais e amaldiçoados). **Pendente do usuário:** rodar `schema_etapa13_sah_itens_celular.sql`.
Falta do SaH: origens (20), poderes gerais (34), poderes paranormais (8), rituais (16, confirmar se entram), poderes e trilhas de classe, conferir a classe Sobrevivente, criaturas (12) e Ameaças da Realidade, regras opcionais (evolução por patentes, limite de itens vestidos etc.). Depois: livros dos arquivos secretos. Pontos a confirmar do livro: Revólver compacto (dano P), Bastão policial (alcance Curto), categoria da Lente de Revelação (inferida) e ficha do Fuzil Alheio (inferida).

**31/10/2026:** SaH completo no site (etapa 15): origens, poderes gerais, poderes e trilhas de classe, Sobrevivente pelo livro, paranormais, rituais, bestiário e regras novas/opcionais. **Pendente do usuário:** rodar `schema_etapa15_sah_livro_celular.sql`. Regras opcionais: só "limite de itens vestidos" tem aviso automático; as outras ficam marcadas na campanha e explicadas em `regras.html`.

## Search For Light (28/10/2026)
Feito: sistema `sfl` (ficha automática, classes, trilhas, origens, linhas de poder, armas com crítico por arma, catálogo e loja em euro). **Pendente do usuário:** rodar `schema_etapa14_sfl_celular.sql` no Supabase (libera o sistema 'sfl'). Falta: base da campanha, bestiário/infectados únicos, chefes, veículos, rolagens no log da mesa, token com Medo/Infecção. Valores [PROPOSTA] do sistema podem mudar após a mesa de teste (regenerar `sfl-dados.js`).
