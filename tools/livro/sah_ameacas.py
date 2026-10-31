"""Bestiário do Sobrevivendo ao Horror (SaH v1.1): 12 criaturas do cap. 3 (com o exemplo pronto de Espectro Inesquecido),
o Terminal (missão 2) e 17 novas Ameaças da Realidade. Formato de livro_inimigos.dados. Só o bônus fixo dos testes é guardado
("3O+10" vira 10; a quantidade de dados é o atributo). Habilidades em redação própria. Usado por gerar_sah_livro.py."""

A = []   # (nome, elemento, vd, pagina, dados)

def atk(n, alc, teste, dano): return dict(n=n, alc=alc, teste=teste, dano=dano)
def hab(n, acao, desc): return dict(n=n, acao=acao, desc=desc)
def per(**k): return [dict(n=n.replace('_', ' '), b=b) for n, b in k.items()]

def cria(nome, el, vd, pag, tam, pv, df, desloc, atr, fort, refl, vont, ini, perc, ataques, habs, pericias=None, resist='', vuln='', sentidos='', desc='', pres=None):
    a = dict(zip(('agi', 'for', 'int', 'pre', 'vig'), atr))
    d = dict(tamanho=tam, pv=pv, desloc=desloc, atr=a, fort=fort, refl=refl, vont=vont, ini=ini, perc=perc, pericias=pericias or [],
             resist=resist, vuln=vuln, sentidos=sentidos, ataques=ataques, habilidades=habs, desc=desc, comp='sah', pag=pag)
    d['def'] = df
    if pres: d['habilidades'] = [hab('Presença Perturbadora', 'Passiva', pres)] + d['habilidades']
    A.append((nome, el, str(vd), pag, d))

# ------------------------------------------------------------------ CRIATURAS (cap. 3)
cria('Sepultado', 'Morte', 20, 127, 'Médio', 50, 16, 9, (1, 3, 0, 1, 3), 5, 0, 0, 0, 0,
     [atk('Dedos Ósseos', 'Corpo a corpo (alcance 3m), x3', 5, '1d6+5 corte')],
     [hab('Membros Longos', 'Passiva', 'Apesar de Médio, alcance natural de 3m.'),
      hab('Parte do Cenário', 'Passiva', 'Como caixão em cemitérios, mausoléus e galerias mortuárias, +10 em Furtividade (parece mobília). Quem é treinado em Ocultismo e procura ameaças faz teste DT 20 como reação para sentir uma criatura oculta.'),
      hab('Agarrão', 'Livre', 'Ao acertar dedos ósseos, pode agarrar (teste +5).'),
      hab('Bater Desesperado', 'Padrão', 'Batidas ouvidas a até 90m, como alguém preso tentando sair. Pessoas e animais a até 9m ficam atordoados por 1 rodada (Vontade DT 14 reduz para abalado 1 rodada; quem passa fica imune na cena).'),
      hab('Tragar', 'Completa', 'Agarrando ser Médio ou menor, fecha-o dentro do caixão (agarrado e imóvel, sensação de ser enterrado vivo). Ao ser tragado e no início de cada turno lá dentro: 2d4 de dano mental (Vontade DT 14 metade). Só sai destruindo o Sepultado. Um ser por vez.')],
     per(Furtividade=10), 'Balístico, corte, impacto e perfuração 5; Morte 10', 'Energia', 'Percepção às cegas; escalada 9m',
     pres='DT 15, 2d4 mental; NEX 25%+ é imune.')

cria('Mescla', 'Sangue', 60, 129, 'Grande', 100, 21, 12, (3, 3, 1, 1, 2), 5, 10, 5, 10, 5,
     [atk('Garras', 'Corpo a corpo, x2', 10, '2d6+5 corte'), atk('Cuspe Ácido', 'À distância, Curto', 10, '3d12 Sangue')],
     [hab('Fluidos Repugnantes', 'Passiva', 'Quem causa dano corpo a corpo ou em alcance curto a ela, ou sofre dano de Sangue dela, fica enjoado 1 rodada (Fortitude DT 20 evita).'),
      hab('Percepção Multifacetada', 'Passiva', 'Não pode ser flanqueada nem surpreendida.'),
      hab('Vomitar Ácido', 'Livre', 'Acertando os dois ataques de garra na mesma ação, a vítima sofre +1d12 de Sangue.'),
      hab('Agarrão', 'Reação', 'Acertando as duas garras no mesmo ser, pode agarrar (teste +12).'),
      hab('Camuflagem Sobrenatural', 'Completa', 'Se ninguém a vê, fica imóvel e muda de cor: camuflagem total e +10 em Furtividade.'),
      hab('Incubar Ovos', 'Completa', 'Agarrando, perfura com ferrão (ataque +10). Acertou: incuba 1d4 ovos (Fortitude DT 5 +5 por ovo evita). Doença Sangue Quente modificada com Estágio IV: uma nova Mescla nasce matando a vítima.'),
      hab('Investida Insectoide', 'Completa', 'De um ponto acima de um ser em alcance médio, salta e cai adjacente; conta como investida e faz os dois ataques de garra com o bônus.')],
     per(Acrobacia=10, Atletismo=10, Furtividade=8), 'Imune: químico; balístico, corte e perfuração 10; Sangue 20', 'Morte, fogo e frio',
     'Faro, percepção às cegas (longo); escalada 12m, voo 9m', pres='DT 20, 3d6 mental; NEX 35%+ é imune.')

