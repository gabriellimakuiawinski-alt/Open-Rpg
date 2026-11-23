# Como funciona a ficha automática do Search For Light

Este arquivo explica **o que a ficha guarda, o que ela calcula e como ela reage** a cada escolha do jogador. Todos os números vêm de `dados/*.json`. Os nomes entre crases são os campos sugeridos; mantenha os que já existem no `sfl-regras.js` quando fizer sentido.

A ideia em uma frase: **a ficha guarda só as escolhas do jogador e os marcadores do momento; todo o resto é calculado a partir das escolhas + os JSON.**

---

## 1. O que a ficha guarda

### Escolhas (mudam pouco)
| Campo | Exemplo | De onde vem |
|---|---|---|
| `atributos` | `{corpo:2, reflexo:4, mente:2, presenca:2}` | Criação e benefício "+1 atributo" |
| `origem` | `"cacador-rural"` | `origens.json` |
| `classe` | `"batedor"` | `classes.json` |
| `periciasOrigem` / `periciasClasse` | `["sobrevivencia","furtividade"]` / `["parkour","percepcao"]` | 2 + 2 na criação |
| `treinos` | `{parkour: 3, ...}` | Começa em +3 nas 4 treinadas; sobe por benefício |
| `armasEspeciais` | `[{familia:"arco", treino:3}]` | 1 na criação (2 com Militar) |
| `marco` | `0` a `8` | O mestre declara |
| `trilha` | `"corredor"` | Escolhida no marco 1 |
| `escolhasPares` | `[{marco:2, tipo:"habilidade", id:"pe-leve"}, {marco:4, tipo:"beneficio", id:"atributo", alvo:"reflexo"}]` | Marcos 2, 4, 6, 8 |
| `infectado` | `"sentidos"` | `infectados.json` |
| `infNiveis` | `{"1":"faro","2":"vibracao"}` | 1 de 3 em cada nível |
| `marcoInf` / `infTrilha` | `1` / `"farejador"` | Marcos de infectado (extras do mestre) |
| `habilidadePropria` | `{molde:"sentido", mutacoes:["duradoura"], fraquezas:["medo"], grau:1, aprovada:false, descricao:"..."}` | Capítulo 8 |
| `inventario` | lista de itens (ver seção 6) | Loja, saque, fabricação |

### Marcadores (mudam toda hora)
`vida`, `folego`, `medo` (0 a 5), `infeccao` (0 a 10), `impulso` (0 a 3), `usos` (contadores de "uma vez por cena/sessão": `{ "aguentar": "cena" }`), `alerta` e `estagioPerseguicao` (esses dois são da mesa/cena, não do personagem).

---

## 2. Como a ficha descobre o que o personagem tem

Monte uma lista de **fontes ativas** sempre que algo mudar:

1. a origem;
2. a classe (bônus e habilidade inicial);
3. as habilidades da trilha **liberadas pelo marco**: marco 1 → habilidade 1; marco 3 → 2; marco 5 → 3; marco 7 → 4;
4. as habilidades de classe escolhidas nos marcos pares (`escolhasPares` do tipo "habilidade");
5. o nível da classe de infectado: **1** na criação, **2** a partir do marco 4, **3** a partir do marco 8, com a opção escolhida em cada nível (`infNiveis`);
6. as habilidades da trilha de infectado: `marcoInf` 1 → habilidade 1, 2 → 2, 3 → 3, 4 → 4;
7. os itens **equipados** (armadura vestida, mochila, bolsa, coldre);
8. os benefícios gerais escolhidos.

Cada fonte pode ter `efeitos`, uma lista como `[{ "soma": "folegoMax", "valor": 2 }]`. A ficha soma os efeitos por alvo, com uma regra:

- **Mesmo tipo não soma:** para `metros` (movimento extra) vale **o maior** de todas as fontes, incluindo o Impulso. Armadura também: vale a maior redução vestida.
- Os outros alvos (`vidaMax`, `folegoMax`, `espacos`, `prontos`, `armasEspeciais`) somam.

Alvos conhecidos (o validador só aceita estes): `vidaMax`, `folegoMax`, `espacos`, `espacosGrupo`, `prontos`, `metros`, `armasEspeciais`, `infeccao` (itens que baixam Infecção ao usar), `margemCritico` e `espacosArma` (modificações de arma).

