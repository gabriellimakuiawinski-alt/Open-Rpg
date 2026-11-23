# Search For Light (SFL 2) — Equipamento e inventário (livro V1.2, cap. 13)

Copiado do cofre do mestre (repositório SFL, nota `Sistema/Equipamento e inventário.md`, 23/11/2026). **`sfl-dados.js` lê as tabelas deste arquivo** (`tools/livro/gerar_sfl_dados.py`): mude aqui e gere de novo. Os preços em euro ficam só aqui e na loja do Open RPG.

[CONFIRMADO 23/11/2026] O mestre aprovou e isto entrou no **livro V1.2 como capítulo 13** (páginas 42 a 46), **sem os preços**: os preços em euro ficam só aqui e na loja do Open RPG. A coluna Espaços das armas ficou na tabela 13.3 (o capítulo 6 continua sem ela). Os números ainda são regra em teste. Marcas: [CONFIRMADO] = decisão do mestre; [PROPOSTA] = ideia do Claude.
Entra no livro como um capítulo novo, **13 · Equipamento e inventário**, e a tabela de armas do capítulo 6 ganha a coluna **Espaços**. As tabelas de saque ficam fora do livro (são só do mestre).

---

## 1. Inventário

### 1.1 Espaços
[CONFIRMADO] **Espaços = 5 + 3 por ponto de Corpo a partir do 2.**

| Corpo | 0 ou 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Espaços | 5 | 8 | 11 | 14 | 17 |

[PROPOSTA] Corpo 0 e 1 ficam com 5 (li "partindo de 2" como: o primeiro +3 vem no Corpo 2). Continuam valendo o +2 espaços do Técnico e as habilidades do Logístico.

### 1.2 Tamanho dos itens [PROPOSTA]
| Tamanho | O que é | Exemplos |
|---|---|---|
| 0 | Cabe no bolso. Até 5 itens de tamanho 0 não ocupam espaço; do 6º em diante, cada 5 ocupam 1 | Isqueiro, canivete, soco inglês, analgésico, estabilizador |
| 1 | Uma mão | Faca, pistola, lanterna, rádio |
| 2 | Grande ou de duas mãos | Machado, escopeta, arco, escudo |
| 3 | Muito pesado | Marreta, motosserra, rifle de precisão, lança-chamas |

**Itens em pilha** ocupam 1 espaço por pilha: 20 balas de pistola ou revólver, 15 de rifle ou fuzil, 10 cartuchos de escopeta, 10 flechas ou virotes, 3 bandagens, 2 rações, 2 garrafas de água, 4 pilhas UV, 5 unidades de material (Sucata, Peças, Químicos ou Tecido).

### 1.3 Itens prontos [PROPOSTA]
- Você tem **2 itens prontos** (na mão, no cinto, no coldre). Sacar um item pronto é **ação livre**; tirar algo da mochila gasta a **ação de movimento**.
- Itens prontos contam nos espaços normalmente.
- Bolsa de cintura e coldre aumentam os itens prontos (ver 3.4).

### 1.4 Armadura [PROPOSTA]
Armadura **vestida não ocupa espaço** (o peso dela já está nas penalidades). Carregada na mochila, ocupa: leve 1, média 2, pesada 3.

### 1.5 Sobrecarga [PROPOSTA]
- Você pode passar do limite em até **3 espaços**. Nesse caso fica **sobrecarregado**: −3 m de movimento, desvantagem em Parkour e Furtividade e **não ganha Impulso** (capítulo 12).
- Mais que isso não dá para carregar.

---

## 2. Espaços de todas as armas [PROPOSTA]
Sem exagero: quase tudo é 1 ou 2; só as armas enormes são 3.

**Contundente**

| Arma | Espaços | Preço | Raridade |
|---|---|---|---|
| Punhos | — | — | — |
| Soco inglês | 0 | 15 € | Comum |
| Taco de madeira | 2 | 15 € | Comum |
| Cano de ferro | 1 | 5 € | Comum |
| Taco com pregos | 2 | 25 € | Comum |
| Barra de ferro / pé de cabra | 1 | 25 € | Comum |
| Martelo | 1 | 15 € | Comum |
| Chave inglesa | 1 | 15 € | Comum |
| Cassetete | 1 | 30 € | Incomum |
| Marreta (2 mãos) | 3 | 50 € | Comum |
| Objeto improvisado | 1 | — | — |
| Taser | 1 | 80 € | Incomum |
| Escudo (policial ou improvisado) | 2 | 60 € | Incomum |

