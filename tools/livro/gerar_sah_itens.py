#!/usr/bin/env python3
"""Gera schema_etapa13_sah_itens.sql: itens do complemento "Sobrevivendo ao Horror" (SaH, v1.1), capítulo 1 (págs. 37 a 61):
armas, munição, modificações, acessórios, explosivos, itens operacionais, medicamentos, itens paranormais e itens amaldiçoados.
Textos em redação própria (mecânica completa, sem copiar o livro). Todas as linhas levam fonte = 'sah' e comp = 'sah' em dados.
Uso: python3 tools/livro/gerar_sah_itens.py   (na raiz do repositório)
Categoria: 0, I=1, II=2, III=3, IV=4. "–1d20" = o símbolo de d20 do livro ("–O")."""
import json, os

FONTE = 'sah'
IT = []   # (grupo, subgrupo, nome, dados)
def add(grupo, sub, nome, dados, pag):
    d = {'comp': FONTE, 'pag': pag}; d.update(dados)
    IT.append((grupo, sub, nome, d))
def l(*p): return [list(x) for x in p]

# ---------------------------------------------------------------- ARMAS (p.37-38, tabela 1.4)
PROF = {'S': 'simples', 'T': 'tática'}
EMP = {'DU': 'disparo, uma mão', 'DD': 'disparo, duas mãos', 'FL': 'fogo, leve', 'FU': 'fogo, uma mão', 'FD': 'fogo, duas mãos',
       'CL': 'corpo a corpo, leve', 'CU': 'corpo a corpo, uma mão', 'AR': 'arremesso'}
MC = {'DU': 'disparo', 'DD': 'disparo', 'FL': 'fogo', 'FU': 'fogo', 'FD': 'fogo', 'CL': 'corpo', 'CU': 'corpo', 'AR': 'arremesso'}
AGIL = 'Arma ágil: usa Agilidade em vez de Força no ataque e no dano.'
def W(prof, emp, nome, cat, dano, crit, alc, td, esp, nota=''):
    per = 'Luta' if emp in ('CL', 'CU') else 'Pontaria'
    d = f'Arma {PROF[prof]}, {EMP[emp]}.' + (' ' + nota if nota else '')
    add('arma', PROF[prof] + ' · ' + EMP[emp], nome, {'tipo': 'arma', 'catg': cat, 'esp': esp, 'mc': MC[emp], 'desc': d,
        'arma': {'dano': dano, 'crit': crit, 'alc': alc, 'td': td, 'per': per}}, 37)

W('S', 'DU', 'Pregador pneumático', 0, '1d4', 'x4', 'Curto', 'P', 1, 'Ferramenta que dispara pregos sob pressão. Para os poderes que afetam armas de fogo, conta como arma de fogo. O rolo tem 300 pregos: dura a missão inteira.')
W('S', 'DD', 'Estilingue', 0, '1d4', 'x2', 'Curto', 'I', 1, 'Ao contrário de outras armas de disparo, soma a sua Força ao dano. Dispara bolinhas reaproveitáveis (ou pedrinhas, se faltarem). Também lança granadas: com ele a granada é arremessada em alcance longo. Um pacote de bolinhas dura a missão inteira.')
W('S', 'FL', 'Revólver compacto', 1, '2d4', '19/x3', 'Curto', 'P', 1, 'Calibre baixo, feito para ser escondido. Se você for treinado em Crime, carrega uma sem que ela ocupe espaço. Usa balas curtas. Com a contagem de munição: 5 balas.')
W('T', 'CL', 'Baioneta', 0, '1d4', '19', '', 'P', 1, 'Lâmina para fixar em fuzil ou arma parecida. Fixar numa arma de fogo de duas mãos gasta ação de movimento; fixada, a baioneta vira arma de duas mãos ágil e seu dano sobe para 1d6. Você ainda ataca à distância com a arma de fogo, mas com –1d20 nesses ataques.')
W('T', 'CL', 'Faca tática', 1, '1d6', '19', 'Curto', 'C', 1, AGIL + ' Pode ser arremessada. Na ação especial contra-ataque, dá +2 no teste de ataque. Na ação especial bloqueio, gaste 2 PE e sacrifique a faca para aumentar a RD do bloqueio em +20.')
W('T', 'CL', 'Gancho de carne', 0, '1d4', 'x4', '', 'P', 1, 'Gancho de frigorífico usado como arma. Amarrado a corda ou corrente, o alcance sobe para 4,5m e o item passa a ocupar 2 espaços.')
W('T', 'CU', 'Bastão policial', 1, '1d6', 'x2', 'Curto', 'I', 1, AGIL + ' Serve para aparar: na ação especial esquiva, o bônus na Defesa aumenta em +1.')
W('T', 'CU', 'Picareta', 0, '1d6', 'x4', '', 'P', 1, 'Ferramenta de mineração e demolição usada como arma na falta de algo melhor.')
W('T', 'AR', 'Shuriken', 1, '1d4', 'x2', 'Curto', 'P', 0.5, 'Arma de arremesso (soma Força ao dano). Se você for veterano em Pontaria, uma vez por rodada, ao atacar com shuriken, pode gastar 1 PE para fazer um ataque adicional de shuriken contra o mesmo alvo. Uma shuriken representa um pacote para duas cenas (10 shurikens, com a contagem de munição).')
W('T', 'FU', 'Pistola pesada', 1, '2d8', '18', 'Curto', 'B', 1, 'Calibre maior que o da pistola. Potência e recuo dão –1d20 no ataque; empunhá-la com as duas mãos anula a penalidade. Usa balas curtas. Com a contagem de munição: 10 balas.')
W('T', 'FD', 'Espingarda de cano duplo', 2, '4d6', 'x3', 'Curto', 'B', 2, 'Dois canos, cada um com um gatilho e um cartucho. Depois de disparar os dois, recarregar gasta ação de movimento. Pode disparar os dois canos no mesmo alvo: –1d20 no ataque, mas o dano sobe para 6d6. Usa cartuchos. Com a contagem de munição: 2 balas.')

