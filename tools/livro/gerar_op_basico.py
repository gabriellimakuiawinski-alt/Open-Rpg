#!/usr/bin/env python3
"""Gera schema_etapa6_livro.sql: habilidades de classe, poderes de classe e trilhas
do Livro de Regras de Ordem Paranormal (v1.2). Textos resumidos (só a mecânica).
Uso: python3 tools/livro/gerar_op_basico.py   (na raiz do repositório)"""
import json, os

# +1d20 no livro aparece como o símbolo de dado; aqui escrevemos "1d20".
EF = lambda a, v, nv=False: ({'a': a, 'v': v, 'nv': True} if nv else {'a': a, 'v': v})
L = []   # linhas: dict(classe, grupo, trilha, nex, nome, pe, pre, desc, ef)

def add(classe, grupo, nome, desc, nex=None, trilha=None, pe=0, pre='', ef=None):
    L.append(dict(classe=classe, grupo=grupo, trilha=trilha, nex=nex, nome=nome, pe=pe, pre=pre, desc=desc, ef=ef or []))

# ---------------------------------------------------------------- CLASSE (comuns)
def comuns(c, poder, grau):
    add(c, 'classe', 'Habilidade de Trilha',
        'NEX 10%: escolha uma trilha da classe e receba o 1º poder dela. Novo poder da trilha em NEX 40%, 65% e 99%.', 10)
    add(c, 'classe', 'Poder de ' + poder,
        'NEX 15%: escolha um poder da classe. Novo poder em NEX 30% e a cada 15% seguintes (45, 60, 75, 90). Veja a lista de poderes.', 15)
    add(c, 'classe', 'Aumento de Atributo',
        'NEX 20%, 50%, 80% e 95%: +1 em um atributo à escolha (máximo 5 por esta via).', 20)
    add(c, 'classe', 'Grau de Treinamento',
        f'NEX 35% e 70%: escolha {grau} perícias treinadas e suba o grau de cada uma (treinado→veterano ou veterano→expert).', 35)
    add(c, 'classe', 'Versatilidade',
        f'NEX 50%: escolha um poder de {poder} ou o 1º poder de uma trilha de {poder} que não seja a sua.', 50)

# ---------------------------------------------------------------- COMBATENTE
add('combatente', 'classe', 'Ataque Especial',
    'Ao atacar, gaste 2 PE para +5 no teste de ataque OU no dano. Cada +5 extra custa +1 PE e você distribui entre ataque e dano. '
    'NEX 25%: 3 PE (+10). NEX 55%: 4 PE (+15). NEX 85%: 5 PE (+20).', 5, pe=2)
comuns('combatente', 'Combatente', '2 + Int')

