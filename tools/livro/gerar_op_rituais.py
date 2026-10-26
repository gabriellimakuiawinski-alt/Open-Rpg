#!/usr/bin/env python3
"""Gera schema_etapa6b_rituais.sql: os 82 rituais do Livro de Regras de Ordem Paranormal (v1.2).
Textos resumidos (só a mecânica), no formato de poder da ficha (tipo 'ritual').
Uso: python3 tools/livro/gerar_op_rituais.py   (na raiz do repositório)
Obs.: o símbolo de dado do livro (+O / –O) vira 1d20 / 2d20 etc."""
import json, os

CONH, ENER, MORT, SANG, MEDO = 'Conhecimento', 'Energia', 'Morte', 'Sangue', 'Medo'
ELEM_ORD = {None: -1, CONH: 0, ENER: 1, MORT: 2, SANG: 3, MEDO: 4}
PE_CIRC = {1: 1, 2: 3, 3: 6, 4: 10}
R = []  # (nome, circ, elem, exec, alc, alvo, dur, res, efeito, discente, verdadeiro)

def r(nome, circ, elem, ex, alc, alvo, dur, res, efeito, disc='', verd=''):
    R.append((nome, circ, elem, ex, alc, alvo, dur, res, efeito, disc, verd))

# ============================================================ 1º CÍRCULO
r('Amaldiçoar Arma', 1, None, 'padrão', 'toque', '1 arma corpo a corpo ou pacote de munição', 'cena', '',
  'Ao aprender, escolha o elemento (Conhecimento, Energia, Morte ou Sangue): o ritual passa a ser dele. A arma ou munição causa +1d6 de dano desse elemento.',
  '+2 PE (2º círculo): +2d6.', '+5 PE (3º círculo e afinidade): +4d6.')
r('Compreensão Paranormal', 1, CONH, 'padrão', 'toque', '1 ser ou objeto', 'cena', 'Vontade anula (veja texto)',
  'Tocando objeto com informação, você entende o idioma humano (não símbolos paranormais). Tocando pessoa, comunicam-se como se tivessem idioma comum. Tocando animal, percebe sentimentos básicos. Alvo involuntário faz Vontade.',
  '+2 PE (2º círculo): alcance curto, alvos escolhidos; entende todos.', '+5 PE (3º círculo): alcance pessoal, alvo você; fala, entende e escreve qualquer idioma humano.')
r('Enfeitiçar', 1, CONH, 'padrão', 'curto', '1 pessoa', 'cena', 'Vontade anula',
  'O alvo fica prestativo (não controlado) e você tem +10 em Diplomacia com ele. Alvo hostil ou em combate: +5 no teste dele. Ação hostil sua ou de aliado dissipa o efeito.',
  '+2 PE (2º círculo): em vez do normal, sugere uma ação aceitável e o alvo obedece; o efeito termina ao executar (pode dar uma condição).', '+5 PE (3º círculo): afeta todos os alvos no alcance.')
r('Ouvir os Sussurros', 1, CONH, 'completa', 'pessoal', 'você', 'instantânea', '',
  'Faça uma pergunta de sim ou não sobre uma ação que fará na cena. O mestre rola 1d6 em segredo: 2 a 6, recebe a resposta (sim, não ou sim e não); 1, falha e a resposta é não. Repetir o ritual dá sempre o primeiro resultado.',
  '+2 PE (2º círculo): execução 1 minuto; pergunta sobre evento até 1 dia à frente; 2 a 6 dá resposta ou pista.', '+5 PE (3º círculo): execução 10 minutos, duração 5 rodadas; uma pergunta por rodada (sim, não ou ninguém sabe).')
r('Perturbação', 1, CONH, 'padrão', 'curto', '1 pessoa', '1 rodada', 'Vontade anula',
  'Dá uma ordem; se falhar, o alvo a cumpre no próprio turno. Escolha: Fuja (gasta o turno se afastando), Largue (solta itens, não os pega até seu próximo turno), Pare (pasmo), Sente-se (senta no chão, só levanta no próximo turno), Venha (gasta o turno se aproximando).',
  '+2 PE: alvo 1 ser; comando extra Sofra: 3d8 de Conhecimento e abalado por 1 rodada.', '+5 PE (3º círculo e afinidade): até 5 seres, ou comando Ataque: o alvo agride outro alvo à sua escolha em alcance médio.')
r('Tecer Ilusão', 1, CONH, 'padrão', 'médio', 'ilusão em até 4 cubos de 1,5m', 'cena', 'Vontade desacredita',
  'Cria ilusão visual ou sonora simples (volume de voz por cubo). Sem cheiro, textura ou temperatura. Seres e objetos a atravessam sem dano. Dissipa se você sair do alcance.',
  '+2 PE (2º círculo): até 8 cubos, sustentada; imagem e som combinados, sons complexos, odores e sensações; seres precisam de Vontade para atravessar; ação livre para mover ou alterar.',
  '+5 PE (3º círculo): ilusão de perigo mortal: Vontade ao conjurar e a cada turno seu; falha = acredita e sofre 6d6 de Conhecimento; 2 sucessos seguidos anulam.')
r('Terceiro Olho', 1, CONH, 'padrão', 'pessoal', 'você', 'cena', '',
  'Vê auras paranormais em alcance longo (rituais, itens amaldiçoados e criaturas), sabendo elemento e poder aproximado: fraca (1º círculo, VD até 80), moderada (2º e 3º, VD 81 a 280), poderosa (4º, VD 281+). Ação de movimento: descobre se um ser visto em alcance médio tem poderes ou conjura rituais, e de quais elementos.',
  '+2 PE: duração 1 dia.', '+5 PE: também enxerga objetos e seres invisíveis (formas translúcidas).')