add('municao', 'munição', 'Bolinhas de estilingue', {'tipo': 'municao', 'catg': 0, 'esp': 1, 'desc': 'Pacote de bolinhas (ou pedrinhas) para estilingue. Reaproveitáveis: o pacote dura a missão inteira. Ocupa o mesmo espaço do estilingue.',
    'fx': l(('Serve em', 'Estilingue'), ('Dura', 'A missão inteira'))}, 37)

# ---------------------------------------------------------------- MODIFICAÇÕES (p.38, 39, 45)
add('modificacao', 'modificação', 'Carregador Rápido', {'tipo': 'modificacao', 'aplica': ['fogo', 'disparo'],
    'desc': 'Só para quem usa a regra opcional de contagem de munição (OPRPG p.174). Para armas de fogo, bestas e balestras. Em arma de fogo, recarrega como ação livre, uma vez por rodada. Em besta ou balestra, permite até cinco recargas como ação livre, com apenas uma mão; depois disso é preciso recarregar o carregador, um virote por vez (ação de movimento por virote).',
    'mod': {'catg': 1, 'esp': 0, 'def': 0}, 'fx': l(('Efeito', 'Recarrega como ação livre'), ('Só vale', 'Armas de fogo, bestas e balestras'), ('Regra opcional', 'Contagem de munição'))}, 38)
add('modificacao', 'modificação', 'Bateria Potente', {'tipo': 'modificacao', 'aplica': ['acessorio'],
    'desc': 'Para objetos elétricos. Em lanternas, celulares e notebooks, dobra a duração da bateria e o alcance da luz. Em taser, dobra os usos, aumenta o dano para 1d8 e a DT para resistir em +5. Em outros objetos, conforme a proposta do jogador e a critério do mestre.',
    'mod': {'catg': 1, 'esp': 0, 'def': 0}, 'fx': l(('Luz', 'Alcance dobrado (lanterna, celular, notebook)'), ('Taser', 'Usos dobrados, dano 1d8, DT +5'), ('Bateria', 'Dura o dobro'))}, 39)
add('modificacao', 'modificação paranormal', 'Lente de Revelação', {'tipo': 'modificacao', 'aplica': ['camera'], 'elemento': 'Conhecimento',
    'desc': 'Modificação paranormal para câmeras de aura paranormal. A câmera com a lente vê seres invisíveis e incorpóreos e ignora a camuflagem deles. Além disso, ação padrão e 1 PE para fotografar uma criatura em alcance curto: até o fim da cena ela perde camuflagem e invisibilidade e se torna corpórea (Vontade DT Pre evita). O livro não dá a categoria da lente; pela Câmera Obscura (categoria III com a lente, contra II da câmera comum), ela sobe a categoria em I.',
    'mod': {'catg': 1, 'esp': 0, 'def': 0}, 'fx': l(('Efeito', 'Vê invisíveis e incorpóreos, ignora camuflagem'), ('Fotografar', 'Ação padrão e 1 PE, alcance curto'), ('Teste', 'Vontade DT Pre evita'), ('Só vale', 'Câmera de aura paranormal'))}, 45)

# ---------------------------------------------------------------- ACESSÓRIOS (p.39, tabela 1.5)
def ac(nome, cat, esp, desc, fx, pag=39, **x):
    d = {'tipo': 'geral', 'catg': cat, 'esp': esp, 'mc': 'acessorio', 'desc': desc, 'fx': fx}; d.update(x)
    add('acessorio', 'acessório', nome, d, pag)
ac('Amuleto Sagrado', 0, 1, 'Xale, rosário, fio de contas ou outro objeto que reforça a sua fé. Ocupa o espaço de um item vestido e dá +2 em Religião e Vontade.',
   l(('Bônus', '+2 em Religião e Vontade'), ('Uso', 'Vestido')), ef=[{'a': 'per:Religião', 'v': 2}, {'a': 'per:Vontade', 'v': 2}], precisaEq=True)
ac('Celular', 0, 1, 'Tira fotos, grava áudio e vídeo, acessa a internet e liga para outras pessoas. Com acesso à internet, dá +2 em testes de perícia que envolvem adquirir informações. A lanterna é fraca, mas serve na falta de coisa melhor: ilumina um cone de 4,5m.',
   l(('Bônus', '+2 em testes para adquirir informações (com internet)'), ('Luz', 'Cone de 4,5m')), luz={'t': 'c', 'm': 4.5})
ac('Chave de Fenda Universal', 0, 1, 'Resolve quase qualquer problema: +2 em testes de perícia para criar ou reparar objetos, de panelas a motores de avião. Também dá o bônus como item de apoio em situações especiais, como mexer em cabos para hackear um servidor.',
   l(('Bônus', '+2 em testes para criar ou reparar objetos')))
ac('Chaves', 0, 1, 'Molho de chaves (casa, veículo, cadeados). Usar o barulho do molho para distrair alguém (jogando as chaves, por exemplo) dá +2 em testes de Furtividade feitos na mesma rodada.',
   l(('Bônus', '+2 em Furtividade na rodada em que distrai com o barulho')))
ac('Documentos Falsos', 1, 1, 'Identidade funcional, carteira de habilitação, cartões de crédito etc. em nome de uma identidade falsa. +2 em testes de Diplomacia, Enganação e Intimidação para se passar pela pessoa dos documentos.',
   l(('Bônus', '+2 em Diplomacia, Enganação e Intimidação para se passar pela identidade')))
ac('Manual Operacional', 1, 1, 'Livro de lições práticas sobre um assunto: existe um manual para cada perícia. Gastar uma ação de interlúdio lendo permite usar essa perícia como se fosse treinado até o próximo interlúdio. Um manual aprimorado (OPRPG p.64) também dá +5 na perícia. Só vale o benefício de um manual por vez.',
   l(('Efeito', 'Usa a perícia como treinado até o próximo interlúdio'), ('Ler', 'Ação de interlúdio'), ('Limite', 'Um manual por vez')))