**Cortante**

| Arma | Espaços | Preço | Raridade |
|---|---|---|---|
| Canivete | 0 | 10 € | Comum |
| Faca de cozinha | 1 | 5 € | Comum |
| Faca de combate | 1 | 60 € | Incomum |
| Machadinha | 1 | 35 € | Comum |
| Facão / machete | 1 | 40 € | Comum |
| Machado (2 mãos) | 2 | 60 € | Comum |
| Foice (2 mãos) | 2 | 40 € | Comum |
| Lança caseira (2 mãos) | 2 | 20 € | Comum |
| Serra manual | 1 | 15 € | Comum |
| Motosserra (2 mãos) | 3 | 200 € | Raro |

**Arremesso**

| Arma | Espaços | Preço | Raridade |
|---|---|---|---|
| Pedra / garrafa | 1 (pilha de 3) | — | — |
| Faca de arremesso | 1 (pilha de 3) | 30 € cada | Incomum |
| Machadinha de arremesso | 1 | 35 € | Comum |
| Molotov | 1 (pilha de 2) | 25 € | Comum (fabricável) |
| Bomba caseira | 1 (pilha de 2) | 50 € | Incomum (fabricável) |
| Granada de fragmentação | 1 (pilha de 2) | 150 € | Raro |
| Granada de fumaça | 1 (pilha de 2) | 60 € | Incomum (fabricável) |
| Granada UV | 1 (pilha de 2) | 120 € | Raro |

**Tiro (armas de fogo simples)**

| Arma | Espaços | Preço | Raridade |
|---|---|---|---|
| Pistola 9 mm | 1 | 180 € | Incomum |
| Pistola .45 | 1 | 220 € | Incomum |
| Revólver .38 | 1 | 150 € | Incomum |
| Revólver .357 | 1 | 250 € | Raro |
| Pistola de sinalização | 1 | 60 € | Comum |
| Escopeta de cano duplo | 2 | 250 € | Incomum |
| Rifle de caça | 2 | 300 € | Incomum |

**Armas especiais**

| Arma | Espaços | Preço | Raridade |
|---|---|---|---|
| Arco curto | 2 | 120 € | Incomum |
| Arco composto | 2 | 250 € | Raro |
| Besta leve | 2 | 200 € | Incomum |
| Besta pesada | 3 | 350 € | Raro |
| Submetralhadora | 2 | 500 € | Raro |
| Escopeta pump | 2 | 400 € | Raro |
| Rifle de precisão | 3 | 800 € | Raro |
| Fuzil de assalto | 2 | 700 € | Raro |
| Lança-chamas improvisado | 3 | 300 € | Raro (fabricável) |

---

## 3. Catálogo de equipamento [PROPOSTA]

### 3.1 Preço e raridade
- **Comum:** quase todo comerciante tem. **Incomum:** só em lojas de facção ou com sorte. **Raro:** só com facção aliada, missão ou saque especial.
- Preços em euro (€), a moeda da Estônia. O dinheiro vale pouco depois do colapso: **escambo** é normal (o mestre aceita itens no lugar de euros pela metade do preço deles).
- **Reputação** muda o preço: aliado (+3) paga 80%; neutro paga 100%; inimigo (−3) paga 140% ou não consegue comprar.
- Vender um item rende metade do preço.

### 3.2 Munição
| Item | Pilha (1 espaço) | Preço da pilha | Raridade |
|---|---|---|---|
| Balas de pistola ou revólver | 20 | 40 € | Incomum |
| Balas de rifle ou fuzil | 15 | 60 € | Raro |
| Cartuchos de escopeta | 10 | 40 € | Incomum |
| Flechas ou virotes | 10 | 20 € | Comum (fabricável) |
| Flechas de fogo | 5 | 40 € | Incomum (fabricável): o acerto deixa o alvo queimando |
| Flechas UV (ponta com tinta reativa) | 5 | 60 € | Raro: ao acertar um volátil, causa 1d6 de UV |
| Combustível (galão pequeno) | 1 | 30 € | Incomum: motosserra, lança-chamas, molotov, veículos |