r('Amaldiçoar Tecnologia', 1, ENER, 'padrão', 'toque', '1 acessório ou arma de fogo', 'cena', '',
  'O item funciona acima da capacidade: recebe uma modificação à sua escolha.', '+2 PE (2º círculo): duas modificações.', '+5 PE (3º círculo e afinidade): três modificações.')
r('Coincidência Forçada', 1, ENER, 'padrão', 'curto', '1 ser', 'cena', '',
  'O alvo recebe +2 em testes de perícia.', '+2 PE (2º círculo): alvo aliados à sua escolha.', '+5 PE (3º círculo e afinidade): aliados à sua escolha e bônus +5.')
r('Eletrocussão', 1, ENER, 'padrão', 'curto', '1 ser ou objeto', 'instantânea', 'Fortitude parcial',
  '3d6 de dano de eletricidade e vulnerável por 1 rodada; passou: metade e sem a condição. Contra objeto eletrônico: dobro do dano e ignora resistência.',
  '+2 PE (2º círculo): área linha de 30m: 6d6 de Energia em todos os seres e objetos livres.', '+5 PE (3º círculo): alvos escolhidos; um relâmpago para cada, 8d6 de Energia.')
r('Embaralhar', 1, ENER, 'padrão', 'pessoal', 'você', 'cena', '',
  'Cria 3 cópias ilusórias: +6 na Defesa. Cada ataque que erra remove uma cópia e o bônus cai 2. O oponente precisa ver as cópias (invisível ou olhos fechados: sem bônus).',
  '+2 PE (2º círculo): 5 cópias, bônus +10.', '+5 PE (3º círculo): 8 cópias, bônus +16; cada cópia destruída emite clarão e quem a destruiu fica ofuscado por 1 rodada.')
r('Luz', 1, ENER, 'padrão', 'curto', '1 objeto', 'cena', 'Vontade anula (veja texto)',
  'O objeto emite luz colorida, sem calor, num raio de 9m. Guardado, a luz para. Objeto em posse de pessoa involuntária: Vontade anula.',
  '+2 PE (2º círculo): alcance longo; 4 esferas de luz (6m cada) que você move com ação livre; ser no espaço da esfera fica ofuscado.', '+5 PE (3º círculo): luz cálida; aliados na área +1d20 em Vontade, inimigos ofuscados.')
r('Polarização Caótica', 1, ENER, 'padrão', 'curto', 'você', 'sustentada', 'Vontade anula',
  'Aura magnética. Escolha: Atrair (ação de movimento puxa objeto metálico de espaço 2 ou menor no alcance) ou Repelir (resistência 5 a balístico, corte, impacto e perfuração contra projéteis de espaço 2 ou menor).',
  '+2 PE: expele a energia de uma vez e arremessa até 10 objetos (ou 10 espaços) a até 3m entre si: 1 a 1d6 de impacto por espaço (Reflexos metade); seres arremessados fazem Vontade para evitar; colisão 1d6 por 3m.',
  '+5 PE: alcance médio; ação de movimento levita e move um ser ou objeto de espaço 10 ou menor por até 9m (Vontade anula).')
r('Cicatrização', 1, MORT, 'padrão', 'toque', '1 ser', 'instantânea', '',
  'O alvo recupera 3d8+3 PV, mas envelhece 1 ano.', '+2 PE (2º círculo): cura 5d8+5.', '+9 PE (4º círculo e afinidade com Morte): alcance curto, seres escolhidos, cura 7d8+7.')
r('Consumir Manancial', 1, MORT, 'padrão', 'pessoal', 'você', 'instantânea', '',
  'Suga o tempo de vida ao redor e recebe 3d6 PV temporários até o fim da cena.',
  '+2 PE (2º círculo): 6d6 PV temporários.', '+5 PE (3º círculo e afinidade): área esfera de 6m de raio em você, Fortitude metade: 3d6 de Morte em cada ser vivo e você recebe PV temporários iguais ao dano total.')
r('Decadência', 1, MORT, 'padrão', 'toque', '1 ser', 'instantânea', 'Fortitude metade',
  'O alvo sofre 2d8+2 de dano de Morte.',
  '+2 PE: sem resistência, 3d8+3; você transfere as espirais a uma arma e ataca corpo a corpo: soma o dano da arma e do ritual.', '+5 PE (3º círculo): alcance pessoal, área explosão de 6m de raio, dano 8d8+8.')
r('Definhar', 1, MORT, 'padrão', 'curto', '1 ser', 'cena', 'Fortitude parcial',
  'O alvo fica fatigado; se passar, fica vulnerável.', '+2 PE (2º círculo): em vez disso fica exausto (passou: fatigado).', '+5 PE (3º círculo e afinidade): como discente, em até 5 seres.')
r('Espirais da Perdição', 1, MORT, 'padrão', 'curto', '1 ser', 'cena', '',
  'O alvo sofre –1d20 em testes de ataque.', '+2 PE (2º círculo): –2d20.', '+8 PE (3º círculo): –2d20 e alvo seres escolhidos.')