ac('Notebook', 0, 2, 'Como o celular: com internet, dá +2 em testes de perícia que envolvem adquirir informações. A tela maior serve melhor para entretenimento: ao relaxar em interlúdio, você recupera 1 ponto adicional de Sanidade. A luz do monitor ilumina um cone de 4,5m. Tablets contam como notebook.',
   l(('Bônus', '+2 em testes para adquirir informações (com internet)'), ('Relaxar', '+1 Sanidade no interlúdio'), ('Luz', 'Cone de 4,5m')), luz={'t': 'c', 'm': 4.5})

# ---------------------------------------------------------------- EXPLOSIVOS (p.41)
def ex(nome, cat, esp, desc, fx):
    add('explosivo', 'explosivo', nome, {'tipo': 'consumivel', 'catg': cat, 'esp': esp, 'desc': desc, 'fx': fx}, 41)
ex('Dinamite', 1, 1, 'Bastão de nitroglicerina de 20 cm. Com a mesma ação padrão você acende o pavio com uma mão e arremessa com a outra em um ponto em alcance médio. Atinge raio de 6m: seres e objetos soltos sofrem 4d6 de impacto e 4d6 de fogo e ficam em chamas (Reflexos DT Agi reduz à metade e evita as chamas).',
   l(('Dano', '4d6 impacto + 4d6 fogo + em chamas'), ('Uso', 'Acender e arremessar (ação padrão)'), ('Alcance', 'Médio'), ('Área', 'Raio de 6m'), ('Teste', 'Reflexos DT Agi: metade e evita as chamas')))
ex('Explosivo Plástico', 1, 1, 'Massa adesiva do tamanho de uma esponja, com pinos de ignição e detonador remoto. Preparar os pinos e grudar numa superfície leva duas rodadas. Detona com o detonador (ação livre, até alcance longo) ou se sofrer ao menos 1 ponto de dano de fogo ou eletricidade. Causa 16d6 de impacto em todos os seres e objetos num raio de 3m (Reflexos DT Int reduz à metade). Um especialista em explosivos (treinado em Crime ou em uma Profissão adequada, a critério do mestre) causa o dobro de dano em objetos e estruturas e ignora a RD deles.',
   l(('Dano', '16d6 impacto'), ('Área', 'Raio de 3m'), ('Teste', 'Reflexos DT Int: metade'), ('Preparar', 'Duas rodadas'), ('Detonar', 'Ação livre, até alcance longo'), ('Especialista', 'Dobro de dano em objetos e ignora RD')))
ex('Galão Vermelho', 0, 2, 'Galão vermelho ou marcado com símbolo de chama: guarda substância inflamável. Ao sofrer dano de fogo ou balístico, explode numa esfera de 6m de raio: 12d6 de fogo e em chamas (Reflexos DT 25 reduz à metade e evita as chamas). A área fica em chamas (1d6 de fogo por rodada em seres e objetos) até ser apagada ou a cena acabar (OPRPG p.292, Fogo e Fumaça).',
   l(('Dano', '12d6 fogo + em chamas'), ('Dispara', 'Ao sofrer dano de fogo ou balístico'), ('Área', 'Esfera de 6m de raio'), ('Teste', 'Reflexos DT 25: metade e evita as chamas'), ('Depois', 'Área em chamas, 1d6 de fogo por rodada')))
ex('Granada de Gás Sonífero', 1, 1, 'Libera fumaça branca num raio de 6m do ponto de impacto, por 2 rodadas. Quem começa o turno na área fica inconsciente e caído; se estiver em atividade física intensa (como combate), fica exausto por 1 rodada e depois fatigado. Em ambos os casos, Fortitude DT Agi reduz para fatigado por 1d4 rodadas.',
   l(('Efeito', 'Inconsciente (ou exausto 1 rodada, depois fatigado)'), ('Área', 'Raio de 6m'), ('Duração', '2 rodadas'), ('Teste', 'Fortitude DT Agi: só fatigado por 1d4 rodadas')))
ex('Granada de PEM', 1, 1, 'Emite um pulso eletromagnético que desativa todos os equipamentos elétricos num raio de 18m até o fim da cena. Criaturas de Energia na área sofrem 6d6 de impacto e ficam paralisadas por 1 rodada (uma vez por cena; Fortitude DT Agi reduz à metade e evita a condição).',
   l(('Efeito', 'Desativa equipamentos elétricos até o fim da cena'), ('Área', 'Raio de 18m'), ('Dano', '6d6 impacto em criaturas de Energia + paralisadas 1 rodada'), ('Teste', 'Fortitude DT Agi: metade e evita a paralisia')))

# ---------------------------------------------------------------- ITENS OPERACIONAIS (p.42-44)
def op(nome, cat, esp, desc, fx, pag=42, **x):
    d = {'tipo': x.pop('tipo', 'geral'), 'catg': cat, 'esp': esp, 'desc': desc, 'fx': fx}; d.update(x)
    add('operacional', 'item operacional', nome, d, pag)
op('Alarme de Movimento', 0, 1, 'Objeto pequeno controlado por dispositivo móvel ou aplicativo de celular. Ação completa para posicionar e ativar. Depois, sempre que houver movimento significativo num cone de 30m para onde foi apontado, sinaliza o dispositivo de controle. Dá para regular a sensibilidade (padrão: ser Pequeno ou maior em movimento). A sinalização pode ser discreta (só no dispositivo) ou um alarme sonoro alto.',
   l(('Efeito', 'Avisa movimento na área'), ('Ativar', 'Ação completa'), ('Área', 'Cone de 30m'), ('Aviso', 'Discreto ou sonoro')))
op('Alimento Energético', 2, 1, 'Alimentos e suplementos de alta tecnologia que recuperam a energia mental. Ação padrão para consumir.',
   l(('Cura', '1d4 PE'), ('Uso', 'Ação padrão')), tipo='consumivel')