C = 'combatente'
add(C, 'poder', 'Armamento Pesado', 'Proficiência com armas pesadas.', pre='For 2')
add(C, 'poder', 'Artista Marcial', 'Ataques desarmados causam 1d6 (letal, contam como armas ágeis). Dano sobe para 1d8 em NEX 35% e 1d10 em NEX 70%.')
add(C, 'poder', 'Ataque de Oportunidade', 'Quando um ser sai voluntariamente de um espaço adjacente ao seu, gaste reação e 1 PE para fazer um ataque corpo a corpo contra ele.', pe=1)
add(C, 'poder', 'Combater com Duas Armas', 'Empunhando duas armas (ao menos uma leve) e agredindo, faça dois ataques (um com cada). Você sofre –1d20 em todos os ataques até o próximo turno.', pre='Agi 3, treinado em Luta ou Pontaria')
add(C, 'poder', 'Combate Defensivo', 'Ao agredir, pode combater defensivamente: –1d20 nos testes de ataque até o próximo turno, mas +5 na Defesa.', pre='Int 2')
add(C, 'poder', 'Golpe Demolidor', 'Ao quebrar ou atacar um objeto, gaste 1 PE para causar 2 dados de dano extra do mesmo tipo da arma.', pe=1, pre='For 2, treinado em Luta')
add(C, 'poder', 'Golpe Pesado', 'O dano das suas armas corpo a corpo aumenta em mais um dado do mesmo tipo.')
add(C, 'poder', 'Incansável', 'Uma vez por cena, gaste 2 PE para fazer uma ação de investigação adicional, usando For ou Agi como atributo-base.', pe=2)
add(C, 'poder', 'Presteza Atlética', 'Ao facilitar a investigação, gaste 1 PE para usar For ou Agi como atributo-base. Se passar, o próximo aliado que usar seu bônus recebe +1d20 no teste.', pe=1)
add(C, 'poder', 'Proteção Pesada', 'Proficiência com proteções pesadas.', pre='NEX 30%')
add(C, 'poder', 'Reflexos Defensivos', '+2 na Defesa e nos testes de resistência.', pre='Agi 2', ef=[EF('def', 2), EF('res', 2)])
add(C, 'poder', 'Saque Rápido', 'Sacar ou guardar itens é ação livre. Com a regra de munição, uma vez por rodada recarrega arma de disparo como ação livre.', pre='Treinado em Iniciativa')
add(C, 'poder', 'Segurar o Gatilho', 'Ao acertar com arma de fogo, pode atacar de novo com a mesma arma no mesmo alvo, pagando 2 PE por cada ataque já feito no turno (2, 4, 6…), até errar ou bater o limite de PE.', pre='NEX 60%')
add(C, 'poder', 'Sentido Tático', 'Ação de movimento + 2 PE: até o fim da cena, bônus em Defesa e resistência igual ao seu Intelecto.', pe=2, pre='Int 2, treinado em Percepção e Tática')
add(C, 'poder', 'Tanque de Guerra', 'Com proteção pesada, a Defesa e a resistência a dano dela aumentam em +2.', pre='Proteção Pesada')
add(C, 'poder', 'Tiro Certeiro', 'Com arma de disparo, soma Agilidade no dano e ignora a penalidade por atacar alvo em corpo a corpo (sem precisar mirar).', pre='Treinado em Pontaria')
add(C, 'poder', 'Tiro de Cobertura', 'Ação padrão + 1 PE: dispare na direção de alguém em alcance. Pontaria contra Vontade; se vencer, até o início do seu próximo turno o alvo não sai do lugar e sofre –5 em ataques (efeito de medo; +5 no teste dele em lugar muito perigoso).', pe=1)
add(C, 'poder', 'Transcender', 'Escolha um poder paranormal. Você o recebe, mas não ganha Sanidade nesse aumento de NEX. Pode ser escolhido várias vezes.')
add(C, 'poder', 'Treinamento em Perícia', 'Escolha duas perícias e fique treinado nelas. De NEX 35% pode tornar veterano, de NEX 70% expert. Pode ser escolhido várias vezes.')

