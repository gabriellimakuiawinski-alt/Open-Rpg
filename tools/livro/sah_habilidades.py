"""Dados de habilidades do complemento Sobrevivendo ao Horror (SaH v1.1): origens, poderes gerais, poderes e trilhas
de classe, classe Sobrevivente, poderes paranormais e rituais. Textos em redação própria (só a mecânica, completa).
Página = página impressa do livro. Usado por gerar_sah_livro.py."""

EF = lambda a, v, nv=False, mn=None: dict({'a': a, 'v': v}, **({'nv': 1} if nv else {}), **({'min': mn} if mn else {}))
H = []   # dict(ref, classe, grupo, trilha, nex, nome, circulo, elemento, pag, dados)

def _add(ref, classe, grupo, nome, pag, dados, trilha=None, nex=None, circulo=None, elemento=None):
    dados = dict(dados, comp='sah', pag=pag)
    H.append(dict(ref=ref, classe=classe, grupo=grupo, trilha=trilha, nex=nex, nome=nome, circulo=circulo, elemento=elemento, dados=dados))

# ======================================================================= ORIGENS (p.7-13)
def origem(nome, per, poder, desc, pag, ef=None):
    _add('op:origem:sah:' + nome, None, 'origem', poder, pag, {'tipo': 'origem', 'pe': 0, 'origem': nome, 'pericias': per, 'desc': desc, 'ef': ef or []})

origem('Amigo dos Animais', ['Adestramento', 'Percepção'], 'Companheiro Animal',
       'Entende intenções e sentimentos de animais e pode usar Adestramento para mudar a atitude deles. Tem um animal de estimação que é um aliado: +2 em uma perícia à sua escolha (aprovada pelo mestre). Em NEX 35% ele também dá o bônus de um tipo de aliado à sua escolha; em NEX 70%, também a habilidade desse tipo de aliado. Se ele morrer: perde 10 de Sanidade permanente e fica perturbado até o fim da cena. Arranjar outro fica a critério do mestre (normalmente entre missões).', 7)
origem('Astronauta', ['Ciências', 'Fortitude'], 'Acostumado ao Extremo',
       'Ao sofrer dano de fogo, frio ou mental, gaste 1 PE para reduzir esse dano em 5. Cada uso seguinte na mesma cena custa +1 PE.', 8)
origem('Chef do Outro Lado', ['Ocultismo', 'Profissão'], 'Fome do Outro Lado',
       'Profissão treinada: cozinheiro. Usa partes de criaturas do Outro Lado como ingredientes (item categoria I, 0,5 espaço; pede no início da missão ou tira de criatura derrotada Pequena ou maior: 1 ingrediente). Ação de interlúdio + 1 ingrediente: prato especial com Profissão (cozinheiro) DT 15 + 1d20 (o mestre esconde o resultado até alguém comer). Passou: RD 10 contra o tipo de dano do elemento da criatura; falhou: vulnerabilidade a esse dano. Dura até o fim da próxima cena. Cada refeição custa 1 de Sanidade permanente. Com a regra opcional de NEX e experiência (SaH p.98), cada parte de criatura diferente ingerida dá +3% de NEX. A Ordem não apoia.', 8)
origem('Colegial', ['Atualidades', 'Tecnologia'], 'Poder da Amizade',
       'Escolha um personagem como melhor amigo. Em alcance médio dele, podendo ao menos trocar olhares, você recebe +2 em todos os testes de perícia. Se ele morrer, seu total de PE cai 1 a cada 5% de NEX até o fim da missão; no início da próxima missão pode escolher outro melhor amigo.', 9)
origem('Cosplayer', ['Artes', 'Vontade'], 'Não É Fantasia, É Cosplay!',
       'Faz testes de disfarce com Artes no lugar de Enganação. Vestindo um cosplay ligado ao teste, recebe +2 nele (ex.: fantasia de gato dá +2 para ser furtivo e se equilibrar).', 9)
origem('Diplomata', ['Atualidades', 'Diplomacia'], 'Conexões',
       '+2 em Diplomacia. Se puder contatar um NPC capaz de ajudar, gaste 10 minutos e 2 PE para trocar um teste de perícia ligado ao conhecimento desse NPC (feito até o fim da cena) por um teste de Diplomacia.', 9, [EF('per:Diplomacia', 2)])
origem('Explorador', ['Fortitude', 'Sobrevivência'], 'Manual do Sobrevivente',
       'Ao testar para resistir a armadilhas, clima, doenças, fome, sede, fumaça, sono, sufocamento ou veneno (inclusive paranormais), gaste 2 PE para +5 no teste. Em interlúdios, sono precário conta como normal.', 9)
origem('Experimento', ['Atletismo', 'Fortitude'], 'Mutação',
       'Resistência a dano 2 e +2 em uma perícia originalmente de Força, Agilidade ou Vigor à sua escolha. Porém sofre –1d20 em Diplomacia.', 9)
origem('Fanático por Criaturas', ['Investigação', 'Ocultismo'], 'Conhecimento Oculto',
       'Pode usar Ocultismo para identificar criatura a partir de imagem, rastros ou indícios (descobre as características, não a identidade nem o tipo). Ao passar num teste de Ocultismo para identificar criatura, recebe +2 em todos os testes contra ela até o fim da missão.', 10)
origem('Fotógrafo', ['Artes', 'Percepção'], 'Através da Lente',
       'Em teste de Investigação ou Percepção olhando por uma câmera ou analisando fotos, gaste 2 PE para +5. Andar olhando pela lente reduz o deslocamento à metade.', 10)
origem('Inventor Paranormal', ['Profissão', 'Vontade'], 'Invenção Paranormal',
       'Profissão treinada: engenheiro. Escolha um ritual de 1º círculo: você tem um invento (categoria 0, 1 espaço) que reproduz a forma básica dele sem gastar PE. Ativar: ação padrão (ou a do ritual, a maior) + Profissão (engenheiro) DT 15, +5 a cada ativação na missão. Falhou: enguiça. Ação de interlúdio de manutenção conserta e volta a DT a 15. Pode trocar o ritual no início de cada missão.', 10)
origem('Jovem Místico', ['Ocultismo', 'Religião'], 'A Culpa é das Estrelas',
       'Escolha um número da sorte de 1 a 6. No início de cada cena, gaste 1 PE e role 1d6: tirou um número da sorte, +2 em testes de perícia até o fim da cena; senão, acrescente mais um número da sorte para a próxima vez. Ao acertar, volta a ter um número só.', 11)
origem('Legista do Turno da Noite', ['Ciências', 'Medicina'], 'Luto Habitual',
       'Sofre metade do dano mental de cenas ligadas à rotina de legista (morte, cadáveres, órgãos), a critério do mestre. Em Medicina para primeiros socorros ou necropsia, gaste 2 PE para +5.', 11)
origem('Mateiro', ['Percepção', 'Sobrevivência'], 'Mapa Celeste',
       'Vendo o céu, sempre sabe os pontos cardeais e chega sem se perder a lugares que já visitou. Em Sobrevivência, gaste 2 PE para rolar de novo e ficar com o melhor. Em interlúdios, sono precário conta como normal.', 12)