cria('Espectro Inesquecido (exemplo)', 'Energia', 220, 133, 'Médio', 340, 27, 9, (2, 1, 3, 3, 2), 5, 15, 15, 5, 15,
     [atk('Lâmina Espectral', 'Corpo a corpo, crítico 19', 10, '1d4+31 Energia'), atk('Pistola Sinalizadora Espectral', 'À distância, Curto', 15, '2d6+32 Energia')],
     [hab('Como criar um espectro', 'Passiva', 'Cada espectro vem de um Marcado morto (SaH p.130-132): vira criatura de Energia, VD = 4 x NEX; mantém atributos, perícias, deslocamento, habilidades e ataques (dano vira Energia, +1d20+5 no ataque e dano extra pela tabela 3.1); +5 em Iniciativa e Percepção; PV multiplicados pela tabela; tem PE, não tem Sanidade. Esta ficha é o exemplo do livro (Marcada de NEX 55%).'),
      hab('Pontos de Esforço', 'Passiva', '66 PE.'),
      hab('Balística Avançada', 'Passiva', 'Proficiência com armas táticas de fogo e +2 no dano com elas.'),
      hab('Conhecimento Aplicado', 'Livre', 'Em perícia (menos Luta e Pontaria), 2 PE para usar Intelecto.'),
      hab('Eclético', 'Livre', '2 PE para ter os benefícios de treinado numa perícia, ou 4 PE para veterano.'),
      hab('Investigação Científica', 'Livre', 'Uma vez por cena de investigação, procura pistas com Ciências.'),
      hab('Na Trilha Certa', 'Livre', 'Após sucesso em procurar pistas, 1 PE para +1d20 no próximo (custos e bônus acumulam).'),
      hab('Pensamento Ágil', 'Livre', 'Uma vez por rodada em investigação, 2 PE para procurar pistas de novo.'),
      hab('Perito', 'Livre', 'Ciências e Medicina: 2 PE para +1d6, 3 PE para +1d8 ou 4 PE para +1d10.'),
      hab('Equipe de Trauma', 'Padrão', '2 PE para remover uma condição negativa (menos morrendo) de aliado adjacente.'),
      hab('Paramédico', 'Padrão', '2 PE para curar 2d10 PV ou 3 PE para 3d10, em si ou aliado adjacente.'),
      hab('Aterrorizar', 'Completa', 'Pessoas e animais em alcance curto: 2d8 de dano mental (Vontade DT 15 metade).'),
      hab('Enigma de Medo', 'Passiva', 'Cada espectro surge de uma morte imprevisível de um Marcado; o que o dissipa está ligado à personalidade, escolhas e ações dele em vida.')],
     per(Atletismo=5, Ciências=10, Furtividade=10, Intimidação=5, Intuição=10, Investigação=10, Medicina=10, Percepção=10),
     'Balístico, corte, impacto, perfuração, Conhecimento e Morte 15; Energia 25', 'Conhecimento', 'Percepção às cegas, visão no escuro',
     'Elementos: Energia (também Conhecimento e Morte). Tabela 3.1 (VD: DT, mental, Defesa/RD, PV, dano extra): 20-40: 15, 2d8, +2, x2, +5 · 60-100: 20, 3d8, +5, x3, +10 · 120-160: 25, 4d8, +10, x4, +20 · 180-300: 35, 6d8, +15, x5, +30 · 320-400: 40, 8d8, +20, x6, +40.',
     pres='DT 35, 6d8 mental; NEX 75%+ é imune (ou 20 pontos acima do NEX do Marcado).')

cria('Derretido', 'Sangue', 80, 135, 'Enorme', 140, 23, 9, (1, 4, 0, 1, 4), 10, 5, 5, 5, 5, [],
     [hab('Amorfo', 'Passiva', 'Passa por qualquer fresta por onde a água passaria (ralo, porta, encanamento); enquanto se espreme, fica lento.'),
      hab('Liberdade de Espaço', 'Passiva', 'Pode ocupar espaços de outros seres; outros podem passar pelo dele, que conta como terreno difícil.'),
      hab('Matéria Nociva', 'Passiva', 'Quem entra ou começa o turno na área dele: 6d6 de Sangue, lento e enjoado 1 rodada (Fortitude DT 20 metade e evita lento). Uma vez por rodada por ser; também corrói objetos.'),
      hab('Arrastar Repulsivo', 'Padrão', 'Até seu próximo turno, ao se mover arrasta seres e objetos da área (Atletismo DT 20 evita): 4d6 de Sangue e caídos.'),
      hab('Rastro Corrosivo', 'Padrão', 'Até seu próximo turno deixa rastro de ácido (terreno difícil): quem entra ou começa o turno nele sofre 1d6 de ácido (uma vez por rodada).'),
      hab('Simular Corpo', 'Padrão', 'Molda a silhueta como pessoa, animal ou objeto; na penumbra ou escuro, +10 em Furtividade para se esconder e Enganação para disfarce.'),
      hab('Consumir', 'Completa', 'Dissolve um ser inconsciente com 0 PV na sua área e recupera 20 PV.'),
      hab('Deslizar Nojento', 'Completa', 'Fora de espaço apertado, percorre o triplo do deslocamento.')],
     per(Enganação=0, Furtividade=0), 'Imune: balístico, corte, impacto e perfuração; Sangue 20', 'Morte, fogo e químico',
     'Percepção às cegas; escalada 9m', 'Elementos: Sangue e Energia.', pres='DT 20, 4d6 mental; NEX 40%+ é imune.')

