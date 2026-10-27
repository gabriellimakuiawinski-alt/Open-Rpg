#!/usr/bin/env python3
"""Gera schema_etapa9d_enigmas.sql: acrescenta aos monstros do bestiário o 'Enigma de Medo' (17 criaturas) e as habilidades
da Degolificada que faltavam. Textos em redação própria (resumo do livro, p.186-283). Re-executável: só acrescenta se a habilidade ainda não existir."""
import json
P = 'Passiva'
ENIGMAS = {
 'Aniquilação': 'O Enigma de Medo dela é desconhecido. Quando for resolvido, a Aniquilação perde a resistência a dano e a habilidade Tempestade de Espinhos.',
 'Dama de Sangue': 'É invocada por um ritual que sacrifica sete pessoas para desabrochar sete flores. Cada flor tem uma fraqueza, descrita nas habilidades da criatura.',
 'Mulher Afogada': 'Atacá-la de frente é inútil: ela se move pelos encanamentos e se recupera dos ferimentos. Só se vence bloqueando todas as saídas de água e fechando o registro hidráulico do local; depois, abrir todas as torneiras força a manifestação física, sem lugar para fugir.',
 'O Diabo': 'Ninguém sabe como derrotá-lo; a pista é que a Morte é a entidade opressora do Sangue (talvez uma manifestação de Morte de força equivalente seja a chave). Resolvido o enigma, ele perde a imunidade a dano e seus bônus de testes de resistência caem para +25.',
 'Aracnasita': 'O Lodo da Morte em seu corpo a protege, mas foge do fogo e do calor. Se sofrer dano de fogo, a aracnasita perde a imunidade a dano até o início do próximo turno dela.',
 'Escutado': 'Tocar a melodia dele exige ação padrão e teste de Artes DT 25 por rodada, ou ligar um aparelho com a música. Enquanto ela toca, o escutado se multiplica (até 16 criaturas em 4 rodadas se nenhuma cópia for destruída). Se ouvir a melodia por 4 rodadas seguidas, perde a imunidade a dano até o fim da cena.',
 'Nidere': 'É preciso achar o covil (cavernas nas profundezas da floresta) e entender a lógica dos ossos das vítimas pendurados ali, que formam a origem da criatura. Dentro do covil ele é ainda mais mortal. Quando a origem é destruída, ele entra em fúria: -10 na Defesa, penalidade nos testes de resistência e perde Regeneração Acelerada e Senso de Direção Perfeito, ficando vulnerável a armadilhas.',
 'Anjo': 'Anjos podem ser enganados pelo alinhamento de Justiça Perfeita: um anjo que falhe em julgar corretamente pode cair. Resolvido o enigma, ele perde a resistência a dano, o deslocamento de voo e a habilidade Julgamento.',
 'Espreitador': 'Às 2h11, se achar o ambiente seguro, ele sai do esconderijo para espreitar de perto (o alvo deve fingir dormir no escuro). Se a porta do esconderijo de onde saiu for fechada antes de ele voltar, fica encurralado e perde a imunidade a dano.',
 'Estrangeiro': 'É preciso decifrar as intenções dele, investigando os sinais e aprendendo sua linguagem. Decifrado, perde a imunidade a dano (mas continua imune a dano de Conhecimento) e não pode usar Incubar.',
 'Parasita de Culpa': 'Os personagens precisam perceber que vivem um sonho compartilhado e descobrir qual deles é o hospedeiro. O hospedeiro deve confrontar e derrotar as manifestações dentro do sonho, sozinho. No sonho, tudo menos os personagens é construto de Conhecimento; o mestre decide como eles descobrem e o que enfrentam.',
 'Anomalia': 'É preciso mergulhar na anomalia para entendê-la no Outro Lado. Resolvido o enigma, ela vira um ser ou objeto aleatório por 2d4 rodadas, perdendo a imunidade a dano e a condições e usando as estatísticas do novo ser (menos os PV).',
 'Ciborgue': 'Ele muda de estado de combate com frequência, e cada estado tem uma fraqueza (por exemplo, sofrer 15 de dano de um tipo num só ataque, ou ser exposto a certo material). A fraqueza só se resolve no estado correspondente, e ele não pode mais assumir esse estado. Sem nenhum estado, desativa: Defesa 10 e deslocamento 0m.',
 'Telopsia': 'Só morre de vez se a fita amaldiçoada que o manifesta for destruída (achar a fita exige investigar as vítimas, que não lembram o que fizeram com ela). Fita destruída, os PV dele vão a 0. Sem isso, mesmo derrotado em combate, ele volta.',
 'Viajante': 'Só aparece em dispositivos de captura de imagem: fotografá-lo, sem que ele esteja viajando pela imagem, o distrai e o deixa visível por alguns segundos. Resolvido o enigma, perde a habilidade Invisibilidade.',
 'Anfitrião': 'Só dá para enfrentá-lo de forma justa sob a proteção soberana do Equilíbrio, que apenas a Máscara do Desespero pode oferecer.',
 'Degolificada': 'Ela precisa ser confrontada com a causa da própria morte, sem poder escapar do confronto. Confrontada assim, perde a imunidade a dano.',
}
EXTRA = {'Degolificada': [
 ('Agarrar e Estrangular', 'Livre', 'Se acertar um ataque de pancada em personagem Médio ou menor, pode tentar agarrá-lo (teste 5O+35). Agarrado, o personagem também fica asfixiado. Pode manter até duas criaturas agarradas por vez.'),
 ('Grito Rasgado', 'Livre', 'Uma vez por cena, ela emite um grito ensurdecedor: cada personagem em alcance médio sofre 4d10+10 de dano mental e um efeito sorteado em 1d4 (Vontade DT 35 reduz o dano à metade e evita o efeito): 1 surdo dos dois ouvidos para sempre; 2 surdo de um ouvido para sempre; 3 surdo dos dois ouvidos até o fim da cena; 4 surdo de um ouvido até o fim da cena.'),
 ('Desfiguramento Capilar', 'Movimento', 'Usa os cabelos e os olhos vazios contra quem está agarrado: cada personagem agarrado sofre 10d6+20 de perfuração (Fortitude DT 35 reduz à metade) e 6d10 de dano mental (Vontade DT 35 reduz à metade).'),
 ('Metamorfose da Degolificada', 'Passiva', 'Ela pode assumir uma forma ligada a um elemento. ENERGIA: se enlouquecer um alvo, vira conturbada (atravessa paredes, ignora cobertura, seus ataques causam dano de Energia, resistência a Energia 20). CONHECIMENTO: se receber a resposta errada ao enigma, vira gnóstica; no fim de cada turno dela, o alvo visível mais próximo tem uma alucinação e sofre 4d6 de dano mental e fica atordoado até o fim do próximo turno (Vontade DT 35 reduz à metade e evita a condição). SANGUE: se matar um alvo e o mantiver agarrado até o próximo turno, vira devoradora (ataque extra de mordida 5O+35, 10d10+20 de Sangue; resistência a Sangue 20). MORTE: após 3 erros seguidos de ataque contra ela, vira decrépita (deslocamento 12m, resistência a Morte 20, os cabelos viram Lodo que agarra: ação de movimento para agarrar criatura em alcance curto, Reflexos DT 35 evita).')]}