op('Aplicador de Medicamentos', 1, 1, 'Bomba injetora portátil, presa ao braço ou à perna, que aplica uma substância (cicatrizante, medicamento) com uma ação de movimento. Tem espaço para três doses (já contado no espaço do item). Carregar uma dose é ação padrão.',
   l(('Efeito', 'Aplica a substância como ação de movimento'), ('Doses', '3'), ('Carregar', 'Ação padrão por dose')))
op('Braçadeira Reforçada', 1, 1, 'Proteção de artes marciais e esportes de contato que ajuda a absorver o impacto ao bloquear com o braço. Aumenta em +2 a RD que você recebe ao bloquear.',
   l(('Efeito', '+2 na RD do bloqueio')))
op('Cão Adestrado', 1, 0, 'Cão grande e corajoso (pastor alemão, dobermann, fila brasileiro, caramelo) treinado para ajudar em investigação e combate. Personagem treinado em Adestramento pode usá-lo como aliado (OPRPG p.171). Bônus: +2 em Investigação e Percepção. Ladrar e Morder: gaste 1 PE para o cão assumir postura defensiva ao seu redor; você recebe +2 na Defesa por 1 rodada.',
   l(('Tipo', 'Aliado (precisa de Adestramento)'), ('Bônus', '+2 em Investigação e Percepção'), ('Ladrar e Morder', '1 PE: +2 Defesa por 1 rodada'), ('Espaço', 'Não ocupa')),
   ef=[{'a': 'per:Investigação', 'v': 2}, {'a': 'per:Percepção', 'v': 2}], aliado=True)
op('Coldre Saque Rápido', 1, 1, 'Coldre que permite sacar ou guardar a arma com movimento mínimo. Uma vez por rodada, saca ou guarda uma arma de fogo leve como ação livre.',
   l(('Efeito', 'Saca ou guarda arma de fogo leve como ação livre'), ('Limite', '1 vez por rodada')))
op('Equipamento de Escuta', 1, 1, 'Um receptor com alcance de 90m e três transmissores minúsculos que captam sons num raio de 9m. Instalar um transmissor leva alguns minutos e exige Crime contra DT 20 (falha: a escuta não transmite). O resultado do teste é também a DT para outros acharem o transmissor. Instalar discretamente com gente presente: ação completa, Furtividade oposta à Percepção dos presentes e DT do teste de Crime +5.',
   l(('Receptor', 'Alcance de 90m'), ('Transmissores', '3, captam num raio de 9m'), ('Instalar', 'Crime DT 20 (+5 se discreto, com Furtividade)')))
op('Estrepes (saco)', 0, 1, 'Peça de metal de quatro pontas afiadas, sempre com uma voltada para cima. Em combate, um saco cobre um quadrado de 1,5m com ação padrão. Quem pisa sofre 1d4 de perfuração e fica lento por um dia. Em perseguição, aplicar faz parte da sua ação, com –1d20 no seu teste naquela rodada; o perseguidor que pisa sofre –1d20 nos testes de perseguição até o fim da cena. Reflexos (DT Agi) evita. Não afeta seres que resistem a todo o dano.',
   l(('Dano', '1d4 perfuração + lento por um dia'), ('Uso', 'Ação padrão, quadrado de 1,5m'), ('Teste', 'Reflexos DT Agi evita'), ('Perseguição', '–1d20 no seu teste; perseguidor –1d20 até o fim da cena')))
op('Faixa de Pregos', 1, 2, 'Trilha de hastes metálicas sanfonadas com pregos, feita para parar veículos. Funciona como estrepes, mas ocupa uma linha de 9m. Veículos de pneus de borracha que passam pela faixa têm os pneus perfurados e o deslocamento cai pela metade.',
   l(('Efeito', 'Como estrepes, numa linha de 9m'), ('Veículos', 'Pneus perfurados: deslocamento pela metade')))
op('Isqueiro', 0, 0.5, 'Do metal sofisticado ao descartável de plástico: ação de movimento para produzir uma chama pequena. Incendeia objetos inflamáveis e emite luz num raio de 3m.',
   l(('Luz', 'Raio de 3m'), ('Acender', 'Ação de movimento')), 43, luz={'t': 'l', 'm': 3})
op('Óculos de Visão Noturna', 1, 1, 'Funcionam a bateria e permitem enxergar no escuro, como visão no escuro. Em troca, quem usa recebe –1d20 em testes de resistência contra a condição ofuscado e contra efeitos baseados em luz (como uma granada de atordoamento).',
   l(('Efeito', 'Visão no escuro'), ('Contra', '–1d20 em resistência a ofuscado e efeitos de luz')), 43)
op('Óculos Escuros', 0, 1, 'Quem usa óculos escuros não pode ser ofuscado.',
   l(('Efeito', 'Imune a ofuscado')), 43)
op('Pá', 0, 2, 'Ferramenta pesada: +5 em testes de Força para cavar buracos e mover detritos. Em combate vale como um bastão.',
   l(('Bônus', '+5 em Força para cavar e mover detritos'), ('Combate', 'Vale como bastão')), 43)
op('Paraquedas', 1, 2, 'Anula o dano de queda. Quem tem grau veterano em Acrobacia, Pilotagem, Reflexos, Tática ou numa Profissão específica sabe usar. Os demais, ou em quedas muito curtas, precisam de Reflexos (DT 20); se falhar, o paraquedas não funciona direito e o dano de queda cai só à metade.',
   l(('Efeito', 'Anula o dano de queda'), ('Teste', 'Reflexos DT 20 (dispensado para veteranos nas perícias do livro)'), ('Se falhar', 'Dano de queda pela metade')), 43)
