#!/usr/bin/env python3
"""Gera schema_etapa10_amaldicoados.sql: maldições (armas, proteções, acessórios) e itens amaldiçoados especiais
do Livro de Regras de Ordem Paranormal v1.2 (capítulo 5, págs. 144 a 151). Textos resumidos pelo Claude.
Uso: python3 tools/livro/gerar_op_amaldicoados.py   (na raiz do repositório)"""
import json, os

IT = []
def add(grupo, sub, nome, dados): IT.append((grupo, sub, nome, dados))

ARMA = ['corpo', 'disparo', 'fogo', 'pesada']
def mal(sub, el, nome, aplica, desc, def_=0, pag=146):
    add('maldicao', sub + ' · ' + el, nome, {'tipo': 'modificacao', 'maldicao': True, 'elemento': el, 'aplica': aplica, 'pag': pag,
        'desc': f'Maldição de {el}. ' + desc, 'mod': {'catg': 1, 'esp': 0, 'def': def_}})

# ------------------------------------------------------------ maldições de armas (livro p.145-146)
mal('arma', 'Conhecimento', 'Antielemento', ARMA, 'Contra criatura de um elemento (role 1d4: 1 Conhecimento, 2 Energia, 3 Morte, 4 Sangue), gaste 2 PE; se acertar, +4d8 de dano.')
mal('arma', 'Conhecimento', 'Ritualística', ARMA, 'Guarda na arma um ritual de alvo ou área (paga os PE na hora). Ao acertar um ataque, solta o ritual como ação livre, centrado no ser atingido. Depois pode guardar outro.')
mal('arma', 'Conhecimento', 'Senciente', ARMA, 'Ação de movimento e 2 PE: a arma flutua ao seu lado e ataca 1 ser por rodada em alcance curto, com as suas estatísticas. Manter custa 1 PE no início de cada turno, senão ela cai.')
mal('arma', 'Energia', 'Empuxo', ['corpo'], 'Só corpo a corpo. Pode ser arremessada em alcance curto (se já podia, o alcance sobe uma categoria) com +1 dado de dano do mesmo tipo, e volta voando no mesmo turno. Pegá-la é reação.')
mal('arma', 'Energia', 'Energética', ARMA, 'Gaste 2 PE por ataque: a arma (ou a munição) vira Energia pura, dá +5 no ataque, ignora resistência a dano e converte todo o dano em Energia.')
mal('arma', 'Energia', 'Vibrante', ARMA, 'Você recebe Ataque Extra da trilha Operações Especiais do combatente; se já tem, o custo dele cai em 1 PE.')
mal('arma', 'Morte', 'Consumidora', ARMA, 'Ao atacar, gaste 2 PE; se acertar, o alvo fica imóvel por uma rodada.')
mal('arma', 'Morte', 'Erosiva', ARMA, 'Causa +1d8 de dano de Morte. Ao atacar, gaste 2 PE; se acertar, a vítima sofre 2d4 de Morte no início dos próximos 2 turnos dela.')
mal('arma', 'Morte', 'Repulsora', ARMA, '+2 de Defesa enquanto empunhada. Ao bloquear, gaste 2 PE para ganhar +5 de Defesa adicional. (Some à mão na Defesa.)')
mal('arma', 'Sangue', 'Lancinante', ARMA, '+1d8 de dano de Sangue, multiplicado em acerto crítico (crítico x3 = +3d8).')
mal('arma', 'Sangue', 'Predadora', ARMA, 'Anula penalidades de camuflagem e cobertura (não cobertura total), dobra a margem de ameaça (aplicado antes dos aumentos) e, se for à distância, aumenta o alcance em uma categoria.')
mal('arma', 'Sangue', 'Sanguinária', ARMA, 'O atingido sangra, e o sangramento acumula (2 acertos = 2d6 por rodada). Em acerto crítico a arma drena sangue: alvo fraco e você ganha 2d10 PV temporários.')

