#!/usr/bin/env python3
"""Gera schema_etapa6c_origens.sql: 26 origens e 22 poderes paranormais do Livro de Regras de Ordem Paranormal (v1.2).
Textos resumidos (só a mecânica). Efeito automático (ef) só onde a ficha consegue aplicar.
Uso: python3 tools/livro/gerar_op_origens.py   (na raiz do repositório)"""
import json, os

# (nome, [perícias treinadas], poder, descrição do poder, ef)
O = []
def o(nome, per, poder, desc, ef=None): O.append((nome, per, poder, desc, ef or []))

o('Acadêmico', ['Ciências', 'Investigação'], 'Saber é Poder', 'Ao fazer um teste usando Intelecto, pode gastar 2 PE para receber +5 nesse teste.')
o('Agente de Saúde', ['Intuição', 'Medicina'], 'Técnica Medicinal', 'Sempre que cura um personagem, soma seu Intelecto ao total de PV curados.')
o('Amnésico', [], 'Vislumbres do Passado', 'Uma vez por sessão, faz um teste de Intelecto (DT 10) para reconhecer pessoas ou lugares familiares de antes da amnésia. Se passar, recebe 1d4 PE temporários e, a critério do mestre, uma informação útil. Perícias treinadas: duas à escolha do mestre.')
o('Artista', ['Artes', 'Enganação'], 'Magnum Opus', 'Uma vez por missão, pode determinar que um personagem envolvido em uma cena de interação o reconheça: +5 em testes de Presença e de perícias baseadas em Presença contra ele. O mestre pode dar o bônus em outras situações em que seria reconhecido.')
o('Atleta', ['Acrobacia', 'Atletismo'], '110%', 'Ao fazer um teste de perícia com Força ou Agilidade (exceto Luta e Pontaria), pode gastar 2 PE para receber +5 nesse teste.')
o('Chef', ['Fortitude', 'Profissão'], 'Ingrediente Secreto', 'Em cenas de interlúdio, pode fazer a ação alimentar-se para cozinhar um prato especial: você e quem fez a ação recebem o benefício de dois pratos (se o mesmo benefício for escolhido duas vezes, os efeitos se acumulam). Profissão treinada é Profissão (cozinheiro).')
o('Criminoso', ['Crime', 'Furtividade'], 'O Crime Compensa', 'No final de uma missão, escolha um item encontrado nela. Na próxima missão, pode incluí-lo no inventário sem que conte no limite de itens por patente.')
o('Cultista Arrependido', ['Ocultismo', 'Religião'], 'Traços do Outro Lado', 'Você possui um poder paranormal à sua escolha (aba Paranormal). Porém, começa o jogo com metade da Sanidade normal para sua classe.')
o('Desgarrado', ['Fortitude', 'Sobrevivência'], 'Calejado', '+1 PV para cada 5% de NEX.', [{'a': 'pv', 'v': 1, 'nv': 1}])
o('Engenheiro', ['Profissão', 'Tecnologia'], 'Ferramenta Favorita', 'Um item à sua escolha (exceto armas) conta como uma categoria abaixo (item de categoria II conta como categoria I para você).')
o('Executivo', ['Diplomacia', 'Profissão'], 'Processo Otimizado', 'Ao fazer um teste de perícia durante um teste estendido, ou uma ação para revisar documentos (físicos ou digitais), pode pagar 2 PE para receber +5 nesse teste.')
o('Investigador', ['Investigação', 'Percepção'], 'Faro para Pistas', 'Uma vez por cena, ao fazer um teste para procurar pistas, pode gastar 1 PE para receber +5 nesse teste.')
o('Lutador', ['Luta', 'Reflexos'], 'Mão Pesada', '+2 em rolagens de dano com ataques corpo a corpo.')
o('Magnata', ['Diplomacia', 'Pilotagem'], 'Patrocinador da Ordem', 'Seu limite de crédito é sempre considerado um acima do atual.')
o('Mercenário', ['Iniciativa', 'Intimidação'], 'Posição de Combate', 'No primeiro turno de cada cena de ação, pode gastar 2 PE para receber uma ação de movimento adicional.')
o('Militar', ['Pontaria', 'Tática'], 'Para Bellum', '+2 em rolagens de dano com armas de fogo.')
o('Operário', ['Fortitude', 'Profissão'], 'Ferramenta de Trabalho', 'Escolha uma arma simples ou tática que, a critério do mestre, poderia ser usada como ferramenta da sua profissão (como uma marreta para um pedreiro). Você sabe usá-la e recebe +1 em testes de ataque, rolagens de dano e margem de ameaça com ela.')
o('Policial', ['Percepção', 'Pontaria'], 'Patrulha', '+2 em Defesa.', [{'a': 'def', 'v': 2}])
o('Religioso', ['Religião', 'Vontade'], 'Acalentar', '+5 em testes de Religião para acalmar. Além disso, quando acalma uma pessoa, ela recebe 1d6 + sua Presença pontos de Sanidade.')
o('Servidor Público', ['Intuição', 'Vontade'], 'Espírito Cívico', 'Sempre que faz um teste para ajudar, pode gastar 1 PE para aumentar o bônus concedido em +2.')
o('Teórico da Conspiração', ['Investigação', 'Ocultismo'], 'Eu Já Sabia', 'Você não se abala tanto com entidades ou anomalias: resistência a dano mental igual ao seu Intelecto.')
o('T.I.', ['Investigação', 'Tecnologia'], 'Motor de Busca', 'A critério do mestre, sempre que tiver acesso à internet, pode gastar 2 PE para substituir um teste de perícia qualquer por um teste de Tecnologia.')
o('Trabalhador Rural', ['Adestramento', 'Sobrevivência'], 'Desbravador', 'Ao fazer um teste de Adestramento ou Sobrevivência, pode gastar 2 PE para receber +5 nele. Além disso, não sofre penalidade de deslocamento por terreno difícil.')
o('Trambiqueiro', ['Crime', 'Enganação'], 'Impostor', 'Uma vez por cena, pode gastar 2 PE para substituir um teste de perícia qualquer por um teste de Enganação.')
o('Universitário', ['Atualidades', 'Investigação'], 'Dedicação', '+1 PE, e mais 1 PE a cada NEX ímpar (15%, 25%…). Além disso, seu limite de PE por turno aumenta em 1 (NEX 5%: limite 2; NEX 10%: 3; e assim por diante; não afeta a DT dos efeitos). Efeito automático só o PE fixo +1; some o restante à mão.', [{'a': 'pe', 'v': 1}])
o('Vítima', ['Reflexos', 'Vontade'], 'Cicatrizes Psicológicas', '+1 de Sanidade para cada 5% de NEX.', [{'a': 'san', 'v': 1, 'nv': 1}])