cria('Uivar', 'Energia', 100, 137, 'Médio', 100, 20, 12, (3, 0, 3, 3, 1), 5, 10, 10, 10, 10, [],
     [hab('Alterações Climáticas', 'Passiva', 'Num raio de 90m: frio extremo, neblina, neve e vento forte (OPRPG p.290).'),
      hab('Vibrações Térmicas', 'Passiva', 'Invisível e incorpóreo; só faz o assovio do vento gelado. Quem consegue vê-lo enxerga uma silhueta Média vazia e curvada. Imune a dano. Força: não tem.'),
      hab('Granizo Perfurante', 'Movimento', 'Começa granizo. Se usar Congelar na mesma rodada, seres sem cobertura na área sofrem 2d8 de perfuração (Reflexos DT 20 metade); destrói coberturas frágeis.'),
      hab('Congelar', 'Padrão', 'Raio de 90m: 2d8 de frio (Fortitude DT 20 metade). Escurece o céu (penumbra de dia, escuridão à noite), cobre objetos de gelo (–1d20 para manipular itens) e gera granizo, chuva e vendaval até o fim da cena ou da missão.'),
      hab('Beijo Gélido', 'Padrão', 'Ser em alcance corpo a corpo: 6d6 de Energia e lento (Fortitude DT 20 metade). A 0 PV vira estátua de gelo (petrificado; gelo com 20 PV e RD 20/fogo; não cura nem morre, mas dano não de fogo no gelo o deixa morrendo). Ao criar estátua recupera 20 PV; destruir uma estátua tira 10 PV dele, e quem mata o ser congelado sofre 6d6 mental (Vontade DT 20 metade).')],
     [], 'Imune: dano', '', 'Percepção às cegas; voo 12m', pres='DT 20, 4d6 mental; NEX 45%+ é imune.')

cria('Melancolia', 'Conhecimento', 140, 140, 'Minúsculo', 200, 29, 9, (4, 0, 4, 3, 1), 5, 5, 5, 5, 5, [],
     [hab('Parasita Invisível', 'Passiva', 'Invisível e incorpórea, imune a dano; escala uma pessoa sem ser sentida. A vítima evita a infecção com Vontade DT 25 no momento; passou, nem percebe e a criatura procura outra.'),
      hab('Parasitose Melancólica', 'Passiva', 'Doença por contato (Vontade). Estágio I (Medo): abalado. II (Sangue): alquebrado e frustrado. III (Morte): esmorecido. IV (Conhecimento): todas as ações buscam tirar a própria vida. Condições valem mesmo para imunes. DT por estágio: I 25 (Minúsculo), II 30 (Pequeno), III 35 (Médio), IV 40 (Grande). Curada, ainda leva um dia por estágio para melhorar.'),
      hab('Parasitas Poderosos', 'Passiva', 'Quem já consumiu outros fica maior: use a DT do estágio equivalente ao tamanho (até Grande, DT 40).'),
      hab('Enigma de Medo', 'Passiva', 'A vítima precisa perceber o parasita (evento da história ou falhar por 5 ou menos na Vontade). Outros podem notar com Intuição, Medicina, Ocultismo ou Profissão (psicólogo) contra a DT atual. Só efeitos paranormais ajudam: pequenos rituais (Ocultismo, DT atual) reduzem a DT em 5 cada. Chegando a 0, perde invisibilidade, incorporeidade e imunidade, fica vulnerável a todo dano não paranormal e foge ou procura outra vítima.')],
     per(Furtividade=5), 'Imune: dano', '', 'Visão no escuro', 'Elementos: Conhecimento (também Sangue e Morte).', pres='DT 25, 4d8 mental; NEX 50%+ é imune.')

cria('Quibungo', 'Sangue', 160, 143, 'Grande', 320, 34, 15, (4, 4, 1, 3, 4), 10, 10, 5, 10, 10,
     [atk('Garras', 'Corpo a corpo, x4', 20, '2d6+10 corte'), atk('Mordida', 'Corpo a corpo', 20, '3d12+10 perfuração')],
     [hab('Besta da Mata', 'Passiva', 'Em mata fechada, +10 em Furtividade e camuflagem total contra seres além de 9m.'),
      hab('Regeneração Acelerada', 'Passiva', 'Cura acelerada 10/Morte.'),
      hab('Agarrão', 'Reação', 'Ao acertar garras, pode agarrar (teste +22).'),
      hab('Dilacerar', 'Livre', 'Uma vez por rodada, acertando duas garras no mesmo alvo, +1d12+10 de perfuração.'),
      hab('Instintos Bestiais', 'Reação', 'Uma vez por rodada, evita completamente o dano de um ataque à distância ou efeito em área.'),
      hab('Bocarra Torturadora', 'Completa', 'Põe um ser agarrado na boca das costas: continua agarrado, cobertura total para dentro e fora, 1d12+10 de Sangue no início de cada turno do Quibungo. Escapa vencendo agarrar ou Acrobacia, ou causando 25 de dano (cai adjacente). A 0 PV lá dentro só grita; ação completa para engolir e matar (recupera 25 PV). Outros libertam vencendo agarrar (falha: 1d12+10 de perfuração). Enquanto mantém alguém a 0 PV, quem vê sofre 4d8 mental por turno (Vontade DT 25 metade).'),
      hab('Investida Brutal', 'Completa', 'Percorre o dobro do deslocamento (não precisa ser reto); conta como investida e faz dois ataques de garra.')],
     per(Atletismo=10, Furtividade=8, Sobrevivência=20), 'Balístico, impacto, perfuração e Sangue 20', 'Morte',
     'Faro, visão no escuro; escalada e natação 15m', pres='DT 25, 4d8 mental; NEX 55%+ é imune.')