### 3.3 Armaduras
| Armadura | Tipo | Reduz | Preço | Raridade | Observação |
|---|---|---|---|---|---|
| Jaqueta de couro | Leve | −1 | 40 € | Comum | — |
| Roupa de motociclista com proteções | Leve | −1 | 90 € | Incomum | Vantagem para não sofrer dano de queda até 6 m |
| Colete balístico | Média | −2 | 300 € | Raro | Contra tiro, reduz −3 |
| Armadura de sucata | Média | −2 | — | Fabricável | Desvantagem em Furtividade |
| Roupa de choque (polícia) | Pesada | −3 | 600 € | Raro | Desvantagem em Parkour e Furtividade (regra da pesada) |

Bônus do mesmo tipo: armadura com armadura não acumula (vale a maior).

### 3.4 Carregar
| Item | Espaços | Efeito | Preço | Raridade |
|---|---|---|---|---|
| Mochila escolar | — | +2 espaços | 15 € | Comum |
| Mochila de trilha | — | +4 espaços | 60 € | Incomum |
| Mochila militar | — | +5 espaços e +1 item pronto | 150 € | Raro |
| Bolsa de cintura | 0 | +1 item pronto | 20 € | Comum |
| Coldre ou bainha | 0 | +1 item pronto (só uma pistola, revólver ou faca) | 25 € | Comum |
| Bandoleira | 0 | Uma pilha de munição conta como pronta (recarregar não pede tirar da mochila) | 30 € | Incomum |

Só uma mochila por vez. Mochilas não ocupam espaço (são o espaço).

### 3.5 Exploração
| Item | Espaços | Efeito | Preço | Raridade |
|---|---|---|---|---|
| Isqueiro | 0 | Acende fogo, molotov e flechas de fogo | 5 € | Comum |
| Lanterna | 1 | Ilumina 10 m; tira a desvantagem do escuro | 20 € | Comum |
| Lanterna UV | 1 | Gasta 1 pilha UV por cena; voláteis no cone de 6 m sofrem 1d6 por rodada e não avançam | 150 € | Raro |
| Pilha UV | 0 (pilha de 4) | Alimenta lanterna ou lâmpada UV por uma cena | 25 € cada | Incomum |
| Corda (15 m) | 1 | Descer e subir sem teste em paredes lisas; o mestre dá vantagem em escaladas | 15 € | Comum |
| Gancho com corda | 2 | Prende num beiral a até 12 m; subir pela corda é parkour livre | 60 € | Incomum |
| Kit de arrombamento | 0 | Vantagem em Técnica para fechaduras e cadeados | 50 € | Incomum |
| Máscara de gás | 1 | Vantagem contra gás, fumaça e esporos; sem desvantagem dentro de fumaça | 120 € | Raro |
| Binóculo | 1 | Vê detalhes a até 500 m; vantagem em Percepção à distância | 60 € | Incomum |
| Rádio portátil | 1 | Capta transmissões das facções | 80 € | Incomum |
| Par de walkie-talkies | 1 | Fala com o grupo a até 2 km | 100 € | Incomum |
| Apito | 0 | Atrai infectados comuns para onde você está (sobe 1 de Alerta ali) | 5 € | Comum |
| Mapa da região | 0 | Vantagem em Sobrevivência para achar rota numa área conhecida | 20 € | Comum |
| Saco de dormir | 2 | Descanso longo no frio sem perder 1d4 PV | 40 € | Comum |