origem('Mergulhador', ['Atletismo', 'Fortitude'], 'Fôlego de Nadador',
       '+5 PV; prende a respiração por rodadas igual ao dobro do Vigor; ao passar em Atletismo para nadar, avança o deslocamento normal (não metade).', 12, [EF('pv', 5)])
origem('Motorista', ['Pilotagem', 'Reflexos'], 'Mãos no Volante',
       'Não sofre penalidade em ataques por estar em veículo em movimento. Pilotando, em teste de Pilotagem ou de resistência, gaste 2 PE para +5.', 13)
origem('Nerd Entusiasta', ['Ciências', 'Tecnologia'], 'O Inteligentão',
       'O bônus da ação de interlúdio ler sobe +1 dado (de +1d6 para +2d6).', 13)
origem('Profetizado', ['Vontade'], 'Luta ou Fuga',
       'Perícias: Vontade e mais uma à escolha ligada à premonição. Você sabe como vai morrer (o mestre define a cena em segredo ou junto com você). +2 em Vontade. Quando surge uma referência à premonição, recebe +2 PE temporários até o fim da cena (respeite o texto: não force gatilhos de propósito).', 13, [EF('per:Vontade', 2)])
origem('Psicólogo', ['Intuição', 'Profissão'], 'Terapia',
       'Profissão treinada: psicólogo. Usa Profissão (psicólogo) como Diplomacia. Uma vez por rodada, quando você ou aliado em alcance curto falha em resistência contra efeito que causa dano mental, gaste 2 PE para fazer Profissão (psicólogo) e usar esse resultado no lugar.', 13)
origem('Repórter Investigativo', ['Atualidades', 'Investigação'], 'Encontrar a Verdade',
       'Usa Investigação no lugar de Diplomacia para persuadir e mudar atitude. Em Investigação, gaste 2 PE para +5.', 13)

# ======================================================================= PODERES GERAIS (p.33-36)
# Contam como poderes de todas as classes: quem pode escolher um poder de classe pode escolher um geral.
def geral(nome, desc, pre='', pe=0, ef=None, treina=None, pag=33):
    d = {'tipo': 'poder', 'desc': desc + (' Pré-requisito: ' + pre + '.' if pre else ''), 'pe': pe, 'ef': ef or [], 'geral': 1}
    if treina: d['treina'] = treina
    _add('op:geral:poder:' + nome, 'geral', 'poder', nome, pag, d)

T = lambda p: f'Treinado em {p} (se já for, +2 em {p}). '
geral('Acrobático', T('Acrobacia') + 'Terreno difícil não reduz seu deslocamento nem impede investidas.', 'Agi 2', treina='Acrobacia')
geral('Ás do Volante', T('Pilotagem') + 'Uma vez por rodada, quando um veículo que você pilota sofre dano, faça Pilotagem (DT = ataque ou DT do efeito); passou, evita o dano.', 'Agi 2', treina='Pilotagem')
geral('Atlético', T('Atletismo') + '+3m de deslocamento.', 'For 2', ef=[EF('desloc', 3)], treina='Atletismo')
geral('Atraente', '+5 em Artes, Diplomacia, Enganação e Intimidação contra pessoas que possam se sentir fisicamente atraídas por você.', 'Pre 2')
geral('Dedos Ágeis', T('Crime') + 'Arromba com ação padrão, furta com ação livre (uma vez por rodada) e sabota com ação completa.', 'Agi 2', treina='Crime')
geral('Detector de Mentiras', T('Intuição') + 'Outros sofrem –10 em Enganação para mentir para você.', 'Pre 2', treina='Intuição')
geral('Especialista em Emergências', T('Medicina') + 'Aplica cicatrizantes e medicamentos com ação de movimento e, uma vez por rodada, saca um deles com ação livre.', 'Int 2', treina='Medicina')
geral('Estigmado', 'Ao sofrer dano mental de efeitos de medo, pode trocá-lo por perda de PV de mesmo valor.')
geral('Foco em Perícia', 'Escolha uma perícia (menos Luta e Pontaria): seus testes dela rolam +1d20. Pode escolher outras vezes para perícias diferentes.', 'treinado na perícia escolhida')
geral('Informado', T('Atualidades') + 'Com aprovação do mestre, usa Atualidades no lugar de qualquer perícia em testes envolvendo informações.', 'Int 2', treina='Atualidades', pag=34)
geral('Interrogador', T('Intimidação') + 'Coage com ação padrão, mas só uma vez por cena contra a mesma pessoa.', 'For 2', treina='Intimidação', pag=34)
geral('Inventário Organizado', 'Soma seu Intelecto no limite de espaços. Itens de 0,5 espaço ocupam 0,25 para você.', 'Int 2', ef=[])
geral('Mentiroso Nato', T('Enganação') + 'A penalidade por mentiras muito implausíveis cai para –1d20.', 'Pre 2', treina='Enganação', pag=34)
geral('Observador', T('Investigação') + 'Soma seu Intelecto em Intuição.', 'Int 2', treina='Investigação', pag=34)
geral('Pai de Pet', T('Adestramento') + 'Tem um animal de estimação que é um aliado: +2 em duas perícias à escolha (menos Luta e Pontaria, aprovadas pelo mestre).', 'Pre 2', treina='Adestramento', pag=34)
geral('Palavras de Devoção', T('Religião') + 'Uma vez por cena, 3 PE e ação completa: oração para até o dobro da sua Presença em pessoas; todas recebem resistência a dano mental 5 até o fim da cena.', 'Pre 2', pe=3, treina='Religião', pag=35)
geral('Parceiro', 'Você tem um parceiro (crie nome, aparência, personalidade): um aliado de um tipo à sua escolha (OPRPG p.171). Obedece e se arrisca por você, mas pode ir embora se maltratado. Se o perder, gaste uma folga da Ordem (SaH p.94) para ter outro.', 'treinado em Diplomacia, NEX 30%', pag=35)
geral('Pensamento Tático', T('Tática') + 'Ao passar em Tática para analisar terreno, você e aliados em alcance médio ganham uma ação de movimento extra na 1ª rodada do próximo combate ali (até o fim do dia).', 'Int 2', treina='Tática', pag=35)
geral('Personalidade Esotérica', '+3 PE e treinado em Ocultismo (se já for, +2 em Ocultismo).', 'Int 2', ef=[EF('pe', 3)], treina='Ocultismo', pag=35)
geral('Persuasivo', T('Diplomacia') + 'Ao persuadir, a penalidade por pedir coisas custosas ou perigosas diminui em 5.', 'Pre 2', treina='Diplomacia', pag=35)
geral('Pesquisador Científico', T('Ciências') + 'Usa Ciências no lugar de Ocultismo para identificar criaturas e no lugar de Sobrevivência para identificar animais.', 'Int 2', treina='Ciências', pag=35)
geral('Proativo', T('Iniciativa') + 'Rolando 19 ou 20 em ao menos um dado de Iniciativa, ganha uma ação padrão extra no primeiro turno.', 'Agi 2', treina='Iniciativa', pag=35)
geral('Provisões de Emergência', 'Tem um esconderijo de suprimentos. Uma vez por missão, uma ação de interlúdio recupera o conteúdo: recebe equipamento novo à escolha equivalente à sua patente no início da missão (como uma nova preparação).', pag=35)
geral('Racionalidade Inflexível', 'Usa Intelecto no lugar de Presença como atributo-chave de Vontade e para calcular seus PE.', 'Int 3', pag=35)
geral('Rato de Computador', T('Tecnologia') + 'Hackeia, localiza arquivo ou opera dispositivo com ação completa. Uma vez por cena de investigação, com acesso a computador, faz Tecnologia para procurar pistas sem gastar a rodada.', 'Int 2', treina='Tecnologia', pag=36)
geral('Resposta Rápida', T('Reflexos') + 'Ao falhar em Percepção para não ficar desprevenido, gaste 2 PE para rolar de novo usando Reflexos.', 'Agi 2', treina='Reflexos', pag=36)
geral('Sentidos Aguçados', T('Percepção') + 'Não fica desprevenido contra inimigos que não vê e, ao errar por camuflagem, rola mais uma vez a chance de falha.', 'Pre 2', treina='Percepção', pag=36)
geral('Sobrevivencialista', T('Sobrevivência') + '+2 para resistir a efeitos de clima; terreno difícil natural não reduz seu deslocamento nem impede investidas.', 'Int 2', treina='Sobrevivência', pag=36)
geral('Sorrateiro', T('Furtividade') + 'Não sofre penalidade por se mover normalmente furtivo nem por seguir alguém em lugar sem esconderijo ou sem movimento.', 'Agi 2', treina='Furtividade', pag=36)
geral('Talentoso', T('Artes') + 'Ao impressionar com Artes, o bônus em perícias sobe +1 a cada 5 pontos que o resultado passar da DT.', 'Pre 2', treina='Artes', pag=36)
geral('Teimosia Obstinada', T('Vontade') + 'Em Vontade contra condição mental ou mudança de atitude (como Enfeitiçar), gaste 2 PE para +5.', 'Pre 2', treina='Vontade', pag=36)
geral('Tenacidade', T('Fortitude') + 'Morrendo mas consciente (ao menos 1 PV), faça Fortitude (DT 20, +10 por teste anterior na cena) com ação livre; passou, deixa de estar morrendo.', 'Vig 2', treina='Fortitude', pag=36)
geral('Vitalidade Reforçada', '+1 PV a cada 5% de NEX (ou por nível) e +2 em Fortitude.', 'Vig 2', ef=[EF('pv', 1, True), EF('per:Fortitude', 2)], pag=36)
geral('Vontade Inabalável', '+1 PE a cada 10% de NEX (ou a cada 2 níveis) e +2 em Vontade.', 'Pre 2', ef=[EF('pe', 0.5, True), EF('per:Vontade', 2)], pag=36)
# do livro básico, viram poderes gerais com o SaH (texto do livro básico)
geral('Artista Marcial', 'Do livro básico, agora poder geral. Ataques desarmados causam 1d6 (letal, contam como armas ágeis). Dano sobe para 1d8 em NEX 35% e 1d10 em NEX 70%.')
geral('Combater com Duas Armas', 'Do livro básico, agora poder geral. Empunhando duas armas (ao menos uma leve) e agredindo, faça dois ataques (um com cada). Você sofre –1d20 em todos os ataques até o próximo turno.', 'Agi 3, treinado em Luta ou Pontaria')
geral('Saque Rápido', 'Do livro básico, agora poder geral. Sacar ou guardar itens é ação livre. Com a regra de munição, uma vez por rodada recarrega arma de disparo como ação livre.', 'treinado em Iniciativa')
geral('Tiro Certeiro', 'Do livro básico, agora poder geral. Com arma de disparo, soma Agilidade no dano e ignora a penalidade por atacar alvo em corpo a corpo (sem precisar mirar).', 'treinado em Pontaria')

