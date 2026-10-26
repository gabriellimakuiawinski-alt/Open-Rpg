#!/usr/bin/env python3
"""Gera schema_etapa6d_itens.sql: armas, munições, proteções, acessórios, explosivos, itens operacionais,
itens paranormais e modificações do Livro de Regras de Ordem Paranormal (v1.2, capítulo 3). Textos resumidos.
Uso: python3 tools/livro/gerar_op_itens.py   (na raiz do repositório)
Categoria: 0, I=1, II=2, III=3."""
import json, os

IT = []   # (grupo, subgrupo, nome, dados)
def add(grupo, sub, nome, dados): IT.append((grupo, sub, nome, dados))

# ---------------------------------------------------------------- ARMAS
PROF = {'S': 'simples', 'T': 'tática', 'P': 'pesada'}
EMP = {'L': 'corpo a corpo, leve', 'U': 'corpo a corpo, uma mão', 'D': 'corpo a corpo, duas mãos', 'A': 'disparo, duas mãos',
       'FL': 'fogo, leve', 'FU': 'fogo, uma mão', 'FD': 'fogo, duas mãos', 'PD': 'à distância, duas mãos'}
MC = {'L': 'corpo', 'U': 'corpo', 'D': 'corpo', 'A': 'disparo', 'FL': 'fogo', 'FU': 'fogo', 'FD': 'fogo', 'PD': 'pesada'}
AGIL = 'Arma ágil: usa Agilidade em vez de Força no ataque e no dano.'
AUTO = 'Arma automática: tiro único normal ou rajada (–1d20 no ataque, +1 dado de dano do mesmo tipo).'
def W(prof, emp, nome, cat, dano, crit, alc, td, esp, nota=''):
    per = 'Pontaria' if emp in ('A', 'FL', 'FU', 'FD', 'PD') else 'Luta'
    d = f'Arma {PROF[prof]}, {EMP[emp]}.' + (' ' + nota if nota else '')
    add('arma', PROF[prof] + ' · ' + EMP[emp], nome, {'tipo': 'arma', 'catg': cat, 'esp': esp, 'mc': MC[emp], 'desc': d,
        'arma': {'dano': dano, 'crit': crit, 'alc': alc, 'td': td, 'per': per}})