cria('Profundo', 'Energia', 200, 147, 'Enorme', 380, 34, 6, (4, 4, 2, 2, 2), 10, 15, 10, 15, 10,
     [atk('Mordida', 'Corpo a corpo', 25, '4d10+20 perfuração'), atk('Tentáculos', 'Corpo a corpo, x6 (no máximo 2 no mesmo ser)', 25, '2d10+10 impacto')],
     [hab('Camuflagem Submersa', 'Passiva', 'Submerso: camuflagem contra seres a 1,5m, total além disso, e +10 em Furtividade.'),
      hab('Regeneração Acelerada', 'Passiva', 'Cura acelerada 20/Morte e fogo.'),
      hab('Agarrão', 'Reação', 'Ao acertar tentáculo, pode agarrar (teste +30); mantém um agarrado sem perder ataques.'),
      hab('Mastigar', 'Livre', 'Uma vez por rodada, acertando dois tentáculos no mesmo ser, ataque extra de mordida.'),
      hab('Engolir', 'Completa', 'Começando o turno agarrando com tentáculo, testa agarrar (+30): vencendo, engole (agarrado, cego, cobertura total, 2d10 de Sangue + 2d10 de perfuração por turno dele). Escapa vencendo agarrar ou Acrobacia, ou com 30 de dano. Um por vez. Aliados de fora acham o ponto com ação de movimento e Percepção DT 25.'),
      hab('Onda Energética', 'Completa', 'Eletrônicos em 90m enlouquecem (desligam, piscam, explodem); quem porta faz Vontade DT 25 para proteger o seu.')],
     per(Furtividade=10), 'Balístico, corte, impacto, perfuração, Energia e Sangue 20', 'Conhecimento',
     'Percepção às cegas, visão no escuro; natação 15m', 'Elementos: Energia e Sangue.', pres='DT 30, 6d6 mental; NEX 65%+ é imune.')

cria('Memento Mori', 'Morte', 260, 149, 'Médio', 650, 44, 9, (1, 1, 3, 3, 3), 20, 15, 20, 15, 20,
     [atk('Garras', 'Corpo a corpo, x2', 30, '4d10+30 corte')],
     [hab('A Ampulheta da Morte', 'Passiva', 'Já surge com um alvo, cujo tempo de vida escorre na ampulheta. Nas mãos de uma pessoa é item amaldiçoado de Morte indestrutível (1 mão, 1 espaço): ação padrão, 2 PE e 2 de Sanidade revelam o nome do vinculado e um tempo estimado de vida.'),
      hab('Ininterrupto', 'Passiva', 'Não corre (uma ação de deslocamento por rodada), mas nada reduz ou impede seu deslocamento.'),
      hab('Inevitável Fim', 'Passiva', 'A 0 PV não morre: some em cinzas até o fim da cena e pode voltar depois.'),
      hab('Visagem', 'Movimento', 'Três vezes por cena, teletransporta em alcance extremo, ou fica invisível até fazer outra ação que não mover.'),
      hab('Encarar o Abismo', 'Padrão', 'Ser em alcance curto: 4d10+30 de Morte e revela memórias e pensamentos (Vontade DT 35 metade e evita revelar).'),
      hab('Revelar a Ampulheta', 'Padrão', 'Quem vê a ampulheta em 36m: 8d6 de dano mental (Vontade DT 35 metade).'),
      hab('Atrair a Ampulheta', 'Completa', 'Em alcance curto da ampulheta, mesmo sem vê-la, a traz para as mãos.'),
      hab('Enigma de Medo', 'Passiva', 'Não há como escapar dele, mas sem a ampulheta ele persegue o item até recuperá-lo; lendas falam de um ritual para destruí-la e matá-lo de vez.')],
     per(Furtividade=30), 'Balístico, corte, impacto, perfuração e Morte 20', 'Energia', 'Visão no escuro',
     'Elementos: Morte (também Conhecimento).', pres='DT 35, 8d6 mental; NEX 80%+ é imune.')

cria('Rascunho', 'Conhecimento', 300, 151, 'Médio', 750, 48, 15, (2, 2, 5, 5, 2), 20, 15, 25, 15, 25, [],
     [hab('Ele Não Existe', 'Passiva', 'Enquanto alguém o olha diretamente (até por espelho), é invisível, inaudível e incorpóreo e passa sempre em Furtividade. Sem ser observado, perde isso. Lutar sem olhar diretamente dá as penalidades de cego.'),
      hab('Vulnerabilidade à Luz', 'Passiva', 'Em luz que o ilumine por completo: –10 na Defesa, perde resistências e tenta fugir.'),
      hab('Possuir Objeto', 'Movimento', 'Sem ser observado, uma vez por rodada arremessa objeto em ser em alcance médio: 4d6 de impacto (Reflexos DT 35 metade; dobro se muito pesado).'),
      hab('Aterrorizar', 'Padrão', 'Seres à escolha a até 9m: 7d8 de dano mental (Vontade DT 35 metade).'),
      hab('Piscar', 'Completa', 'Três vezes por cena, teletransporta em alcance extremo sem linha de visão; surgindo adjacente a alguém, usa Aterrorizar como ação livre nele.')],
     [], 'Balístico, corte, impacto, perfuração, Conhecimento e Energia 20', 'Sangue', 'Percepção às cegas, visão no escuro',
     'Elementos: Conhecimento e Energia.', pres='DT 35, 7d8 mental; NEX 90%+ é imune.')