# ======================================================================= PODERES DE CLASSE (p.14-15, 22-23, 26-27)
def poder(cl, nome, desc, pag, pre='', pe=0, ef=None):
    _add(f'op:{cl}:poder:sah:{nome}', cl, 'poder', nome, pag, {'tipo': 'poder', 'desc': desc + (' Pré-requisito: ' + pre + '.' if pre else ''), 'pe': pe, 'ef': ef or []})

C = 'combatente'
poder(C, 'Apego Angustiado', 'Não fica inconsciente por estar morrendo; mas, a cada rodada que termina morrendo e consciente, perde 2 de Sanidade.', 14)
poder(C, 'Caminho para Forca', 'Na ação sacrifício de uma perseguição (SaH p.90), gaste 1 PE para dar +1d20 extra (total +2d20) aos outros. Na ação chamar atenção de uma cena de furtividade (SaH p.92), gaste 1 PE para baixar a visibilidade de todos os aliados próximos em 2 (em vez de 1).', 14, pe=1)
poder(C, 'Ciente das Cicatrizes', 'Em teste para achar pista ligada a armas ou ferimentos (necropsia, identificar arma amaldiçoada), usa Luta ou Pontaria no lugar da perícia original.', 14, 'treinado em Luta ou Pontaria')
poder(C, 'Correria Desesperada', '+3m de deslocamento e +1d20 em testes de perícia para fugir em perseguição (SaH p.90).', 14, ef=[EF('desloc', 3)])
poder(C, 'Engolir o Choro', 'Não sofre penalidades de condições em testes de perícia para fugir nem em Furtividade.', 14)
poder(C, 'Instinto de Fuga', 'Quando começa uma cena de perseguição (ou parecida), +2 em todos os testes de perícia dela.', 14, 'treinado em Intuição')
poder(C, 'Mochileiro', 'Limite de carga +5 espaços e pode se beneficiar de uma vestimenta adicional.', 14, 'Vig 2', ef=[EF('carga', 5)])
poder(C, 'Paranoia Defensiva', 'Uma vez por cena, gaste uma rodada e 3 PE: você e cada aliado presente escolhem +5 na Defesa contra o próximo ataque da cena ou +5 em um teste de perícia até o fim da cena.', 15, pe=3)
poder(C, 'Sacrificar os Joelhos', 'Uma vez por cena de perseguição, ao usar esforço extra, gaste 2 PE para passar automaticamente no teste.', 15, 'treinado em Atletismo', pe=2)
poder(C, 'Sem Tempo, Irmão', 'Uma vez por cena de investigação, ao facilitar investigação, ajude às pressas: passa automaticamente no teste para auxiliar, mas o mestre faz uma rolagem extra na tabela de eventos de investigação (SaH p.82).', 15)
poder(C, 'Valentão', 'Usa Força no lugar de Presença em Intimidação. Uma vez por cena, gaste 1 PE para assustar com Intimidação como ação livre.', 15, pe=1)