# simples
W('S', 'L', 'Coronhada', 0, '1d4', 'x2', '', 'I', 0, 'Ataque corpo a corpo com arma de fogo: 1d4 de impacto (leve/uma mão) ou 1d6 (duas mãos).')
W('S', 'L', 'Faca', 0, '1d4', '19', 'Curto', 'C', 1, AGIL + ' Pode ser arremessada.')
W('S', 'L', 'Martelo', 0, '1d6', 'x2', '', 'I', 1)
W('S', 'L', 'Punhal', 0, '1d4', 'x3', '', 'P', 1, AGIL)
W('S', 'U', 'Bastão', 0, '1d6', 'x2', '', 'I', 1, 'Com duas mãos o dano é 1d8.')
W('S', 'U', 'Machete', 0, '1d6', '19', '', 'C', 1)
W('S', 'U', 'Lança', 0, '1d6', 'x2', 'Curto', 'P', 1, 'Pode ser arremessada.')
W('S', 'D', 'Cajado', 0, '1d6', 'x2', '', 'I', 2, AGIL + ' Pode ser usado em Combater com Duas Armas como arma de uma mão + leve.')
W('S', 'A', 'Arco', 0, '1d6', 'x3', 'Médio', 'P', 2, 'Usa flechas.')
W('S', 'A', 'Besta', 0, '1d8', '19', 'Médio', 'P', 2, 'Usa flechas. Recarregar custa ação de movimento a cada disparo.')
W('S', 'FL', 'Pistola', 1, '1d12', '18', 'Curto', 'B', 1, 'Usa balas curtas.')
W('S', 'FL', 'Revólver', 1, '2d6', '19/x3', 'Curto', 'B', 1, 'Usa balas curtas.')
W('S', 'FD', 'Fuzil de caça', 1, '2d8', '19/x3', 'Médio', 'B', 2, 'Usa balas longas.')
# táticas
W('T', 'L', 'Machadinha', 0, '1d6', 'x3', 'Curto', 'C', 1, 'Pode ser arremessada.')
W('T', 'L', 'Nunchaku', 0, '1d8', 'x2', '', 'I', 1, AGIL)
W('T', 'U', 'Corrente', 0, '1d8', 'x2', '', 'I', 1, '+2 em testes para desarmar e derrubar.')
W('T', 'U', 'Espada', 1, '1d8', '19', '', 'C', 1, 'Com duas mãos o dano é 1d10.')
W('T', 'U', 'Florete', 1, '1d6', '18', '', 'C', 1, AGIL)
W('T', 'U', 'Machado', 1, '1d8', 'x3', '', 'C', 1)
W('T', 'U', 'Maça', 1, '2d4', 'x2', '', 'I', 1)
W('T', 'D', 'Acha', 1, '1d12', 'x3', '', 'C', 2)
W('T', 'D', 'Gadanho', 1, '2d4', 'x4', '', 'C', 2)
W('T', 'D', 'Katana', 1, '1d10', '19', '', 'C', 2, AGIL + ' Veterano em Luta pode usá-la com uma mão.')
W('T', 'D', 'Marreta', 1, '3d4', 'x2', '', 'I', 2, 'Vale também para outras ferramentas de construção, como picaretas.')
W('T', 'D', 'Montante', 1, '2d6', '19', '', 'C', 2)
W('T', 'D', 'Motosserra', 1, '3d6', 'x2', '', 'C', 2, 'Ao rolar 6 em um dado de dano, role um dado de dano adicional. Desajeitada: –1d20 no ataque. Ligar gasta ação de movimento.')
W('T', 'A', 'Arco composto', 1, '1d10', 'x3', 'Médio', 'P', 2, 'Permite somar sua Força ao dano. Usa flechas.')
W('T', 'A', 'Balestra', 1, '1d12', '19', 'Médio', 'P', 2, 'Usa flechas. Recarregar custa ação de movimento a cada disparo.')
W('T', 'FU', 'Submetralhadora', 1, '2d6', '19/x3', 'Curto', 'B', 1, AUTO + ' Usa balas curtas.')
W('T', 'FD', 'Espingarda', 1, '4d6', 'x3', 'Curto', 'B', 2, 'Metade do dano em alcance médio ou maior. Usa cartuchos.')
W('T', 'FD', 'Fuzil de assalto', 2, '2d10', '19/x3', 'Médio', 'B', 2, AUTO + ' Usa balas longas.')
W('T', 'FD', 'Fuzil de precisão', 3, '2d10', '19/x3', 'Longo', 'B', 2, 'Veterano em Pontaria que mira com ele: +5 na margem de ameaça. Usa balas longas.')
# pesadas
W('P', 'PD', 'Bazuca', 3, '10d8', 'x2', 'Médio', 'I', 2, 'Dano no alvo e em todos num raio de 3m (Reflexos DT Agi reduz à metade; o alvo direto não tem teste). Pode disparar em um ponto em alcance médio sem rolar ataque. Recarregar custa ação de movimento. Usa foguete.')
W('P', 'PD', 'Lança-chamas', 3, '6d6', 'x2', 'Curto', 'Fogo', 2, 'Atinge todos numa linha de 1,5m de largura em alcance curto, com um único ataque contra a Defesa de cada um; os atingidos ficam em chamas. Usa combustível.')
W('P', 'PD', 'Metralhadora', 2, '2d12', '19/x3', 'Médio', 'B', 2, AUTO + ' Exige Força 4 ou ação de movimento para apoiar no tripé; senão –5 nos ataques. Usa balas longas.')

# ---------------------------------------------------------------- MUNIÇÕES
for n, c, desc in [
    ('Balas curtas', 0, 'Pistolas, revólveres e submetralhadoras. Um pacote dura 2 cenas.'),
    ('Balas longas', 1, 'Fuzis e metralhadoras. Um pacote dura 1 cena.'),
    ('Cartuchos', 1, 'Espingardas. Um pacote dura 1 cena.'),
    ('Combustível', 1, 'Tanque para lança-chamas. Dura 1 cena.'),
    ('Flechas', 0, 'Arcos e bestas. Reaproveitáveis: um pacote dura a missão inteira.'),
    ('Foguete', 1, 'Para bazucas. Cada foguete dura um único disparo.')]:
    add('municao', 'munição', n, {'tipo': 'municao', 'catg': c, 'esp': 1, 'mc': 'municao' if 'Balas' in n else '', 'desc': desc})

