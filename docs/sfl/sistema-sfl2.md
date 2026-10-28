# Sistema SFL 2 — v0.5 (rascunho completo)

Feito para o mestre Gabriel. Marcas: [CONFIRMADO] = decisão do mestre; [PROPOSTA] = ideia do Claude, não vale até aprovar; [PENDENTE] = falta decidir. Tudo abaixo que não está como [CONFIRMADO] é [PROPOSTA].

Classes, trilhas e origens estão em `classes-sfl2.md` (v0.1). Melhoria de base, economia e parkour (rascunhos) estão em `base-economia-parkour-sfl2.md`.

## 1. Decisões confirmadas (27/10/2026)
- [CONFIRMADO] Foco em sobrevivência e tensão.
- [CONFIRMADO] Mecânica d20, em reserva de dados igual ao atributo (seção 2).
- [CONFIRMADO] Poderes herdados de Viktor são dom com custo; cada jogador escolhe o tipo de poder ao criar a ficha.
- [CONFIRMADO] Complexidade média: atributos, perícias, inventário e subsistemas simples (como a Infecção).
- [CONFIRMADO] (28/10/2026) Armas: simples e especiais; cada arma especial exige treinamento próprio; sem treino, o teste perde um dado (desvantagem); corpo a corpo só tem Contundente e Cortante; Arremesso é uma perícia à parte. Ver seção 8.
- [CONFIRMADO] (28/10/2026) A ficha tem **origem**, **classe** e **trilha**. A classe tem várias habilidades à escolha do jogador quando evolui; a trilha tem habilidades fixas (4), parecido com Ordem Paranormal, mas com habilidades diferentes. O sistema deve ser **bem equilibrado** (a SFL 1 foi fácil demais), criativo e sem complexidade demais. Ver `classes-sfl2.md`.
- [CONFIRMADO] (28/10/2026) **O atributo decide quantos dados rola e NÃO soma ao resultado.** Seção 2.
- [CONFIRMADO] (28/10/2026) **O crítico muda por arma**, parecido com Ordem Paranormal. Crítico é **tirar um número alto no dado**, e **nem todo crítico acerta**. Seções 2, 8 e 8.3.
- [CONFIRMADO] (28/10/2026) Variações da mesma arma (arco curto e composto, besta leve e pesada) **dividem o mesmo treino**.
- [CONFIRMADO] (28/10/2026) **Os selos da SFL 1 não existem na SFL 2**, ou existirão de forma diferente, porque representavam o que Helena conseguiu conter. Os novos tipos de zumbis e os infectados únicos serão criados com o mestre.
- [CONFIRMADO] (28/10/2026) O mestre quer um **bom sistema de melhoria de base**, **economia na moeda da Estônia com loja no Open RPG**, e uma **mecânica única para o parkour**. Chefes ficam para depois. **Todo o sistema vai para o Open RPG** (ficha digital e loja). Ver `base-economia-parkour-sfl2.md`.
- [PENDENTE] Nome do sistema.

## 2. Teste básico (reserva de d20)
- [CONFIRMADO] O teste rola uma **reserva de d20 igual ao valor do atributo** usado e fica com o **maior** resultado.
- [CONFIRMADO] (28/10/2026) **O atributo só decide quantos dados rola; ele não soma ao resultado.** A perícia soma o bônus de treino (leigo +0, treinado +3, veterano +6, expert +9).
  - Resultado = maior d20 + bônus da perícia.
- [PROPOSTA] Atributo 0: rola 2 dados e fica com o **menor**.
- [CONFIRMADO] Vantagem = +1 dado na reserva; desvantagem = −1 dado. Sem treino em arma especial = −1 dado e sem bônus de treino (seção 8.1). Neste documento, "vantagem" e "desvantagem" sempre significam isso.
- [PROPOSTA] Se a reserva cair abaixo de 1 dado, rola 2 e fica com o menor.
- [CONFIRMADO] A **DT depende do que o mestre pedir**; não há tabela fixa.
- [PROPOSTA] Guia de referência, **recalibrado em 28/10** porque o atributo não soma mais (os totais caíram uns 3 pontos): ~10 fácil, ~15 normal, ~20 difícil, ~25 extremo. As DT 18 antigas viraram 15; só o teste de Vontade da Infecção Instável ficou em 18, de propósito.
- [CONFIRMADO] **Crítico = tirar um número alto no dado que ficou.** Nem todo crítico acerta: o ataque ainda precisa vencer a reação (seção 8). Em ataques, a **margem de crítico e o multiplicador mudam por arma**, como em Ordem Paranormal (seção 8.3).
- [PROPOSTA] Em testes comuns (não ataque): 20 no dado que ficou e passar na DT = sucesso excepcional (o mestre dá um bônus). 1 no dado que ficou = complicação (barulho, item danificado, +1 Infecção se for teste de poder).
- [PROPOSTA] Teste em grupo: todos rolam, o grupo passa se metade ou mais passar.