E = 'especialista'
poder(E, 'Acolher o Terror', 'Pode se entregar para o medo (SaH p.88) uma vez a mais por sessão de jogo.', 22)
poder(E, 'Contatos Oportunos', 'Ação de interlúdio: aciona contatos locais e recebe um aliado de um tipo à escolha (OPRPG p.170) até o fim da missão ou até dispensá-lo. Só um por vez; o mestre decide a disponibilidade.', 22, 'treinado em Crime')
poder(E, 'Disfarce Sutil', 'Ao se disfarçar com Enganação, gaste 1 PE para fazê-lo com ação completa e sem kit (com kit, +5 no teste).', 22, 'Pre 2, treinado em Enganação', pe=1)
poder(E, 'Esconderijo Desesperado', 'Não sofre –1d20 em Furtividade por se mover no deslocamento normal. Em cenas de furtividade (SaH p.92), ao passar em esconder-se, a visibilidade cai 2 (em vez de 1).', 22)
poder(E, 'Especialista Diletante', 'Aprende um poder de outra classe (não de trilha nem paranormal) cujos pré-requisitos cumpra.', 22, 'NEX 30%')
poder(E, 'Flashback', 'Escolha uma origem que não é a sua: recebe o poder dela.', 22)
poder(E, 'Leitura Fria', 'Uma vez por interlúdio, após alguns minutos com uma pessoa (ou observando-a), faça três perguntas pessoais sobre ela. O mestre responde a verdade ou se nega; cada recusa dá 2 PE temporários até o fim da missão. Uma vez por pessoa, só NPCs.', 22, 'treinado em Intuição')
poder(E, 'Mãos Firmes', 'Em Furtividade para esconder-se ou para ação discreta manipulando objeto, gaste 2 PE para +1d20.', 22, 'treinado em Furtividade', pe=2)
poder(E, 'Plano de Fuga', 'Usa Intelecto no lugar de Força na ação criar obstáculos de perseguição (SaH p.90). Uma vez por cena, gaste 2 PE para ter sucesso nela sem teste.', 23, pe=2)
poder(E, 'Remoer Memórias', 'Uma vez por cena, em teste de perícia de Intelecto ou Presença, gaste 2 PE para trocá-lo por um teste de Intelecto com DT 15.', 23, 'Int 1', pe=2)
poder(E, 'Resistir à Pressão', 'Uma vez por cena de investigação, gaste 5 PE: a urgência aumenta 1 rodada e, nessa rodada extra, todos (você incluso) têm +2 nos testes de perícia.', 23, 'treinado em Investigação', pe=5)

O = 'ocultista'
poder(O, 'Deixe os Sussurros Guiarem', 'Uma vez por cena, 2 PE e uma rodada: +2 em testes de perícia de investigação até o fim da cena; enquanto ativo, cada teste de perícia que falhar custa 1 de Sanidade.', 26, pe=2)
poder(O, 'Domínio Esotérico', 'Ao conjurar, combina os efeitos de até dois catalisadores ritualísticos diferentes.', 26, 'Int 3')
poder(O, 'Estalos Macabros', 'Em ação para distrair outro ser (distrair na furtividade, fintar), gaste 1 PE para usar Ocultismo; contra pessoa ou animal, +5 no teste.', 26, pe=1)
poder(O, 'Minha Dor me Impulsiona', 'Em Acrobacia, Atletismo ou Furtividade, gaste 1 PE para +1d6, desde que tenha ao menos 5 de dano nos PV.', 26, 'Vig 2', pe=1)
poder(O, 'Nos Olhos do Monstro', 'Em cena com criatura paranormal, gaste uma rodada e 3 PE encarando seus olhos (ou o mais próximo de um rosto): +5 em testes contra ela (menos ataques) até o fim da cena.', 26, pe=3)
poder(O, 'Olhar Sinistro', 'Usa Presença no lugar de Intelecto em Ocultismo e pode usar Ocultismo para coagir.', 26, 'Pre 1')
poder(O, 'Sentido Premonitório', '3 PE para ativar (e 1 PE no início de cada rodada para manter): você vê uma rodada à frente (fim da urgência, evento de investigação que vem, ações dos inimigos em furtividade e perseguição). Não funciona em combate.', 26, pe=3)
poder(O, 'Sincronia Paranormal', 'Ação padrão e 2 PE: sincronia com quantos personagens quiser em alcance médio com quem já sobreviveu a encontro paranormal. No início de cada rodada, distribui 1d20 de bônus igual à sua Presença para testes de Intelecto ou Presença deles (somem no fim da rodada). Manter custa 1 PE por rodada.', 27, 'Pre 2', pe=2)
poder(O, 'Traçado Conjuratório', '1 PE e ação completa: traça símbolo num quadrado de 1,5m que dura a cena. Dentro dele, +2 em Ocultismo e resistência e +2 na DT dos seus rituais.', 27, pe=1)

# ======================================================================= TRILHAS (p.15-29)
def trilha(cl, t, nex, nome, desc, pag, pe=0, ef=None):
    _add(f'op:{cl}:trilha:{t}:{nome}', cl, 'trilha', nome, pag, {'tipo': 'trilha', 'desc': desc, 'pe': pe, 'ef': ef or []}, trilha=t, nex=nex)

t = 'Agente Secreto'
trilha(C, t, 10, 'Carteirada', 'Treinado em Diplomacia ou Enganação (se já for, +2). No início de cada missão recebe documentos com privilégios jurídicos (acesso a locais restritos, porte de armas, assumir investigações da polícia; detalhes com o mestre). Gente comum não percebe que são falsos; agentes de segurança ou veteranos em Crime podem desconfiar. Contam como item operacional sem espaço.', 15)
trilha(C, t, 40, 'O Sorriso', '+2 em Diplomacia e Enganação. Ao falhar numa delas, gaste 2 PE para rolar de novo (uma vez por teste, fica com o novo). Uma vez por cena, Diplomacia para acalmar a si mesmo.', 16, pe=2, ef=[EF('per:Diplomacia', 2), EF('per:Enganação', 2)])
trilha(C, t, 65, 'Método Investigativo', 'A urgência das cenas de investigação em que você está sobe 1 rodada. Quando o mestre rola evento de investigação, gaste 2 PE para virar "sem evento" (cada uso extra na cena custa +2 PE).', 16, pe=2)
trilha(C, t, 99, 'Multifacetado', 'Uma vez por cena, gaste 5 de Sanidade para receber todas as habilidades até NEX 65% de uma trilha de combatente ou especialista (cumprindo pré-requisitos) até o fim da cena. Não repete a mesma trilha na missão. Essa Sanidade só volta no fim da missão.', 16)