### 3.6 Médicos
| Item | Espaços | Efeito | Preço | Raridade |
|---|---|---|---|---|
| Bandagem | 1 (pilha de 3) | Medicina DT 15: recupera 1d4 PV, uma vez por ferimento; para sangramento | 10 € cada | Comum (fabricável) |
| Kit médico | 1 | 5 usos. Cada uso é uma bandagem com vantagem que para qualquer sangramento | 120 € | Incomum |
| Analgésico | 0 | Por uma cena, ignora desvantagens de dor e ganha 2 PV temporários | 20 € | Comum |
| Antibiótico | 0 | Cura uma ferida infeccionada ou doença comum (não baixa a Infecção do composto) | 60 € | Incomum |
| Adrenalina | 0 | Recupera 3 Fôlego na hora; −1 de Fôlego máximo até o descanso longo | 80 € | Raro |
| Estabilizador | 0 | Baixa 2 de Infecção. Só 1 por dia | 500 € | Raro |

### 3.7 Comida e ferramentas
| Item | Espaços | Efeito | Preço | Raridade |
|---|---|---|---|---|
| Ração | 1 (pilha de 2) | Comida para um dia | 8 € cada | Comum |
| Água (garrafa) | 1 (pilha de 2) | Água para um dia | 5 € cada | Comum |
| Kit de ferramentas | 1 | Necessário para instalar modificações fora da base e para reparos | 60 € | Incomum |
| Kit de química | 2 | Necessário para receitas químicas (molotov, fumaça, veneno, bomba) fora da base | 100 € | Incomum |
| Materiais (Sucata, Peças, Químicos, Tecido) | 1 (pilha de 5) | Usados em receitas e modificações | Sucata 2 €, Tecido 3 €, Peças 10 €, Químicos 10 € cada | Sucata e Tecido comuns; Peças e Químicos incomuns |

---

## 4. Modificações de arma [PROPOSTA]

Como as armas só quebram com 1 natural, a melhoria de arma vem das **modificações**.

### 4.1 Regras
- Instalar: **Técnica DT 15**, os materiais da modificação e **1 hora** (na oficina da base, sem teste). Fora da base precisa do **kit de ferramentas**.
- Cada modificação só pode ser instalada **uma vez por arma**. Tirar uma modificação devolve metade dos materiais.
- **Bônus do mesmo tipo continuam não acumulando** (dados com dados, dano com dano, margem com margem): vale o maior entre mod, habilidade e origem.
- Quando a arma quebra (1 natural), as modificações ficam; ao consertar, voltam a funcionar.

### 4.2 Limite por tipo de arma
| Tipo de arma | Limite | Quais |
|---|---|---|
| Pequena de corpo a corpo | **1** | Soco inglês, canivete, facas, martelo, chave inglesa, cassetete, taser |
| Corpo a corpo comum | **2** | Taco, taco com pregos, cano, barra / pé de cabra, machadinha, facão, serra manual |
| Corpo a corpo pesada (2 mãos) | **3** | Marreta, machado, foice, lança caseira |
| Motosserra e escudo | **1** | — |
| Arremesso | **0** | São consumíveis: a variação vem das receitas |
| Pistolas e revólveres | **2** | Pistola 9 mm e .45, revólveres, pistola de sinalização (só 1) |
| Armas longas simples | **2** | Escopeta de cano duplo, rifle de caça |
| Arcos e bestas | **2** | — |
| Armas militares | **3** | Submetralhadora, escopeta pump, rifle de precisão, fuzil de assalto |
| Lança-chamas | **1** | — |

### 4.3 Modificações de corpo a corpo
| Modificação | Para | Efeito | Materiais |
|---|---|---|---|
| Pregos e arame | Contundente | Sangramento vira efeito do crítico (além do efeito da arma) | 2 Sucata |
| Lâmina soldada | Contundente | Pode usar Cortante ou Contundente (o que for melhor) | 2 Sucata, 1 Peça |
| Fio afiado | Cortante | Margem de crítico +1 (20 vira 19–20; 19–20 vira 18–20) | 1 Sucata, 1 Peça |
| Empunhadura de fita | Qualquer corpo a corpo | +1 dado no bloqueio com essa arma | 1 Tecido |
| Contrapeso | Pesada (2 mãos) | Derruba vira efeito do crítico | 3 Sucata |
| Eletrificada | Metal | No crítico, o alvo fica atordoado 1 rodada; gasta 1 pilha por cena de uso | 2 Peças, 1 pilha UV |
| Pano em chamas | Qualquer corpo a corpo, menos motosserra | Por uma cena, o crítico deixa o alvo queimando; Alerta +1 (luz). Recarregar gasta 1 Tecido e combustível | 1 Tecido, combustível |
| Alça leve | Qualquer arma de 2 ou 3 espaços | Ocupa 1 espaço a menos | 1 Tecido, 1 Sucata |