# trilhas de combatente
T = 'Aniquilador'
add(C, 'trilha', 'A Favorita', 'Escolha uma arma favorita (ex.: katana, fuzil de assalto). A categoria dela é reduzida em I.', 10, T)
add(C, 'trilha', 'Técnica Secreta', 'Categoria da favorita reduzida em II. Ao atacar com ela, gaste 2 PE para um efeito, +2 PE por efeito adicional. Amplo: atinge um alvo adicional adjacente (mesmo teste). Destruidor: +1 no multiplicador de crítico.', 40, T, pe=2)
add(C, 'trilha', 'Técnica Sublime', 'Novos efeitos da Técnica Secreta. Letal: +2 na margem de ameaça (duas vezes = +5). Perfurante: ignora até 5 de resistência a dano do alvo.', 65, T)
add(C, 'trilha', 'Máquina de Matar', 'Categoria da favorita reduzida em III, +2 na margem de ameaça e +1 dado de dano do mesmo tipo.', 99, T)
T = 'Comandante de Campo'
add(C, 'trilha', 'Inspirar Confiança', 'Reação + 2 PE: um aliado em alcance curto rola novamente um teste que acabou de fazer.', 10, T, pe=2)
add(C, 'trilha', 'Estrategista', 'Ação padrão + 1 PE por aliado (até seu Intelecto) em alcance curto: no próximo turno deles, ganham uma ação de movimento adicional.', 40, T, pe=1)
add(C, 'trilha', 'Brecha na Guarda', 'Uma vez por rodada, quando um aliado causa dano a inimigo em alcance curto seu, gaste reação + 2 PE: você ou outro aliado em alcance curto faz um ataque adicional contra o inimigo. Inspirar Confiança e Estrategista passam a alcance médio.', 65, T, pe=2)
add(C, 'trilha', 'Oficial Comandante', 'Ação padrão + 5 PE: cada aliado que você vê em alcance médio recebe uma ação padrão adicional no próximo turno dele.', 99, T, pe=5)
T = 'Guerreiro'
add(C, 'trilha', 'Técnica Letal', '+2 na margem de ameaça com todos os ataques corpo a corpo.', 10, T)
add(C, 'trilha', 'Revidar', 'Ao bloquear um ataque, gaste reação + 2 PE para fazer um ataque corpo a corpo no inimigo que atacou.', 40, T, pe=2)
add(C, 'trilha', 'Força Opressora', 'Ao acertar corpo a corpo, gaste 1 PE para fazer derrubar ou empurrar como ação livre (empurrar: +5 para cada 10 de dano causado). Se derrubar e vencer o teste oposto, gaste 1 PE para um ataque adicional no alvo caído.', 65, T, pe=1)
add(C, 'trilha', 'Potência Máxima', 'No Ataque Especial com arma corpo a corpo, todos os bônus numéricos são dobrados.', 99, T)
T = 'Operações Especiais'
add(C, 'trilha', 'Iniciativa Aprimorada', '+5 em Iniciativa e uma ação de movimento adicional na primeira rodada.', 10, T, ef=[EF('per:Iniciativa', 5)])
add(C, 'trilha', 'Ataque Extra', 'Uma vez por rodada, ao atacar, gaste 2 PE para fazer um ataque adicional.', 40, T, pe=2)
add(C, 'trilha', 'Surto de Adrenalina', 'Uma vez por rodada, gaste 5 PE para uma ação padrão ou de movimento adicional.', 65, T, pe=5)
add(C, 'trilha', 'Sempre Alerta', 'Uma ação padrão adicional no início de cada cena de combate.', 99, T)
T = 'Tropa de Choque'
add(C, 'trilha', 'Casca Grossa', '+1 PV para cada 5% de NEX e, ao bloquear, soma seu Vigor na resistência a dano recebida.', 10, T, ef=[EF('pv', 1, True)])
add(C, 'trilha', 'Cai Dentro', 'Quando um oponente em alcance curto ataca um aliado, gaste reação + 1 PE: ele faz Vontade (DT Vig) ou deve atacar você. Quem passa fica imune até o fim da cena. Precisa poder ser alvo do ataque.', 40, T, pe=1)
add(C, 'trilha', 'Duro de Matar', 'Ao sofrer dano não paranormal, gaste reação + 2 PE para reduzi-lo à metade. Em NEX 85% também vale contra dano paranormal.', 65, T, pe=2)
add(C, 'trilha', 'Inquebrável', 'Machucado: +5 na Defesa e resistência a dano 5. Morrendo: não fica indefeso e ainda pode agir (segue as regras de morte).', 99, T)

