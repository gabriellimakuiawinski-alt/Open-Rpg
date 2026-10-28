# Base, economia e parkour — SFL 2 (rascunho v0.1)

Criado em 28/10/2026 para o mestre Gabriel. Marcas: [CONFIRMADO] = decisão do mestre; [PROPOSTA] = ideia do Claude; [PENDENTE] = falta decidir. O sistema principal está em `sistema-sfl2.md` (v0.5).

## 1. O que o mestre já decidiu (28/10/2026)
- [CONFIRMADO] Quer um **bom sistema de melhoria de base**.
- [CONFIRMADO] A economia usa a **moeda da Estônia** e a **loja fica no Open RPG**.
- [CONFIRMADO] (revisado em 28/10, 13:12) **Sem mecânica única de parkour.**
- [CONFIRMADO] **Todo o sistema vai para o Open RPG.** Feito em 28/10: ficha, rolagens, catálogo e loja em euro (PR 37 do repositório).
- [CONFIRMADO] Chefes ficam para depois.

## 2. Melhoria de base
Hoje a base tem 4 recursos de 0 a 5 (Energia, Comida, Luz UV, Moral). Tudo abaixo é [PROPOSTA].

### 2.1 Ideia central
A base é uma "ficha do grupo". Ela tem **cômodos** (módulos) que o grupo constrói e melhora com **Materiais** e **tempo**. Cada cômodo dá um benefício e um custo, e a base **pode ser atacada**, então melhorar também atrai perigo.

### 2.2 Materiais da base (3, para não complicar)
- **Sucata**: metal, madeira, fios. Vem de saques.
- **Peças**: eletrônica, motores, baterias. Mais rara.
- **Mantimentos de base**: o que sustenta o grupo (vira Comida).

### 2.3 Cômodos (cada um tem Nível 0 a 3)
| Cômodo | Nível 1 | Nível 2 | Nível 3 |
|---|---|---|---|
| Gerador | +1 Energia por descanso | Energia não cai abaixo de 1 | Energia pode ir a 6 |
| Oficina | Reparo de arma sem teste | Fabrica munição e bandagem | Fabrica item especial |
| Enfermaria | Descanso longo cura +1d6 | Remove 1 Infecção a mais por semana | Estabilizador raro uma vez por arco |
| Horta e cozinha | +1 Comida por descanso | Moral +1 sempre que Comida ≥ 3 | Comida pode ir a 6 |
| Sala UV | Uma lâmpada UV fixa | Cobre a entrada | Defende a base inteira de voláteis |
| Rádio | Ouve notícias | Contato com facções | Chama NPCs e comércio |
| Defesas | Barricada (+1 de armadura em ataque à base) | Armadilhas | Torre de vigia |
| Dormitório | Moral +1 | Mais NPCs abrigados | Moral pode ir a 6 |

- [PROPOSTA] Custos de exemplo: Nível 1 = 3 Sucata; Nível 2 = 5 Sucata + 2 Peças; Nível 3 = 8 Sucata + 4 Peças e um marco da história (o grupo precisa de um motivo narrativo).
- [PROPOSTA] Melhorar é uma **ação de base** num descanso longo. Cada jogador pode dedicar o descanso a um cômodo (teste de Técnica ou Sobrevivência), em vez de recuperar tudo. Isso cria escolha: descansar ou construir.

### 2.4 Ataques à base (o custo de crescer)
- [PROPOSTA] Existe um **Nível de Ameaça da base** (0 a 5) que sobe com o tamanho da base, barulho (Alerta) e Moral baixa. A cada arco, o mestre pode rolar um evento: ataque de horda, facção em visita, falta de recurso.
- [PROPOSTA] Defesas altas diminuem o dano da base e protegem NPCs. Sem Defesas, um ataque derruba um cômodo de nível.
- [PENDENTE] Se NPCs têm função fixa na base (Marco Smirnov Rott cuida da Energia).

### 2.5 Perguntas para o mestre
1. A base é uma só ou o grupo pode ter bases em vários lugares?
2. Os NPCs resgatados viram trabalhadores (bônus ao cômodo)?
3. O mestre quer que a base possa ser perdida/destruída na campanha?
4. Quer acompanhar Sucata e Peças como número ou como itens no inventário?

## 3. Economia e loja (Open RPG)
### 3.1 Moeda
- A moeda da Estônia é o **euro (€)**. A Estônia adotou o euro em 2011. [Fato público; a data dispensa pesquisa nova para o jogo.]
- [PENDENTE] Como funciona dinheiro depois do colapso na ilha. Opções (o mestre escolhe):
  - (a) **Euro como lembrança**: ninguém compra nada com ele, a loja é metáfora de trocas na base.
  - (b) **Euro como moeda de facção**: Pacificadores e Sobreviventes aceitam euros, outros trocam por itens.
  - (c) **Escambo + euro**: o preço aparece em euro, mas a loja é "moeda virtual" que o grupo ganha em missões.
- [PROPOSTA] Sugestão: (c). Para o jogo a loja fica simples, e o mestre ajusta o que aparece por facção.

### 3.2 Loja no Open RPG
- [PROPOSTA] A loja lista itens do sistema (armas da seção 8.3, bandagens, pilhas UV, munição, material de base). O jogador compra com a carteira do grupo; o mestre aprova ou libera por facção e reputação.
- [PROPOSTA] Preços ligados à **reputação**: aliado (+3) paga 80%, inimigo (-3) paga 140% ou não vende.
- [PROPOSTA] Ao criar os itens, cada um tem: nome, categoria, preço em €, espaço no inventário, e qual facção vende.
- [PENDENTE] Faixa de preços (balanceamento): para segurar o poder, itens fortes devem ser raros e caros.

## 4. Parkour
[CONFIRMADO 28/10] Sem mecânica única de parkour. A perícia Parkour continua valendo para esquiva e fuga. As três direções que o Claude tinha proposto (trilha, manobras, Ímpeto) ficam descartadas.

## 5. Colocar o sistema no Open RPG
- [CONFIRMADO] Todo o sistema vai para o Open RPG.
- [PROPOSTA] Etapas: (1) fichas (atributos, perícias, recursos, Infecção), (2) classes, trilhas, origens e poderes, (3) armas e loja, (4) base, (5) combate e testes com rolagem de dados, (6) nome do sistema.
- Feito em 28/10/2026: sistema `sfl` no repositório gabriellimakuiawinski-alt/Open-Rpg (`sfl-dados.js`, `sfl-regras.js`, `ficha-sfl.js`, SQL `schema_etapa14_sfl_celular.sql`). Falta a base, o bestiário e as rolagens no log da mesa.

## 6. Pendências deste arquivo
- Responder as 4 perguntas da base.
- Escolher como a moeda funciona no jogo (a, b ou c).
- Nome do sistema.