r('Nuvem de Cinzas', 1, MORT, 'padrão', 'curto', 'nuvem de 6m de raio e 6m de altura', 'cena', '',
  'Fuligem espessa: camuflagem a até 1,5m e camuflagem total a partir de 3m. Vento forte dispersa em 4 rodadas, vendaval em 1. Não funciona sob a água.',
  '+2 PE (2º círculo): você escolhe seres que enxergam através do efeito.', '+5 PE (3º círculo): nuvem quase sólida: deslocamento 3m e –2 em ataques para quem estiver dentro.')
r('Arma Atroz', 1, SANG, 'padrão', 'toque', '1 arma corpo a corpo', 'sustentada', '',
  'A arma fornece +2 em testes de ataque e +1 na margem de ameaça.', '+2 PE (2º círculo): bônus de ataque +5.', '+5 PE (3º círculo e afinidade): +5 em ataque e +2 na margem de ameaça e no multiplicador de crítico.')
r('Armadura de Sangue', 1, SANG, 'padrão', 'pessoal', 'você', 'cena', '',
  '+5 na Defesa, cumulativo com outros rituais mas não com bônus de equipamento.',
  '+5 PE (3º círculo): +10 na Defesa e resistência 5 a balístico, corte, impacto e perfuração.', '+9 PE (4º círculo e afinidade): +15 na Defesa e resistência 10 a esses tipos.')
r('Corpo Adaptado', 1, SANG, 'padrão', 'toque', '1 pessoa ou animal', 'cena', '',
  'Imune a calor e frio extremos, respira na água (ou no ar) e não sufoca em fumaça densa.', '+2 PE: duração 1 dia.', '+5 PE: alcance curto, pessoas ou animais escolhidos.')
r('Distorcer Aparência', 1, SANG, 'padrão', 'pessoal', 'você', 'cena', 'Vontade desacredita',
  'Muda sua aparência (altura, peso, pele, cabelo, voz, impressão digital etc.): +10 em Enganação para disfarce. Não ganha habilidades da nova forma.',
  '+2 PE: alcance curto, alvo 1 ser (involuntário anula com Vontade).', '+5 PE (3º círculo): como discente, seres escolhidos.')
r('Fortalecimento Sensorial', 1, SANG, 'padrão', 'pessoal', 'você', 'cena', '',
  '+1d20 em Investigação, Luta, Percepção e Pontaria.', '+2 PE (2º círculo): inimigos sofrem –1d20 em ataques contra você.', '+5 PE (4º círculo e afinidade): imune a surpreendido e desprevenido, +10 em Defesa e Reflexos.')
r('Ódio Incontrolável', 1, SANG, 'padrão', 'toque', '1 pessoa', 'cena', '',
  'Frenesi: +2 em ataque e dano corpo a corpo e resistência 5 a balístico, corte, impacto e perfuração. Não faz ações calmas (Furtividade, rituais) e deve atacar todo turno, mesmo um aliado se for o único ao alcance.',
  '+2 PE: ao usar agredir, faz um ataque corpo a corpo adicional contra o mesmo alvo.', '+5 PE (3º círculo e afinidade): bônus +5 e o alvo sofre só metade do dano desses tipos.')
r('Cinerária', 1, MEDO, 'padrão', 'curto', 'nuvem de 6m de raio', 'cena', '',
  'Névoa de essência paranormal: rituais conjurados dentro dela têm DT +5.', '+2 PE: rituais conjurados na névoa custam –2 PE.', '+5 PE: rituais conjurados na névoa causam dano maximizado.')

# ============================================================ 2º CÍRCULO
r('Aprimorar Mente', 2, CONH, 'padrão', 'toque', '1 ser', 'cena', '',
  '+1 em Intelecto ou Presença à escolha do alvo (não fornece PE nem perícias treinadas).', '+3 PE (3º círculo): +2.', '+7 PE (4º círculo e afinidade): +3.')
r('Detecção de Ameaças', 2, CONH, 'padrão', 'pessoal', 'esfera de 18m de raio', 'cena', '',
  'Quando ser hostil ou armadilha entra na área, você sente o perigo e pode, com ação de movimento, fazer Percepção (DT 20): se passar, sabe direção e distância.',
  '+3 PE (3º círculo): não fica desprevenido contra perigos detectados e +5 em resistência contra armadilhas.', '+5 PE (4º círculo): duração 1 dia, com os benefícios do discente.')
r('Esconder dos Olhos', 2, CONH, 'livre', 'pessoal', 'você', '1 rodada', '',
  'Fica invisível (com equipamento): camuflagem total e +15 em Furtividade; quem não o vê fica desprevenido. Termina se atacar ou usar habilidade hostil. Luz carregada continua visível.',
  '+3 PE (3º círculo): sustentada; esfera de invisibilidade: você e aliados a até 3m ficam invisíveis.', '+7 PE (4º círculo e afinidade): execução padrão, toque, 1 ser, sustentada; ação hostil não dissipa.')
r('Invadir Mente', 2, CONH, 'padrão', 'médio ou toque', '1 ser ou 2 pessoas voluntárias', 'instantânea ou 1 dia', 'Vontade parcial ou nenhuma',
  'Escolha: Rajada Mental (6d6 de Conhecimento e atordoado por 1 rodada; passou: metade e sem atordoar; atordoa 1 vez por cena) ou Ligação Telepática (elo mental entre duas pessoas, 1 dia).',
  '+3 PE (3º círculo): rajada 10d6; ou ligação em que você usa ação de movimento para ver e ouvir pelo alvo (involuntário suprime 1h com Vontade).', '+7 PE (4º círculo): rajada 10d6 em seres escolhidos; ou ligação entre até 5 pessoas.')