op('Traje de Mergulho', 1, 2, 'Roupa impermeável que cobre quase o corpo todo, com tanque e máscara para 1 hora de oxigênio. Dá +5 em testes de resistência contra efeitos ambientais e resistência a dano químico 5. Ocupa o espaço de uma vestimenta; vestir ou despir é ação completa.',
   l(('Bônus', '+5 em resistência a efeitos ambientais'), ('Resistência', 'Químico 5'), ('Oxigênio', '1 hora'), ('Vestir', 'Ação completa (ocupa uma vestimenta)')), 44)
op('Traje Espacial', 2, 5, 'Roupa impermeável de corpo inteiro para o vácuo, com água e oxigênio para oito horas e proteção contra raios cósmicos e micrometeoros. Dá +10 em testes de resistência contra efeitos ambientais e resistência a dano químico 20. Ocupa o espaço de uma vestimenta; vestir ou despir leva duas rodadas.',
   l(('Bônus', '+10 em resistência a efeitos ambientais'), ('Resistência', 'Químico 20'), ('Suprimento', '8 horas de água e oxigênio'), ('Vestir', 'Duas rodadas (ocupa uma vestimenta)')), 44)

# ---------------------------------------------------------------- MEDICAMENTOS (p.43) — categoria nova
MED = [
    ('Antibiótico', 'Fortalece a imunidade contra vírus e bactérias.', 'Fortitude +5 contra doença', 'Vale para o próximo teste de Fortitude contra os efeitos de uma doença feito até o fim do dia.'),
    ('Antídoto', 'Ajuda o corpo a lidar com venenos.', 'Fortitude +5 contra veneno', 'Vale para o próximo teste de Fortitude contra os efeitos de um veneno feito até o fim do dia. Um antídoto feito para um veneno específico, em vez disso, remove o veneno por completo.'),
    ('Antiemético', 'Combate náuseas.', 'Remove enjoado e +5 contra enjoado', 'Remove a condição enjoado e dá +5 em testes para evitá-la até o fim da cena. A critério do mestre, funciona contra outras condições causadas por náuseas e vômitos.'),
    ('Antihistamínico', 'Reduz reações alérgicas perigosas.', 'Teste contra alergia +5', 'Dá +5 no próximo teste contra os efeitos de uma alergia feito até o fim do dia.'),
    ('Anti-inflamatório', 'Reduz inflamação, dor e inchaço.', 'Cura 1d8+2 PV temporários', 'Fornece 1d8+2 PV temporários.'),
    ('Antitérmico', 'Reduz febre e alivia dor de cabeça.', 'Novo teste contra condição mental', 'Permite um novo teste contra uma condição mental que o usuário esteja sofrendo. Só funciona uma vez por cena.'),
    ('Broncodilatador', 'Auxilia na respiração.', 'Contra asfixiado e fatigado +5', 'Dá +5 em testes para evitar as condições asfixiado ou fatigado feitos até o fim do dia.'),
    ('Coagulante', 'Aumenta a capacidade de coagulação.', 'Estabilizar sangrando +5', 'Dá +5 em testes para se estabilizar da condição sangrando feitos até o fim do dia. Usado junto com um teste de Medicina para remover a condição morrendo, também dá +5 nesse teste.'),
]
for n, intro, efx, regra in MED:
    add('medicamento', 'medicamento', n, {'tipo': 'consumivel', 'catg': 1, 'esp': 0.5,
        'desc': f'Medicamento. {intro} Ação padrão e o medicamento para aplicar em você ou em um ser adjacente. {regra}',
        'fx': l(('Efeito', efx), ('Uso', 'Ação padrão (você ou ser adjacente)'))}, 43)

# ---------------------------------------------------------------- ITENS PARANORMAIS (p.44-46)
CAT_FIM = {'Sangue': 'derrete e vira uma gosma vermelha e pulsante, inútil.', 'Morte': 'envelhece rapidamente até se desintegrar em pó.',
           'Conhecimento': 'é inexistido da Realidade.', 'Energia': 'vibra até implodir e se tornar inútil.'}
CAT_EX = {'Sangue': 'larvas e vermes, coração coberto de arame farpado que bate sozinho, faca de um serial killer famoso',
          'Morte': 'crânio pequeno com Lodo escorrendo, paranormal apodrecido, raízes mortas que se movem, filhote preso numa gaiola',
          'Conhecimento': 'pergaminho com sigilos, joias paranormais, balança dourada que nunca se move, um Existido inofensivo aprisionado',
          'Energia': 'cubo mágico que nunca para de se embaralhar, cartas que mudam, uma brasa que nunca se apaga, celular com vírus paranormal, bola plasmática'}
CATS = [('Ampliador', 'Aumenta o alcance do ritual em um passo (de curto para médio, de médio para longo ou de longo para extremo) ou dobra a área de efeito. Ex.: uma Dissonância Acústica ampliada passa a alcance longo ou área de 12m de raio.', 'Alcance +1 passo ou área dobrada'),
        ('Perturbador', 'A DT para resistir ao ritual aumenta em +2.', 'DT do ritual +2'),
        ('Potencializador', 'O dano do ritual aumenta em um dado do mesmo tipo.', 'Dano +1 dado do mesmo tipo'),
        ('Prolongador', 'A duração do ritual dobra (ex.: Distorcer Aparência prolongado dura duas cenas). Não funciona em rituais instantâneos ou sustentados.', 'Duração dobrada')]
for el in ['Conhecimento', 'Energia', 'Morte', 'Sangue']:
    for tp, regra, efx in CATS:
        add('paranormal', 'catalisador ritualístico · ' + el, f'Catalisador Ritualístico de {el} ({tp})', {'tipo': 'paranormal', 'catg': 1, 'esp': 0.5, 'elemento': el,
            'desc': f'Componente ritualístico de {el} alterado por exposição paranormal, mais eficiente. É consumido ao ser usado. Você precisa empunhá-lo e só usa um catalisador por ritual; não pode ser improvisado (Improvisar Componentes), mas pode ser fabricado em campo. Serve para rituais de {el}. {tp}: {regra} Ao ser consumido, {el.lower() if False else "o catalisador"} {CAT_FIM[el]} Exemplos: {CAT_EX[el]}.',
            'fx': l(('Elemento', el), ('Efeito', efx), ('Uso', 'Empunhado; consumido; 1 por ritual'))}, 44)

