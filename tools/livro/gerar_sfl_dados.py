#!/usr/bin/env python3
# Gera sfl-dados.js (Search For Light) a partir de docs/sfl/classes-sfl2.md e docs/sfl/sistema-sfl2.md.
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

out = {'classes': classes, 'origens': origens, 'poderes': poderes, 'armas': armas}
js = '/* sfl-dados.js — Search For Light: classes, trilhas, origens, poderes e armas. GERADO por tools/livro/gerar_sfl_dados.py (não edite à mão). */\nwindow.SFLD=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n'
(R/'sfl-dados.js').write_text(js, encoding='utf-8')
print(len(classes), 'classes', sum(len(c['trilhas']) for c in classes), 'trilhas', len(origens), 'origens', len(poderes), 'poderes', len(armas), 'armas')
for c in classes: print(c['n'], len(c['habs']), [len(t['habs']) for t in c['trilhas']])