t = 'Caçador'
trilha(C, t, 10, 'Rastrear o Paranormal', 'Treinado em Sobrevivência (se já for, +2). Usa Sobrevivência no lugar de Ocultismo para identificar criaturas e de Investigação e Percepção para notar e achar rastros, pistas e criaturas com traços paranormais.', 16)
trilha(C, t, 40, 'Estudar Fraquezas', 'Ação de interlúdio estudando um ser específico com uma pista ligada a ele (parte do corpo, das vestes): recebe uma informação útil (característica ou hábito) e, por pista, +1 em testes contra ele até o fim da missão.', 16)
trilha(C, t, 65, 'Atacar das Sombras', 'Sem –1d20 em Furtividade por mover no deslocamento normal; com arma silenciosa (faca, arco) a penalidade por atacar cai para –1d20. Sua visibilidade inicial em cenas de furtividade é 1 abaixo (pode ser negativa).', 17)
trilha(C, t, 99, 'Estudar a Presa', 'Ao usar Estudar Fraquezas em criatura paranormal ou cultista, pode tornar o tipo dela sua presa: +1d20 em testes de perícia, +1 na margem de ameaça e no multiplicador de crítico e RD 5 contra esses seres. Uma presa por vez.', 17)

t = 'Monstruoso'
M = 'Especial: usa a Progressão de NEX da regra opcional NEX e Experiência (SaH p.98) mesmo sem ela; com a regra, ganha o dobro de NEX ao se expor. Em NEX 75% fica permanentemente perturbado e é banido pela Ordem (equipamento como patente um nível abaixo). Em NEX 99% a Sanidade cai a 1 e, ao enlouquecer, fica confuso em vez de efeito de insanidade; se enlouquecer com 99%, vira criatura do Outro Lado. '
trilha(C, t, 10, 'Ser Amaldiçoado', M + 'Treinado em Ocultismo (se já for, +2). Escolha Sangue, Morte, Conhecimento ou Energia (sua afinidade terá de ser esse). Uma vez por dia faça a etapa ritualística do elemento; se fizer, até o fim do dia tem os efeitos abaixo, senão sofre fome e sede naquele dia. Sangue: RD balístico e Sangue 5, faro, soma Vigor no dano de contra-ataque, –1d20 em Ciências e Intuição. Morte: RD perfuração e Morte 5, imune a fadiga, soma Força nos PV, –1d20 em Diplomacia e Enganação. Conhecimento: RD balístico e Conhecimento 5, visão no escuro, soma Intelecto na Defesa, –1d20 em Atletismo e Acrobacia. Energia: RD corte, eletricidade, fogo e Energia 5, soma Agilidade na RD do bloqueio, –1d20 em Investigação e Percepção.', 17)
trilha(C, t, 40, 'Ser Macabro', 'A RD da etapa ritualística sobe para 10 e a penalidade para –2d20. Efeitos extras: Sangue: PE calculados com Força; ação de movimento e PE (até sua Força) para curar 1d8 PV por PE. Morte: +1d20 em Intimidação, PE com Vigor, só morre ao iniciar 4 turnos morrendo na cena e não precisa comer ou beber (mas sente a fome da trilha). Conhecimento: +1 em Intelecto, Intelecto como chave de Enganação e dos PE. Energia: PE com Agilidade; ao acertar corpo a corpo, gaste PE (até sua Agilidade) para +1d6 de Energia por PE.', 18)
trilha(C, t, 65, 'Ser Assustador', 'A RD sobe para 15 e sua Presença cai 1 permanentemente. Efeitos extras: Sangue: 50% de ignorar dano extra de crítico ou ataque furtivo; mordida natural 1d8 (x2, perfuração) e, uma vez por rodada ao agredir com outra arma, 1 PE para um ataque extra de mordida. Morte: no início de cada turno morrendo, Vigor DT 15 para acordar com 1 PV; crítico ou inimigo a 0 PV recupera 2 PE. Conhecimento: deixa de ser treinado em uma perícia para ganhar dados de bônus igual ao Intelecto até o fim da cena (cada um dá +1d20 num teste); a perícia volta no fim do próximo interlúdio. Energia: a RD vale contra químico; ação de movimento tocando fonte elétrica recupera 1d4 PE (portátil), 2d4 (grande) ou 4d4 (casa), queimando a fonte.', 19)
trilha(C, t, 99, 'Ser Aterrorizante', 'Os efeitos da etapa ritualística viram permanentes (ainda precisa fazê-la para não ter fome e sede), RD 20 e você conta como criatura paranormal. Sangue: Int –1, For +1; mordida cura 5 PV (multiplica no crítico); aprende Forma Monstruosa e, ao sofrer dano, Vontade (DT 10 + dano) ou a próxima ação padrão é conjurá-lo. Morte: Pre –1, Vig +1, imune a dano de Morte e imortal (volta no dia seguinte), salvo se for a 0 PV por fogo ou Energia; aprende Fim Inevitável. Conhecimento: For –1, Int +1, percepção às cegas e um ritual de Conhecimento de 4º círculo (ao conjurá-lo, esquece tudo desde o início da cena). Energia: For –1, Agi +1, paira a 1,5m com deslocamento 12m, passa por espaços de criatura Minúscula, imune a paralisia física, aprende Deflagração de Energia; não usa itens vestidos e só manipula objetos com a mente, um por vez.', 20)

t = 'Bibliotecário'
trilha(E, t, 10, 'Conhecimento Prático', 'Em teste de perícia (menos Luta e Pontaria), gaste 2 PE para trocar o atributo-base por Intelecto. Com Conhecimento Aplicado, custa 1 PE a menos.', 23, pe=2)
trilha(E, t, 40, 'Leitor Contumaz', 'Os dados de bônus da ação de interlúdio ler viram 1d8 e valem para qualquer perícia. Ao usar o bônus, gaste 2 PE para +1 dado (2d8).', 23, pe=2)
trilha(E, t, 65, 'Rato de Biblioteca', 'Num lugar com muitos livros (livraria, biblioteca, antiquário), gaste alguns minutos (ou uma rodada de investigação) para ter os benefícios de ler ou revisar caso. Uma vez por cena.', 23)
trilha(E, t, 99, 'A Força do Saber', '+1 em Intelecto e soma o Intelecto no total de PE. Escolha uma perícia: o atributo-base dela vira Intelecto.', 23)

t = 'Perseverante'
trilha(E, t, 10, 'Soluções Improvisadas', 'Gaste 2 PE para rolar de novo 1 dos dados de um teste que acabou de fazer (uma vez por teste) e ficar com o melhor.', 24, pe=2)
trilha(E, t, 40, 'Fuga Obstinada', '+1d20 em testes de perícia para fugir de um inimigo (em perseguição ou não). Como presa numa perseguição, aguenta até 4 falhas antes de ser pego.', 24)
trilha(E, t, 65, 'Determinação Inquestionável', 'Uma vez por cena, 5 PE e ação padrão: remove de você uma condição de medo, mental ou de paralisia (o mestre pode vetar algumas, como paralisia de doença).', 24, pe=5)
trilha(E, t, 99, 'Só Mais um Passo...', 'Uma vez por rodada, ao sofrer dano que o levaria a 0 PV, gaste 5 PE para ficar com 1 PV. Não vale contra dano massivo.', 24, pe=5)