## 3. Atributos (0 a 5; 10 pontos na criação, máximo 4)
- **Corpo**: força, vigor, resistência física.
- **Reflexo**: agilidade, pontaria, furtividade, parkour.
- **Mente**: percepção, investigação, técnica, conhecimento.
- **Presença**: vontade, liderança, empatia, persuasão.

## 4. Perícias
- Níveis de treino: leigo +0, treinado +3, veterano +6, expert +9.
- Lista (15): Atletismo, Furtividade, Parkour, Percepção, Investigação, Técnica (energia, rádio, mecânica), Medicina, Sobrevivência, Persuasão, Intimidação, Vontade e as 4 perícias de combate: **Contundente**, **Cortante**, **Arremesso** e **Tiro** (armas de fogo simples).
- Armas especiais (arco, besta e armas de fogo complexas) não são perícias da lista: cada uma tem o seu treino próprio (seção 8).
- [PROPOSTA] Cada protagonista começa com 4 perícias treinadas: **2 da origem** e **2 da classe** (ver `classes-sfl2.md`). Se uma perícia se repetir, escolhe outra.

## 5. Recursos
- **Vida (PV)**: 10 + Corpo × 2. Em 0 PV fica caído e sangrando; morre em 3 rodadas sem socorro (teste de Medicina DT 15 estabiliza).
- **Fôlego**: 5 + Reflexo. Gasta 1 para correr uma rodada, esquivar, escalar ou atacar com força. Sem Fôlego: desvantagem em tudo que exige esforço. Recupera todo em descanso curto (10 minutos seguros).
- **Medo** (0 a 5): sobe com sustos, perdas, noite e cenas de horror. Medo 3+: desvantagem em Vontade e em ataques à distância. Medo 5: congela ou foge por uma rodada. Baixa com descanso seguro, companhia e um momento de calma.
- **Suprimentos**: itens contáveis (munição, bandagens, comida, pilhas UV). Inventário em espaços: 5 + Corpo.
- **Durabilidade**: arma corpo a corpo quebra em 1 natural ou depois de 10 usos. Reparo com Técnica DT 15.

## 6. Infecção (o custo dos poderes)
- Marcador de 0 a 10 por personagem. Todo uso de poder custa Infecção (cada poder diz quanto).
- Faixas:
  - 0 a 2, Controlado: sem efeitos.
  - 3 a 5, Inquieto: sintomas leves (febre, fome, sentidos alterados). Poderes ficam mais fortes (+2 no teste).
  - 6 a 8, Instável: ao usar um poder, teste de Vontade DT 18 (acima do normal, de propósito). Falha = perde o controle por uma cena (o mestre conduz).
  - 9 a 10, Limiar: o Ódio assume. O personagem vira NPC do mestre ou sofre mudança permanente, a critério do mestre e com conversa com o jogador.
- Redução: descanso longo seguro (-1), estabilizador raro (-2), laço humano marcante (-1, uma vez por sessão). Nunca zera de graça.
- Gancho do mestre: o Ódio puro sente quem está em Instável ou pior.

## 7. Poderes (linhas)
Cada jogador escolhe uma linha na criação e começa com o Nível 1. [PROPOSTA] O Nível 2 chega no marco 4 e o Nível 3 no marco 8 (ver seção 12). Custo em Infecção entre parênteses.

**Predador** (força e velocidade; fraqueza: fome, precisa comer cru ou em abundância após usar muito)
- N1 Garras (1): ataque desarmado vira 1d8 e ignora armadura leve.
- N2 Investida (1): move até o dobro e ataca, sem gastar Fôlego.
- N3 Frenesi (2): duas ações de ataque no turno por uma cena; Medo +1.