# ---------------------------------------------------------------- PROTEÇÕES
add('protecao', 'proteção', 'Proteção leve', {'tipo': 'protecao', 'sub': 'leve', 'def': 5, 'catg': 1, 'esp': 2, 'mc': 'protecao', 'desc': 'Jaqueta de couro pesada ou colete de kevlar. Defesa +5.'})
add('protecao', 'proteção', 'Proteção pesada', {'tipo': 'protecao', 'sub': 'pesada', 'def': 10, 'catg': 2, 'esp': 5, 'mc': 'protecao', 'desc': 'Capacete, ombreiras, joelheiras, caneleiras e colete de kevlar. Defesa +10; resistência 2 a balístico, corte, impacto e perfuração; –5 em perícias com penalidade de carga.'})
add('protecao', 'proteção', 'Escudo', {'tipo': 'protecao', 'sub': 'escudo', 'def': 2, 'catg': 1, 'esp': 2, 'mc': 'protecao', 'desc': 'Empunhado em uma mão. Defesa +2, acumula com a proteção. Conta como proteção pesada para proficiência.'})

# ---------------------------------------------------------------- ACESSÓRIOS
add('acessorio', 'acessório', 'Kit de perícia', {'tipo': 'geral', 'catg': 0, 'esp': 1, 'mc': 'acessorio', 'desc': 'Ferramentas necessárias para uma perícia (um kit por perícia). Sem o kit, –5 no teste.'})
add('acessorio', 'acessório', 'Utensílio', {'tipo': 'geral', 'catg': 1, 'esp': 1, 'mc': 'acessorio', 'desc': 'Item comum com uma utilidade (canivete, lupa, smartphone, notebook): +2 em uma perícia (exceto Luta e Pontaria). Precisa ser empunhado. Bônus de itens não se acumulam.'})
add('acessorio', 'acessório', 'Vestimenta', {'tipo': 'geral', 'catg': 1, 'esp': 1, 'mc': 'acessorio', 'desc': 'Peça de roupa com +2 em uma perícia (exceto Luta e Pontaria). Vale o bônus de no máximo duas vestimentas. Vestir ou despir é ação completa.'})

# ---------------------------------------------------------------- EXPLOSIVOS
G = 'Granada: empunhe e gaste ação padrão para arremessar em alcance médio; afeta raio de 6m. '
add('explosivo', 'explosivo', 'Granada de atordoamento', {'tipo': 'consumivel', 'catg': 0, 'esp': 1, 'desc': G + 'Flash-bang: seres na área ficam atordoados por 1 rodada (Fortitude DT Agi reduz para ofuscado e surdo por 1 rodada).'})
add('explosivo', 'explosivo', 'Granada de fragmentação', {'tipo': 'consumivel', 'catg': 1, 'esp': 1, 'desc': G + '8d6 de perfuração (Reflexos DT Agi reduz à metade).'})
add('explosivo', 'explosivo', 'Granada de fumaça', {'tipo': 'consumivel', 'catg': 0, 'esp': 1, 'desc': G + 'Seres na área ficam cegos e sob camuflagem total. Dura 2 rodadas.'})
add('explosivo', 'explosivo', 'Granada incendiária', {'tipo': 'consumivel', 'catg': 1, 'esp': 1, 'desc': G + '6d6 de fogo e em chamas (Reflexos DT Agi reduz o dano à metade e evita as chamas).'})
add('explosivo', 'explosivo', 'Mina antipessoal', {'tipo': 'consumivel', 'catg': 1, 'esp': 1, 'desc': 'Detonada por controle remoto (ação padrão, até alcance longo). Cone de 6m: 12d6 de perfuração (Reflexos DT Int reduz à metade). Instalar: ação completa e Tática DT 15 (falhou, a mina é gasta). Achar uma mina instalada: Percepção contra o resultado de quem instalou.'})

# ---------------------------------------------------------------- ITENS OPERACIONAIS
def op(nome, cat, esp, desc, **x):
    d = {'tipo': x.pop('tipo', 'geral'), 'catg': cat, 'esp': esp, 'desc': desc}; d.update(x); add('operacional', 'item operacional', nome, d)
