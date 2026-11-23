#!/usr/bin/env python3
# Gera sfl-dados.js (Search For Light) a partir de docs/sfl/classes-sfl2.md, docs/sfl/sistema-sfl2.md e docs/sfl/equipamento-sfl2.md.
# Edite os .md (regras do mestre) e rode de novo: python3 tools/livro/gerar_sfl_dados.py
import re, json, pathlib
R = pathlib.Path(__file__).resolve().parents[2]
cl = (R/'docs/sfl/classes-sfl2.md').read_text(encoding='utf-8')
si = (R/'docs/sfl/sistema-sfl2.md').read_text(encoding='utf-8')
def limpa(s): return re.sub(r'\*\*', '', s).strip()
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower().replace('ç','c').replace('ã','a').replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ô','o').replace('ê','e').replace('ú','u').replace('â','a')).strip('-')

# ---- classes
classes = []
sec = re.split(r'\n### 4\.\d ', cl)[1:]
for s in sec:
    s = s.split('\n## 5.')[0]
    cab = s.split('\n', 1)[0]
    m = re.match(r'(\w+) \((\w+)\)', cab)
    nome, atr = m.group(1), m.group(2).lower()
    per = re.search(r'Perícias \(2 entre\): (.+)', s).group(1).rstrip('.').split(', ')
    bonus = re.search(r'- Bônus: (.+)', s).group(1).strip()
    ini = re.search(r'- Inicial \*\*(.+?):?\*\*:? (.+)', s)
    habs = []
    h = s.split('**Habilidades à escolha**')[1].split('**Trilhas')[0]
    for l in h.strip().split('\n'):
        mm = re.match(r'- \*\*(.+?):\*\* (.+)', l)
        if mm: habs.append({'n': mm.group(1), 'd': mm.group(2)})
    tr = []
    t = s.split('**Trilhas (marcos 1, 3, 5, 7)**')[1]
    for bloco in re.split(r'\n- \*\*', '\n' + t.strip())[1:]:
        tn = re.match(r'(.+?)\*\* \((.+?)\)', bloco)
        hs = [{'n': a, 'd': b} for a, b in re.findall(r'\d\. \*\*(.+?):\*\* (.+)', bloco)]
        tr.append({'id': slug(tn.group(1)), 'n': tn.group(1), 't': tn.group(2), 'habs': hs})
    classes.append({'id': slug(nome), 'n': nome, 'atr': atr, 'pericias': per, 'bonus': bonus,
                    'ini': {'n': ini.group(1).rstrip(':'), 'd': ini.group(2)}, 'habs': habs, 'trilhas': tr})
ATRID = {'corpo': 'cor', 'reflexo': 'ref', 'mente': 'men', 'presença': 'pre', 'presenca': 'pre'}
for c in classes: c['atr'] = ATRID[c['atr']]

# ---- origens
origens = []
for l in cl.split('## 5. Origens')[1].split('\n'):
    mm = re.match(r'\| (\d+) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|', l)
    if mm: origens.append({'id': slug(mm.group(2)), 'n': mm.group(2), 'pericias': [x.strip() for x in mm.group(3).split(',')], 'traco': mm.group(4), 'peso': mm.group(5)})

# ---- poderes
poderes = []
p7 = si.split('## 7. Poderes (linhas)')[1].split('[PENDENTE]')[0]
for bloco in re.split(r'\n\*\*', p7)[1:]:
    cab = bloco.split('\n', 1)[0]
    mm = re.match(r'(.+?)\*\* \((.+?)\)', cab)
    nv = [{'nv': int(a), 'n': b, 'custo': int(c), 'd': d} for a, b, c, d in re.findall(r'- N(\d) (.+?) \((\d)\): (.+)', bloco)]
    poderes.append({'id': slug(mm.group(1)), 'n': mm.group(1), 't': mm.group(2), 'niveis': nv})

# ---- armas (seção 8.3)
armas = []
s83 = si.split('### 8.3 Tabela de armas')[1].split('### 8.4')[0]
espec = s83.split('**Armas especiais')[1]
simples = s83.split('**Armas especiais')[0]
def linhas(txt, cat):
    for l in txt.split('\n'):
        c = [x.strip() for x in l.strip().strip('|').split('|')]
        if len(c) == 5 and c[0] not in ('Arma', '---') and not c[0].startswith('---'):
            yield {'n': c[0], 'dano': c[1], 'crit': c[2], 'traco': c[3], 'efeito': c[4], 'cat': cat}
for bloco in re.split(r'\n#### ', simples)[1:]:
    nome = bloco.split('\n', 1)[0].strip()
    cat = {'Contundente': 'contundente', 'Cortante': 'cortante', 'Arremesso': 'arremesso'}.get(nome, 'tiro')
    armas += list(linhas(bloco, cat))