def par(nome, cat, esp, desc, fx, pag, **x):
    d = {'tipo': x.pop('tipo', 'paranormal'), 'catg': cat, 'esp': esp, 'desc': desc, 'fx': fx}; d.update(x)
    add('paranormal', 'item paranormal', nome, d, pag)
par('Ligação Direta Infernal', 2, 1, 'Fios de cobre contaminados com Sangue e Energia. Ação completa para ligar um veículo sozinho: os fios invadem os controles e animam o veículo de modo paranormal. Ele ganha resistência a dano 20 (cumulativa com a que já tiver) e imunidade a Sangue, e você recebe +5 em Pilotagem para conduzi-lo. Em troca, o veículo tenta causar o máximo de confusão: as consequências de falhas em Pilotagem são amplificadas a critério do mestre (em geral, dano ou penalidade de falha dobra). Remover a ligação é ação completa.',
    l(('Ativar', 'Ação completa'), ('Veículo', 'RD 20 (soma) e imune a Sangue'), ('Bônus', '+5 em Pilotagem'), ('Custo', 'Falhas em Pilotagem pioram (dano ou penalidade dobra)')), 44)
par('Medidor de Condição Vertebral', 2, 1, 'Coluna vertebral sustentada por Lodo de Morte e revestida de cabos de Energia. Conectar à coluna é ação completa, causa dor e agonia profundas e deixa o usuário atordoado por uma rodada. Conta como vestimenta e dá +2 em Fortitude. Depois de conectado, brilha do vermelho (base) ao verde (topo), indicando a saúde do usuário (verde é a melhor). Sob efeito paranormal, emite pulsos de luz lilás. As informações dão +5 em testes de Medicina feitos para ajudar o usuário.',
    l(('Bônus', '+2 em Fortitude'), ('Bônus', '+5 em Medicina para ajudá-lo'), ('Conectar', 'Ação completa; atordoado por 1 rodada'), ('Uso', 'Vestimenta')), 44,
    ef=[{'a': 'per:Fortitude', 'v': 2}], precisaEq=True)
par('Pé de Morto', 2, 1, 'Botas costuradas com pele de cadáveres amaldiçoados pela Morte: passos leves e quase inaudíveis. Dão +5 em Furtividade. Em cenas de furtividade (p.92), qualquer ação chamativa que envolva apenas se mover (correr, saltar) aumenta a visibilidade em apenas +1.',
    l(('Bônus', '+5 em Furtividade'), ('Furtividade', 'Mover chama pouca atenção: visibilidade só +1'), ('Uso', 'Vestimenta (botas)')), 45,
    ef=[{'a': 'per:Furtividade', 'v': 5}], precisaEq=True)
par('Pendrive Selado', 2, 0.5, 'Gravado com sigilos dourados de Conhecimento. Não pode ser invadido nem afetado por rituais, seres e efeitos de Energia, e por isso serve para invadir outros dispositivos sem ser contaminado pela entidade. Existem outros modelos selados (HDs externos, celulares).',
    l(('Efeito', 'Imune a rituais, seres e efeitos de Energia'), ('Uso', 'Invadir dispositivos sem contaminação')), 45)
par('Valete da Salvação', 1, 0.5, 'Valete de ouros pintado de dourado e coberto de sigilos de Conhecimento. Ação padrão para atirá-lo ao ar: ele voa em alcance médio apontando a melhor rota de fuga e deixa de existir. Gasto numa cena de perseguição (p.90), você é bem-sucedido numa ação de cortar caminho.',
    l(('Efeito', 'Aponta a melhor rota de fuga e some'), ('Uso', 'Ação padrão, alcance médio'), ('Perseguição', 'Cortar caminho automático')), 45, tipo='consumivel')

# ---------------------------------------------------------------- ITENS AMALDIÇOADOS (p.57-61, tabela 1.6)
def am(el, nome, cat, esp, desc, pag, tipo='paranormal', **x):
    d = {'tipo': tipo, 'catg': cat, 'esp': esp, 'desc': f'Amaldiçoado de {el}. ' + desc, 'elemento': el, 'amaldicoado': True}; d.update(x)
    add('amaldicoado', el, nome, d, pag)