op('Algemas', 0, 1, 'Prender quem não está indefeso exige agarrar e vencer novo teste de agarrar. Os dois pulsos: –5 em testes com as mãos e impede conjuração. Escapar: Acrobacia DT 30 (ou ter a chave).')
op('Arpéu', 0, 1, 'Gancho de aço na ponta de uma corda. Prender: Pontaria DT 15. Subir com a corda: +5 em Atletismo.')
op('Bandoleira', 1, 1, 'Cinto com bolsos e alças. Uma vez por rodada, saca ou guarda um item como ação livre.')
op('Binóculos', 0, 1, '+5 em Percepção para observar coisas distantes.', ef=[{'a': 'per:Percepção', 'v': 5}])
op('Bloqueador de sinal', 1, 1, 'Impede que celulares em alcance médio se conectem.')
op('Cicatrizante', 1, 1, 'Spray de efeito cicatrizante. Ação padrão e o item: cura 2d8+2 PV em você ou em um ser adjacente.', tipo='consumivel')
op('Corda', 0, 1, '10 metros de corda resistente. +5 em Atletismo para descer buracos ou prédios; serve para amarrar pessoas inconscientes.')
op('Equipamento de sobrevivência', 0, 2, 'Mochila com saco de dormir, panelas, GPS etc. +5 em Sobrevivência para acampar e se orientar, mesmo sem treinamento.')
op('Lanterna tática', 1, 1, 'Ilumina lugares escuros. Ação de movimento: mira a luz nos olhos de um ser em alcance curto, que fica ofuscado por 1 rodada e imune à lanterna pelo resto da cena.', luz={'t': 'c', 'm': 18})
op('Máscara de gás', 0, 1, 'Cobre o rosto inteiro: +10 em Fortitude contra efeitos que dependam de respiração.')
op('Mochila militar', 1, 0, 'Mochila leve e de alta qualidade: não ocupa espaço e aumenta sua capacidade de carga em 2 espaços.', ef=[{'a': 'carga', 'v': 2}])
op('Óculos de visão térmica', 1, 1, 'Eliminam a penalidade em testes por camuflagem.')
op('Pé de cabra', 0, 1, '+5 em Força para arrombar portas. Em combate vale como um bastão.')
op('Pistola de dardos', 1, 1, 'Dispara dardos com sonífero. Ataque à distância; se acertar, o alvo fica inconsciente até o fim da cena (Fortitude DT Agi reduz para desprevenido e lento por 1 rodada). Vem com 2 dardos; caixa extra com 2 dardos: categoria 0, 1 espaço.')
op('Pistola sinalizadora', 0, 1, 'Dispara um sinalizador luminoso para chamar outras pessoas. Pode servir como arma de disparo leve, alcance curto, 2d6 de fogo. Vem com 2 cargas; caixa extra com 2 cargas: categoria 0, 1 espaço.')
op('Soqueira', 0, 1, '+1 em rolagens de dano desarmado. Aceita modificações e maldições de armas corpo a corpo, aplicadas aos ataques desarmados.')
op('Spray de pimenta', 1, 1, 'Ação padrão: ser adjacente fica cego por 1d4 rodadas (Fortitude DT Agi evita). A carga dura 2 usos.')
op('Taser', 1, 1, 'Ação padrão em ser adjacente: 1d6 de eletricidade e atordoado por 1 rodada (Fortitude DT Agi evita). A bateria dura 2 usos.')
op('Traje hazmat', 1, 2, 'Roupa impermeável de corpo inteiro: +5 em resistência contra efeitos ambientais e resistência a químico 10.')

# ---------------------------------------------------------------- ITENS PARANORMAIS
ELS = ['Conhecimento', 'Energia', 'Morte', 'Sangue']
COMP = {'Energia': 'eletricidade, dispositivos tecnológicos, circuitos, fontes de calor e luz, pilhas, baterias, cabos de cobre e prata, pólvora, moedas, dados, ímãs…',
        'Sangue': 'órgãos, carne, sangue, animais vivos (sacrifício), navalhas, agulhas, arame farpado, correntes, metal enferrujado, fluidos corporais…',
        'Morte': 'ossos, dentes, cinzas, fios de cabelo, cristais pretos, relógios, galhos e folhas secos, plantas mortas, raízes, areia, poeira, lodo…',
        'Conhecimento': 'escrituras, papéis, livros, pergaminhos, instrumentos de escrita, pedras preciosas, ouro, cordas, tecido, cristais brancos, vidro, máscaras…'}