**Sentidos** (percepção; fraqueza: barulho alto e luz forte incomodam, desvantagem)
- N1 Faro (1): vantagem em Percepção e Sobrevivência para achar infectados e rastro.
- N2 Vibração (1): sente criaturas num raio de 10 m, mesmo sem ver.
- N3 Mapa (2): uma vez por cena, o mestre descreve a posição de todos os infectados próximos.

**Carne Viva** (regeneração; fraqueza: cada cura aumenta a Infecção)
- N1 Fechar feridas (1): recupera 1d6 PV como ação rápida.
- N2 Pele dura (1): +2 de armadura por uma cena.
- N3 Não cair (2): ao chegar em 0 PV, volta com 1d6 PV uma vez por sessão.

**Eco** (influência sobre infectados; fraqueza: atrai atenção, Alerta +1 a cada uso)
- N1 Chamado (1): atrai um grupo de infectados a um ponto, DT 15.
- N2 Calar (1): infectados comuns e virais ignoram o personagem por uma rodada.
- N3 Comando (2): controla 1 infectado comum por uma cena (não afeta selo nem volátil).

**Sombra** (furtividade; fraqueza: sofre com UV, desvantagem e 1d4 de dano por rodada sob luz UV)
- N1 Passo leve (1): vantagem em Furtividade no escuro.
- N2 Vulto (1): desaparece da vista de quem não o está encarando; ataque furtivo causa +1d6.
- N3 Névoa (2): escurece uma área de 5 m por uma cena, apagando luz comum.

[PENDENTE] Se o jogador pode misturar linhas ao longo da campanha (o mestre pediu uma explicação melhor da pergunta; ver pendências). Os selos da SFL 1 não entram aqui; a relação com a linhagem de Viktor continua em aberto.

## 8. Combate
- Iniciativa: teste de Reflexo (seção 2). Por turno: 1 ação, 1 movimento (9 m) e 1 reação limitada.
- **Ataque** = reserva de d20 igual à Mira, maior dado + treino da arma ou categoria (o atributo não soma). [CONFIRMADO] **Não existe Defesa automática**: quem é atacado **rola a reação** (seção 8.2). [PROPOSTA] O ataque acerta se o total do atacante for **maior** que o total da reação; empate favorece quem se defende.
- [CONFIRMADO] Mira: o **Reflexo define os dados** do ataque à distância e do Arremesso; no corpo a corpo, quem define os dados é o **Corpo** (força).
- [PROPOSTA] Dano: dados da arma, mais o Corpo no corpo a corpo. [PENDENTE] Como o atributo não soma nos testes, o Corpo ainda soma no dano?
- [CONFIRMADO] **Crítico:** se o dado que ficou cair na **margem de crítico da arma** e o ataque **acertar**, é crítico: o **efeito da arma** acontece e, [PROPOSTA] os dados de dano são multiplicados pelo multiplicador da arma (só os dados da arma, não o Corpo). Um crítico que **erra** não faz nada (seção 8.3).
- [PENDENTE] Reação contra poderes (como alguém se defende de um poder).

### 8.1 Armas simples e especiais
- [CONFIRMADO] **Armas simples**: qualquer um usa sem treino. Entram nas categorias:
  - **Contundente** (punhos, taco, cano, martelo): [PROPOSTA] gancho de derrubar ou atordoar. Briga fica dentro de Contundente.
  - **Cortante** (faca, facão, machado): [PROPOSTA] gancho de sangramento.
  - **Arremesso** (facas, molotov, granadas, pedras).
  - **Tiro** [PROPOSTA, necessária para as armas de fogo simples]: pistolas, revólveres, escopeta de cano duplo, rifle de caça e pistola de sinalização. O Reflexo define os dados (Mira).
  - O treino da categoria (+0/+3/+6/+9) soma ao ataque.
- [CONFIRMADO] **Armas especiais** (arcos, bestas e armas mais complexas: submetralhadora, escopeta pump, rifle de precisão, fuzil de assalto, lança-chamas improvisado): cada arma exige um **treinamento só para ela**. Saber usar o arco não ensina a usar a besta.
  - [CONFIRMADO] Variações próximas da mesma arma (arco curto e composto, besta leve e pesada) **contam como o mesmo treino**.
  - [CONFIRMADO] Sem o treino daquela arma, o personagem **rola um dado a menos** do que rolaria com a Mira (ex.: Reflexo 3 = 3 dados, sem treino rola 2) e **não recebe nenhum bônus de treino**. Não é a desvantagem 2d20 do rascunho antigo.
  - [CONFIRMADO] Com o treino, rola todos os dados e soma o bônus do treino (+3 treinado, +6 veterano, +9 expert, valores a confirmar) ao ataque.
  - [CONFIRMADO] Treinos de arma especial não gastam as 4 perícias treinadas. O personagem começa com **1 arma especial treinada** (2 se a origem justificar, como caçador ou militar). As outras se aprendem na história (NPC que ensina, treino) ou por marco (seção 12).