# ---------------------------------------------------------------- ESPECIALISTA
E = 'especialista'
add(E, 'classe', 'Eclético', 'Ao fazer teste de perícia, gaste 2 PE para ter os benefícios de ser treinado nela.', 5, pe=2)
add(E, 'classe', 'Perito', 'Escolha duas perícias treinadas (menos Luta e Pontaria). Nelas, gaste 2 PE para somar +1d6 ao teste. Cada +1 PE sobe o dado: NEX 25%: 3 PE (+1d8); NEX 55%: 4 PE (+1d10); NEX 85%: 5 PE (+1d12).', 5, pe=2)
add(E, 'classe', 'Engenhosidade', 'Ao usar Eclético, NEX 40%: gaste +2 PE para ter os benefícios de veterano. NEX 75%: gaste +4 PE para os de expert.', 40)
comuns(E, 'Especialista', '5 + Int')

add(E, 'poder', 'Artista Marcial', 'Ataques desarmados causam 1d6 (letal, contam como armas ágeis). Dano sobe para 1d8 em NEX 35% e 1d10 em NEX 70%.')
add(E, 'poder', 'Balística Avançada', 'Proficiência com armas táticas de fogo e +2 no dano com armas de fogo.')
add(E, 'poder', 'Conhecimento Aplicado', 'Ao fazer teste de perícia (menos Luta e Pontaria), gaste 2 PE para trocar o atributo-base por Int.', pe=2, pre='Int 2')
add(E, 'poder', 'Hacker', '+5 em Tecnologia para invadir sistemas, e hackear qualquer sistema leva uma ação completa.', pre='Treinado em Tecnologia')
add(E, 'poder', 'Mãos Rápidas', 'Ao fazer teste de Crime, pague 1 PE para fazê-lo como ação livre.', pe=1, pre='Agi 3, treinado em Crime')
add(E, 'poder', 'Mochila de Utilidades', 'Um item à sua escolha (menos armas) conta como uma categoria abaixo e ocupa 1 espaço a menos.')
add(E, 'poder', 'Movimento Tático', 'Gaste 1 PE para ignorar a penalidade de deslocamento por terreno difícil e por escalar até o fim do turno.', pe=1, pre='Treinado em Atletismo')
add(E, 'poder', 'Na Trilha Certa', 'Ao passar em teste para procurar pistas, gaste 1 PE para +1d20 no próximo teste. Custos e bônus acumulam (2º sucesso: 2 PE, +2d20…).', pe=1)
add(E, 'poder', 'Nerd', 'Uma vez por cena, gaste 2 PE e faça Atualidades (DT 20). Se passar, recebe uma informação útil (pista, fraqueza de inimigo etc.).', pe=2)
add(E, 'poder', 'Ninja Urbano', 'Proficiência com armas táticas corpo a corpo e de disparo (exceto de fogo) e +2 no dano com armas corpo a corpo e de disparo.')
add(E, 'poder', 'Pensamento Ágil', 'Uma vez por rodada, em cena de investigação, gaste 2 PE para uma ação de procurar pistas adicional.', pe=2)
add(E, 'poder', 'Perito em Explosivos', 'Soma seu Intelecto na DT para resistir aos seus explosivos e exclui da explosão alvos igual ao seu Intelecto.')
add(E, 'poder', 'Primeira Impressão', '+2d20 no primeiro teste de Diplomacia, Enganação, Intimidação ou Intuição em cada cena.')
add(E, 'poder', 'Transcender', 'Escolha um poder paranormal. Você o recebe, mas não ganha Sanidade nesse aumento de NEX. Pode ser escolhido várias vezes.')
add(E, 'poder', 'Treinamento em Perícia', 'Escolha duas perícias e fique treinado nelas. De NEX 35% pode tornar veterano, de NEX 70% expert. Pode ser escolhido várias vezes.')