r('Localização', 2, CONH, 'padrão', 'pessoal', 'círculo de 90m de raio', 'cena', '',
  'Encontra pessoa ou objeto (geral ou específico): indica direção e distância do mais próximo. Algo muito específico exige imagem precisa; falha gasta os PE. Chumbo fino bloqueia.',
  '+3 PE: alcance toque, 1 pessoa, 1 hora: descobre o caminho mais direto para entrar ou sair de um lugar.', '+7 PE (4º círculo): área de 1 km de raio.')
r('Chamas do Caos', 2, ENER, 'padrão', 'curto', 'veja texto', 'cena', '',
  'Escolha: Chamejar (arma corpo a corpo +1d6 de fogo), Esquentar (objeto sofre 1d6 de fogo por rodada e passa o dano a quem o segura; ação completa para resfriar), Extinguir (apaga chama Grande ou menor; fumaça de 3m dá camuflagem), Modelar (move chama 9m por rodada com ação livre; 3d6 de fogo em ser atravessado, uma vez por rodada).',
  '+3 PE: sustentada, Reflexos metade; 1x por rodada, ação de movimento para labareda em alvo no alcance curto: 4d6 de Energia.', '+7 PE (3º círculo): como discente com 8d6.')
r('Contenção Fantasmagórica', 2, ENER, 'padrão', 'médio', '1 ser', 'cena', 'Reflexos anula',
  'Três laços de Energia agarram o alvo. Ele pode gastar ação padrão e Atletismo (DT do ritual) para destruir um laço (mais um por 5 acima da DT). Laços: Defesa 10, 10 PV, RD 5, imunes a Energia; afetam incorpóreos.',
  '+3 PE (3º círculo): 6 laços; você escolhe o alvo de cada um (mínimo 2 por alvo).', '+5 PE (3º círculo e afinidade): como discente; cada laço destruído causa 2d6+2 de Energia no alvo agarrado.')
r('Dissonância Acústica', 2, ENER, 'padrão', 'médio', 'esfera de 6m de raio', 'sustentada', '',
  'Todos na área ficam surdos e não conseguem conjurar rituais.', '+1 PE: alvo 1 objeto, que emana silêncio de 3m (objeto de involuntário: Vontade anula).', '+3 PE (3º círculo): duração cena; nenhum som sai da área, mas quem está dentro fala, ouve e conjura normalmente.')
r('Sopro do Caos', 2, ENER, 'padrão', 'médio', 'área varia', 'sustentada', 'veja texto',
  'Escolha: Ascender (ergue ser ou objeto Médio até 30m, 6m por rodada com ação de movimento; vulnerável; involuntário faz Fortitude no início dos turnos), Sopro (cone de 4,5m: empurrar com Ocultismo em alvos Médios ou menores; manter exige ação padrão) ou Vento (área de vento forte; manter exige ação de movimento).',
  '+3 PE: afeta alvos Grandes.', '+9 PE: afeta alvos Enormes.')
r('Tela de Ruído', 2, ENER, 'padrão', 'pessoal', 'você', 'cena', '',
  'Película que dá 30 PV temporários apenas contra dano balístico, de corte, de impacto ou de perfuração. Alternativa: como reação ao sofrer dano, resistência 15 só contra esse dano.',
  '+3 PE: 60 PV temporários / resistência 30.', '+7 PE (4º círculo): alcance curto, 1 ser ou objeto Enorme ou menor: esfera imóvel que nada atravessa (Reflexos evita ser aprisionado).')
r('Desacelerar Impacto', 2, MORT, 'reação', 'curto', '1 ser ou objetos até 10 espaços', 'até chegar ao solo ou cena', '',
  'O alvo cai a 18m por rodada (sem dano). Projétil causa metade do dano. Só funciona em queda livre.', '+3 PE: até 100 espaços.')
r('Eco Espiral', 2, MORT, 'padrão', 'curto', '1 ser', '2 rodadas', 'Fortitude metade',
  'Cópia de cinzas do alvo. No turno seguinte, ação padrão para se concentrar; no segundo turno, ação padrão para descarregar: o alvo sofre dano de Morte igual ao dano que sofreu na rodada de concentração (Fortitude metade).',
  '+3 PE: até 5 seres.', '+7 PE (4º círculo e afinidade): até 3 rodadas (concentra nas duas primeiras, descarrega na terceira).')
r('Miasma Entrópico', 2, MORT, 'padrão', 'médio', 'nuvem de 6m de raio', 'instantânea', 'Fortitude parcial (veja texto)',
  '4d8 de dano químico e enjoado por 1 rodada; passou: metade e sem enjoo.', '+3 PE: 6d8 de Morte.', '+7 PE (3º círculo): duração 3 rodadas; quem inicia o turno na área sofre o dano de novo.')
r('Paradoxo', 2, MORT, 'padrão', 'médio', 'esfera de 6m de raio', 'instantânea', 'Fortitude metade',
  '6d6 de Morte em todos os seres da área.',
  '+3 PE: efeito esfera Média (1,5m) por cena: 4d6 de Morte a quem estiver no mesmo espaço; ação de movimento move 9m; cada ser sofre 1x por rodada.', '+7 PE (4º círculo): 13d6; quem chegar a 0 PV faz Fortitude: falha = reduzido a cinzas (morre).')
r('Velocidade Mortal', 2, MORT, 'padrão', 'curto', '1 ser', 'sustentada', '',
  'O alvo ganha uma ação de movimento adicional por turno (não pode conjurar rituais com ela).', '+3 PE: ação padrão adicional.', '+7 PE (4º círculo e afinidade): alvos escolhidos.')