def q(s): return s.replace("'", "''")
def upd(nome, n, acao, desc):
    j = json.dumps([{'n': n, 'acao': acao, 'desc': desc}], ensure_ascii=False)
    return (f"update public.livro_inimigos set dados = jsonb_set(dados, '{{habilidades}}', coalesce(dados->'habilidades', '[]'::jsonb) || '{q(j)}'::jsonb) "
            f"where nome = '{q(nome)}' and not exists (select 1 from jsonb_array_elements(coalesce(dados->'habilidades', '[]'::jsonb)) h where h->>'n' = '{q(n)}');")
out = ['-- Etapa 9d — Enigma de Medo (17 criaturas), habilidades que faltavam da Degolificada e correção de 5 ataques e 4 habilidades repetidas (Livro de Regras v1.2).',
       '-- Re-executável: só acrescenta a habilidade se ela ainda não existir. Rode DEPOIS de schema_etapa9c_ameacas.sql.',
       '-- Gerado por tools/livro/gerar_op_enigmas.py (não edite as linhas à mão).', '']
for nome, t in ENIGMAS.items(): out.append(upd(nome, 'Enigma de Medo', P, t))
for nome, L in EXTRA.items():
    for n, a, d in L: out.append(upd(nome, n, a, d))
ATQ = [('Perturbado de Energia', 'Toque Plasmático', 'Corpo a corpo x2', '2d12 Energia', 10),
       ('Sukkalgir', 'Mordida do Outro Lado', 'Corpo a corpo x2', '2d12 mental', 15),
       ('Enraizado', 'Punho Espinhento', 'Corpo a corpo x2', '2d8+8 impacto mais 2d12 Morte', 15),
       ('Escutado', 'Cabeça Arremessada', 'Distância x2 CURTO', '1d10+10 impacto', 15),
       ('Succ', 'Mordida', 'Corpo a corpo', '2d8+2 perfuração', 10)]
for nome, n, alc, dano, teste in ATQ:
    j = json.dumps({'alc': alc, 'dano': dano, 'teste': teste}, ensure_ascii=False)
    out.append(f"update public.livro_inimigos set dados = jsonb_set(dados, '{{ataques}}', (select jsonb_agg(case when a->>'n' = '{q(n)}' then a || '{q(j)}'::jsonb else a end) from jsonb_array_elements(dados->'ataques') a)) where nome = '{q(nome)}';")
# habilidades que eram só cópias de ataques (nome do ataque ou título 'Agredir (...)')
DUP = [('Perturbado de Energia', 'Toque Plasmático'), ('Sukkalgir', 'Mordida do Outro Lado'), ('Escutado', 'Cabeça Arremessada')]
for nome, n in DUP:
    out.append(f"update public.livro_inimigos set dados = jsonb_set(dados, '{{habilidades}}', (select coalesce(jsonb_agg(h), '[]'::jsonb) from jsonb_array_elements(dados->'habilidades') h where h->>'n' <> '{q(n)}')) where nome = '{q(nome)}';")
for nome in ('Anfitrião', 'Ciborgue'):
    out.append(f"update public.livro_inimigos set dados = jsonb_set(dados, '{{habilidades}}', (select coalesce(jsonb_agg(h), '[]'::jsonb) from jsonb_array_elements(dados->'habilidades') h where h->>'n' not like 'Agredir (%')) where nome = '{q(nome)}';")
open('schema_etapa9d_enigmas.sql', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(len(out) - 4, 'comandos')