Tudo que **não** tem `efeitos` é texto: aparece na ficha com o nome e a descrição. Se o texto diz "uma vez por cena" ou "uma vez por sessão", mostre um botão de uso que zera quando o mestre encerra a cena ou a sessão.

---

## 3. Valores calculados

Com `C` = Corpo, `R` = Reflexo e `E(alvo)` = soma dos efeitos ativos:

| Valor | Fórmula (dados em `regras.json`) |
|---|---|
| **Vida máxima** | `10 + 2×C + E(vidaMax) + benefícios de Vida` (cada benefício "+1 Vida por Corpo" vale o Corpo **no momento da escolha**; guarde o número na escolha, não recalcule) |
| **Fôlego máximo** | `5 + R + E(folegoMax)` |
| **Espaços** | tabela `recursos.espacos.tabela[C]` (Corpo 0–1 = 5, 2 = 8, 3 = 11, 4 = 14, 5 = 17) `+ E(espacos)` |
| **Itens prontos** | `2 + E(prontos)` |
| **Movimento** | `9 m + maior(E(metros), metros do Impulso)`; sobrecarregado: `−3 m` |
| **Armadura** | maior redução entre as armaduras vestidas |
| **Faixa de Infecção** | `regras.infeccao.faixas` pelo valor atual; mostrar o efeito e, de 6 a 9, o dado de descontrole (d12, d10, d8, d6) |
| **Medo** | 3 ou mais: avisar "desvantagem em Vontade e ataques à distância"; 5: "congela ou foge por uma rodada" |
| **Armas especiais treinadas (máximo)** | `1 + E(armasEspeciais)` (Militar tem 2) |
| **Pendências de evolução** | marcos pares sem escolha, trilha não escolhida no marco 1, nível de infectado sem opção, trilha de infectado não escolhida com `marcoInf ≥ 1` |

---

## 4. Rolagens

### Teste comum
1. **Quantidade de dados** = valor do atributo. Vantagem soma 1 dado; desvantagem tira 1. Vantagem de várias fontes continua sendo +1.
2. Se a quantidade ficar **menor que 1** (atributo 0, desvantagens): rola **2 d20 e fica com o menor**.
3. Senão, rola e fica com o **maior**.
4. **Resultado** = dado que ficou + treino da perícia (`0, 3, 6, 9`). **O atributo não soma.**
5. Fora de combate: 20 no dado que ficou e passou na DT = sucesso excepcional; qualquer dado com **1** num teste que **falhou** = complicação.
6. Mostre no log da mesa todos os dados e qual ficou.

### Ataque
- Atributo: **Corpo** no corpo a corpo; **Reflexo** à distância e no arremesso.
- Bônus: treino da categoria (Contundente, Cortante, Arremesso, Tiro) ou o treino da **família** da arma especial. Arma especial sem treino: **1 dado a menos** e sem bônus.
- Acerta se o total for **maior** que o da reação (empate é de quem defende). Infectado comum não reage: acerta com 10 ou mais.
- **Crítico**: o dado que ficou ≥ `critico.margem` da arma (menos `margemCritico` das modificações) **e** acertou → multiplica só os dados de dano por `critico.mult` e aplica o efeito da arma.
- **Dano** = dados da arma (+ multiplicador no crítico) + **Corpo** no corpo a corpo.
- Munição: tiro gasta 1, rajada gasta 2 (dois ataques).
- Arma corpo a corpo **quebra** com um 1 natural num ataque ou bloqueio que falhou: marque `quebrada: true` (as modificações ficam).

### Reações
- Esquiva: Reflexo + Parkour ou Atletismo, **gasta 1 Fôlego**.
- Bloqueio: Corpo + Contundente ou Cortante; dano bloqueado = resultado ÷ 5 (mão) ou ÷ 3 (arma, escudo), arredonda para baixo; depois a armadura reduz o resto.
- Contra-ataque: Corpo + treino da arma, só com arma na mão.

### Poderes de infectado
- Ao usar um poder: soma o **custo** em Infecção (o número entre parênteses).
- Poder que só afeta você ou aliados que concordam: sem teste.
- Poder que ataca: atributo da arma (Corpo ou Reflexo) + treino de **Vontade**.
- Poder sobre mente ou infectado: Presença + treino de Vontade.
- Infecção 3 a 5: **+2** no teste do poder.
- Infecção 6 a 9: depois de usar, a ficha rola o **dado de descontrole** da faixa; se sair o valor máximo, mostra "perdeu a rodada".
- Infecção chega a 10: a ficha mostra o aviso da transformação (Vontade DT 15 e Persuasão do grupo DT 15).