armas += list(linhas(espec, 'especial'))

# ---- equipamento e inventário (livro V1.2, cap. 13): docs/sfl/equipamento-sfl2.md
eq = (R/'docs/sfl/equipamento-sfl2.md').read_text(encoding='utf-8')
def secao(cab, txt=eq):
    i = txt.index(cab); j = txt.find('\n#', i + len(cab))
    return txt[i:j if j > 0 else None]
def tabela(txt):
    L = [[c.strip() for c in l.strip().strip('|').split('|')] for l in txt.split('\n') if l.strip().startswith('|')]
    if not L: return []
    cab = L[0]
    return [dict(zip(cab, r)) for r in L[1:] if not set(''.join(r)) <= set('-: ')]
def num(s):
    m = re.search(r'(\d+(?:[.,]\d+)?)', s or ''); return float(m.group(1).replace(',', '.')) if m else None
def espaco(s):
    """'1 (pilha de 3)' -> (1, 3); '0' -> (0, None); '—' -> (0, None)"""
    e = num(s.split('(')[0]) if s and s[0].isdigit() else 0
    m = re.search(r'pilha de (\d+)', s or '')
    return (int(e or 0), int(m.group(1)) if m else None)
def rar(s):
    s = s or ''; r = re.match(r'(Comum|Incomum|Raro|Fabricável)', s)
    return (r.group(1) if r else ''), ('fabricável' in s.lower() or s.startswith('Fabricável')), (s.split(':', 1)[1].strip() if ':' in s else '')
def nrm(s): return slug(s.replace(' / ', ' ou ').replace('/', ' ou '))

# espaços, preço e raridade das armas (seção 2)
ARMA_EQ = {}
for r in tabela(secao('## 2. Espaços de todas as armas')):
    if 'Arma' not in r: continue
    e, pl = espaco(r['Espaços']); ra, fab, _ = rar(r['Raridade'])
    ARMA_EQ[nrm(r['Arma'])] = {'esp': e, 'pilha': pl, 'preco': num(r['Preço']), 'rar': ra, 'fab': fab, 'n': r['Arma']}
# grupo de modificação e marcas de cada arma (seção 4.2 e 4.3/4.4; "metal" é leitura do Claude)
GRUPO = {'soco-ingles': ('pequena', 'cont metal'), 'taco-de-madeira': ('comum', 'cont'), 'cano-de-ferro': ('comum', 'cont metal'), 'taco-com-pregos': ('comum', 'cont'),
  'barra-de-ferro-ou-pe-de-cabra': ('comum', 'cont metal'), 'martelo': ('pequena', 'cont metal'), 'chave-inglesa': ('pequena', 'cont metal'), 'cassetete': ('pequena', 'cont'),
  'marreta-2-maos': ('pesada', 'cont metal duas'), 'taser': ('pequena', 'cont'), 'canivete': ('pequena', 'cort metal'), 'faca-de-cozinha': ('pequena', 'cort metal'),
  'faca-de-combate': ('pequena', 'cort metal'), 'machadinha': ('comum', 'cort metal machado'), 'facao-ou-machete': ('comum', 'cort metal'), 'machado-2-maos': ('pesada', 'cort metal duas machado'),
  'foice-2-maos': ('pesada', 'cort metal duas'), 'lanca-caseira-2-maos': ('pesada', 'cort duas'), 'serra-manual': ('comum', 'cort metal'), 'motosserra-2-maos': ('moto', 'cort motosserra'),
  'pistola-9-mm': ('pistola', 'fogo pistola'), 'pistola-45': ('pistola', 'fogo pistola'), 'revolver-38': ('pistola', 'fogo revolver'), 'revolver-357': ('pistola', 'fogo revolver'),
  'pistola-de-sinalizacao': ('sinal', 'fogo'), 'escopeta-de-cano-duplo': ('longa', 'fogo escopeta caneduplo'), 'rifle-de-caca': ('longa', 'fogo rifle'),
  'arco-curto': ('arco', 'arco'), 'arco-composto': ('arco', 'arco'), 'besta-leve': ('arco', 'arco'), 'besta-pesada': ('arco', 'arco'),
  'submetralhadora': ('militar', 'fogo smg'), 'escopeta-pump': ('militar', 'fogo escopeta pump'), 'rifle-de-precisao': ('militar', 'fogo precisao'), 'fuzil-de-assalto': ('militar', 'fogo fuzil'),
  'lanca-chamas-improvisado': ('chamas', 'chamas')}
