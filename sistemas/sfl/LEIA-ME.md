# Search For Light (SFL 2) — sistema completo para o Open RPG

Esta pasta é a **fonte única** do sistema Search For Light dentro do Open RPG. Versão das regras: **1.2** (23/11/2026), igual ao livro `livro-sfl-v1.2.pdf` do mestre.

Se você é o Claude trabalhando no Open RPG: **leia este arquivo inteiro antes de mexer no SFL**. Depois leia `FICHA-AUTOMATICA.md`.

## O que tem aqui

| Pasta / arquivo | O que é | Quem usa |
|---|---|---|
| `livro/` | Transcrição completa do livro V1.2, um arquivo por capítulo (00 a 13) | Para entender a regra e conferir texto |
| `livro/LIVRO-COMPLETO.md` | Os 14 arquivos juntos num só | Para ler ou buscar tudo de uma vez |
| `dados/` | As regras em JSON: números, listas e efeitos | **O site lê daqui** |
| `FICHA-AUTOMATICA.md` | Como a ficha calcula tudo sozinha, passo a passo | Quem programa a ficha |
| `ferramentas/validar.py` | Confere os JSON (ids, perícias, efeitos, contagens) | Rodar antes de publicar |

### Os arquivos de `dados/`

| Arquivo | Conteúdo |
|---|---|
| `regras.json` | Atributos, teste, treino, fórmulas de Vida, Fôlego e espaços, Infecção (faixas e dado de descontrole), descanso, combate, reações, armadura, Alerta, marcos, benefícios gerais, inventário, base, reputação |
| `pericias.json` | As 15 perícias |
| `origens.json` | As 30 origens (perícias, traço, peso e efeitos numéricos) |
| `classes.json` | Combatente, Batedor, Técnico e Voz: perícias, bônus, habilidade inicial, 9 habilidades à escolha e 3 trilhas de 4 |
| `infectados.json` | As 10 classes de infectado: papel, fraqueza, 3 opções por nível (com custo em Infecção) e 3 trilhas de 4 |
| `habilidade-propria.json` | Moldes, mutações, fraquezas e graus da habilidade de infectado própria (capítulo 8) |
| `armas.json` | As 47 armas: dano, crítico, traço/efeito, espaços, pilha, raridade, **preço** e limite de modificações |
| `itens.json` | Munição, armaduras, mochilas, exploração, médicos, comida, materiais e ferramentas, com espaços, raridade e **preço** |
| `modificacoes.json` | As 17 modificações de arma, para quais armas servem e os materiais |
| `receitas.json` | As 9 receitas de fabricação |
| `parkour.json` | Movimentos, falhas, sequência, Impulso e estágios de perseguição |

**Preços:** só existem nos JSON, para a loja do Open RPG. O livro não mostra preço. Não coloque preço em nenhum texto que o jogador leia como regra do livro; na loja, pode.

## Regras de ouro para quem mexe

1. **Os JSON mandam.** Se o texto do `livro/` e o JSON discordarem num número, avise o mestre; não escolha sozinho.
2. **Ids nunca mudam.** A ficha salva guarda ids (`"origem": "lenhador"`). Para renomear, mude só o campo `n`. Para tirar algo do jogo, marque `"removida": true` em vez de apagar, senão fichas antigas quebram.
3. **Automatize só o que é número.** Vida, Fôlego, espaços, itens prontos, metros, treinos, dados e custos. Habilidades de cena ("uma vez por cena, derruba o alvo") aparecem como **texto** na ficha, com um contador de usos se fizer sentido. Não tente transformar as quase 300 habilidades em código.
4. **Bônus do mesmo tipo não somam** (vale o maior): armadura, dados, metros, dano de furtivo, redução de custo de Fôlego. Vantagem de duas fontes continua sendo +1 dado.
5. **Mudou uma regra?** Edite o JSON, rode `python3 sistemas/sfl/ferramentas/validar.py`, suba a `versao` em todos os JSON se for uma versão nova do livro, e atualize o texto em `livro/` se a mudança aparece no livro.
6. Tudo do `CLAUDE.md` da raiz continua valendo (subir `?v=N`, não editar `mesa.html` à mão, SQL re-executável, publicar por PR).

## Estado atual do Open RPG (antes desta pasta)

O SFL já existe no site, mas na **versão 0.6** (antiga):