# poderes paranormais: (nome, elemento ou None, pré-requisito, descrição, afinidade, ef)
P = []
def p(nome, el, pre, desc, af='', ef=None): P.append((nome, el, pre, desc, af, ef or []))

p('Aprender Ritual', None, '', 'Aprende e pode conjurar um ritual de 1º círculo à sua escolha; também pode trocar um ritual que já conhece por outro. A partir de 45% de NEX, ao escolher este poder aprende um ritual de até 2º círculo e, a partir de 75%, de até 3º. Pode escolher várias vezes, respeitado o limite de rituais conhecidos. Conta como poder do elemento do ritual escolhido.')
p('Resistir a <Elemento>', None, '', 'Escolha Conhecimento, Energia, Morte ou Sangue: resistência 10 contra esse elemento. Conta como poder do elemento escolhido.', 'Resistência 20.')
p('Expansão de Conhecimento', 'Conhecimento', 'Conhecimento 1', 'Aprende um poder de classe que não é da sua classe (cumprindo os pré-requisitos dele).', 'Aprende um segundo poder de classe de fora da sua classe.')
p('Percepção Paranormal', 'Conhecimento', '', 'Em cenas de investigação, ao testar para procurar pistas, pode rolar de novo um dado com resultado menor que 10 (aceitando a segunda rolagem).', 'Pode rolar de novo até dois dados com resultado menor que 10.')
p('Precognição', 'Conhecimento', 'Conhecimento 1', '+2 em Defesa e em testes de resistência.', 'Fica imune à condição desprevenido.', [{'a': 'def', 'v': 2}, {'a': 'res', 'v': 2}])
p('Sensitivo', 'Conhecimento', '', 'Sente emoções e intenções de outros personagens: +5 em Diplomacia, Intimidação e Intuição.', 'Em teste oposto com uma dessas perícias, o oponente sofre –1d20.',
  [{'a': 'per:Diplomacia', 'v': 5}, {'a': 'per:Intimidação', 'v': 5}, {'a': 'per:Intuição', 'v': 5}])