am('Sangue', 'Conector de Membros', 3, 1, 'Dois anéis metálicos ajustáveis ligados por uma sanfona de tecido humano. Ação padrão para reconectar braço, perna ou cabeça decepados de uma pessoa ou animal, se o ferimento foi há até três rodadas. Não cura PV, mas se o alvo estava morrendo ou morto, perde essas condições e fica inconsciente com 1 PV. Se o conector for removido, a parte é decepada de novo e este item não a reconecta mais. A cada uso há 25% de chance de a parte ganhar "vida própria": perna, o alvo fica lento; braço, –1d20 nos testes que usam aquele braço; cabeça, no início de cada cena de grande tensão (combate, perseguição) o alvo tem 25% de ficar confuso. Há boatos de que esses efeitos podem ser removidos, mas não se sabe como.', 57)
am('Sangue', 'Dose d’A Praga', 3, 1, 'Frasco de vidro reforçado com líquido vermelho espesso que se debate nas paredes. Ação padrão para abrir: você ou um ser adjacente fica sob os poderes paranormais Arma de Sangue, Sangue de Ferro e Sangue Vivo até o fim da cena. Quando acaba, faz Fortitude (DT 20, +5 por dose anterior desde o último interlúdio). Se falhar, sofre 2d4 de dano mental, mantém os poderes até o fim da próxima cena e fica sob efeito do ritual Ódio Incontrolável.', 57)
am('Sangue', 'Mandíbula Agonizante', 2, 1, 'Parte inferior de um crânio, ainda com músculos e símbolos de sangue, que emite sons de tortura. Ação padrão para pressioná-la e arremessá-la num ponto em alcance médio: ela agoniza aos gritos e cobre qualquer outro som num raio de 30m até o fim da cena. Numa cena de furtividade (p.92), você passa automaticamente num teste para distrair. Criaturas de Sangue são atraídas e precisam passar em Vontade (DT 35) para não ir até ela e comê-la. No fim da cena volta a agonizar baixinho e só pode ser usada de novo depois de você descansar por uma cena.', 57)
am('Sangue', 'Retalho Tenebroso', 2, 1, 'Pedaço retangular de carne com pele e pelos bestiais, cheio de instintos primais. Ação padrão para aplicá-lo no rosto como máscara: você recebe faro e visão no escuro, mas sofre vulnerabilidade a Morte e –2d20 em testes de perícias de interação social (Diplomacia, Enganação etc.). Para cada dia seguido com o retalho, recebe um bônus cumulativo de +1 nas rolagens de dano. Custo: ele tenta se alimentar da sua carne; ao fim de cada dia você perde 1d6 PV (Fortitude DT 15, +5 a cada teste adicional em sequência, evita). Remover exige ação padrão e passar no mesmo teste; se falhar, perde 1d6 PV. A perda de vida causada pelo retalho só pode ser recuperada depois de removê-lo. Ele se solta sozinho se quem o usa morrer.', 57)
am('Morte', 'Ampulheta do Tempo Sofrido', 2, 1, 'Ampulheta de madeira trabalhada com areia negra; os grãos viram formas humanoides que erguem os braços em desespero. Empunhando-a, gaste 5 PE para receber de imediato os benefícios de uma ação de interlúdio à sua escolha. Depois de usada, só pode ser usada de novo quando você gastar uma ação de interlúdio para devolver o tempo que a Morte emprestou.', 58)
am('Morte', 'Injeção de Lodo', 2, 0.5, 'Velha seringa de bronze enferrujado com agulha grande cheia do Lodo preto da Morte. Ação padrão e o conteúdo da seringa para injetar o Lodo em você ou em um ser adjacente voluntário. Até o fim da cena, o ser fica vulnerável a dano balístico e de Energia, mas na próxima vez em que for reduzido a 0 PV nesta cena, em vez disso fica com 1 PV.', 59)
am('Morte', 'Instantâneo Mortal', 2, 0.5, 'Fotografia (em papel, quadro ou imagem digital) de um dos últimos momentos de uma pessoa antes da morte, como um condenado na forca. Cada instantâneo retrata pessoas e mortes diferentes. Empunhando-o ao fazer teste de perícia para procurar pistas, olhe fixamente a imagem e gaste 1 PE: se a perícia tem relação com as circunstâncias da morte retratada, a imagem se move e aponta uma direção útil, dando +1d20 no teste. Ex.: Crime, se o instantâneo mostra um criminoso. O mestre decide quais perícias se relacionam.', 59)
am('Morte', 'Projétil de Lodo, curto', 1, 1, 'Munição forjada com Lodo no processo de fundição, que carrega a Morte e é poderosa contra criaturas de Sangue. Versão curta (para armas de balas curtas). Usar o projétil troca todo o dano da arma para Morte; ao fim da cena, a arma se degrada, consumida pelo tempo, até ser desfeita por completo.', 59, tipo='municao')
am('Morte', 'Projétil de Lodo, longo', 2, 1, 'Munição forjada com Lodo no processo de fundição, que carrega a Morte e é poderosa contra criaturas de Sangue. Versão longa (para armas de balas longas). Usar o projétil troca todo o dano da arma para Morte; ao fim da cena, a arma se degrada, consumida pelo tempo, até ser desfeita por completo.', 59, tipo='municao')
am('Morte', 'Rádio Chiador', 2, 1, 'Rádio gravador de bolso empoeirado que captou inúmeras vidas se esvaindo. Funciona com pilhas que duram doze horas antes de virarem Lodo preto. Ligado, chia se houver criatura Paranormal em alcance extremo; o chiado fica mais alto conforme ela se aproxima, o que permite estimar direção e categoria de alcance. Criaturas Paranormais tendem a ser atraídas pelo chiado quando o ouvem. As funções normais do rádio não funcionam, mas ele pode ficar desligado para não fazer barulho.', 59)
am('Conhecimento', 'Câmera Obscura', 3, 1, 'Polaroid Model 95, uma das câmeras de aura paranormal mais antigas e usadas; capturou tantas auras que ficou poderosa contra criaturas fantasmagóricas. Tem a modificação Lente de Revelação, mas a DT para resistir ao efeito aumenta em +10. Além disso, se a criatura falhar, sofre 6d6 de dano de frio conforme partes da sua forma são inexistidas. Só criaturas com alguma habilidade de invisibilidade, incorporeidade ou camuflagem sofrem esse dano.', 59)
am('Conhecimento', 'Enxame Fantasmagórico', 3, 1, 'Manto leve e quase invisível de traças e mariposas esbranquiçadas, tecido por algum bruxo de séculos atrás. Vestido, deixa o usuário invisível (veja p.125). Em troca, o usuário é o alimento das traças: enquanto vestir o manto, sofre 1 ponto de dano mental no início de cada um dos seus turnos, que ignora qualquer resistência a dano.', 60)
am('Conhecimento', 'Repositório do Fracasso', 2, 1, 'Caixinha de madeira que parece um antigo porta-joias, decorada com figuras espectrais de desespero. Sempre que uma criatura Paranormal em alcance médio faz um teste, para cada resultado 1 nos d20 desse teste o repositório recebe uma carga, até 6 cargas. Uma vez por rodada, você pode consumir uma carga para recuperar 1d4 PE; cada vez que faz isso, sofre –1 cumulativo em Vontade até o próximo interlúdio.', 60)
am('Conhecimento', 'Tábula do Saber Custoso', 2, 1, 'Tábula marcada com sigilos de Conhecimento que dá o saber do Outro Lado às custas da mente (a tabela do livro a chama de "Tablet do Saber Custoso"). Empunhando-a, você recebe os benefícios de ser treinado em uma perícia por um único teste. Se fizer isso, perde Sanidade igual ao seu valor no atributo-chave dessa perícia.', 60)
am('Energia', 'Arreio Neural', 2, 1, 'Correias de couro e fivelas metálicas que se prendem à cabeça como a cabeçada de um cavalo, expondo os dentes e mantendo os olhos abertos. Aparato amaldiçoado da era vitoriana que converte certas correntes em estímulos cerebrais. Usando-o, sempre que sofrer 5 ou mais pontos de dano de eletricidade ou Energia, você recupera 1 PE. Máximo por dia: o dobro do seu Vigor em PE.', 60)
am('Energia', 'Centrifugador Existencial', 3, 1, 'Dois círculos de cobre concêntricos criados por um inventor desconhecido do século XVII. Ação padrão e 3 PE para ativar: os círculos giram em sentidos opostos e você se divide em duas possibilidades de futuro, recebendo um turno adicional na última contagem de iniciativa da rodada, brevemente em dois lugares ao mesmo tempo. As duas versões são sua "versão verdadeira", e você sorteia qual se dissipa ao fim da rodada. Efeitos que afetem qualquer versão durante a rodada continuam afetando seu personagem, se aplicáveis. O "outro você" não conta como outra pessoa para nenhum efeito de jogo. A cada uso, faça Ocultismo (DT 15, +5 por uso adicional no mesmo dia). Se falhar, você é separado em nível energético e perde metade dos atributos (arredondado para baixo). Recupera 1 ponto de cada atributo ao fim de cada interlúdio.', 60)
am('Energia', 'Espelho Refletor', 2, 1, 'Placa metálica tirada de corpos de criaturas como o Ciborgue e polida ritualisticamente até refletir. Ação de movimento para observar um ponto ou ser fora do seu ângulo de visão, em alcance médio: você recebe +1d20 em Percepção e tem chance de enxergar até objetos e seres com cobertura total. Além disso, ao sofrer dano de Energia, pode sacrificar o espelho para evitar o dano e refleti-lo de volta à origem.', 61)
am('Energia', 'Fuzil Alheio', 4, 2, 'Arma paranormal deixada pelo Estrangeiro e seus Alheios, adquirida por agentes de limpeza. É um fuzil de precisão com mira telescópica e mira laser, que causa dano de Energia e não precisa de munição. Com a mira laser a margem de ameaça é 17 e, com a mira telescópica, o alcance sobe uma categoria (Longo para Extremo).', 61,
   tipo='arma', mc='fogo', arma={'dano': '2d10', 'crit': '17/x3', 'alc': 'Extremo', 'td': 'Energia', 'per': 'Pontaria'})