r('Aprimorar Físico', 2, SANG, 'padrão', 'toque', '1 ser', 'cena', '',
  '+1 em Agilidade ou Força à escolha do alvo.', '+3 PE (3º círculo): +2.', '+7 PE (4º círculo e afinidade): +3.')
r('Descarnar', 2, SANG, 'padrão', 'toque', '1 ser', 'instantânea', 'Fortitude parcial',
  '6d8 de dano (metade corte, metade Sangue) e hemorragia: no início de cada turno, Fortitude; falha = 2d8 de Sangue; 2 sucessos seguidos estancam. Passou no teste inicial: metade e sem hemorragia.',
  '+3 PE (3º círculo): dano 10d8 e hemorragia 4d8.', '+7 PE (3º círculo e afinidade): alvo você, sustentada: seus ataques corpo a corpo causam +4d8 de Sangue e hemorragia automática.')
r('Flagelo de Sangue', 2, SANG, 'padrão', 'toque', '1 pessoa', 'cena', 'Fortitude parcial',
  'Marca com uma ordem (ex.: não ataque meus aliados). A cada rodada que o alvo desobedecer, sofre 10d6 de Sangue e fica enjoado (Fortitude reduz à metade e evita a condição). 2 sucessos seguidos apagam a marca.',
  '+3 PE (3º círculo): alvo 1 ser (exceto criaturas de Sangue).', '+7 PE (4º círculo e afinidade): como discente, duração 1 dia.')
r('Hemofagia', 2, SANG, 'padrão', 'toque', '1 ser', 'instantânea', 'Fortitude metade',
  '6d6 de Sangue no alvo; você recupera PV iguais à metade do dano causado.',
  '+3 PE: sem resistência; ataque corpo a corpo como parte da execução, somando dano; recupera metade do total.', '+7 PE (4º círculo): pessoal, duração cena: a cada rodada, ação padrão para tocar 1 ser: 4d6 de Sangue, recupera metade.')
r('Transfusão Vital', 2, SANG, 'padrão', 'toque', '1 ser', 'instantânea', '',
  'Você sofre até 30 de dano de Sangue para o alvo recuperar a mesma quantidade em PV (não deixa você abaixo de 1 PV).', '+3 PE (3º círculo): até 50.', '+7 PE (4º círculo): até 100.')
r('Proteção contra Rituais', 2, MEDO, 'padrão', 'toque', '1 ser', 'cena', '',
  'Resistência a dano paranormal 5 e +5 em testes de resistência contra rituais e habilidades de criaturas paranormais.',
  '+3 PE (3º círculo): até 5 seres tocados.', '+6 PE (4º círculo): até 5 seres, resistência 10 e +10 nos testes.')
r('Rejeitar Névoa', 2, MEDO, 'padrão', 'curto', 'nuvem de 6m de raio', 'cena', '',
  'Rituais conjurados na área custam +2 PE por círculo e têm a execução aumentada em um passo. Anula Cinerária, a menos que o conjurador dela gaste ação completa por rodada para mantê-la (neutralizando os dois).',
  '+2 PE: DT de resistência contra rituais feitos na área –5.', '+5 PE: como discente; dano de rituais dentro da névoa é sempre o mínimo.')

# ============================================================ 3º CÍRCULO
r('Alterar Memória', 3, CONH, 'padrão', 'toque', '1 pessoa', 'instantânea', 'Vontade anula',
  'Altera ou apaga memórias de até 1 hora atrás (muda detalhes, não reescreve eventos). O alvo as recupera em 1d4 dias.', '', '+4 PE (4º círculo): memórias de até 24 horas.')
r('Contato Paranormal', 3, CONH, 'completa', 'pessoal', 'você', '1 dia', '',
  'Recebe 6d6. Em qualquer teste de perícia, gasta um, rola e soma ao resultado; ao rolar 6, a entidade toma 2 de Sanidade. Sem dados ou SAN 0, o ritual acaba.',
  '+4 PE (4º círculo): d8; ao rolar 8, perde 3 SAN.', '+9 PE (4º círculo e afinidade): d12; ao rolar 12, perde 5 SAN.')
r('Mergulho Mental', 3, CONH, 'padrão', 'toque', '1 pessoa', 'sustentada', 'Vontade parcial (veja texto)',
  'Você fica desprevenido. No início de cada turno seu tocando o alvo, ele faz Vontade; se falhar, responde uma pergunta de sim ou não sem poder mentir.',
  '', '+4 PE (4º círculo): execução 1 dia, alcance ilimitado; exige cuba de ouro com água e máscara (acessório cat. II), informação e objeto pessoal ou foto do alvo.')
r('Vidência', 3, CONH, 'completa', 'ilimitado', '1 ser', '5 rodadas', 'Vontade anula',
  'Por superfície reflexiva, vê e ouve o alvo e o entorno (6m). O alvo faz resistência no início de cada turno dele; 2 sucessos seguidos encerram e o tornam imune por 1 semana. Precisa de informação sobre o alvo; bônus dele na resistência: quase nada sabido +10, algumas informações +5, conhece bem 0, pertence pessoal –5, parte do corpo –10.')