LIMITE = {'pequena': 1, 'comum': 2, 'pesada': 3, 'moto': 1, 'escudo': 1, 'arr': 0, 'pistola': 2, 'sinal': 1, 'longa': 2, 'arco': 2, 'militar': 3, 'chamas': 1}
for a in armas:
    k = nrm(a['n']); x = ARMA_EQ.get(k) or next((v for kk, v in ARMA_EQ.items() if k.startswith(kk) or kk.startswith(k)), None)
    if x: a.update({kk: v for kk, v in x.items() if kk != 'n' and v is not None})
    g = GRUPO.get(k, ('arr', 'arr') if a['cat'] == 'arremesso' else (None, ''))
    a['g'] = g[0]; a['tags'] = g[1].split()
    if a['cat'] == 'arremesso' and 'arr' not in a['tags']: a['tags'].append('arr')
faltam = [a['n'] for a in armas if 'esp' not in a and a['n'] != 'Punhos']
assert not faltam, ('armas sem espaço', faltam)

def mats(s):
    """'2 Sucata, 1 Peça' -> {'Sucata': 2, 'Peças': 1}; 'combustível' -> {'Combustível': 1}"""
    out = {}
    for p in re.split(r',\s*', s):
        p = p.strip().rstrip('.')
        if not p or p.lower() == 'sem teste': continue
        m = re.match(r'(\d+|Uma|Um)?\s*(.+)', p, re.I); q = m.group(1); nome = m.group(2).strip()
        q = 1 if not q or not q.isdigit() else int(q)
        low = nome.lower()
        if 'garrafa' in low or 'sucata' in low: nome = 'Sucata'
        elif low.startswith('peça'): nome = 'Peças'
        elif low.startswith('químico'): nome = 'Químicos'
        elif low.startswith('tecido'): nome = 'Tecido'
        elif low.startswith('combust'): nome = 'Combustível'
        elif 'pilha uv' in low: nome = 'Pilha UV'
        elif 'lanterna' in low: nome = 'Lanterna|Lanterna UV'
        elif 'flecha' in low: nome = 'Flechas ou virotes'
        out[nome] = out.get(nome, 0) + q
    return out

# modificações (4.3 e 4.4)
PARA = {'pregos-e-arame': 'cont', 'lamina-soldada': 'cont', 'fio-afiado': 'cort', 'empunhadura-de-fita': 'corpo', 'contrapeso': 'duas', 'eletrificada': 'metal',
  'pano-em-chamas': 'corpo !motosserra', 'alca-leve': 'grande', 'silenciador-improvisado': 'pistola smg rifle fuzil', 'mira-luneta-ou-ponto-vermelho': 'fogo arco',
  'carregador-estendido': 'pistola smg fuzil pump', 'carregador-rapido': 'revolver caneduplo', 'lanterna-acoplada': 'fogo', 'cano-serrado': 'escopeta',
  'corda-reforcada': 'arco', 'aljava-de-cinto': 'arco', 'bocal-largo': 'chamas'}
AUTO = {'fio-afiado': {'crit': 1}, 'empunhadura-de-fita': {'blq': 1}, 'mira-luneta-ou-ponto-vermelho': {'mira': 1}, 'corda-reforcada': {'dano': 1},
  'silenciador-improvisado': {'dano': -1}, 'cano-serrado': {'dados': 1}, 'alca-leve': {'esp': -1}, 'lamina-soldada': {'dual': 1},
  'pregos-e-arame': {'fx': 'Sangramento'}, 'contrapeso': {'fx': 'Derruba'}, 'eletrificada': {'fx': 'Atordoa 1 rodada'}, 'pano-em-chamas': {'fx': 'Queimando'},
  'lanterna-acoplada': {'luz': 10}}
mods = []
for cab in ('### 4.3', '### 4.4'):
    for r in tabela(secao(cab)):
        i = slug(r['Modificação'])
        assert i in PARA, ('modificação sem regra de arma', i)
        mods.append({'id': i, 'n': r['Modificação'], 'para': r['Para'], 'pp': PARA[i].split(), 'd': r['Efeito'], 'mat': mats(r['Materiais']), 'auto': AUTO.get(i, {})})

# receitas (seção 5)
QUIM = {'Molotov', 'Granada de fumaça', 'Bomba caseira'}
receitas = []
for r in tabela(secao('## 5. Fabricação')):
    m = re.match(r'(.+?)(?: \((\d+)\))?$', r['Receita']); prod, q = m.group(1).strip(), int(m.group(2) or 1)
    te = r['Teste']; mt = re.match(r'(.+?) DT (\d+)', te)
    pers = [x.strip() for x in mt.group(1).split(' ou ')] if mt else []
    receitas.append({'n': prod, 'q': q, 'mat': mats(r['Materiais']), 'per': pers, 'dt': int(mt.group(2)) if mt else 0, 'quim': prod in QUIM,
                     'nota': (re.search(r'\((.+)\)', te).group(1) if '(' in te else ''), 'explode': 'explode' in te})