def par(nome, cat, esp, desc): add('paranormal', 'item paranormal', nome, {'tipo': 'paranormal', 'catg': cat, 'esp': esp, 'desc': desc})
for e in ELS:
    par('Amarras de ' + e, 2, 1, f'Cordas ou correntes de {e} para imobilizar criaturas vulneráveis a esse elemento. Armadilha: gasta as amarras, ação completa e 2 PE para uma armadilha 3x3m; quem atravessa pela primeira vez no turno faz Reflexos (DT Int) ou fica imóvel até o fim da cena (passando, o espaço é terreno difícil). Laçar: ação padrão e 1 PE em criatura em alcance curto; se falhar em Vontade (DT Agi), fica paralisada até o início do seu próximo turno (repete o teste); manter custa 1 PE por rodada.')
par('Câmera de aura paranormal', 2, 1, 'Câmera amaldiçoada com Energia, com sigilos de Conhecimento. Tirar uma foto gasta ação padrão e 1 PE; revela auras paranormais em pessoas e objetos, na cor do elemento.')
for e in ELS:
    par('Componentes ritualísticos de ' + e, 0, 1, f'Objetos usados em rituais de {e}; necessários para conjurá-los. Exemplos: {COMP[e]}')
par('Emissor de pulsos paranormais', 2, 1, 'Caixa com sigilos usada como isca. Ativar: ação completa e 1 PE. Emite um pulso do elemento escolhido que atrai criaturas desse elemento e afasta as do elemento oposto (Vontade DT Pre evita).')
par('Escuta de ruídos paranormais', 2, 1, 'Microfone espião que capta ruídos paranormais. Ativar: ação completa e 2 PE; grava por até 24 horas. Ouvir a gravação dá +5 em Ocultismo para identificar criatura.')
par('Medidor de estabilidade da membrana', 2, 1, 'Dispositivo com medidores de temperatura, campo magnético, dilatação temporal etc. Agente treinado em Ocultismo avalia o estado da Membrana na área (chance de uma entidade se manifestar). Não dá resposta definitiva. (O livro não traz este item na tabela de categorias; usada a categoria II dos demais itens paranormais.)')
for e in ELS:
    par('Scanner de manifestação paranormal de ' + e, 2, 1, f'Ativar: ação padrão; consome 1 PE por rodada. Você sempre sabe a direção de todas as manifestações paranormais ativas de {e} (rituais, criaturas, itens amaldiçoados) em alcance longo, inclusive criaturas que tenham esse elemento como complemento.')

# ---------------------------------------------------------------- MODIFICAÇÕES
MD = []
def mod(nome, aplica, desc, catg=1, esp=0, d=0):
    add('modificacao', 'modificação', nome, {'tipo': 'modificacao', 'aplica': aplica, 'desc': desc, 'mod': {'catg': catg, 'esp': esp, 'def': d}})