t = 'Muambeiro'
trilha(E, t, 10, 'Mascate', 'Treinado em Profissão (armeiro, engenheiro ou químico) e +5 na capacidade de carga. Itens improvisados têm DT reduzida em 10 (em vez de 5).', 25, ef=[EF('carga', 5)])
trilha(E, t, 40, 'Fabricação Própria', 'Fabrica itens mundanos na metade do tempo: uma ação de manutenção faz duas munições, explosivos ou consumíveis; armas, proteções e equipamentos gerais pedem só uma (modificados e paranormais não).', 25)
trilha(E, t, 65, 'Laboratório de Campo', 'Treinado em Profissão (armeiro, engenheiro ou químico) ou +5 se já for. Pode fabricar e consertar itens paranormais em campo (três ações de interlúdio, não seguidas; SaH p.94).', 25)
trilha(E, t, 99, 'Achado Conveniente', 'Ação completa e 5 PE: "produz" um item de até categoria III (não paranormal), que funciona até o fim da cena e então para de vez.', 25, pe=5)

t = 'Exorcista'
trilha(O, t, 10, 'Revelação do Mal', 'Treinado em Religião (se já for, +2). Usa Religião no lugar de Investigação e Percepção para notar e achar seres, rastros ou pistas com traços paranormais e no lugar de Ocultismo.', 27)
trilha(O, t, 40, 'Poder da Fé', 'Veterano em Religião (se já for, +1d20 nela). Ao falhar em resistência, gaste 2 PE para repetir usando Religião (fica com o segundo resultado).', 27, pe=2)
trilha(O, t, 65, 'Parareligiosidade', 'Ao conjurar, gaste +2 PE para dar ao ritual o efeito de um catalisador ritualístico à escolha.', 27, pe=2)
trilha(O, t, 99, 'Chagas da Resistência', 'Quando sua Sanidade iria a 0, gaste 10 PV para ficar com SAN 1.', 28)

t = 'Possuído'
trilha(O, t, 10, 'Poder Não Desejado', 'Todo novo poder de ocultista vira Transcender. Você tem pontos de possessão (PP): 3 + 2 por Transcender. Gasta até sua Presença em PP por turno; cada PP recupera 10 PV ou 2 PE. Recupera 1 PP a cada ação de dormir.', 28)
trilha(O, t, 40, 'As Sombras Dentro de Mim', 'Recupera 2 PP por ação de dormir. Gaste 2 PE: por uma rodada, +1d20 em Acrobacia, Atletismo e Furtividade e, em cena de furtividade, o aumento de visibilidade de cada ação cai 1.', 28, pe=2)
trilha(O, t, 65, 'Ele Me Ensina', 'Escolha: transcender ou o primeiro poder de outra trilha de ocultista (cumprindo pré-requisitos).', 28)
trilha(O, t, 99, 'Tornamo-nos Um', 'Pela afinidade, recebe um poder. Sangue (Presente da Obsessão): uma vez por rodada, 6 PE para curar 50 PV; até seu próximo turno, perícias de Força, Vigor e Intimidação ficam com +35 de treino e as outras de Presença com –10 (funciona inconsciente). Morte (Presente do Tempo): uma vez por rodada, 6 PE para um turno extra na última iniciativa (funciona inconsciente). Conhecimento (Presente do Saber): uma vez por cena, 6 PE para ganhar qualquer poder (não de NEX 99%) até o fim da cena; depois Vontade DT 15 +5 por uso na missão ou perde 1d6 de Sanidade por uso. Energia (Presente do Espaço): uma vez por rodada, 6 PE para teletransportar a um ponto em alcance médio (se ocupado, vai ao espaço livre mais próximo).', 28, pe=6)

t = 'Parapsicólogo'
trilha(O, t, 10, 'Terapia', 'Para escolher esta trilha precisa ser treinado em Profissão (psicólogo). Usa Profissão (psicólogo) como Diplomacia. Uma vez por rodada, quando você ou aliado em alcance curto falha em resistência contra dano mental, gaste 2 PE para usar um teste de Profissão (psicólogo) no lugar. Se já tem Terapia (origem Psicólogo), custa 1 PE a menos e +2 em Profissão (psicólogo).', 29, pe=2)
trilha(O, t, 40, 'Palavras-chave', 'Ao passar em teste para acalmar, gaste PE até seu limite: cada PE devolve 1 de Sanidade (ou 1 PD) a quem é tratado.', 29)
trilha(O, t, 65, 'Reprogramação Mental', '5 PE e ação de interlúdio (a pessoa voluntária em alcance curto também gasta a dela): até o próximo interlúdio, ela ganha um poder geral, um poder da classe dela ou o 1º poder de outra trilha, cumprindo pré-requisitos.', 29, pe=5)
trilha(O, t, 99, 'A Sanidade Está Lá Fora', 'Ação de movimento e 5 PE: remove todas as condições de medo e mentais de uma pessoa adjacente (ou de você).', 29, pe=5)

# ======================================================================= CLASSE SOBREVIVENTE (p.30-32)
S = 'sobrevivente'
def sob(grupo, nome, desc, nex, pag, pe=0, ef=None, t=None):
    _add(f'op:{S}:{grupo}:{(t + ":") if t else ""}{nome}', S, grupo, nome, pag, {'tipo': 'trilha' if grupo == 'trilha' else 'classe', 'desc': desc, 'pe': pe, 'ef': ef or []}, trilha=t, nex=nex)