cria('Medusa', 'Conhecimento', 320, 153, 'Grande', 380, 50, 12, (5, 5, 4, 5, 3), 20, 20, 25, 20, 25,
     [atk('Garras', 'Corpo a corpo, x2', 35, '8d8+20 corte'), atk('Cauda', 'À distância, Curto', 35, '8d8+40 impacto'), atk('Jato Venenoso', 'À distância, Longo', 35, '8d12 Morte')],
     [hab('Camuflagem Sombria', 'Passiva', 'Na penumbra ou escuro, camuflagem e +10 em Furtividade.'),
      hab('Conhecimento de Eras', 'Passiva', 'Expert em todas as perícias (as não listadas: +20 com 4 dados) e fala com pessoas.'),
      hab('Olhar Petrificante', 'Passiva', 'Quem olha nos olhos dela faz Reflexos DT 40 ou fica petrificado no tempo (parece paralisado; ferimentos não mostram tempo passando). Só matar a Medusa salva. Lutar sem olhar dá as penalidades de cego.'),
      hab('Recuperação Acelerada', 'Passiva', 'Cura acelerada 20, que não cura dano de críticos nem de golpes de corte no pescoço (Defesa 60).'),
      hab('Veneno Mortal', 'Passiva', 'Garras ou jato envenenam: no início de cada turno, Fortitude DT 40; falhou, 4d10 de Morte; passou, se cura.'),
      hab('Agarrão', 'Reação', 'Ao acertar a cauda, pode agarrar (teste +37).'),
      hab('Dilacerar', 'Livre', 'Acertando as duas garras, +8d8 de corte.'),
      hab('Sussurrar Maléfico', 'Padrão', 'Ser em alcance médio: 6d10 de dano mental (Vontade DT 40 metade).'),
      hab('Sugestões Irresistíveis', 'Padrão', 'Ser em alcance médio: Vontade DT 40 ou não consegue deixar de olhar para ela até o início do próximo turno.'),
      hab('Rastejar Imparável', 'Completa', 'Percorre o dobro do deslocamento ignorando terreno difícil; terminando adjacente a alguém, ataca com garras ou cauda como ação livre.')],
     per(Furtividade=20), 'Imune: Conhecimento; corte, impacto, perfuração e Morte 20', 'Sangue', 'Faro, visão no escuro; escalada e natação 12m',
     'Elementos: Conhecimento e Morte.', pres='DT 40, 9d6 mental; NEX 95%+ é imune.')

cria('Amigo Imaginário', 'Morte', 360, 156, 'Grande', 1000, 56, 12, (5, 5, 3, 5, 4), 20, 30, 30, 30, 30,
     [atk('Garras', 'Corpo a corpo, x2', 40, '4d10+10 corte'), atk('Tentáculos', 'À distância, Médio', 40, '4d10+20 impacto')],
     [hab('Quadros', 'Passiva', 'Ligado a sete quadros do Medo. Quem observa um quadro faz Vontade DT 40; falhou, "entra no quadro" (memórias, traumas, ilusões) e sofre 8d8 de dano mental (Vontade DT 40 evita); cada vez a Membrana local piora.'),
      hab('O Sino', 'Passiva', 'Ao aparecer e no início de cada turno dele, quem ouve em alcance extremo fica pasmo 1 rodada (Vontade DT 40 evita e fica imune na cena). Quem falhou e já entrou num quadro não consegue se afastar dele na cena.'),
      hab('Frenesi de Sangue', 'Passiva', 'Machucado: Vigor 5, Fortitude +30 (5 dados), escalada 15m, duas ações padrão e duas de movimento; o Sino passa a dar fome e abstinência: quem falha gasta as ações para morder o ser vivo mais próximo ou a si (todos testam de novo; quem passa fica imune na cena).'),
      hab('Agarrão', 'Reação', 'Ao acertar tentáculo, pode agarrar (teste +42). O tentáculo pode ser destruído (Defesa 30, 50 PV, imune a Morte e Sangue, vulnerável a Energia); destruí-lo tira 50 PV dele.'),
      hab('Derreter', 'Completa', 'Despeja tinta no rosto de um agarrado: 4d10+10 de Morte e 4d10+10 de Sangue (Fortitude DT 40 metade).'),
      hab('Dissolver', 'Completa', 'Envolve um agarrado: 4d10+20 de químico (Fortitude DT 40 metade) e recupera PV igual ao dano.')],
     per(Furtividade=28), 'Imune: Morte e Sangue; balístico, corte, impacto e perfuração 20', 'Energia', 'Percepção às cegas (extremo)',
     'Elementos: Morte e Sangue. Furtividade +48 dentro de um quadro.', pres='DT 40, 8d8 mental.')