- A tabela de armas, com dano, traços e efeitos, está na seção 8.3.

### 8.2 Reações (esquiva, bloqueio e contra-ataque)
- [CONFIRMADO] Quem é atacado rola os dados para se defender, escolhendo uma reação. Só dá para fazer **uma reação por rodada** [PROPOSTA]. Na esquiva e no contra-ataque, o atacante rola o ataque, o defensor rola a reação e vence o maior total (empate para o defensor). O bloqueio funciona diferente, como descrito abaixo.
- **Esquiva**: reserva de Reflexo + treino de Parkour ou Atletismo, a critério do mestre. Gasta 1 Fôlego. Serve contra ataques corpo a corpo e à distância. Sucesso: não sofre o ataque. [PROPOSTA]
- [CONFIRMADO] **Bloqueio**: pode ser feito **com a mão** ou com arma/escudo, só contra corpo a corpo. Não evita o golpe: **a pessoa leva parte do dano, e quanto maior o resultado do teste, mais dano ela bloqueia**. Teste: reserva de Corpo + treino de Contundente ou Cortante. [PROPOSTA] Dano bloqueado = resultado do teste ÷ 5 (arredondado para baixo) na mão, ou ÷ 3 com arma ou escudo; a armadura reduz o que sobrar. A arma ou escudo usado perde 1 de durabilidade (seção 5).
- **Contra-ataque**: ataque corpo a corpo (reserva de Corpo + treino da arma). Só contra corpo a corpo, com arma na mão. [PROPOSTA] Se vencer, evita o ataque **e** causa dano ao atacante (o contra-ataque também pode ser crítico); se perder, sofre o dano normalmente e não ataca.
- [CONFIRMADO] Infectados: o mestre rola a reação deles, com um bônus simples por tipo (valores [PROPOSTA] na seção 9). Hordas e infectados comuns podem não reagir.
- [PENDENTE] Reação contra poderes.

### 8.3 Tabela de armas
- [CONFIRMADO] O **efeito** de cada arma só acontece num **crítico que acerta**. O **traço** (silenciosa, alcance, barulho, recarga) vale sempre.
- [CONFIRMADO] A **margem de crítico e o multiplicador variam por arma**, como em Ordem Paranormal. **Crítico é tirar número alto no dado, e nem sempre um crítico acerta** (o ataque ainda precisa vencer a reação).
- Coluna **Crítico** = margem do dado que ficou e multiplicador dos dados de dano. Ex.: "19–20 ×2" = um 19 ou 20 no dado que ficou, que acerte, dobra os dados de dano e ativa o efeito. "×1" = só o efeito, sem multiplicar. Todos os valores abaixo são [PROPOSTA]: armas leves e precisas têm margem maior e multiplicador menor; armas pesadas têm margem 20 e multiplicador ×3.
- [PROPOSTA] Como o jogador rola vários dados e fica com o maior, tirar 19 ou 20 é comum (cerca de 27% com 3 dados). Por isso a maioria das armas tem margem só no 20. Testar na mesa.
- Dano corpo a corpo soma o Corpo [PENDENTE, ver seção 8]. Alerta +1 ou +2 é o barulho que a arma faz.

**Armas simples (sem treino; usam o bônus de Contundente, Cortante, Arremesso ou Tiro)**

#### Contundente

| Arma | Dano | Crítico | Traço | Efeito no crítico |
|---|---|---|---|---|
| Punhos | 1d4 | 20 ×2 | n/a | n/a |
| Soco inglês | 1d6 | 20 ×2 | n/a | n/a |
| Taco de madeira | 1d8 | 20 ×2 | n/a | Derruba |
| Cano de ferro | 1d8 | 20 ×2 | n/a | n/a |
| Taco com pregos | 1d8 | 20 ×2 | n/a | Sangramento |
| Barra de ferro ou pé de cabra | 1d8 | 20 ×2 | Arromba portas e trancas | Atordoa 1 rodada |
| Martelo | 1d6 | 20 ×2 | n/a | n/a |
| Chave inglesa | 1d6 | 20 ×2 | n/a | n/a |
| Cassetete | 1d6 | 20 ×2 | n/a | Atordoa 1 rodada |
| Marreta (2 mãos) | 1d12 | 20 ×3 | Lenta: ataca 1 vez a cada 2 rodadas | Atordoa 1 rodada |
| Objeto improvisado (frigideira, perna de cadeira) | 1d4 | 20 ×2 | Quebra em 1 natural | n/a |
| Taser | 1d4 | 20 ×2 | Alcance curto; sem dano a infectados com armadura | Atordoa 1 rodada |