sob('classe', 'Empenho', 'Estágio 1: ao fazer um teste de perícia, gaste 1 PE para +2 nele. Sobrevivente: PV 8 + Vigor (+2 por estágio), PE 2 + Presença (+1 por estágio), SAN 8 (+2 por estágio), limite de PE sempre 1 (mas sempre pode usar uma habilidade no custo mínimo por turno), perícias 1 + Intelecto, armas simples, atributos começam em 1 com 3 pontos para distribuir, sobe um estágio no fim de cada missão, equipamento: um item de categoria I e itens de categoria 0 coerentes com a origem.', 1, 30, pe=1)
sob('classe', 'Habilidade de Trilha', 'Estágio 2: escolha uma trilha de sobrevivente (Durão, Esperto ou Esotérico) e receba o 1º poder; no estágio 4 recebe o 2º (e último).', 2, 31)
sob('classe', 'Aumento de Atributo', 'Estágio 3: +1 em um atributo (máximo 3 por esta via).', 3, 31)
sob('classe', 'Cicatrizado', 'Estágio 5: escolha um perigo paranormal de um elemento que já enfrentou: –1d20 em resistência contra ele. Uma vez por sessão, como reação, sacrifique 1 PV permanente para ignorar um dano mental ou gasto de PE, ou 1 PE permanente para reduzir um dano físico à metade.', 5, 31)
sob('classe', 'Treinamento Especial', 'Pela história (não por escolha do jogador), ao subir de estágio vira personagem de NEX 5% de outra classe e mantém o que já tinha. Combatente: +8 PV; Fortitude ou Reflexos e Luta ou Pontaria; armas táticas e proteções leves; Ataque Especial. Especialista: +4 PV, +1 PE, +4 SAN; 6 perícias; proteções leves; Eclético e Perito. Ocultista: +2 PE, +8 SAN; Ocultismo, Vontade e mais 2; Escolhido pelo Outro Lado. Depois sobe por NEX.', None, 32)
sob('trilha', 'Durão', '+4 PV; ao subir para o 3º estágio, +2 PV.', 2, 31, ef=[EF('pv', 4), EF('pv', 2, mn=3)], t='Durão')
sob('trilha', 'Pancada Forte', 'Ao atacar, gaste 1 PE para +1d20 no teste de ataque. Se virar combatente, perde esta habilidade e o Ataque Especial custa 1 PE a menos.', 4, 31, pe=1, t='Durão')
sob('trilha', 'Esperto', 'Treinado em uma perícia adicional à escolha.', 2, 32, t='Esperto')
sob('trilha', 'Entendido', 'Escolha duas perícias treinadas (menos Luta e Pontaria): nelas, gaste 1 PE para +1d4. Se virar especialista, perde esta habilidade e o Perito custa 1 PE a menos.', 4, 32, pe=1, t='Esperto')
sob('trilha', 'Esotérico', 'Ação padrão e 1 PE: sente energias paranormais em alcance curto (pode dar pista ou alertar de perigo; o mestre diz o que você percebe).', 2, 32, pe=1, t='Esotérico')
sob('trilha', 'Iniciado', 'Aprende e pode conjurar um ritual de 1º círculo à escolha. Se virar ocultista, ele soma aos três rituais de Escolhido pelo Outro Lado.', 4, 32, t='Esotérico')

# ======================================================================= PODERES PARANORMAIS (p.46-47)
def para(nome, el, desc, af, pag, pre=''):
    t = desc + ' Afinidade: ' + af + (' Pré-requisito: ' + pre + '.' if pre else '')
    _add('op:paranormal:sah:' + nome, None, 'paranormal', nome, pag, {'tipo': 'paranormal', 'pe': 0, 'el': el, 'pre': pre, 'desc': t, 'ef': []}, elemento=el)

para('Espreitar da Besta', 'Sangue', '+5 em Furtividade. Como caçador numa perseguição, usa Furtividade no lugar de Atletismo. Em cenas de furtividade, faz ações discretas sem a penalidade de –1d20.', 'o bônus em Furtividade sobe para +10.', 46)
para('Instintos Sanguinários', 'Sangue', 'Visão no escuro e faro.', 'não pode ser flanqueado, não fica desprevenido e +5 em resistência contra armadilhas reais ou paranormais.', 46)
para('Antecipar Vitalidade', 'Morte', 'Num teste, acumule uma carga de antecipação para +1d20. Máximo de cargas igual ao Vigor. Com carga, na próxima ação de dormir perde uma carga em vez de recuperar PV.', 'limite de cargas +2 e perde 2 cargas por ação de dormir.', 46)
para('Aura de Pavor', 'Morte', '2 PE e ação de movimento: uma pessoa ou animal em alcance médio fica apavorado (Vontade DT Pre reduz para abalado), mesmo sem ver você. Termina no fim da cena, se o alvo passar de alcance médio ou se você usar em outro. Uma vez por dia por alvo.', 'DT +5 e afeta quaisquer pessoas ou animais escolhidos no alcance.', 46)
para('Absorver Conhecimento', 'Conhecimento', 'Empunhando uma fonte escrita, 1 PE e ação completa: faça uma pergunta; se a resposta estiver nela, você a obtém. Junto com a ação ler, o dado de bônus sobe um passo.', 'rituais de Conhecimento com alvo 1 pessoa (não você) custam –1 PE se puder tocar o alvo.', 46)
para('Apatia Herege', 'Conhecimento', 'Em teste contra condição de medo, gaste 2 PE para rolar de novo (fica com o segundo).', 'pode usar depois de saber o resultado e fica com o melhor.', 47, 'Conhecimento 1')
para('Conexão Empática', 'Energia', 'Ação completa e 2 PE tocando objeto elétrico ligado: até o fim da cena (ou soltar), conversa com ele (memória só pelos arquivos que tem; atitude inicial indiferente, Vontade 1 a 3 para Diplomacia). Só você ouve; depois ele fica traumatizado e hostil.', '+5 em perícias de Intelecto ou Presença com o objeto.', 47, 'Energia 1')
para('Valer-se do Caos', 'Energia', 'Num teste, controle o caos para +1d20; se o teste falhar ou esse d20 extra der 5 ou menos, perde 1d4 de Sanidade.', 'só perde Sanidade se falhar ou se o d20 extra der 1 ou 2.', 47)

# ======================================================================= RITUAIS (p.48-56)
PE_CIRC = {1: 1, 2: 3, 3: 6, 4: 10}
def rit(nome, circ, el, ex, alc, alvo, dur, res, efeito, pag, disc='', verd=''):
    cab = f'Execução: {ex}. Alcance: {alc}. Alvo/área: {alvo}. Duração: {dur}.' + (f' Resistência: {res}.' if res else '')
    desc = cab + ' ' + efeito + (' Discente ' + disc if disc else '') + (' Verdadeiro ' + verd if verd else '')
    _add('op:ritual:sah:' + nome, None, 'ritual', nome, pag, {'tipo': 'ritual', 'circ': circ, 'el': el, 'pe': PE_CIRC[circ], 'desc': desc, 'ef': []}, circulo=circ, elemento=el)

rit('Esfolar', 1, 'Sangue', 'padrão', 'curto', '1 ser', 'instantânea', 'Reflexos parcial',
    'Lâminas rubras: 3d4+3 de corte e sangrando. Passou: metade do dano e sem a condição.', 48,
    '(+2 PE, 2º círculo): alcance médio, 5d4+5, explosão de 6m de raio.', '(+5 PE, 3º círculo): alcance longo, 10d4+10, explosão de 6m; passar não evita a condição.')
rit('Sede de Adrenalina', 2, 'Sangue', 'reação', 'pessoal', 'você', 'instantânea', '',
    'Ao falhar em Acrobacia ou Atletismo, repete usando Presença como atributo; ou, ao sofrer dano de impacto, reduz em 20 (depois fica 1 rodada atordoado se contorcendo). Uma vez por rodada.', 49,
    '(+3 PE): redução de impacto 40.', '(+7 PE, 4º círculo e afinidade): redução de impacto 70.')
rit('Odor da Caçada', 3, 'Sangue', 'padrão', 'pessoal', 'você', 'cena', '',
    'Recebe faro. Numa perseguição, +5 em Atletismo e esforço extra não custa PV, se o perseguidor ou a presa emitir cheiro. Na cena seguinte fica sob fome e sede (como se falhasse no 1º dia) até se alimentar.', 49,
    '(+4 PE): alcance toque, alvo 1 ser.', '(+9 PE, afinidade): alcance curto, até 5 seres.')