---

## 5. Criação de ficha (guia passo a passo)

Siga o capítulo 11 (`livro/11-guia-de-criacao-de-ficha.md`). A ficha conduz o jogador e **bloqueia o "pronto"** até a conferência passar:

1. História (resumo, segredo, última lembrança): texto livre.
2. Origem (30): marca as 2 perícias.
3. Classe (4): escolhe 2 perícias entre as da classe, sem repetir a origem; mostra o bônus e a habilidade inicial.
4. Atributos: 10 pontos, máximo 4 em cada; avisar se algum ficar 0.
5. Perícias: confere 2 + 2 treinadas (+3).
6. Arma especial: 1 família (2 com Militar).
7. Classe de infectado (10) e 1 das 3 opções do Nível 1.
8. Habilidade própria: molde, 1 mutação, 1 fraqueza; fica "aguardando o mestre".
9. Recursos: calculados sozinhos.
10. Equipamento: 1 arma simples **ou** a especial, e 1 item de Suprimento (Pesquisador e Morador de rua sem Suprimento: `semSuprimento` na origem).
11. **Conferência**: 4 perícias sem repetir; atributos somam 10, nenhum acima de 4; origem, classe e infectado com Nível 1; arma especial; habilidade própria entregue; Vida, Fôlego e espaços calculados; segredo e lembrança anotados. **Sem trilha ainda** (é normal).

---

## 6. Inventário

Cada item na ficha: `{ ref: "arma:pistola-9-mm" ou "item:bandagem", qtd, equipado, pronto, quebrada, mods: [] }`.

- **Espaço usado** = soma, por item, de `ceil(qtd / pilha) × espacos`.
- Itens de **tamanho 0**: os 5 primeiros não ocupam espaço; do 6º em diante, cada 5 ocupam 1.
- **Armadura vestida** ocupa 0; na mochila ocupa `regras.inventario.armaduraNaMochila`.
- **Mochila** equipada não ocupa espaço e dá `efeitos` (+espaços, +prontos). Só uma mochila.
- **Prontos**: no máximo `2 + E(prontos)` itens marcados como prontos. Coldre só aceita pistola, revólver ou faca.
- **Sobrecarga**: usado acima do limite em até +3 → mostra "sobrecarregado: −3 m, desvantagem em Parkour e Furtividade, sem Impulso". Mais que +3: não deixa adicionar.
- **Loja**: preço = `preco × multiplicador da reputação` (aliado +3: 0,8; neutro: 1,0; inimigo −3: 1,4 ou não vende). Vender rende metade. O mestre pode liberar itens por raridade.

## 7. Modificações e fabricação

- Uma arma aceita até `limiteMods` modificações, **cada uma uma vez**.
- A modificação serve para a arma se bater com `para`: `categorias`, `ids`, `familias`, `duasMaos`, `espacosMin`, `exceto`.
- Instalar: Técnica DT 15 (sem teste na oficina da base), 1 hora e os materiais; fora da base precisa do kit de ferramentas no inventário.
- Receitas: consomem os materiais do inventário, pedem o teste da receita, e a falha perde metade dos materiais.

## 8. Parkour e perseguição

- `impulso` de 0 a 3. O jogador (ou o mestre) aperta **+1** ao superar um obstáculo relevante (no máximo 1 por rodada) e **zerar** ao parar, falhar ou cair.
- Metros do Impulso: `parkour.impulso.metros[impulso]`, comparados com os outros metros (vale o maior).
- No nível 3, mostrar "vantagem no próximo teste de Parkour" com um botão de usar; a vantagem só volta quando o Impulso chegar a 3 de novo.
- Sobrecarregado: o botão +1 de Impulso fica desligado.
- Na mesa, o mestre tem um marcador de estágio de perseguição de 1 a 6 (`parkour.estagios`), que começa em 3 (Perto).

## 9. O que fica de fora da automação (de propósito)

- O texto de quase todas as habilidades de classe, trilha e infectado.
- A habilidade própria: a ficha só guarda as peças e o custo (1 + número de mutações); o efeito é o mestre quem aprova.
- Alerta e base são da mesa e do grupo, não do personagem.
- Tabelas de saque: são só do mestre e não entram no site.