p('Visão do Oculto', 'Conhecimento', '', '+5 em testes de Percepção e enxerga no escuro.', 'Ignora camuflagem.', [{'a': 'per:Percepção', 'v': 5}])
p('Afortunado', 'Energia', '', 'Uma vez por rolagem, pode rolar de novo um resultado 1 em qualquer dado que não seja d20.', 'Também, uma vez por teste, pode rolar de novo um 1 em d20.')
p('Campo Protetor', 'Energia', 'Energia 1', 'Ao usar a ação esquiva, pode gastar 1 PE para receber +5 em Defesa.', 'Ao usar, também recebe +5 em Reflexos e, até o início do próximo turno, se passar em Reflexos que reduziria o dano à metade, não sofre dano nenhum.')
p('Causalidade Fortuita', 'Energia', '', 'Em cenas de investigação, a DT para procurar pistas diminui em 5 para você até encontrar uma pista.', 'A DT para procurar pistas sempre diminui em 5 para você.')
p('Golpe de Sorte', 'Energia', 'Energia 1', 'Seus ataques recebem +1 na margem de ameaça.', 'Seus ataques recebem +1 no multiplicador de crítico.')
p('Manipular Entropia', 'Energia', 'Energia 1', 'Gasta 2 PE para fazer um alvo em alcance curto (exceto você) rolar de novo um dos dados de um teste de perícia.', 'O alvo rola de novo todos os dados que você escolher.')
p('Encarar a Morte', 'Morte', '', 'Em cenas de ação, seu limite de gasto de PE aumenta em +1 (não afeta a DT dos efeitos).', 'Em cenas de ação, o limite aumenta em +2 (total +3).')
p('Escapar da Morte', 'Morte', 'Morte 1', 'Uma vez por cena, ao receber dano que o deixaria com 0 PV, fica com 1 PV. Não funciona contra dano massivo.', 'Em vez disso, evita completamente o dano; contra dano massivo, fica com 1 PV.')
p('Potencial Aprimorado', 'Morte', '', '+1 PE por NEX (ao escolher no NEX 30%, recebe 6 PE; cresce a cada subida de NEX).', '+1 PE adicional por NEX (total +2 PE por NEX).', [{'a': 'pe', 'v': 1, 'nv': 1}])
p('Potencial Reaproveitado', 'Morte', '', 'Uma vez por rodada, ao passar num teste de resistência, ganha 2 PE temporários cumulativos, que somem no fim da cena.', 'Ganha 3 PE temporários em vez de 2.')
p('Surto Temporal', 'Morte', 'Morte 2', 'Uma vez por cena, no seu turno, gasta 3 PE para realizar uma ação padrão adicional.', 'Em vez de uma vez por cena, pode usar uma vez por turno.')
p('Anatomia Insana', 'Sangue', 'Sangue 2', '50% de chance (par em 1d4) de ignorar o dano adicional de um acerto crítico ou ataque furtivo.', 'Imune aos efeitos de acertos críticos e ataques furtivos.')
p('Arma de Sangue', 'Sangue', '', 'Gasta ação de movimento e 2 PE para criar garras, chifres ou lâmina de sangue: arma simples, corpo a corpo e leve, que não precisa empunhar, 1d6 de dano de Sangue. Uma vez por turno, ao agredir, gasta 1 PE para um ataque adicional com ela. Dura até o fim da cena.', 'A arma é permanente e causa 1d10 de dano de Sangue.')
p('Sangue de Ferro', 'Sangue', '', '+2 PV por NEX (ao escolher no NEX 50%, recebe 20 PV; cresce a cada subida de NEX).', '+5 em Fortitude e imunidade a venenos e doenças.', [{'a': 'pv', 'v': 2, 'nv': 1}])
p('Sangue Fervente', 'Sangue', 'Sangue 2', 'Enquanto estiver machucado, +1 em Agilidade ou Força (escolha a cada ativação).', 'O bônus sobe para +2.')
p('Sangue Vivo', 'Sangue', 'Sangue 1', 'Na primeira vez que ficar machucado em uma cena, recebe cura acelerada 2. Nunca cura acima da metade dos PV máximos; termina no fim da cena ou ao perder a condição machucado.', 'A cura acelerada sobe para 5.')