# ------------------------------------------------------------ maldições de proteções (p.146-147)
P = ['protecao']
mal('proteção', 'Conhecimento', 'Abascanta', P, '+5 em resistência contra rituais. Uma vez por cena, ao ser alvo de um ritual, gaste reação e PE igual ao custo dele para refleti-lo ao conjurador (você decide o que o ritual exigir).', 0, 146)
mal('proteção', 'Conhecimento', 'Profética', P, 'Resistência a Conhecimento 10. Gaste 2 PE para rolar de novo um teste de resistência (uma vez).', 0, 146)
mal('proteção', 'Conhecimento', 'Sombria', P, '+5 em Furtividade e ignora a penalidade de carga nela. Ação de movimento e 1 PE: o item parece roupa comum, mantendo as propriedades.', 0, 147)
mal('proteção', 'Energia', 'Cinética', P, 'Barreira invisível: +2 de Defesa e resistência a dano 2 (proteção leve ou escudo) ou 5 (pesada).', 2, 147)
mal('proteção', 'Energia', 'Lépida', P, '+10 em Atletismo e +3m de deslocamento. Com 2 PE, até o fim do turno ignora terreno difícil, escala com deslocamento terrestre e é imune a queda de até 9m.', 0, 147)
mal('proteção', 'Energia', 'Voltaica', P, 'Resistência a Energia 10. Ação de movimento e 2 PE: até o fim da cena, no fim dos seus turnos causa 2d6 de Energia em todos os seres adjacentes.', 0, 147)
mal('proteção', 'Morte', 'Letárgica', P, '+2 de Defesa e 25% (leve ou escudo) ou 50% (pesada) de chance de ignorar o dano extra de crítico e ataque furtivo.', 2, 147)
mal('proteção', 'Morte', 'Repulsiva', P, 'Resistência a Morte 10. Ação de movimento e 2 PE: até o fim da cena, quem te ataca em corpo a corpo sofre 2d8 de Morte.', 0, 147)
mal('proteção', 'Sangue', 'Regenerativa', P, 'Resistência a Sangue 10. Ação de movimento e 1 PE: recupera 1d12 PV.', 0, 147)
mal('proteção', 'Sangue', 'Sádica', P, 'No início do seu turno, +1 em ataque e dano para cada 10 pontos de dano sofridos desde o fim do seu último turno.', 0, 147)

# ------------------------------------------------------------ maldições de acessórios (p.147)
A = ['acessorio']
mal('acessório', 'Conhecimento', 'Carisma', A, '+1 em Presença (não dá PE extra).', 0, 147)
mal('acessório', 'Conhecimento', 'Conjuração', A, 'Guarda um ritual de 1º círculo: empunhando o item, você o conjura como se o conhecesse (se já conhece, custa 1 PE a menos).', 0, 147)
mal('acessório', 'Conhecimento', 'Escudo Mental', A, 'Resistência mental 10.', 0, 147)
mal('acessório', 'Conhecimento', 'Reflexão', A, 'Uma vez por rodada, ao ser alvo de um ritual, gaste PE igual ao custo dele para refleti-lo ao conjurador.', 0, 147)
mal('acessório', 'Conhecimento', 'Sagacidade', A, '+1 em Intelecto (não dá perícias).', 0, 147)
mal('acessório', 'Energia', 'Defesa', A, '+5 de Defesa (some à mão na Defesa da ficha).', 0, 147)
mal('acessório', 'Energia', 'Destreza', A, '+1 em Agilidade.', 0, 147)
mal('acessório', 'Energia', 'Potência', A, '+1 na DT das suas habilidades, poderes e rituais.', 0, 147)
mal('acessório', 'Morte', 'Esforço Adicional', A, '+5 PE (ativa depois de um dia de uso).', 0, 147)
mal('acessório', 'Sangue', 'Disposição', A, '+1 em Vigor.', 0, 147)
mal('acessório', 'Sangue', 'Pujança', A, '+1 em Força.', 0, 147)
mal('acessório', 'Sangue', 'Vitalidade', A, '+15 PV (ativa depois de um dia de uso).', 0, 147)
mal('acessório', 'Varia', 'Proteção Elemental', A, 'Resistência 10 a um elemento; o acessório conta como item desse elemento.', 0, 147)

# ------------------------------------------------------------ itens especiais (p.148-151). Cat. II, 1 espaço, salvo indicação
def esp(el, nome, desc, pag, catg=2, esp_=1, tipo='paranormal', extra=None):
    d = {'tipo': tipo, 'catg': catg, 'esp': esp_, 'desc': f'Amaldiçoado de {el}. ' + desc, 'elemento': el, 'pag': pag, 'amaldicoado': True}
    if extra: d.update(extra)
    add('amaldicoado', el, nome, d)