r('Convocação Instantânea', 3, ENER, 'padrão', 'ilimitado', '1 objeto de até 2 espaços', 'instantânea', 'Vontade anula',
  'Convoca para a mão um objeto previamente marcado com o símbolo do ritual. Se estiver com outra pessoa, ela faz Vontade para negar, mas você sabe onde está. Por até 1h pode mandá-lo de volta (ação de movimento).',
  '+4 PE: objeto de até 10 espaços.', '+9 PE: 1 recipiente Médio com itens até 10 espaços, permanente: escondido no Outro Lado, convocado com ação padrão; exige miniatura (utensílio cat. II); você perde 1 PE permanentemente.')
r('Salto Fantasma', 3, ENER, 'padrão', 'médio', 'você', 'instantânea', '',
  'Vira Energia e reaparece em ponto que já observou (sem precisar de linha de efeito). Não age pelo resto do turno. Sem espaço livre, surge no mais próximo.',
  '+2 PE: execução reação: salta para espaço adjacente, +10 na Defesa e Reflexos contra um ataque ou efeito.', '+4 PE: alcance longo; alvo você e até 2 seres voluntários tocados.')
r('Transfigurar Água', 3, ENER, 'padrão', 'longo', 'esfera de 30m de raio', 'cena', 'veja texto',
  'Escolha: Congelar (água vira gelo; nadadores imóveis, Atletismo DT do ritual), Derreter (gelo vira água, termina), Enchente (+4,5m de nível; ou embarcação com +6m de deslocamento), Evaporar (5d8 de Energia em seres vivos, Fortitude metade, Morte dobro; termina), Partir (–4,5m: caminho seco ou redemoinho que prende barcos, Pilotagem DT do ritual).',
  '', '+5 PE: enchente +12m de deslocamento; evaporar 10d8.')
r('Transfigurar Terra', 3, ENER, 'padrão', 'longo', '9 cubos de 1,5m', 'instantânea', 'veja texto',
  'Escolha: Amolecer (teto ou suporte desaba: 10d6 de impacto, Reflexos metade; piso vira terreno difícil), Modelar (objetos simples até Enorme sem mecanismos; paredes dão cobertura total, RD 8 e 50 PV por 3m), Solidificar (lama ou areia vira terra ou pedra; seres agarrados, Atletismo DT do ritual).',
  '+3 PE: 15 cubos.', '+7 PE (4º círculo): afeta também todos os minerais e metais.')
r('Âncora Temporal', 3, MORT, 'padrão', 'curto', '1 ser', 'cena', 'Vontade parcial',
  'No início de cada turno do alvo, Vontade; se falhar, ele não pode se deslocar naquele turno. 2 sucessos seguidos terminam o efeito.', '', '+4 PE (4º círculo): alvo seres à sua escolha.')
r('Poeira da Podridão', 3, MORT, 'padrão', 'médio', 'nuvem de 6m de raio', 'sustentada', 'Fortitude (veja texto)',
  'Ao conjurar e no início de cada turno seu, seres e objetos na área sofrem 4d8 de Morte (Fortitude metade). Quem falha não recupera PV por 1 rodada.', '', '+4 PE: dano 4d8+16.')
r('Tentáculos de Lodo', 3, MORT, 'padrão', 'médio', 'círculo de 6m de raio', 'cena', '',
  'Ao conjurar e no início de cada turno seu, faz agarrar (Ocultismo no lugar de Luta) contra cada alvo na área; vencendo, agarra; se já agarrado, esmaga: 4d6 (metade impacto, metade Morte). Área é terreno difícil; tentáculos imunes a dano.',
  '', '+5 PE: raio 9m e dano 6d6.')
r('Zerar Entropia', 3, MORT, 'padrão', 'curto', '1 pessoa', 'cena', 'Vontade parcial',
  'O alvo fica paralisado (passou: lento). No início de cada turno dele, pode gastar ação completa para novo teste de Vontade e encerrar o efeito.', '+4 PE (4º círculo): alvo 1 ser.', '+11 PE (4º círculo e afinidade): seres escolhidos.')
r('Ferver Sangue', 3, SANG, 'padrão', 'curto', '1 ser', 'sustentada', 'Fortitude parcial',
  'Ao conjurar e no início de cada turno dele, Fortitude; falha = 4d8 de Sangue e fraco; passou = metade e sem fraco. 2 sucessos seguidos terminam.', '', '+4 PE (4º círculo e afinidade): seres escolhidos.')
r('Forma Monstruosa', 3, SANG, 'padrão', 'pessoal', 'você', 'cena', '',
  'Assume forma de criatura de Sangue: tamanho Grande, +5 em ataque e dano corpo a corpo, 30 PV temporários. Equipamento fica inacessível (bônus mantidos). Não fala nem conjura; a cada rodada deve atacar o ser mais próximo (se for aliado, Vontade DT do ritual para escolher).',
  '+3 PE: imunidade a atordoamento, fadiga, sangramento, sono e veneno.', '+9 PE (4º círculo e afinidade): bônus +10 e 50 PV temporários.')
r('Purgatório', 3, SANG, 'padrão', 'curto', 'área de 6m de raio', 'sustentada', 'Fortitude parcial',
  'Poça de sangue: inimigos na área ficam vulneráveis a dano balístico, de corte, de impacto e de perfuração. Quem tenta sair sofre 6d6 de Sangue e faz Fortitude: passou, sai; falhou, perde a ação de movimento.')
r('Vomitar Pestes', 3, SANG, 'padrão', 'médio', '1 enxame Grande (quadrado de 3m)', 'sustentada', 'Reflexos metade',
  'Enxame de criaturas de Sangue surge adjacente. No fim de cada turno seu, causa 5d12 de Sangue a quem estiver no espaço dele (Reflexos metade). Ação de movimento move o enxame 12m.',
  '+2 PE: quem falha no Reflexos fica agarrado (ação padrão com Acrobacia ou Atletismo para escapar).', '+5 PE: enxame Enorme (cubo de 6m) com voo 18m.')