cria('O Terminal', 'Morte', 260, 218, 'Colossal', 700, 28, 0, (0, 5, 2, 4, 5), 15, 0, 20, 15, 5,
     [atk('Tentáculos', 'Corpo a corpo (9m), x2', 30, '3d6 impacto + 3d6 Morte')],
     [hab('Corpo Tentacular', 'Passiva', 'Não se move nem pode ser movido; falha automaticamente em Reflexos; sem ação de movimento, mas faz três ações padrão por rodada.'),
      hab('Lamúrio Melancólico', 'Passiva', 'Quem termina o turno a 9m ou menos: Vontade DT 30 ou 1d6 de dano mental e frustrado até o fim do próximo turno.'),
      hab('Troca Equivalente', 'Passiva', 'Sempre que sofre dano, transfere 10 para um casulo com vítima (20 PV cada; a 0 PV a vítima morre). Começa com 8 casulos. Abrir casulo adjacente: ação padrão. Tentáculo do casulo: Defesa 18, 25 PV.'),
      hab('Úlcera Raivosa', 'Passiva', 'No fim de rodada em que sofreu 50+ de dano, cria uma bolha (Defesa 20, 100 PV) que explode em 2 rodadas soltando 2d4 esqueletos de Lodo.'),
      hab('Surto de Negação', 'Reação', 'Uma vez por rodada, nega um efeito negativo de habilidade ou ritual.'),
      hab('Enigma de Medo', 'Passiva', 'Vive num covil protegido por neblina; para enfrentá-lo é preciso um ritual de ações ligadas às histórias que o criaram (missão O Terminal do Fim).')],
     [], 'Balístico, impacto e perfuração 10; Morte 20', 'Energia', 'Percepção às cegas',
     'Criatura da missão 2 (O Terminal do Fim). Reflexos: falha sempre.', pres='DT 30, 8d6 mental; NEX 85%+ é imune.')

# ------------------------------------------------------------------ NOVAS AMEAÇAS DA REALIDADE (p.158-165)
O = 'Outro'
cria('Bêbado Local', O, 10, 158, 'Médio', 6, 12, 6, (1, 1, 0, 0, 1), 5, 0, 0, 0, 5, [atk('Soco', 'Corpo a corpo', 0, '1d3+1 impacto')],
     [hab('Causos e Histórias', 'Passiva', 'Conhece as histórias da região: +5 em Investigação para interrogá-lo se a DT da informação for 20 ou menos.'),
      hab('Espião Involuntário', 'Passiva', 'Pode ser usado como espião por um NPC: quem interage com ele faz Intuição ou Vontade DT 15; falhou, revela algo e o mestre ganha +5 para aumentar a DT de um teste da investigação.'),
      hab('Invisibilidade Social', 'Passiva', 'Sem ação chamativa, notar a presença dele exige Percepção DT 15.')],
     per(Diplomacia=5), 'Químico 1', sentidos='Percepção com –2 dados', desc='Percepção –2O+5; Vontade –2O.')
cria('Burocrata', O, 10, 158, 'Médio', 6, 11, 9, (1, 1, 2, 2, 1), 0, 0, 5, 0, 5, [atk('Soco', 'Corpo a corpo', 0, '1d3+1 impacto')],
     [hab('Atendimento Protocolar', 'Passiva', 'Começa indiferente com desconhecidos; enquanto indiferente ou pior, a pessoa sofre –5 em testes de Intelecto e Presença contra ele.'),
      hab('Burocracia Frustrante', 'Passiva', 'Cada falha em teste de Intelecto ou Presença contra ele custa 1 de Sanidade.'),
      hab('Morosidade', 'Passiva', 'Em cena com tempo contado, cada personagem faz Diplomacia DT 15 ao encontrá-lo; falhou, perde uma rodada.'),
      hab('Preencha o Formulário', 'Passiva', 'Para interrogá-lo é preciso a perícia certa da área dele (definida pelo mestre); perícia errada falha automaticamente.')],
     per(Diplomacia=5, Profissão=10))
cria('Fazendeiro Isolado', O, 20, 159, 'Médio', 16, 16, 9, (1, 2, 1, 2, 2), 5, 0, 5, 0, 5,
     [atk('Peixeira', 'Corpo a corpo, crítico 19', 5, '1d8+5 corte'), atk('Espingarda', 'À distância, Curto, crítico x3', 5, '4d6 balístico')],
     [hab('De Sol a Sol', 'Passiva', 'Não fica inconsciente com 0 PV.'),
      hab('Histórias de Pescador', 'Passiva', 'Se o grupo compartilhar a investigação, pode fazer revisar o caso com Profissão (fazendeiro) e dar uma pista.'),
      hab('Resiliência do Campo', 'Passiva', 'Usa Profissão (fazendeiro) no lugar de perícias de Força ou Presença.'),
      hab('Atiçar os Cães', 'Movimento', 'Manda os cães num alvo em alcance curto: o próximo ataque que acertar causa +1d8 de perfuração e derruba (Luta DT 15 evita).')],
     per(Profissão=10))
cria('Investigador', O, 40, 159, 'Médio', 68, 18, 9, (2, 1, 2, 1, 2), 0, 5, 5, 5, 5,
     [atk('Soco', 'Corpo a corpo', 10, '1d3+1 impacto'), atk('Revólver', 'À distância, Curto, crítico 19/x3', 10, '2d6+6 balístico')],
     [hab('Fonte de Informações', 'Passiva', 'Amigável, uma vez por interlúdio dá +5 numa ação de revisar caso.'),
      hab('Olhar do Investigador', 'Movimento', 'Investigação DT 15 num ser em alcance médio: passou, +1d6 de dano contra ele até o fim da cena.')],
     per(Crime=5, Diplomacia=5, Furtividade=5, Intuição=5, Investigação=5))