T = 'Atirador de Elite'
add(E, 'trilha', 'Mira de Elite', 'Proficiência com armas de fogo de balas longas e soma seu Intelecto no dano com elas.', 10, T)
add(E, 'trilha', 'Disparo Letal', 'Ao mirar, gaste 1 PE: +2 na margem de ameaça do próximo ataque até o fim do seu próximo turno.', 40, T, pe=1)
add(E, 'trilha', 'Disparo Impactante', 'Com arma de fogo de calibre grosso, gaste 2 PE para fazer derrubar, desarmar, empurrar ou quebrar com ataque à distância.', 65, T, pe=2)
add(E, 'trilha', 'Atirar para Matar', 'Em acerto crítico com arma de fogo, causa dano máximo sem rolar os dados.', 99, T)
T = 'Infiltrador'
add(E, 'trilha', 'Ataque Furtivo', 'Uma vez por rodada, ao atingir alvo desprevenido (corpo a corpo ou alcance curto) ou que você flanqueia, gaste 1 PE para +1d6 de dano do mesmo tipo. Sobe para +2d6 (NEX 40%), +3d6 (65%) e +4d6 (99%).', 10, T, pe=1)
add(E, 'trilha', 'Gatuno', '+5 em Atletismo e Crime e anda o deslocamento normal ao se esconder sem penalidade.', 40, T, ef=[EF('per:Atletismo', 5), EF('per:Crime', 5)])
add(E, 'trilha', 'Assassinar', 'Ação de movimento + 3 PE: analisa alvo em alcance curto. Até o fim do próximo turno, seu primeiro Ataque Furtivo nele tem os dados extras dobrados e, se causar dano, ele fica inconsciente ou morrendo à sua escolha (Fortitude DT Agi evita).', 65, T, pe=3)
add(E, 'trilha', 'Sombra Fugaz', 'Em Furtividade logo após atacar ou fazer ação chamativa, gaste 3 PE para não sofrer a penalidade de –3d20.', 99, T, pe=3)
T = 'Médico de Campo'
P = 'Precisa ser treinado em Medicina para escolher a trilha e ter um kit de medicina para usar as habilidades.'
add(E, 'trilha', 'Paramédico', 'Ação padrão + 2 PE: cura 2d10 PV de si ou de aliado adjacente. +1d10 em NEX 40%, 65% e 99%, gastando +1 PE por dado. ' + P, 10, T, pe=2)
add(E, 'trilha', 'Equipe de Trauma', 'Ação padrão + 2 PE: remove uma condição negativa (menos morrendo) de aliado adjacente.', 40, T, pe=2)
add(E, 'trilha', 'Resgate', 'Uma vez por rodada, ao ver aliado machucado ou morrendo em alcance curto, aproxime-se dele com ação livre. Ao curar PV ou remover condições, você e o aliado ganham +5 na Defesa até seu próximo turno. Carregar um personagem ocupa metade dos espaços.', 65, T)
add(E, 'trilha', 'Reanimação', 'Uma vez por cena, ação completa + 10 PE: traz de volta à vida personagem que morreu na mesma cena (exceto por dano massivo).', 99, T, pe=10)
T = 'Negociador'
add(E, 'trilha', 'Eloquência', 'Ação completa + 1 PE por alvo em alcance curto: teste de Diplomacia, Enganação ou Intimidação contra a Vontade deles. Se vencer, ficam fascinados enquanto você se concentrar (ação padrão por rodada). Alvo hostil ou em combate: +5 no teste e novo teste a cada rodada. Quem passa fica imune por um dia.', 10, T, pe=1)
add(E, 'trilha', 'Discurso Motivador', 'Ação padrão + 4 PE: você e aliados em alcance curto ganham +1d20 nos testes de perícia até o fim da cena. Em NEX 65%, 8 PE dão +2d20.', 40, T, pe=4)
add(E, 'trilha', 'Eu Conheço um Cara', 'Uma vez por missão, ative sua rede de contatos para um favor (trocar o equipamento do grupo, local de descanso, ser resgatado de uma cena). O mestre decide quando e quais favores.', 65, T)
add(E, 'trilha', 'Truque de Mestre', 'Gaste 5 PE para simular qualquer habilidade que um aliado usou na cena. Ignora pré-requisitos, mas paga todos os custos (ações, PE, materiais) e usa os seus parâmetros.', 99, T, pe=5)
T = 'Técnico'
add(E, 'trilha', 'Inventário Otimizado', 'Soma seu Intelecto à Força para a capacidade de carga.', 10, T)
add(E, 'trilha', 'Remendão', 'Ação completa + 1 PE: remove a condição quebrado de equipamento adjacente até o fim da cena. Equipamento geral tem a categoria reduzida em I para você.', 40, T, pe=1)
add(E, 'trilha', 'Improvisar', 'Ação completa + 2 PE (mais 2 PE por categoria do item): cria versão funcional de um equipamento geral, que fica inútil ao fim da cena.', 65, T, pe=2)
add(E, 'trilha', 'Preparado para Tudo', 'Ação de movimento + 3 PE por categoria: encontra na bolsa qualquer item (exceto armas).', 99, T, pe=3)

