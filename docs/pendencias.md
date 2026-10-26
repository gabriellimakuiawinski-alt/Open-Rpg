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