CF = ['corpo', 'disparo']; F = ['fogo']
mod('Certeira', CF, 'Arma mais precisa e balanceada: +2 em testes de ataque.')
mod('Cruel', CF, 'Lâmina afiada ou materiais mais densos: +2 nas rolagens de dano.')
mod('Perigosa', CF, 'Golpes de impacto terrível: +2 na margem de ameaça.')
mod('Discreta', CF + F, 'Chama menos atenção e ocupa menos espaço: +5 em Crime para ocultá-la (mesmo sem treinamento) e –1 espaço.', esp=-1)
mod('Tática', CF + F, 'Cabo texturizado, bandoleira etc.: pode sacar a arma como ação livre.')
mod('Alongada', F, 'Cano mais longo: +2 em testes de ataque.')
mod('Calibre Grosso', F, 'Munição de maior calibre: +1 dado de dano do mesmo tipo. Exige munição específica de calibre grosso (mesma categoria da normal, mas não serve em armas normais).')
mod('Compensador', F, 'Só para armas automáticas: anula a penalidade de ataque por disparar rajadas.')
mod('Ferrolho Automático', F, 'A arma se torna automática (rajadas).')
mod('Mira Laser', F, '+2 na margem de ameaça.')
mod('Mira Telescópica', F, 'Aumenta o alcance da arma em uma categoria e permite Ataque Furtivo em qualquer alcance.')
mod('Silenciador', F, 'Reduz em 2d20 a penalidade em Furtividade para se esconder no mesmo turno em que atacou.')
mod('Visão de Calor', F, 'Mira com imagem infravermelha: ao disparar, ignora qualquer camuflagem do alvo.')
mod('Dum Dum', ['municao'], 'Só para balas curtas e longas: +1 no multiplicador de crítico.')
mod('Explosiva', ['municao'], 'Só para balas curtas e longas: +2d6 de dano.')
mod('Antibombas', ['protecao'], 'Só para proteção pesada: +5 em testes de resistência contra efeitos de área; acompanha capacete com viseira.')
mod('Blindada', ['protecao'], 'Só para proteção pesada: resistência a dano 5 e +1 espaço.', esp=1)
mod('Reforçada', ['protecao'], 'Defesa +2 e +1 espaço. Não pode ser reforçada e discreta ao mesmo tempo.', esp=1, d=2)
mod('Discreta (proteção)', ['protecao'], 'Só para proteção leve: –1 espaço e +5 em Crime para ocultar (mesmo sem treinamento).', esp=-1)
mod('Aprimorado', ['acessorio'], 'O bônus em perícia do acessório sobe para +5 (com função adicional, pode escolher de novo para ela).')
mod('Discreto', ['acessorio'], 'Miniaturizado ou disfarçado: –1 espaço e +5 em Crime para ocultar (mesmo sem treinamento).', esp=-1)
mod('Função adicional', ['acessorio'], '+2 em uma perícia adicional à sua escolha (aprovada pelo mestre).')
mod('Instrumental', ['acessorio'], 'O acessório funciona como um kit de perícia específico, escolhido ao aplicar.')

N = {g: sum(1 for x in IT if x[0] == g) for g in dict.fromkeys(x[0] for x in IT)}
assert N['arma'] == 35 and N['municao'] == 6 and N['protecao'] == 3 and N['acessorio'] == 3 and N['explosivo'] == 5, N
nomes = set()
def q(s): return "'" + str(s).replace("'", "''") + "'"
vals = []
for i, (g, sub, nome, d) in enumerate(IT):
    assert (g, nome) not in nomes, nome
    nomes.add((g, nome))
    vals.append('(%s,%s,%s,%s,%s,%s,%d,%s::jsonb)' % (q('op:item:' + g + ':' + nome), q('op'), q('livro-basico'), q(g), q(sub), q(nome), 100 + i, q(json.dumps(d, ensure_ascii=False))))

SQL = """-- Etapa 6d — Itens e armas do livro (Ordem Paranormal, Livro de Regras v1.2, capítulo 3)
-- Tabela global livro_itens (só leitura, atrás de login). Re-executável.
-- Gerado por tools/livro/gerar_op_itens.py (não edite as linhas à mão).

create table if not exists public.livro_itens (
  ref      text primary key,
  sistema  text not null default 'op',
  fonte    text not null default 'livro-basico',
  grupo    text not null check (grupo in ('arma', 'municao', 'protecao', 'acessorio', 'explosivo', 'operacional', 'paranormal', 'modificacao')),
  subgrupo text,
  nome     text not null,
  ordem    int  not null default 0,
  dados    jsonb not null default '{}'::jsonb
);
create index if not exists livro_itens_idx on public.livro_itens(sistema, grupo, ordem);
alter table public.livro_itens enable row level security;
drop policy if exists livro_itens_ler on public.livro_itens;
create policy livro_itens_ler on public.livro_itens for select to authenticated using (true);
revoke all on public.livro_itens from anon, authenticated;
grant select on public.livro_itens to authenticated;

insert into public.livro_itens(ref, sistema, fonte, grupo, subgrupo, nome, ordem, dados) values
""" + ',\n'.join(vals) + """
on conflict (ref) do update set sistema = excluded.sistema, fonte = excluded.fonte, grupo = excluded.grupo,
  subgrupo = excluded.subgrupo, nome = excluded.nome, ordem = excluded.ordem, dados = excluded.dados;
"""
raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
with open(os.path.join(raiz, 'schema_etapa6d_itens.sql'), 'w', encoding='utf-8') as fh:
    fh.write(SQL)
print(len(IT), 'linhas', N)