# ---------------------------------------------------------------- OCULTISTA
O = 'ocultista'
add(O, 'classe', 'Escolhido pelo Outro Lado', 'Lança rituais de 1º círculo; 2º círculo em NEX 25%, 3º em 55% e 4º em 85%. Começa com 3 rituais de 1º círculo e aprende 1 ritual de círculo que possa lançar a cada avanço de NEX (não contam no limite de rituais conhecidos).', 5)
comuns(O, 'Ocultista', '3 + Int')
add(O, 'classe', 'Envolto em Mistério', '+5 em Enganação e Intimidação contra pessoas não treinadas em Ocultismo (o mestre define quem se encaixa).', 25)
add(O, 'classe', 'Especialista em Elemento', 'Escolha um elemento: a DT para resistir aos seus rituais desse elemento aumenta em +2.', 55)
add(O, 'classe', 'Ferramentas Paranormais', 'Reduz em I a categoria de um item paranormal e ativa itens paranormais sem pagar o custo em PE.', 70)

add(O, 'poder', 'Camuflar Ocultismo', 'Ação livre: esconde símbolos e sigilos (em objetos ou na pele), visíveis só para você. Ao lançar ritual, gaste +2 PE para lançá-lo sem componentes e sem gesticular. Outros só percebem com Ocultismo (DT 25).')
add(O, 'poder', 'Criar Selo', 'Fabrica selos paranormais de rituais que conhece: uma ação de interlúdio e PE igual ao custo do ritual. Máximo de selos ao mesmo tempo igual à sua Presença.')
add(O, 'poder', 'Fluxo de Poder', 'Mantém dois efeitos sustentados de rituais ao mesmo tempo com uma ação livre, pagando o custo de cada um.', pre='NEX 60%')
add(O, 'poder', 'Guiado pelo Paranormal', 'Uma vez por cena, gaste 2 PE para uma ação de investigação adicional.', pe=2)
add(O, 'poder', 'Identificação Paranormal', '+10 em Ocultismo para identificar criaturas, objetos ou rituais.')
add(O, 'poder', 'Improvisar Componentes', 'Uma vez por cena, ação completa + Investigação (DT 15): encontra objetos que servem de componentes ritualísticos de um elemento à escolha (o mestre define se cabe na cena).')
add(O, 'poder', 'Intuição Paranormal', 'Ao facilitar a investigação, soma seu Intelecto ou Presença (à escolha) no teste.')
add(O, 'poder', 'Mestre em Elemento', 'Escolha um elemento: o custo de lançar rituais dele diminui em 1 PE.', pre='Especialista em Elemento no mesmo elemento, NEX 45%')
add(O, 'poder', 'Ritual Potente', 'Soma seu Intelecto nas rolagens de dano ou nos efeitos de cura dos seus rituais.', pre='Int 2')
add(O, 'poder', 'Ritual Predileto', 'Escolha um ritual que conhece: o custo dele diminui em 1 PE (acumula com outras reduções).')
add(O, 'poder', 'Tatuagem Ritualística', 'Rituais de alcance pessoal que têm você como alvo custam 1 PE a menos.')
add(O, 'poder', 'Transcender', 'Escolha um poder paranormal. Você o recebe, mas não ganha Sanidade nesse aumento de NEX. Pode ser escolhido várias vezes.')
add(O, 'poder', 'Treinamento em Perícia', 'Escolha duas perícias e fique treinado nelas. De NEX 35% pode tornar veterano, de NEX 70% expert. Pode ser escolhido várias vezes.')