#### Cortante

| Arma | Dano | Crítico | Traço | Efeito no crítico |
|---|---|---|---|---|
| Canivete | 1d4 | 19–20 ×2 | Cabe no bolso | n/a |
| Faca de cozinha | 1d4 | 19–20 ×2 | n/a | n/a |
| Faca de combate | 1d6 | 19–20 ×2 | Silenciosa; +1d6 em ataque furtivo | Sangramento |
| Machadinha | 1d8 | 20 ×3 | n/a | n/a |
| Facão ou machete | 1d8 | 19–20 ×2 | n/a | Sangramento |
| Machado (2 mãos) | 1d10 | 20 ×3 | Quebra portas | Sangramento |
| Foice (2 mãos) | 1d8 | 20 ×3 | Alcance de 2 m | Sangramento |
| Lança caseira (2 mãos) | 1d8 | 19–20 ×2 | Alcance de 2 m | Prende o alvo (lento) |
| Serra manual | 1d6 | 20 ×2 | n/a | n/a |
| Motosserra (2 mãos) | 2d8 | 20 ×3 | Alerta +2; gasta combustível | Sangramento |

#### Arremesso

| Arma | Dano | Crítico | Traço | Efeito no crítico |
|---|---|---|---|---|
| Pedra ou garrafa | 1d4 | 20 ×2 | Atrai infectados a um ponto, sem Alerta | n/a |
| Faca de arremesso | 1d6 | 19–20 ×2 | Pode ser recuperada | Sangramento |
| Machadinha de arremesso | 1d8 | 20 ×3 | Pode ser recuperada | n/a |
| Molotov | 2d6 de fogo | 20 ×1 | Área pequena | Queima: 1d4 por rodada por 3 rodadas |
| Bomba caseira | 2d6 em área | 20 ×1 | Alerta +2; explode na mão em 1 natural | Derruba |
| Granada de fragmentação | 3d6 em área | 20 ×1 | Alerta +2 | Derruba |
| Granada de fumaça | n/a | n/a | Bloqueia a visão numa área | n/a |
| Granada UV | n/a | n/a | Luz UV por 3 rodadas; machuca voláteis (1d6 por rodada) | n/a |

#### Tiro (armas de fogo simples)

| Arma | Dano | Crítico | Traço | Efeito no crítico |
|---|---|---|---|---|
| Pistola 9 mm | 1d8 | 19–20 ×2 | Pente de 12; Alerta +1 | n/a |
| Pistola .45 | 1d10 | 19–20 ×2 | Pente de 8; Alerta +1 | Atordoa 1 rodada |
| Revólver .38 | 1d8 | 19–20 ×2 | 6 tiros; recarga lenta; Alerta +1 | n/a |
| Revólver .357 | 1d12 | 20 ×3 | 6 tiros; recarga lenta; Alerta +2 | Derruba |
| Pistola de sinalização | 1d6 de fogo | 20 ×2 | 1 tiro; Alerta +1; ilumina a área | Queima: 1d4 por rodada por 3 rodadas |
| Escopeta de cano duplo | 2d6 | 20 ×3 | Curto alcance (cerca de 10 m); 2 tiros; Alerta +2 | Derruba |
| Rifle de caça | 1d10+2 | 20 ×3 | Longo alcance; Alerta +1 | Sangramento |

**Armas especiais (exigem treino na própria arma)**