cria('Médico', O, 20, 160, 'Médio', 14, 13, 9, (1, 1, 2, 2, 1), 5, 0, 5, 0, 5, [atk('Bisturi', 'Corpo a corpo, crítico 18', 5, '1d4+1 corte')],
     [hab('Conhecimento Anatômico', 'Passiva', 'Quem é atingido pelo bisturi fica atordoado 1 rodada e sangrando (Fortitude DT 15 evita; atordoa uma vez por cena por pessoa).'),
      hab('Tratar Ferimentos', 'Padrão', 'Cura 2d10+2 PV de si ou de ser adjacente (uma vez por dia por ser).')],
     per(Ciências=5, Medicina=10))
cria('Religioso', O, 40, 160, 'Médio', 32, 15, 9, (1, 1, 2, 3, 1), 0, 0, 5, 5, 5, [atk('Pancada', 'Corpo a corpo', 5, '1d3+1 impacto')],
     [hab('Fé Inabalável', 'Passiva', '+10 em Vontade contra efeitos paranormais (inclusive rituais).'),
      hab('Potência da Voz', 'Passiva', 'Com microfone ou amplificador, o alcance das habilidades sobe um passo e a DT +5.'),
      hab('Seguidores', 'Passiva', 'Sempre com 1d4+1 devotos (ficha de iniciado, OPRPG p.286).'),
      hab('Voz Guia', 'Padrão', 'Pessoa em alcance curto que o ouve recebe bônus no próximo teste de perícia até o fim da próxima rodada.'),
      hab('Voz Acusadora', 'Padrão', 'Pessoa em alcance curto: 3d6 de dano mental e alquebrada (Vontade DT 15 metade e evita a condição).'),
      hab('Sacrifício Sagrado', 'Reação', 'Uma vez por rodada, ao sofrer dano, troca de lugar com seguidor adjacente, que sofre o dano.')],
     per(Diplomacia=5, Intuição=5, Religião=5))
cria('Predador Sofisticado', O, 60, 161, 'Médio', 60, 21, 9, (3, 3, 2, 3, 1), 5, 10, 10, 5, 10,
     [atk('Navalha', 'Corpo a corpo, x2, crítico 19/x3', 10, '1d8+13 corte'), atk('Machado', 'Corpo a corpo, x2, crítico x3', 10, '2d8+13 corte'),
      atk('Pistola Silenciada', 'À distância, Curto, x2, crítico x3', 10, '1d12+13 balístico')],
     [hab('Escondido em Plena Vista', 'Passiva', 'Em lugares movimentados, usa Enganação no lugar de Furtividade e não sofre penalidades por ações chamativas furtivo.'),
      hab('Recursos Abundantes', 'Passiva', 'Entra em lugares e documentos restritos e escapa de crimes menores; para os graves arranja bode expiatório (a critério do mestre).'),
      hab('Sorriso Sedutor', 'Passiva', 'Quem não sabe que ele é assassino fica desprevenido contra ele e sofre –1 dado em testes contra ele.'),
      hab('Ataque Furtivo', 'Livre', 'Uma vez por rodada, +3d6 contra desprevenidos ou flanqueados (corpo a corpo ou alcance curto).'),
      hab('Guarda-costas', 'Padrão', 'Uma vez por cena chama 1d4+1 capangas (OPRPG p.284), que entram na próxima rodada.')],
     per(Diplomacia=10, Enganação=10, Intimidação=10), desc='Serial killer.')
cria('Caçador de Gente', O, 80, 162, 'Médio', 80, 23, 9, (2, 3, 1, 1, 3), 10, 10, 5, 10, 5,
     [atk('Pancada', 'Corpo a corpo, x2', 15, '1d4+15 impacto'), atk('Machado', 'Corpo a corpo, x2, crítico x3', 15, '2d8+15 corte'),
      atk('Motosserra', 'Corpo a corpo, x2, crítico x4', 15, '3d6+15 corte')],
     [hab('Abrutalhado', 'Passiva', 'Usa itens de duas mãos com uma e itens de criaturas Grandes sem penalidade. Machucado, RD 10/paranormal.'),
      hab('Área de Caça', 'Passiva', 'Na área isolada onde caça, +1d20 em testes de perícia.'),
      hab('Faro para Humanos', 'Passiva', '+2d20 em Sobrevivência envolvendo pessoas e sente humanos pelo cheiro (faro).'),
      hab('Ataque Furtivo', 'Livre', 'Uma vez por rodada, +4d6 contra desprevenidos ou flanqueados.'),
      hab('Imparável', 'Movimento', 'Anula efeitos que reduzem seu deslocamento (outras consequências continuam).'),
      hab('Assustar', 'Padrão', 'Quem o vê ou ouve em alcance curto: 4d6 de dano mental (Vontade DT 20 metade).'),
      hab('Fatalidade', 'Padrão', 'Um ataque de pancada: se acertar, além do dano causa ferimento debilitante (SaH p.105). Uma vez por cena por ser.')],
     per(Atletismo=10, Sobrevivência=10), desc='Serial killer.')
cria('Artista da Morte', O, 140, 162, 'Médio', 150, 27, 9, (3, 1, 3, 3, 1), 5, 15, 15, 15, 15,
     [atk('Bisturi', 'Corpo a corpo, x2, crítico 19/x4', 15, '1d4+17 corte')],
     [hab('Matar é uma Arte', 'Passiva', 'Usa Artes no lugar de qualquer perícia envolvendo mentes e corpos humanos (necropsia, persuadir). Com horas numa cena de crime, troca Investigação por Artes com +1d20.'),
      hab('Cenas Imprevisíveis', 'Passiva', 'Se quis disfarçar a morte, testes por pistas na cena têm DT +5. Se quis deixar marca, quem vê fica enjoado e, sem sair, sofre 4d8 de dano mental (Vontade DT 25 metade e evita a condição).'),
      hab('Ataque Furtivo', 'Livre', 'Uma vez por rodada, +7d6 contra desprevenidos ou flanqueados.'),
      hab('Discurso Artístico', 'Padrão', 'Quem o ouve em alcance curto: 4d8 de dano mental, alquebrado e frustrado (Vontade DT 25 metade e evita frustrado). Uma vez por cena por pessoa.')],
     per(Artes=15, Enganação=15, Furtividade=15), desc='Serial killer.')