rit('Martírio de Sangue', 4, 'Sangue', 'padrão', 'pessoal', 'você', 'veja texto', '',
    'Faro, visão no escuro, cura acelerada 10, +10 em ataques e dano corpo a corpo e na Defesa, 30 PV temporários; desarmado causa +1 dado e é letal (corte, impacto ou perfuração). Não faz ações de concentração (rituais) e sofre –3d20 em interação social. Não termina: no fim da cena você vira criatura de Sangue para sempre (personagem perdido).', 50,
    '(+5 PE, afinidade): bônus +20 e 50 PV temporários.')
rit('Apagar as Luzes', 1, 'Morte', 'padrão', 'pessoal', 'você', 'instantânea', '',
    'Toda luz em alcance curto (natural ou paranormal) se apaga e fica assim ao menos até o fim da cena (penumbra ou escuridão). Você recebe visão no escuro até o fim da cena.', 50,
    '(+2 PE, 2º círculo): luzes em alcance longo.', '(+5 PE, 3º círculo): como discente e até cinco outros seres no alcance também recebem visão no escuro.')
rit('Língua Morta', 2, 'Morte', 'padrão', 'toque', '1 cadáver', 'sustentada', '',
    'O cadáver humano responde uma pergunta por rodada, até 3 rodadas (clareza a critério do mestre). Parou antes: vira Lodo. Na 3ª resposta vira esqueleto de Lodo (OPRPG p.217).', 51,
    '(+3 PE): 4 rodadas; no fim vira enraizado.', '(+7 PE, 4º círculo e afinidade): 5 rodadas; no fim vira marionete.')
rit('Fedor Pútrido', 3, 'Morte', 'padrão', 'pessoal', 'você', 'sustentada', '',
    'Cheira como cadáver: animais se afastam, –3d20 em Diplomacia, +5 em Furtividade e +10 em Enganação para se fingir de morto; parado numa cena de furtividade, visibilidade 1 menor. Cada rodada mantido: 1d4 de dano de Morte que ignora resistências.', 52,
    '(+4 PE): alcance toque, 1 ser voluntário.', '(+9 PE, afinidade): alcance curto, até 5 seres voluntários.')
rit('Singularidade Temporal', 4, 'Morte', 'padrão', 'curto', '1 objeto não paranormal Médio', 'instantânea', 'veja texto',
    'Avança o objeto até a decomposição máxima do seu tipo: danificado (ex. –5 em testes com ele) ou destruído, a critério do mestre. Objeto em uso: o portador faz Fortitude para protegê-lo.', 52,
    '(+5 PE): objeto Grande.', '(+10 PE): objeto Enorme.')
rit('Desfazer Sinapses', 1, 'Conhecimento', 'padrão', 'curto', '1 ser (com cérebro)', 'instantânea', 'Vontade parcial',
    '2d6+2 de dano de Conhecimento e frustrado por 1 rodada. Passou: metade e sem condição.', 53,
    '(+2 PE, 2º círculo): alcance longo, 3d6+3, até 5 seres.', '(+5 PE, 3º círculo): alcance extremo, 8d6+8 e esmorecido (passou: frustrado).')
rit('Aurora da Verdade', 2, 'Conhecimento', 'padrão', 'curto', 'esfera de 3m de raio', 'sustentada', 'Vontade parcial',
    'Quem está na área (inclusive você) só fala a verdade; passou, pode mentir (ainda percebido com Intuição). Quem tenta se esconder, ter camuflagem ou ficar invisível na luz é revelado.', 53,
    '(+3 PE): alcance médio, esfera de 9m e você não é afetado.', '(+7 PE, 4º círculo e afinidade): como discente, alcance longo, duração cena e você ouve tudo dito na área.')
rit('Relembrar Fragmento', 3, 'Conhecimento', 'padrão', 'toque', '1 objeto (fonte escrita)', 'instantânea', '',
    'Com um pedaço do texto, restaura o objeto ao momento da última anotação enquanto você o tocar. Não funciona em objetos destruídos por meios paranormais.', 54,
    '(+4 PE): fica restaurado até o fim da missão.', '(+9 PE, afinidade): em vez disso altera o objeto de forma imperceptível como quiser (ex. documento "legítimo") até o fim da missão.')
rit('Pronunciar Sigilo', 4, 'Conhecimento', 'padrão', 'curto', '1 ser', 'instantânea/veja texto', 'Vontade parcial',
    'Escolha: Esquecer (atordoado 1d4+1 rodadas, uma vez por cena; passou ou já foi atordoado: desprevenido 1d4 rodadas); Cegar (cego; passou: ofuscado 1d4 rodadas); Inexistir (deixa de existir 1d4+1 rodadas, ou 1 se passar; volta ao lugar; criatura volta a um ponto em 18m; uma vez por cena).', 54,
    '(+5 PE): alcance extremo.', '(+10 PE, afinidade): até cinco seres.')
rit('Overclock', 1, 'Energia', 'reação', 'pessoal', 'você', 'instantânea', '',
    'Depois de um teste de Tecnologia com aparelho eletrônico, consegue a informação por outro caminho: o mestre põe uma música e você joga "estátua" (ou outro jogo da mesa); se não errar até o fim, descobre o que queria. Depois o aparelho fica inutilizável.', 55,
    '(+2 PE, 2º círculo): só falha com dois erros.', '(+5 PE, 3º círculo): só falha com três erros.')
rit('Tremeluzir', 2, 'Energia', 'padrão', 'pessoal', 'você', 'sustentada', '',
    'Você e o que carrega atravessam objetos sólidos: ação de movimento por objeto, 25% (1 em 1d4) de bater nele. Numa perseguição, corta caminho sem penalidade em Atletismo. Cada rodada: 1d4 de Energia que ignora resistência (+1d4 se terminar dentro de um sólido).', 55,
    '(+3 PE): alcance toque, 1 ser voluntário.', '(+7 PE, 4º círculo): alcance curto, até 5 seres voluntários.')
rit('Mutar', 3, 'Energia', 'padrão', 'pessoal', 'você', 'cena', '',
    'Você não emite nenhum som e não ouve nada: +10 em Furtividade e ganhos de visibilidade em furtividade caem 1. O jogador só fala na mesa com permissão do mestre (falou, o ritual acaba).', 56,
    '(+4 PE): alcance toque, 1 ser.', '(+9 PE, afinidade com Energia): alcance curto, até 5 seres.')
rit('Milagre Ionizante', 3, 'Energia', 'completa', 'toque', '1 ser', 'instantânea', '',
    'Cura uma condição (abalado, apavorado, alquebrado, atordoado, cego, confuso, debilitado, enjoado, envenenado, esmorecido, exausto, fascinado, fatigado, fraco, frustrado, lento, ofuscado, paralisado, pasmo ou surdo) ou uma doença ou veneno, inclusive paranormal (menos de Energia e condições permanentes). Depois o ser faz Fortitude DT 30 ou é incubado pelo vírus do infectcídio (OPRPG p.292).', 56)