r('Dissipar Ritual', 3, MEDO, 'padrão', 'médio', '1 ser ou objeto, ou esfera de 3m de raio', 'instantânea', '',
  'Teste de Ocultismo: anula rituais ativos no alvo ou na área com DT igual ou menor ao resultado (não afeta efeitos instantâneos). Em item amaldiçoado, torna-o mundano por 1 dia (o portador faz Vontade para negar).')

# ============================================================ 4º CÍRCULO
r('Controle Mental', 4, CONH, 'padrão', 'médio', '1 pessoa ou animal', 'sustentada', 'Vontade parcial',
  'O alvo obedece todos os comandos, exceto ordens suicidas. Vontade no fim de cada turno dele para se livrar; quem passa fica pasmo por 1 rodada (uma vez por cena).', '+5 PE: até 5 pessoas ou animais.', '+10 PE (afinidade com Conhecimento): até 10.')
r('Inexistir', 4, CONH, 'padrão', 'toque', '1 ser', 'instantânea', 'Vontade parcial',
  '10d12+10 de Conhecimento (passou: 2d12 e debilitado por 1 rodada). Se os PV chegarem a 0, o alvo é apagado da existência.', '+5 PE: 15d12+15 (resistido 3d12).', '+10 PE (afinidade): 20d12+20 (resistido 4d12).')
r('Possessão', 4, CONH, 'padrão', 'longo', '1 pessoa viva ou morta', '1 dia', 'Vontade anula',
  'Projeta sua consciência no corpo do alvo e o controla (usa sua ficha com Agilidade, Força, Vigor e deslocamento do alvo). Se ele passar, sabe da tentativa e fica imune por 1 dia. Se um dos dois morrer, a mente sobrevivente fica presa no corpo novo. Voltar ao seu corpo é ação livre.')
r('Alterar Destino', 4, ENER, 'reação', 'pessoal', 'você', 'instantânea', '',
  'Vislumbra o futuro próximo: +15 em um teste de resistência ou na Defesa contra um ataque.', '', '+5 PE: alcance curto, alvo um aliado à sua escolha.')
r('Deflagração de Energia', 4, ENER, 'completa', 'pessoal', 'explosão de 15m de raio', 'instantânea', 'Fortitude parcial',
  '3d10 x 10 de Energia em todos na área e itens tecnológicos quebram. Você não é afetado. Quem passa sofre metade e seus itens voltam após 1d4 rodadas.', '', '+5 PE: afeta apenas alvos à sua escolha.')
r('Teletransporte', 4, ENER, 'padrão', 'toque', 'até 5 seres voluntários', 'instantânea', '',
  'Leva os alvos a um lugar a até 1.000 km. Ocultismo: DT 25 (lugar que visita com frequência), 30 (já visitou uma vez), 35 (só por descrição de alguém). Falha: chega a lugar parecido (até 1d10 x 10 km errado); falha por 5 ou mais: o ritual falha e você fica atordoado por 1d4 rodadas.',
  '', '+5 PE: qualquer local na Terra.')
r('Convocar o Algoz', 4, MORT, 'padrão', '1,5m', '1 pessoa', 'sustentada', 'Vontade parcial, Fortitude parcial',
  'Cria o maior medo do alvo (só ele o vê com nitidez). O algoz surge adjacente a você e flutua 12m em direção à vítima no fim de cada turno seu. Em alcance curto da vítima: Vontade ou abalada. Adjacente: Fortitude; falha = 0 PV; passou = 6d6 de Morte (não reduz a menos de 1 PV). Incorpóreo e imune a dano; some se deixar o alvo morrendo ou for dissipado.')
r('Distorção Temporal', 4, MORT, 'padrão', 'pessoal', 'veja texto', 'veja texto', '',
  'Cria um bolsão temporal de 3 rodadas: você age, mas não se desloca nem interage com seres e objetos. Efeitos contínuos não o afetam e o que você iniciar não afeta o entorno. Efeitos de área mais longos agem normalmente depois.')
r('Fim Inevitável', 4, MORT, 'completa', 'extremo', 'buraco negro de 1,5m de diâmetro', '4 rodadas', 'Fortitude parcial',
  'No início de cada um dos seus 4 turnos, todos a até 90m (você incluído) fazem Fortitude; falha = caído e puxado 30m ao vácuo. Segurar-se em objeto fixo dá +5. Quem inicia o turno tocando o vácuo sofre 100 de Morte por rodada.',
  '+5 PE (afinidade): 5 rodadas; você não é afetado.', '+10 PE (afinidade): 6 rodadas; seres escolhidos não são afetados.')
r('Capturar o Coração', 4, SANG, 'padrão', 'curto', '1 pessoa', 'cena', 'Vontade parcial',
  'Paixão obsessiva por você. No início de cada turno do alvo, Vontade; falha = age para ajudá-lo da melhor forma. 2 sucessos seguidos terminam.')
r('Invólucro de Carne', 4, SANG, 'padrão', 'curto', '1 clone seu', 'cena', '',
  'Cria cópia idêntica, com as mesmas estatísticas e cópia do equipamento mundano. Sem consciência (Intelecto e Presença nulos): só age por ordem (ação de movimento) ou você a controla em transe, usando os sentidos dela. Percepção (DT do ritual) revela a cópia. Desfaz-se com 0 PV ou fora do alcance.')