am('Medo', 'A Primeira Adaga', 3, 1, 'A primeira adaga já usada num ritual: lâmina de pedra polida e cabo de madeira, primitiva como os primeiros sacrifícios. Quem é treinado em Ocultismo reconhece o horror que ela representa. Usada como componente ritualístico, dá ao ritual os efeitos dos catalisadores ampliador, perturbador, potencializador e prolongador (p.44) e faz o tempo de conjuração virar 1 rodada (mesmo com as regras opcionais Conjuração Complexa e Combate Narrativo). Preço: o conjurador perde PV iguais à metade dos seus PV totais (conta como dano para dano massivo; OPRPG p.88). Uma vítima de sacrifício pode pagar esse preço em vida, mas é ato de extrema crueldade ou desespero.', 61)

# ---------------------------------------------------------------- saída
assert len(IT) == 91, len(IT)
nomes = set()
for g, s, n, d in IT:
    assert (g, n) not in nomes, n
    nomes.add((g, n))
q = lambda s: "'" + str(s).replace("'", "''") + "'"
vals = []
for i, (g, sub, nome, d) in enumerate(IT):
    vals.append('(%s,%s,%s,%s,%s,%s,%d,%s::jsonb)' % (q('sah:item:' + g + ':' + nome), q('op'), q(FONTE), q(g), q(sub), q(nome), 1000 + i, q(json.dumps(d, ensure_ascii=False))))
SQL = """-- Etapa 13 — Itens do complemento "Sobrevivendo ao Horror" (SaH v1.1, capítulo 1, págs. 37 a 61)
-- Depois do schema_etapa10_amaldicoados.sql. Re-executável. Todas as linhas levam fonte = 'sah'.
-- Acrescenta o grupo 'medicamento' em livro_itens e cria o índice por fonte.
-- Gerado por tools/livro/gerar_sah_itens.py (não edite as linhas à mão).

alter table public.livro_itens drop constraint if exists livro_itens_grupo_check;
alter table public.livro_itens add constraint livro_itens_grupo_check check (grupo in
  ('arma', 'municao', 'protecao', 'acessorio', 'explosivo', 'operacional', 'paranormal', 'modificacao', 'maldicao', 'amaldicoado', 'medicamento'));
create index if not exists livro_itens_fonte_idx on public.livro_itens(sistema, fonte, grupo, ordem);

insert into public.livro_itens(ref, sistema, fonte, grupo, subgrupo, nome, ordem, dados) values
""" + ',\n'.join(vals) + """
on conflict (ref) do update set sistema = excluded.sistema, fonte = excluded.fonte, grupo = excluded.grupo,
  subgrupo = excluded.subgrupo, nome = excluded.nome, ordem = excluded.ordem, dados = excluded.dados;
"""
raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
with open(os.path.join(raiz, 'schema_etapa13_sah_itens.sql'), 'w', encoding='utf-8') as fh:
    fh.write(SQL)
N = {}
for g, *_ in IT: N[g] = N.get(g, 0) + 1
print(len(IT), 'linhas', N)