| Arma | Dano | Crítico | Traço | Efeito no crítico |
|---|---|---|---|---|
| Arco curto | 1d8 | 19–20 ×2 | Silencioso; recarga rápida; recupera metade das flechas | Prende o alvo (lento) |
| Arco composto | 1d10 | 19–20 ×2 | Silencioso; recarga rápida; recupera metade das flechas | Prende o alvo (lento) |
| Besta leve | 1d10 | 19–20 ×2 | Silenciosa; recarga completa | Sangramento |
| Besta pesada | 2d6 | 20 ×3 | Silenciosa; ignora armadura leve; recarga completa | Sangramento |
| Submetralhadora | 1d8 | 20 ×2 | Rajada: 2 tiros por ação; Alerta +2 | n/a |
| Escopeta pump | 2d6 | 20 ×3 | Curto alcance (cerca de 10 m); pente de 5; Alerta +2 | Derruba |
| Rifle de precisão | 2d8 | 20 ×3 (19–20 ao mirar) | Longo alcance; precisa mirar (1 ação) para o bônus completo; Alerta +1 | Sangramento |
| Fuzil de assalto | 1d10 | 20 ×2 | Rajada: 2 tiros por ação; Alerta +2 | n/a |
| Lança-chamas improvisado | 2d6 de fogo | 20 ×2 | Cone curto; gasta combustível; Alerta +1 | Queima: 1d4 por rodada por 3 rodadas |

- [CONFIRMADO] Variações próximas da mesma arma (arco curto e composto, besta leve e pesada) contam como o **mesmo treino**.

- Estados: **sangramento** = 1 de dano por rodada até curar; **atordoado** = perde a ação na próxima rodada; **derrubado** = cai e gasta o movimento para levantar.

### 8.4 Resto do combate
- [PROPOSTA] Armadura: **reduz o dano sofrido** em 1 (leve), 2 (média) ou 3 (pesada); a pesada impõe desvantagem em Parkour e Furtividade. (Armadura não aumenta defesa, porque não há Defesa fixa.)
- Estados: caído, sangrando (1 de dano por rodada até curar), atordoado (perde a ação), agarrado.
- [CONFIRMADO] **Alerta** (0 a 5, da cena): barulho (tiro, grito, explosão) sobe o Alerta. **Só vale em cidades e ambientes abertos**, onde o som se espalha. Em Alerta 3+, chegam mais infectados; em 5, horda.
  - [PROPOSTA] Em ambientes fechados (prédios, bunkers, cavernas) não há marcador de Alerta: o mestre decide quem ouve, conforme a cena.
  - [PROPOSTA] O Alerta volta a 0 quando o grupo muda de área ou fica em silêncio por um tempo.
- Combate é perigoso: fugir, usar o terreno e luz UV vale mais que lutar.

## 9. Infectados
Valores base [PROPOSTA], **recalibrados em 28/10** porque o atributo não soma mais: os bônus caíram 3 pontos. Ataque e reação: o mestre rola 1d20 + o bônus. Testar na mesa.
- **Comum**: 8 PV, ataque +3, reação +0, dano 1d6. Lento, ruas, em grupo.
- **Viral** (recém-infectado): 6 PV, ataque +6, reação +3, dano 1d6. Rápido, 2 ataques fracos. Surge em surtos.
- **Volátil** (cavernas): 12 PV, ataque +7, reação +3, dano 1d8. Ativo à noite e no escuro. Sob luz UV leva 1d6 por rodada e foge.
- **Brutamonte** (modificado pelo ambiente): 30 PV, ataque +7, reação +0, dano 2d6. Ignora armadura leve. Lento, derruba.
- **Infectados únicos** (antes, com selo): [CONFIRMADO] os selos da SFL 1 não existem na SFL 2, ou existirão de forma diferente. Os infectados únicos da SFL 2 serão criados com o mestre. [PENDENTE]
- Novos tipos de noite e novos zumbis: a criar com o mestre. [PENDENTE]

## 10. Dia, noite e luz UV
- Dia: infectados comuns e virais mais lentos; voláteis enfraquecidos pelo sol.
- Noite: Medo sobe 1 por hora de exploração, voláteis e novos tipos ativos, visão limitada (desvantagem sem luz).
- Luz UV (lanterna, lâmpada, granada): recurso da base. Usa pilha UV (Suprimento). Afeta voláteis e a linha Sombra.

## 11. Facções e reputação
- Quatro facções provisórias: Pacificadores, Sobreviventes, Renegados e Serafitas (nomes definitivos depois).
- Reputação com cada uma: -3 (inimigo) a +3 (aliado). Muda por escolhas do grupo. Efeitos: preços, passagem, favores, emboscadas.
- A reputação é do grupo e, em casos especiais, pessoal.