cria('Ariranha', O, 20, 163, 'Médio', 32, 16, 12, (2, 1, 0, 1, 2), 0, 5, 0, 5, 5, [atk('Mordida', 'Corpo a corpo', 5, '2d4+2 corte')],
     [hab('Evasão', 'Passiva', 'Passando em Reflexos que reduziria o dano à metade, não sofre dano.'),
      hab('Táticas Familiares', 'Passiva', '+2 no ataque e dano para cada outra ariranha atacando o mesmo alvo na rodada.')],
     sentidos='Faro, visão na penumbra; natação 9m')
cria('Cavalo', O, 10, 163, 'Grande', 12, 13, 15, (1, 3, 0, 1, 2), 0, 5, 0, 5, 5, [atk('Cascos', 'Corpo a corpo', 5, '2d4+3 impacto')],
     [hab('Montaria', 'Passiva', 'Treinado em Adestramento usa como montaria: aliado que deixa o deslocamento em 15m e dá uma ação extra por rodada só para se deslocar.')],
     sentidos='Faro, visão na penumbra')
cria('Enxame de Tocandiras', O, 20, 164, 'Médio', 22, 16, 6, (1, 0, 0, 1, 0), 0, 5, 0, 5, 5, [],
     [hab('Enxame', 'Passiva', 'Entra no espaço de outros; no fim do turno causa 4d4 de perfuração a quem estiver no espaço. Imune a manobras e efeitos de alvo único sem dano; metade do dano de armas, +50% de efeitos em área.'),
      hab('Dor Debilitante', 'Passiva', 'Quem sofre dano dele fica com –1d20 em todos os testes (Fortitude DT 20 evita) até uma ação de dormir ou um antídoto.'),
      hab('Por Dentro das Roupas', 'Passiva', 'Quem sai do espaço continua sofrendo 2d4 até gastar uma ação de movimento para se livrar das formigas.')],
     sentidos='Visão na penumbra; escalada 6m', desc='Fortitude –2O.')
cria('Gorila', O, 40, 164, 'Grande', 70, 19, 9, (2, 3, 0, 1, 3), 5, 5, 0, 5, 5, [atk('Pancada', 'Corpo a corpo, x2', 10, '1d6+3 impacto')],
     [hab('Morder', 'Livre', 'Acertando as duas pancadas no mesmo ser, ataca com mordida (+10, 1d6+4 corte).')],
     per(Atletismo=5), sentidos='Faro, visão na penumbra; escalada 9m')
cria('Leão', O, 60, 164, 'Grande', 80, 18, 15, (3, 3, 0, 2, 2), 5, 10, 5, 10, 10,
     [atk('Garras', 'Corpo a corpo, x2, crítico 19', 10, '1d6+4 corte'), atk('Mordida', 'Corpo a corpo', 10, '1d8+4 corte')],
     [hab('Agarrão', 'Livre', 'Acertando mordida em ser Médio ou menor, pode agarrar (teste +12).'),
      hab('Bote', 'Completa', 'Investida com mordida e as duas garras no mesmo alvo, todos com o bônus.')],
     per(Atletismo=10, Furtividade=8), sentidos='Faro, visão na penumbra')
cria('Lobo', O, 20, 165, 'Médio', 18, 15, 12, (3, 3, 0, 1, 2), 5, 5, 0, 5, 5, [atk('Mordida', 'Corpo a corpo', 5, '1d6+4 corte')],
     [hab('Táticas de Alcateia', 'Passiva', 'Flanqueando, +1d20 extra no ataque e +1d6 de dano na mordida.'),
      hab('Derrubar', 'Livre', 'Acertando a mordida, pode derrubar (teste +5).')],
     per(Sobrevivência=10), sentidos='Faro, visão na penumbra')
cria('Touro', O, 20, 165, 'Grande', 38, 15, 12, (1, 3, 0, 1, 2), 5, 0, 0, 0, 5, [atk('Chifres', 'Corpo a corpo', 5, '2d6+6 perfuração')],
     [hab('Atropelamento', 'Completa', 'Até o dobro do deslocamento em linha reta passando por seres menores: 2d6+6 de impacto e caídos (Reflexos DT 15 metade e evita). Recarga: movimento.')],
     sentidos='Faro, visão na penumbra')
cria('Urso Pardo', O, 60, 165, 'Grande', 90, 19, 12, (1, 3, 0, 2, 3), 10, 5, 0, 5, 5,
     [atk('Garras', 'Corpo a corpo, x2, crítico 19', 10, '1d6+4 corte'), atk('Mordida', 'Corpo a corpo', 10, '1d8+4 corte')],
     [hab('Agarrão', 'Livre', 'Acertando mordida em ser Médio ou menor, pode agarrar (teste +12).')],
     per(Atletismo=10), 'Balístico, corte, impacto e perfuração 2', sentidos='Faro, visão na penumbra')