T = 'Conduíte'
add(O, 'trilha', 'Ampliar Ritual', 'Ao lançar ritual, gaste +2 PE para aumentar o alcance em um passo (curto→médio→longo→extremo) ou dobrar a área.', 10, T, pe=2)
add(O, 'trilha', 'Acelerar Ritual', 'Uma vez por rodada, some 4 PE ao custo de um ritual para lançá-lo como ação livre.', 40, T, pe=4)
add(O, 'trilha', 'Anular Ritual', 'Ao ser alvo de um ritual, gaste PE igual ao custo pago por ele e faça teste oposto de Ocultismo contra o conjurador. Se vencer, o ritual é anulado.', 65, T)
add(O, 'trilha', 'Canalizar o Medo', 'Você aprende o ritual Canalizar o Medo.', 99, T)
T = 'Flagelador'
add(O, 'trilha', 'Poder do Flagelo', 'Ao lançar ritual, pode pagar o custo em PE com seus PV, à taxa de 2 PV por PE. Os PV gastos só voltam com descanso.', 10, T)
add(O, 'trilha', 'Abraçar a Dor', 'Ao sofrer dano não paranormal, gaste reação + 2 PE para reduzi-lo à metade.', 40, T, pe=2)
add(O, 'trilha', 'Absorver Agonia', 'Ao reduzir um ou mais inimigos a 0 PV com ritual, recebe PE temporários igual ao círculo do ritual.', 65, T)
add(O, 'trilha', 'Medo Tangível', 'Você aprende o ritual Medo Tangível.', 99, T)
T = 'Graduado'
add(O, 'trilha', 'Saber Ampliado', 'Aprende um ritual de 1º círculo e, a cada novo círculo, mais um ritual daquele círculo (não contam no limite).', 10, T)
add(O, 'trilha', 'Grimório Ritualístico', 'Cria um grimório com rituais de 1º ou 2º círculo em quantidade igual ao seu Intelecto (e um novo a cada círculo que ganhar acesso). Para lançá-los, empunhe o grimório e gaste uma ação completa folheando. Ocupa 1 espaço; se perdido, replica com 2 ações de interlúdio.', 40, T)
add(O, 'trilha', 'Rituais Eficientes', 'A DT para resistir a todos os seus rituais aumenta em +5.', 65, T)
add(O, 'trilha', 'Conhecendo o Medo', 'Você aprende o ritual Conhecendo o Medo.', 99, T)
T = 'Intuitivo'
add(O, 'trilha', 'Mente Sã', 'Resistência paranormal +5 (+5 em testes de resistência contra efeitos paranormais).', 10, T)
add(O, 'trilha', 'Presença Poderosa', 'Soma sua Presença ao limite de PE por turno, só para conjurar rituais (não para DT).', 40, T)
add(O, 'trilha', 'Inabalável', 'Resistência a dano mental e paranormal 10. Em efeito paranormal com Vontade para reduzir dano à metade, se passar não sofre dano algum.', 65, T)
add(O, 'trilha', 'Presença do Medo', 'Você aprende o ritual Presença do Medo.', 99, T)
T = 'Lâmina Paranormal'
add(O, 'trilha', 'Lâmina Maldita', 'Aprende o ritual Amaldiçoar Arma (ou, se já o conhece, o custo cai 1 PE). Ao lançá-lo, pode usar Ocultismo no lugar de Luta ou Pontaria nos ataques com a arma.', 10, T)
add(O, 'trilha', 'Gladiador Paranormal', 'Ao acertar ataque corpo a corpo, recebe 2 PE temporários, até o limite de PE por cena igual ao seu limite de PE. Somem no fim da cena.', 40, T)
add(O, 'trilha', 'Conjuração Marcial', 'Uma vez por rodada, ao lançar ritual de ação padrão, gaste 2 PE para fazer um ataque corpo a corpo como ação livre.', 65, T, pe=2)
add(O, 'trilha', 'Lâmina do Medo', 'Você aprende o ritual Lâmina do Medo.', 99, T)