# itens do catálogo (seção 3)
itens = []
def item(n, tipo, esp, pilha, preco, ra, fab, d, extra=None, lote=None):
    it = {'n': n, 'tipo': tipo, 'esp': esp, 'preco': preco, 'rar': ra, 'd': d}
    if pilha: it['pilha'] = pilha
    if esp == 0 and tipo not in ('mochila',): it['bolso'] = 1
    if fab: it['fab'] = 1
    if lote: it['lote'] = lote
    if extra: it.update(extra)
    itens.append(it)
for r in tabela(secao('### 3.2 Munição')):
    ra, fab, ef = rar(r['Raridade']); pl = int(num(r['Pilha (1 espaço)']))
    item(r['Item'], 'municao', 1, pl if pl > 1 else None, num(r['Preço da pilha']), ra, fab, ef, lote=pl if pl > 1 else None)
for r in tabela(secao('### 3.3 Armaduras')):
    ra, fab, _ = rar(r['Raridade']); sub = r['Tipo'].lower()
    ob = '' if r['Observação'] in ('—', '') else r['Observação']
    ex = {'sub': sub, 'red': int(num(r['Reduz'])), 'desvVest': [x for x in ('Parkour', 'Furtividade') if x in ob or sub == 'pesada']}
    if 'Contra tiro' in ob: ex['redTiro'] = 3
    item(r['Armadura'], 'armadura', {'leve': 1, 'média': 2, 'pesada': 3}[sub], None, num(r['Preço']), ra or ('Fabricável' if 'abric' in r['Preço'] else ''), fab or 'abric' in r['Preço'], ob, ex)
CARGA = {'Mochila escolar': {'mochila': 2}, 'Mochila de trilha': {'mochila': 4}, 'Mochila militar': {'mochila': 5, 'prontos': 1}, 'Bolsa de cintura': {'prontos': 1},
  'Coldre ou bainha': {'prontos': 1}, 'Bandoleira': {'bandoleira': 1}}
LUZ = {'Lanterna': {'luz': {'t': 'c', 'm': 10}}, 'Lanterna UV': {'luz': {'t': 'c', 'm': 6}, 'uv': 1}}
USO = {'Bandagem': 'bandagem', 'Kit médico': 'kit', 'Analgésico': 'analgesico', 'Antibiótico': 'gasta', 'Adrenalina': 'adrenalina', 'Estabilizador': 'estabilizador',
  'Ração': 'gasta', 'Água (garrafa)': 'gasta', 'Pilha UV': 'gasta'}
for cab, tp in (('### 3.4 Carregar', 'geral'), ('### 3.5 Exploração', 'geral'), ('### 3.6 Médicos', 'consumivel'), ('### 3.7 Comida e ferramentas', 'consumivel')):
    for r in tabela(secao(cab)):
        n = r['Item']; e, pl = espaco(r['Espaços']); ra, fab, _ = rar(r['Raridade'])
        ex = dict(CARGA.get(n, {})); ex.update(LUZ.get(n, {}))
        if n in USO: ex['uso'] = USO[n]
        if n == 'Kit médico': ex['usos'] = 5
        t = 'mochila' if 'mochila' in ex else ('consumivel' if n in USO else ('geral' if tp == 'consumivel' and n.startswith('Kit') else tp))
        if n.startswith('Materiais'):
            for mn, pr in re.findall(r'(Sucata|Tecido|Peças|Químicos) (\d+) €', r['Preço']):
                item(mn, 'material', 1, 5, float(pr), 'Comum' if mn in ('Sucata', 'Tecido') else 'Incomum', False, r['Efeito'])
            continue
        item(n, t, e, pl, num(r['Preço']), ra, fab, r['Efeito'], ex)
s1 = secao('## 1. Inventário')
out_eq = {'mods': mods, 'limites': LIMITE, 'receitas': receitas, 'itens': itens}

out = {'classes': classes, 'origens': origens, 'poderes': poderes, 'armas': armas, **out_eq}
js = '/* sfl-dados.js — Search For Light: classes, trilhas, origens, poderes, armas, equipamento, modificações e receitas. GERADO por tools/livro/gerar_sfl_dados.py (não edite à mão). */\nwindow.SFLD=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n'
(R/'sfl-dados.js').write_text(js, encoding='utf-8')
print(len(mods), 'modificações', len(receitas), 'receitas', len(itens), 'itens');print(len(classes), 'classes', sum(len(c['trilhas']) for c in classes), 'trilhas', len(origens), 'origens', len(poderes), 'poderes', len(armas), 'armas')
for c in classes: print(c['n'], len(c['habs']), [len(t['habs']) for t in c['trilhas']])