| Arquivo | O que faz hoje | Problema |
|---|---|---|
| `tools/livro/gerar_sfl_dados.py` | Lê `docs/sfl/*.md` por regex e gera `sfl-dados.js` | Quebra quando o texto muda de formato; está preso na v0.6 |
| `sfl-dados.js` | `window.SFLD` com classes, 10 origens, 5 "linhas de poder" antigas e armas | Desatualizado: faltam 20 origens, as 10 classes de infectado, itens, parkour |
| `sfl-regras.js` | Regras da ficha | Tem regras fixas no código (Combatente +4 PV, Batedor +2 Fôlego, Militar +1 arma, faixas de Infecção com a regra velha "Vontade DT 18", inventário 5 + Corpo) |
| `ficha-sfl.js` | Tela da ficha SFL | Mostra as "linhas de poder" antigas |
| `docs/sfl/*.md` | Documentos v0.6 | **Substituídos por esta pasta** |

## Plano de implementação (fazer nesta ordem)

Cada etapa é um PR separado. Teste no celular entre uma e outra.

### Etapa 1 — Carregar os dados novos
- Reescreva `tools/livro/gerar_sfl_dados.py` para **só juntar os JSON** de `sistemas/sfl/dados/` num `sfl-dados.js` (`window.SFLD = { versao, regras, pericias, origens, classes, infectados, habilidadePropria, armas, itens, modificacoes, receitas, parkour }`). Nada de regex.
  - Motivo de gerar um `.js` em vez de `fetch` no JSON: o site é PWA e funciona com cache; um arquivo só com `?v=N` é mais simples. (Se preferir `fetch`, tudo bem, mas cuide do cache offline.)
- Rode o validador dentro do gerador: se der erro, não gere.
- Pronto quando: `window.SFLD.versao === "1.2"` e o teste de dados passar.

### Etapa 2 — Tirar as regras fixas do `sfl-regras.js`
- Vida, Fôlego e espaços saem de `SFLD.regras.recursos` + a soma de `efeitos` (veja `FICHA-AUTOMATICA.md`).
- Faixas de Infecção e dado de descontrole saem de `SFLD.regras.infeccao`.
- Treino (+0/+3/+6/+9), benefícios gerais e marcos saem de `SFLD.regras`.
- Nenhum `if (classe == 'combatente')` deve sobrar.
- Pronto quando: mudar `vidaMax.porCorpo` no JSON muda a Vida na ficha sem tocar em JS.

### Etapa 3 — Classes de infectado no lugar das "linhas de poder"
- A ficha passa a ter `infectado` (id da classe), as escolhas de nível `infNiveis: {"1": id, "2": id, "3": id}`, a `infTrilha` e quantos **marcos de infectado** o personagem tem (`marcoInf`, 0 a 4).
- Migração: fichas antigas com `sfl.linha` ficam com `infectado` vazio e um aviso "escolha a classe de infectado"; não tente converter sozinho (as linhas antigas não batem 1 para 1 com as classes novas).
- Pronto quando: dá para escolher qualquer das 10 classes, ver as 3 opções do nível certo e os custos em Infecção.

### Etapa 4 — Origens, classes e criação de ficha
- 30 origens, 4 classes, perícias da origem + classe (2 + 2, sem repetir), arma especial (2 com Militar), habilidade própria (molde, mutação, fraqueza) como campos simples para o mestre aprovar.
- Guia de criação passo a passo e a **conferência** do capítulo 11 (veja `FICHA-AUTOMATICA.md`).

### Etapa 5 — Inventário V1.2
- Espaços por Corpo, tamanho dos itens, pilhas, bolso, itens prontos, armadura vestida, sobrecarga, mochilas.
- Catálogo novo (armas + itens) na loja, com preço em euro ajustado pela reputação.

### Etapa 6 — Modificações e fabricação
- Até `limiteMods` modificações por arma, cada uma uma vez só, filtrando pelas regras de `para`.
- Receitas consomem materiais do inventário.

### Etapa 7 — Parkour e perseguição
- Contador de Impulso (0 a 3) com os metros e a vantagem do nível 3; desliga o ganho de Impulso quando sobrecarregado.
- Na mesa, um marcador de estágio de perseguição (1 a 6) que o mestre controla.

### Etapa 8 — Limpeza
- Apagar `docs/sfl/*.md` (ou deixar um aviso apontando para esta pasta) e atualizar `docs/inicio-ficha.md` e `docs/testes.md`.
- Atualizar os testes t43 e t44 (ou criar novos) para a V1.2.

## Pendências conhecidas do livro (não decidir sozinho)

- O capítulo 11 ainda fala em "capturado por volta dos 25 anos", "família adotiva" e "vida normal", que contradizem a lore revisada (programa da vacina). O mestre ainda vai ajustar.
- Os valores são de teste: depois da primeira mesa, números de dano, crítico, Vida e Fôlego podem mudar. Por isso tudo fica nos JSON.