### 4.4 Modificações de arma de fogo, arco e besta
| Modificação | Para | Efeito | Materiais |
|---|---|---|---|
| Silenciador improvisado | Pistolas, submetralhadora, rifle de caça, fuzil | O tiro não sobe o Alerta (ou sobe 1 a menos nas armas de Alerta +2); −1 de dano | 2 Sucata, 1 Peça |
| Mira (luneta ou ponto vermelho) | Armas de fogo, arcos e bestas | Depois de mirar, +1 dado no ataque | 2 Peças |
| Carregador estendido | Pistolas, submetralhadora, fuzil, escopeta pump | +50% de munição no pente | 2 Peças |
| Carregador rápido | Revólveres e escopeta de cano duplo | Recarga lenta vira recarga normal (só a ação) | 1 Peça, 1 Sucata |
| Lanterna acoplada | Armas de fogo | Ilumina 10 m sem ocupar a outra mão (uma lanterna UV acoplada também funciona, gastando pilha) | Uma lanterna ou lanterna UV |
| Cano serrado | Escopetas | +1 dado de dano a até 5 m; o alcance cai para 5 m | 1 Sucata |
| Corda reforçada | Arcos e bestas | +1 de dano | 1 Peça, 1 Tecido |
| Aljava de cinto | Arcos e bestas | A pilha de flechas conta como pronta | 1 Tecido |
| Bocal largo | Lança-chamas | O cone vai de curto para médio (6 m) | 2 Peças |

---

## 5. Fabricação [PROPOSTA]
- Fabricar gasta **1 hora**, os materiais e um teste: **Técnica DT 15** para objetos, **Medicina DT 15** para itens médicos, **Técnica ou Sobrevivência DT 15** para receitas químicas (com kit de química fora da base). Falhar perde metade dos materiais.
- As habilidades que já fabricam (Técnico, Toxina) continuam valendo como estão e não pedem teste quando o texto delas diz isso.

| Receita | Materiais | Teste |
|---|---|---|
| Bandagem (3) | 2 Tecido | Medicina DT 12 |
| Molotov (2) | 2 garrafas (Sucata), 1 Tecido, combustível | Técnica DT 12 |
| Flechas ou virotes (10) | 2 Sucata, 1 Tecido | Técnica DT 12 |
| Flechas de fogo (5) | 5 flechas, 1 Tecido, combustível | Técnica DT 15 |
| Granada de fumaça (2) | 2 Químicos, 1 Sucata | Técnica ou Sobrevivência DT 15 |
| Bomba caseira (2) | 2 Químicos, 2 Sucata, 1 Peça | Técnica DT 18 (falhar por 5 ou mais: explode na mão, 1d6) |
| Armadura de sucata | 6 Sucata, 2 Tecido | Técnica DT 15 |
| Lança-chamas improvisado | 4 Peças, 3 Sucata, combustível | Técnica DT 20 |
| Lança caseira | 1 Sucata, 1 Tecido | Sem teste |

---

## 6. Correções que entram junto na V1.2 [PROPOSTA]
- Capítulo 9: trocar "a origem (sua vida normal até os 25 anos)" por **"a origem (o que você fazia antes de entrar no programa da vacina)"**, de acordo com a lore de 04/11.
- Capítulo 9: renumerar as tabelas de classes de 9.3–9.6 para 9.2–9.5 (a 9.2 sumiu quando as origens viraram uma tabela só).
- Capítulo 3: a linha do inventário passa a dizer "5 + 3 por ponto de Corpo a partir do 2 (capítulo 13)".
- Capítulo 6: coluna **Espaços** na tabela de armas.
- Índice, consulta rápida e marcadores com o capítulo 13.

## 7. Fica para a V1.3 (não entra agora)
Facções em detalhe, melhoria da base, inverno da Estônia, veículos, livro do mestre e ficha imprimível. As tabelas de saque ficam só com o mestre.