r('Vínculo de Sangue', 4, SANG, 'padrão', 'curto', '1 ser', 'cena', 'Fortitude anula',
  'Sempre que você sofre dano, o alvo faz Fortitude; falha = você sofre metade e ele a outra metade. Versão inversa: você recebe metade de todo dano que o alvo receberia. Voluntários não testam.')
r('Canalizar o Medo', 4, MEDO, 'padrão', 'toque', '1 pessoa', 'permanente até ser descarregada', '',
  'Escolha um ritual de até 3º círculo que conheça: o alvo o conjura uma vez em forma básica sem pagar PE (formas avançadas com PE próprios). Até ser usado, seus PE máximos diminuem pelo custo dele. Rituais de Medo custam Sanidade igual ao custo em PE.')
r('Conhecendo o Medo', 4, MEDO, 'padrão', 'toque', '1 pessoa', 'instantânea', 'Vontade parcial',
  'Falha: Sanidade do alvo vai a 0 e ele fica enlouquecendo; passou: 10d6 de dano mental e apavorado por 1 rodada. Quem enlouquece vira criatura paranormal a critério do mestre.')
r('Lâmina do Medo', 4, MEDO, 'padrão', 'toque', '1 ser', 'instantânea', 'Fortitude parcial',
  'Golpeia com uma fenda na Realidade: falha = PV a 0 e morrendo; passou = 10d8 de Medo (ignora resistências) e apavorado por 1 rodada. O ferimento nunca cicatriza. Aprender exige poder de trilha específico (Lâmina Paranormal).')
r('Medo Tangível', 4, MEDO, 'padrão', 'pessoal', 'você', 'cena', '',
  'Imune a atordoado, cego, debilitado, enjoado, envenenado, exausto, fatigado, fraco, lento, ofuscado e paralisado, a doenças e venenos; sem dano extra de crítico ou ataque furtivo. Dano balístico, de corte, de impacto ou de perfuração não reduz seus PV abaixo de 1.')
r('Presença do Medo', 4, MEDO, 'padrão', 'pessoal', 'emanação de 9m de raio', 'sustentada', 'Vontade reduz à metade',
  'Ao conjurar e no início do turno de cada alvo na área: 5d8 de dano mental e 5d8 de Medo (Vontade metade nos dois). Quem falha fica atordoado por 1 rodada (uma vez por cena).')

# ============================================================ SQL
assert len(R) == 82, len(R)
def q(s): return "'" + str(s).replace("'", "''") + "'"
R.sort(key=lambda x: (x[1], ELEM_ORD[x[2]], x[0]))
nomes, vals = set(), []
for i, (nome, circ, el, ex, alc, alvo, dur, res, efeito, disc, verd) in enumerate(R):
    assert nome not in nomes, nome
    nomes.add(nome)
    cab = f'Execução: {ex}. Alcance: {alc}. Alvo/área: {alvo}. Duração: {dur}.' + (f' Resistência: {res}.' if res else '')
    desc = cab + ' ' + efeito + (' Discente ' + disc if disc else '') + (' Verdadeiro ' + verd if verd else '')
    dados = {'tipo': 'ritual', 'circ': circ, 'el': el or '', 'pe': PE_CIRC[circ], 'desc': desc, 'ef': []}
    vals.append('(%s,%s,%s,null,%s,%s,%d,%s,%d,%s::jsonb)' % (q('op:ritual:' + nome), q('op'), q('livro-basico'), q('ritual'), q(nome), circ,
                                                               q(el) if el else 'null', 1000 + i, q(json.dumps(dados, ensure_ascii=False))))

SQL = """-- Etapa 6b — Rituais do livro (Ordem Paranormal, Livro de Regras v1.2)
-- Os 82 rituais (1º ao 4º círculo) na tabela livro_habilidades (grupo = 'ritual').
-- Re-executável. Gerado por tools/livro/gerar_op_rituais.py (não edite as linhas à mão).
-- Rode DEPOIS do schema_etapa6_livro.sql.

alter table public.livro_habilidades alter column classe drop not null;       -- ritual não pertence a uma classe
alter table public.livro_habilidades add column if not exists circulo int;     -- 1 a 4 (rituais)
alter table public.livro_habilidades add column if not exists elemento text;   -- Conhecimento, Energia, Morte, Sangue, Medo (null = escolhe ao aprender)
alter table public.livro_habilidades drop constraint if exists livro_habilidades_grupo_check;
alter table public.livro_habilidades add constraint livro_habilidades_grupo_check check (grupo in ('classe', 'poder', 'trilha', 'ritual'));
create index if not exists livro_habilidades_ritual_idx on public.livro_habilidades(sistema, grupo, circulo, elemento);

insert into public.livro_habilidades(ref, sistema, fonte, classe, grupo, nome, circulo, elemento, ordem, dados) values
""" + ',\n'.join(vals) + """
on conflict (ref) do update set sistema = excluded.sistema, fonte = excluded.fonte, classe = excluded.classe, grupo = excluded.grupo,
  nome = excluded.nome, circulo = excluded.circulo, elemento = excluded.elemento, ordem = excluded.ordem, dados = excluded.dados;
"""
raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
with open(os.path.join(raiz, 'schema_etapa6b_rituais.sql'), 'w', encoding='utf-8') as fh:
    fh.write(SQL)
por = {}
for x in R: por[x[1]] = por.get(x[1], 0) + 1
print(len(R), 'rituais', por)