# ---------------------------------------------------------------- SQL
def q(s): return "'" + str(s).replace("'", "''") + "'"
def ref(r): return 'op:%s:%s:%s%s' % (r['classe'], r['grupo'], (r['trilha'] + ':') if r['trilha'] else '', r['nome'])
TIPO = {'classe': 'classe', 'poder': 'poder', 'trilha': 'trilha'}
rows = []
seen = set()
for i, r in enumerate(L):
    k = ref(r)
    assert k not in seen, k
    seen.add(k)
    dados = {'tipo': TIPO[r['grupo']], 'desc': r['desc'] + (' Pré-requisito: ' + r['pre'] + '.' if r['pre'] else ''), 'pe': r['pe'], 'ef': r['ef']}
    rows.append('(%s,%s,%s,%s,%s,%s,%s,%s)' % (q(k), q(r['classe']), q(r['grupo']), q(r['trilha']) if r['trilha'] else 'null',
                r['nex'] if r['nex'] is not None else 'null', i + 1, q(r['nome']), q(json.dumps(dados, ensure_ascii=False)) + '::jsonb'))

SQL = """-- Etapa 6 — Habilidades do livro (Ordem Paranormal, Livro de Regras v1.2)
-- Catálogo GLOBAL e somente leitura: habilidades de classe, poderes de classe e trilhas.
-- Re-executável. Gerado por tools/livro/gerar_op_basico.py (não edite as linhas à mão).
-- Rode DEPOIS do schema_etapa5.sql. Outros livros/rituais entram na mesma tabela (coluna "fonte").

create table if not exists public.livro_habilidades (
  ref text primary key,                                   -- ex.: op:combatente:trilha:Guerreiro:Revidar
  sistema text not null default 'op',
  fonte text not null default 'livro-basico',
  classe text not null,                                   -- combatente | especialista | ocultista
  grupo text not null check (grupo in ('classe', 'poder', 'trilha')),
  trilha text,                                            -- nome da trilha (grupo = trilha)
  nex int,                                                -- NEX em que a habilidade é recebida (null = escolha livre)
  ordem int not null default 0,
  nome text not null,
  dados jsonb not null default '{}'::jsonb                -- já no formato de poder da ficha: tipo, desc, pe, ef[]
);
create index if not exists livro_habilidades_busca_idx on public.livro_habilidades(sistema, classe, grupo);

alter table public.livro_habilidades enable row level security;
drop policy if exists livro_habilidades_ler on public.livro_habilidades;
create policy livro_habilidades_ler on public.livro_habilidades for select to authenticated using (true);
-- sem policy de escrita: só quem roda SQL no painel (dono do projeto) altera o catálogo
revoke all on public.livro_habilidades from anon, authenticated;
grant select on public.livro_habilidades to authenticated;

insert into public.livro_habilidades(ref, classe, grupo, trilha, nex, ordem, nome, dados) values
""" + ',\n'.join(rows) + """
on conflict (ref) do update set classe = excluded.classe, grupo = excluded.grupo, trilha = excluded.trilha,
  nex = excluded.nex, ordem = excluded.ordem, nome = excluded.nome, dados = excluded.dados;
"""

raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
with open(os.path.join(raiz, 'schema_etapa6_livro.sql'), 'w', encoding='utf-8') as fh:
    fh.write(SQL)
c = {}
for r in L: c[(r['classe'], r['grupo'])] = c.get((r['classe'], r['grupo']), 0) + 1
print(len(L), 'linhas', c)