## 12. Evolução (marcos)
- Sem XP. A evolução vem por **marcos** da história (decididos pelo mestre, em média a cada 2 ou 3 sessões).
- [PROPOSTA] Ciclo (detalhes e listas em `classes-sfl2.md`):
  - **Marcos 1, 3, 5 e 7:** o jogador ganha a próxima habilidade da **trilha** (fixa). A trilha é escolhida no marco 1.
  - **Marcos 2, 4, 6 e 8:** o jogador escolhe **uma** coisa: uma habilidade da **classe** ou um benefício geral (+1 atributo, máximo 5; subir uma perícia de nível; treinar uma nova arma especial ou subir o treino de uma; +1 de Vida máxima por ponto de Corpo).
  - **Poder:** Nível 2 no marco 4 e Nível 3 no marco 8, além do que o jogador escolher naquele marco.
- O ganho em poder sempre vem com um custo narrativo definido pelo mestre.
- [PROPOSTA] Equilíbrio: o ritmo é mais lento que o do primeiro desenho (que dava um benefício geral em todo marco), para segurar o poder dos jogadores.

## 13. Descanso e cura
- Curto (10 min seguros): recupera Fôlego.
- Longo (noite em local seguro): recupera 1d6 + Corpo PV, baixa Medo em 2 e Infecção em 1.
- Medicina DT 15 com bandagem recupera 1d4 PV (uma vez por ferimento).

## 14. A base
- O grupo tem uma base (ver nota A Base). Recursos de base: Energia, Comida, Luz UV, Moral. Cada um de 0 a 5.
- A cada sessão de descanso, o mestre ajusta os valores. Zerar Energia apaga as luzes UV; zerar Comida derruba a Moral.
- Marco Smirnov Rott cuida da Energia e das comunicações (proposta; a confirmar com o mestre).

## 15. Criação de ficha
[PROPOSTA] na ordem abaixo (origem, classe, atributos). Detalhes em `classes-sfl2.md`.
1. **Origem**: escolhe uma das 10 origens (2 perícias, 1 traço, 1 peso). País, se nasceu na Estônia ou se mudou, família adotiva e se conhece algum dos outros continuam livres.
2. **Classe**: Combatente, Batedor, Técnico ou Voz. Dá 2 perícias, 1 bônus e a habilidade inicial.
3. Atributos: 10 pontos, máximo 4 (a classe costuma pedir o atributo dela).
4. As 4 perícias treinadas são as 2 da origem + as 2 da classe.
5. Linha de poder (escolha do jogador) e poder de Nível 1.
   - Arma especial treinada: 1 (ou 2 conforme a origem).
6. Um segredo da vida normal (o mestre usa depois).
7. A última lembrança antes da captura (sem memória do laboratório).
8. Equipamento: quase nada, acordaram em criogenia. 1 arma simples (ou a arma especial treinada, sem munição extra), 1 item de Suprimento (a origem Pesquisador começa sem esse item).
9. A **trilha** é escolhida no marco 1, depois do primeiro marco da campanha.

## 16. Pendências do sistema
**A decidir com o mestre**
- Nome do sistema.
- Se o jogador pode misturar linhas de poder (explicação pedida pelo mestre; ver abaixo).
- Se o Corpo ainda soma no dano.
- Reação contra poderes.
- Origens ligadas à Estônia, nomes finais de classes e habilidades, trocar de trilha ou misturar classes.
- Ritmo dos marcos e equilíbrio de tudo (testar na mesa).

**A criar com o mestre**
- Infectados únicos (no lugar dos selos) e novos tipos de zumbis.
- Melhoria da base, economia e loja, mecânica única de parkour (rascunhos em `base-economia-parkour-sfl2.md`).
- Chefes (depois).
- Veículos.
- Colocar o sistema inteiro no Open RPG (ficha digital e loja).
- Teste na mesa (uma sessão curta) para ajustar números.

**Sobre misturar linhas de poder (a pergunta explicada)**
Hoje cada jogador escolhe **uma linha** (Predador, Sentidos, Carne Viva, Eco ou Sombra) na criação e sobe só nela. A dúvida é se, depois, ele pode aprender poderes de **outra** linha. Opções: (a) nunca, cada um fica na sua linha; (b) uma vez na campanha (por exemplo no marco 6) pega o Nível 1 de outra linha, com custo extra de Infecção; (c) só por evento da história (Marco, o Ódio, um experimento). Sugestão do Claude: (a) com exceção (c), para manter cada jogador com identidade própria e segurar o poder.