esp('Sangue', 'Coração Pulsante', 'Empunhando, ao sofrer dano gaste reação para reduzi-lo à metade. Cada uso pede Fortitude (DT 15, +5 por uso extra no dia); se falhar, o item é destruído. Precisa ser drenado uma vez por dia.', 148)
esp('Sangue', 'Coroa de Espinhos', 'Uma vez por rodada, reação para trocar dano mental por dano de Sangue; mas você não recupera sanidade descansando enquanto a veste. Precisa ser vestida por uma semana.', 148)
esp('Sangue', 'Frasco de Vitalidade', 'Em 1 minuto, sofra até 20 de dano para guardar o seu sangue. Ação padrão para beber e recuperar os PV guardados; Fortitude (DT 20) ou fica enjoado por uma rodada.', 148)
esp('Sangue', 'Pérola de Sangue', 'Ação de movimento para absorver: +5 em Agilidade, Força, Vigor e testes deles até o fim da cena. No fim, Fortitude (DT 20): falhou, fatigado até o fim do dia; falhou por 5+, parada cardíaca e morrendo (se morrer, vira criatura de Sangue de VD parecido com o seu NEX).', 148)
esp('Sangue', 'Punhos Enraivecidos', 'Ataques desarmados causam 1d8 de Sangue. Ao acertar, pode atacar de novo o mesmo alvo pagando 2 PE por ataque já feito no turno (2, 4, 6...).', 148)
esp('Sangue', 'Seringa de Transfiguração', 'Ação padrão para colher sangue de alvo adjacente (inimigo exige ataque corpo a corpo). Ação padrão para injetar em outra pessoa: ela assume a aparência do dono do sangue por um dia (Distorcer Aparência). No fim, rola 1d6: com 1, perde 1 PV permanentemente.', 148)
esp('Morte', 'Amarras Mortais', 'Uma vez por rodada, ação padrão e 2 PE para agarrar alvo Grande ou menor em alcance curto, com +10 no teste oposto. Ação de movimento para puxar um agarrado até ficar adjacente.', 148)
esp('Morte', 'Casaco de Lodo', 'Vestimenta: resistência 5 a corte, impacto, Morte e perfuração, mas vulnerabilidade a dano balístico e de Energia.', 149, 2, 1, 'paranormal')
esp('Morte', 'Coletora', 'Punhal. Ação completa para matar uma pessoa que esteja morrendo e guardar 1d8 PE (máximo 20, usáveis como seus se portar a adaga há uma semana). Pesadelos: descanso sempre ruim enquanto a portar.', 149, 2, 1, 'arma', {'mc': 'corpo', 'arma': {'dano': '1d4', 'crit': 'x3', 'alc': '', 'td': 'P', 'per': 'Luta'}})
esp('Morte', 'Crânio Espiral', 'Empunhando, uma vez por rodada ação livre para ganhar uma ação padrão adicional. Cada uso pede Vontade (DT 15, +5 por uso extra no dia); se falhar, ganha o benefício, envelhece 1d4 anos e não usa mais naquele dia.', 149)
esp('Morte', 'Frasco de Lodo', 'Uma dose. Ação padrão em ferimento recente (até 1 rodada): recupera 6d8+20 PV. Ferida mais antiga: par recupera 3d8+10; ímpar infecciona e causa 3d8+10 de Morte.', 149)
esp('Morte', 'Vislumbre do Fim', 'Óculos. Ação de movimento focando um ser visível: em pessoas comuns mostra um contador do tempo até a morte; em Marcados e criaturas mostra o pior valor de resistência e as vulnerabilidades.', 149)
esp('Conhecimento', 'Anéis do Elo Mental', 'Dois anéis, usados por duas pessoas por 24h, criam ligação telepática. Nos testes de Vontade usam a melhor quantidade de dados e bônus das duas. Dano mental e condições mentais ou de medo de uma passam para a outra.', 149)
esp('Conhecimento', 'Lanterna Reveladora', 'Ação padrão e 1 PE: luz por uma cena com as propriedades do ritual Terceiro Olho. Criaturas de Sangue iluminadas atacam você de preferência, na mesma categoria de alcance.', 149)
esp('Conhecimento', 'Máscara das Pessoas nas Sombras', 'Resistência a Conhecimento 10. Ação de movimento e 2 PE para entrar numa sombra adjacente e sair em outra sombra visível em alcance médio. Vesti-la pode atrair a atenção da mente única das Máscaras.', 149)
esp('Conhecimento', 'Munição Jurada', 'Uma bala. Ritual de 1 hora a liga a um ser que você conheça. Contra ele: +10 no ataque, margem de ameaça dobrada e +6d12 de Conhecimento. Você fica obcecado: –2 em Defesa e ataques contra outros alvos.', 150)
esp('Conhecimento', 'Pergaminho da Pertinácia', 'Ação padrão: +5 PE temporários até o fim da cena. Cada uso pede Ocultismo (DT 15, +5 por uso extra no dia); se falhar, o pergaminho se desfaz.', 150)
esp('Energia', 'Arcabuz dos Moretti', 'Arma simples, de fogo, uma mão, +2 no ataque, alcance curto, crítico x3, sem munição. Role 1d6 com o ataque para o dano: 1 2d4, 2 2d6, 3 2d8, 4 2d10, 5 2d12, 6 2d20.', 150, 2, 1, 'arma', {'mc': 'fogo', 'arma': {'dano': '2d6', 'crit': 'x3', 'alc': 'Curto', 'td': 'B', 'per': 'Pontaria'}})
esp('Energia', 'Bateria Reversa', 'Ação padrão e 2 PE: descarrega um aparelho eletrônico em alcance curto; cheia, recarrega um aparelho. Cada uso pede Ocultismo (DT 15, +5 por uso extra no dia); se falhar, explode: 12d6 de Energia a até 3m.', 150)
esp('Energia', 'Peitoral da Segunda Chance', 'Colete. Ao chegar a 0 PV, gasta 5 PE seus e o reanima com 4d10 PV (falha se faltar PE). A cada uso há 1 chance em 1d10 de descarga forte demais, que mata e vira você plasma de Energia.', 150, 2, 1, 'paranormal')
esp('Energia', 'Relógio de Arnaldo', 'Uma vez por rodada, gaste 1 PE para rolar de novo qualquer dado que deu 1. O custo sobe +1 a cada ativação no mesmo dia. Item único (só um agente pode escolher).', 150)
esp('Energia', 'Talismã da Sorte', 'Vestindo, ao sofrer dano gaste reação e 3 PE e role 1d4: 2 ou 3 evita o dano; 4 evita e vira cinzas; 1 você sofre o dobro e vira cinzas.', 150)
esp('Energia', 'Teclado de Conexão Neural', 'Plugado (ação de movimento), liga sua mente à máquina: sem barreira de idioma ou tecnologia, +10 para hackear e metade do tempo para achar arquivos. Você sofre 1d6 de dano mental por rodada de uso.', 150)
esp('Energia', 'Tela do Pesadelo', 'Ação padrão e 2 PE ativam a tela. Quem tocá-la a seguir faz Vontade (DT do usuário +5): falhou, fica atordoada, sofre 4d6 de dano mental e repete o teste a cada rodada até passar, enlouquecer ou a tela ser destruída.', 151)
esp('Energia', 'Veículo Energizado', 'Veículo sem combustível. Reação e Pilotagem (DT 25) para virar energia pura por um instante e atravessar um obstáculo como se fosse incorpóreo.', 151)
esp('Medo', 'Jaqueta de Veríssimo', 'Categoria IV, item único. Resistência a dano paranormal 15. Quando um aliado adjacente sofreria dano, gaste reação e 2 PE para ser o alvo no lugar dele.', 151, 4)
esp('Varia', 'Dedo Decepado', 'Dá um poder paranormal que o dono do dedo tinha (o elemento do poder define o da maldição). Ao dormir ou relaxar no interlúdio, 1d4: com 1 você é assombrado e não recupera PV, PE nem sanidade. –10 em Diplomacia se for visto. Vestir por uma semana.', 151)
esp('Varia', 'Selos Paranormais', 'Selo com um ritual. Empunhe e leia em voz alta (ação padrão ou a do ritual, a maior); conhecendo o ritual, ou passando em Ocultismo (DT 20 + custo em PE). O ritual é conjurado e o selo vira cinzas, sem componentes. Pode usar versões avançadas pagando só o custo adicional. Categoria = círculo do ritual.', 151, 1)

raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
q = lambda s: "'" + s.replace("'", "''") + "'"
vals, N = [], 600
for g, sub, nome, d in IT:
    N += 1
    vals.append(f"({q('op:item:' + g + ':' + nome)},'op','livro-basico',{q(g)},{q(sub)},{q(nome)},{N},{q(json.dumps(d, ensure_ascii=False))}::jsonb)")
SQL = """-- Etapa 10 — Itens amaldiçoados do livro (Ordem Paranormal, Livro de Regras v1.2, capítulo 5, págs. 144 a 151)
-- Depois do schema_etapa6d_itens.sql. Re-executável. Acrescenta os grupos 'maldicao' e 'amaldicoado' em livro_itens.
-- Gerado por tools/livro/gerar_op_amaldicoados.py (não edite as linhas à mão).

alter table public.livro_itens drop constraint if exists livro_itens_grupo_check;
alter table public.livro_itens add constraint livro_itens_grupo_check check (grupo in
  ('arma', 'municao', 'protecao', 'acessorio', 'explosivo', 'operacional', 'paranormal', 'modificacao', 'maldicao', 'amaldicoado'));

insert into public.livro_itens(ref, sistema, fonte, grupo, subgrupo, nome, ordem, dados) values
""" + ',\n'.join(vals) + """
on conflict (ref) do update set sistema = excluded.sistema, fonte = excluded.fonte, grupo = excluded.grupo,
  subgrupo = excluded.subgrupo, nome = excluded.nome, ordem = excluded.ordem, dados = excluded.dados;
"""
with open(os.path.join(raiz, 'schema_etapa10_amaldicoados.sql'), 'w', encoding='utf-8') as fh:
    fh.write(SQL)
print(len(IT), 'linhas')