assert len(O) == 26, len(O)
assert len(P) == 22, len(P)
def q(s): return "'" + str(s).replace("'", "''") + "'"
vals = []
for i, (nome, per, poder, desc, ef) in enumerate(O):
    d = {'tipo': 'origem', 'pe': 0, 'origem': nome, 'pericias': per, 'desc': desc, 'ef': ef}
    vals.append('(%s,%s,%s,null,%s,%s,null,null,%d,%s::jsonb)' % (q('op:origem:' + nome), q('op'), q('livro-basico'), q('origem'), q(poder), 2000 + i, q(json.dumps(d, ensure_ascii=False))))
ORD = {None: 0, 'Conhecimento': 1, 'Energia': 2, 'Morte': 3, 'Sangue': 4}
P.sort(key=lambda x: (ORD[x[1]], x[0]))
for i, (nome, el, pre, desc, af, ef) in enumerate(P):
    t = desc + (' Afinidade: ' + af if af else '') + (' Pré-requisito: ' + pre + '.' if pre else '')
    d = {'tipo': 'paranormal', 'pe': 0, 'el': el or '', 'pre': pre, 'desc': t, 'ef': ef}
    vals.append('(%s,%s,%s,null,%s,%s,null,%s,%d,%s::jsonb)' % (q('op:paranormal:' + nome), q('op'), q('livro-basico'), q('paranormal'), q(nome), q(el) if el else 'null', 3000 + i, q(json.dumps(d, ensure_ascii=False))))

SQL = """-- Etapa 6c — Origens e poderes paranormais do livro (Ordem Paranormal, Livro de Regras v1.2)
-- 26 origens (grupo 'origem') e 22 poderes paranormais (grupo 'paranormal') na tabela livro_habilidades.
-- Re-executável. Gerado por tools/livro/gerar_op_origens.py (não edite as linhas à mão).
-- Rode DEPOIS do schema_etapa6b_rituais.sql.

alter table public.livro_habilidades drop constraint if exists livro_habilidades_grupo_check;
alter table public.livro_habilidades add constraint livro_habilidades_grupo_check check (grupo in ('classe', 'poder', 'trilha', 'ritual', 'origem', 'paranormal'));

insert into public.livro_habilidades(ref, sistema, fonte, classe, grupo, nome, circulo, elemento, ordem, dados) values
""" + ',\n'.join(vals) + """
on conflict (ref) do update set sistema = excluded.sistema, fonte = excluded.fonte, classe = excluded.classe, grupo = excluded.grupo,
  nome = excluded.nome, circulo = excluded.circulo, elemento = excluded.elemento, ordem = excluded.ordem, dados = excluded.dados;
"""
raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
with open(os.path.join(raiz, 'schema_etapa6c_origens.sql'), 'w', encoding='utf-8') as fh:
    fh.write(SQL)
print(len(O), 'origens,', len(P), 'poderes paranormais')
