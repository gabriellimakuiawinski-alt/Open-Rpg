#!/usr/bin/env python3
"""Extrai as criaturas do capítulo Ameaças do Livro de Regras de Ordem Paranormal (PDF) para um JSON.
Uso: python3 tools/livro/extrair_op_inimigos.py <livro.pdf> <saida.json> [pagina_ini pagina_fim]
Lê o PDF com pdfplumber (posição + fonte de cada palavra). Guarda só números fixos: o PDF mostra "3O+15"
(3 dados d20 + 15); como a contagem de dados é igual ao atributo, só o +15 vai para o banco."""
import sys, re, json
import pdfplumber

ELEM = {'SANGUE': 'Sangue', 'MORTE': 'Morte', 'CONHECIMENTO': 'Conhecimento', 'ENERGIA': 'Energia', 'MEDO': 'Medo'}
ACOES = {'PADRÃO': 'Padrão', 'MOVIMENTO': 'Movimento', 'COMPLETA': 'Completa', 'REAÇÃO': 'Reação', 'LIVRE': 'Livre', 'PASSIVA': 'Passiva'}
# elemento principal quando o PDF lista vários (ou nenhum) no cartão
SOBRE = {'O Diabo': 'Sangue', 'O Deus da Morte': 'Morte', 'Máscara do Desespero': 'Conhecimento', 'Anfitrião': 'Energia',
         'Degolificada': 'Medo', 'Anárquico': 'Energia'}
MIN = {'de', 'da', 'do', 'das', 'dos', 'e', 'o', 'a'}

def titulo(s):
    ps = s.lower().split()
    return ' '.join(p if (i and p in MIN) else p[:1].upper() + p[1:] for i, p in enumerate(ps))

def bonus(t):
    """'3O+15' -> 15 ; 'O+5' -> 5 ; '2O' -> 0 ; '5O-2' -> -2"""
    m = re.search(r'(?:^|\s)\d*\s*O(?:\s*([+\-–−]\s*\d+))?(?=[\s,;.)]|$)', t)
    if not m or not m.group(1): return 0
    return int(re.sub(r'\s|–|−', lambda x: '-' if x.group(0) in '–−' else '', m.group(1)))

def linhas(ws):
    ws = sorted(ws, key=lambda w: (round(w['top'] / 3), w['x0']))
    out, cur, ct = [], [], None
    for w in ws:
        t = w['top']
        if ct is None or abs(t - ct) > 3.2:
            if cur: out.append(cur)
            cur, ct = [w], t
        else: cur.append(w)
    if cur: out.append(cur)
    return [sorted(l, key=lambda w: w['x0']) for l in out]

def classe(w):
    f = w['fontname']
    if 'Wingdings' in f: return 'W'
    if 'd20' in f: return 'D'
    if 'ExtraBlack' in f: return 'H'
    if 'Black' in f: return 'K'      # TESTE / DANO
    if 'Bold' in f: return 'B'
    if 'Italic' in f: return 'I'
    return 'M'

def txt(l, excl=''):
    return re.sub(r'\s+', ' ', ' '.join(w['text'] for w in l if classe(w) not in excl)).strip()

def extrai(pdf, p0, p1):
    res = []
    for pi in range(p0 - 1, p1):
        pg = pdf.pages[pi]
        ws = pg.extract_words(extra_attrs=['size', 'fontname'])
        for i, w in enumerate(ws):
            if not (w['text'] == 'PONTOS' and ws[i + 1]['text'] == 'DE'): continue
            ya, xa = w['top'], w['x0']
            # nome + VD
            vds = [x for x in ws if x['text'] == 'VD' and 12.5 <= x['size'] <= 16.5 and x['top'] < ya]
            vds.sort(key=lambda x: (abs(x['x0'] - xa) > 300, ya - x['top']))
            vd = vds[0] if vds else None
            nome, vdn = '', ''
            if vd:
                nums = [x for x in ws if x['size'] >= 24 and x['text'].isdigit() and abs(x['top'] - vd['top']) < 15 and x['x0'] > vd['x0']]
                vdn = nums[0]['text'] if nums else ''
                if not vdn:     # ameaças da Realidade: o número do VD tem o mesmo tamanho do 'VD'
                    n2 = [x for x in ws if x['text'].isdigit() and abs(x['top'] - vd['top']) < 6 and 0 < x['x0'] - vd['x1'] < 40]
                    vdn = n2[0]['text'] if n2 else ''
                nw = [x for x in ws if 12.5 <= x['size'] <= 28 and x['text'] != 'VD' and not x['text'].isdigit()
                      and vd['top'] - 40 <= x['top'] <= vd['top'] + 30 and x['x0'] < vd['x0'] and x['x0'] > vd['x0'] - 230]
                nome = ' '.join(x['text'] for x in sorted(nw, key=lambda x: (round(x['top'] / 4), x['x0'])))
            if not vdn:
                for x in ws:
                    if x['text'] == 'VD' and 12.5 <= x['size'] <= 16.5:
                        nn = [y for y in ws if y['size'] >= 24 and y['text'].isdigit() and abs(y['top'] - x['top']) < 15 and y['x0'] > x['x0']]
                        if nn: vdn = nn[0]['text']
            boss = False
            if not nome:  # chefes: título grande
                nw = [x for x in ws if x['size'] >= 40 and x['top'] < ya]
                nome = ' '.join(x['text'] for x in sorted(nw, key=lambda x: (round(x['top'] / 4), x['x0'])))
                boss = True
            ref = vd['top'] if vd else ya - 130
            rx = vd['x0'] if vd else xa
            cri = [x for x in ws if x['text'] == 'CRIATURA' and x['top'] >= ref - 5 and abs(x['x0'] - rx) < 260]
            cri.sort(key=lambda x: x['top'] - ref)
            ctop = cri[0]['top'] if cri else ya - 130
            cx = cri[0]['x0'] if cri else xa
            L = min(cx if cx < 290 or xa >= 290 else xa, xa if xa < 290 else cx) - 3
            esq_col = cx < 290
            els = [ELEM[x['text']] for x in ws if x['text'] in ELEM and x['size'] <= 10 and ctop - 40 < x['top'] < ctop + 6 and abs(x['x0'] - cx) < 260]
            els = list(dict.fromkeys(els))
            ok = [x for x in ws if any(k in x['fontname'] for k in ('Optima', 'd20', 'Wingdings')) and x['size'] <= 12.5 and x['top'] < 748]
            if boss:      # chefes: ficha inteira, esquerda e depois direita
                esq = [x for x in ok if x['x0'] < 290 and x['top'] >= 90]
                dir_ = [x for x in ok if x['x0'] >= 290 and x['top'] >= 90]
            elif esq_col:   # coluna da esquerda (+ continuação na direita)
                esq = [x for x in ok if x['x0'] < 290 and x['top'] >= ctop - 2]
                dir_ = [x for x in ok if x['x0'] >= 290 and (xa >= 290 or True)]
            else:
                esq = [x for x in ok if x['x0'] >= 290 and x['top'] >= ctop - 2]
                dir_ = []
            ln = linhas([x for x in esq if classe(x) != 'W']) + linhas([x for x in dir_ if classe(x) != 'W'])
            # continuação na página seguinte (sem outra ficha)
            if pi + 1 < len(pdf.pages):
                nx = pdf.pages[pi + 1].extract_words(extra_attrs=['size', 'fontname'])
                if not any(a['text'] == 'PONTOS' and nx[j + 1]['text'] == 'DE' for j, a in enumerate(nx[:-1])):
                    ox = [x for x in nx if 'Optima' in x['fontname'] or 'd20' in x['fontname']]
                    ox = [x for x in ox if x['size'] <= 12.5 and 60 < x['top'] < 745]
                    if len(ox) >= 8:
                        ln += linhas([x for x in ox if x['x0'] < 290 and classe(x) != 'W']) + linhas([x for x in ox if x['x0'] >= 290 and classe(x) != 'W'])
            vdn = vdn.lstrip('0') or vdn
            res.append(dict(pag=pi + 1, nome=nome, vd=vdn, elementos=els, L=L,
                            linhas=[l for l in ln if txt(l) not in ('|', '')]))
    return res

def le(b):
    d = dict(tamanho='', pv=0, def_=0, desloc=9, atr=dict(agi=0, **{'for': 0}, int=0, pre=0, vig=0), fort=0, refl=0, vont=0, ini=0, perc=0,
             pericias=[], resist='', vuln='', sentidos='', ataques=[], habilidades=[], desc='')
    L = b['linhas']; n = len(L); i = 0
    campo = None; acao = 'Passiva'; atual = None; emacoes = False; atk = None
    def fecha():
        nonlocal atual
        if atual and (atual['desc'].strip() or atual['n']):
            atual['desc'] = atual['desc'].strip(); d['habilidades'].append(atual)
        atual = None
    while i < n:
        l = L[i]; t = txt(l); c = classe(l[0]); u = t.upper()
        i += 1
        if not t: continue
        m = re.search(r'(?:C\s?RIATURA|RELÍQUIA)\s+(PEQUENO|M[ÉE]DIO|GRANDE|ENORME|COLOSSAL|MIN[ÚU]SCULO|DIMINUTO)', t)
        if m and not d['tamanho']:
            d['tamanho'] = titulo(m.group(1)); campo = None; continue
        if u.startswith('PRESENÇA PERTURBADORA'):
            nx = txt(L[i]) if i < n else ''; i += 1
            atual = dict(n='Presença Perturbadora', acao='Passiva', desc=nx); fecha(); campo = None; continue
        if c in 'BH' and not emacoes and u.startswith('SENTIDOS'):
            m = re.search(r'PERCEPÇÃO\s*(.*?)(?:\s{2,}|$)', t)
            d['perc'] = bonus(' ' + re.sub(r'^SENTIDOS\s*PERCEPÇÃO', '', t).split('Percep')[0])
            r = re.sub(r'^SENTIDOS\s*PERCEPÇÃO\s*', '', t).strip()
            d['sentidos'] = r; campo = None; continue
        if c in 'BH' and not emacoes and u.startswith('INICIATIVA'):
            d['ini'] = bonus(' ' + re.sub(r'^INICIATIVA', '', t)); campo = None; continue
        if c in 'BH' and not emacoes and u.startswith('DEFESA'):
            m = re.match(r'DEFESA\s*(\d+)\s*FORTITUDE\s*(.*)', t)
            if m: d['def_'] = int(m.group(1)); d['fort'] = bonus(' ' + m.group(2))
            campo = None; continue
        if c in 'BH' and not emacoes and u.startswith('REFLEXOS'): d['refl'] = bonus(' ' + t[8:]); continue
        if c in 'BH' and not emacoes and u.startswith('VONTADE'): d['vont'] = bonus(' ' + t[7:]); continue
        if c in 'BH' and not emacoes and u.startswith('PONTOS DE VIDA'):
            m = re.search(r'(\d+)\s*[|ǀI]', t) or re.search(r'VIDA\s*(\d+)', t); d['pv'] = int(m.group(1)) if m else 0; campo = None; continue
        if c in 'BH' and not emacoes and u.startswith('RESISTÊNCIAS'): campo = 'resist'; d['resist'] = re.sub(r'^RESISTÊNCIAS\s*', '', t); continue
        if c in 'BH' and not emacoes and u.startswith('IMUNIDADES'): campo = 'resist'; d['resist'] = (d['resist'] + ' ' if d['resist'] else '') + 'Imune: ' + re.sub(r'^IMUNIDADES\s*', '', t); continue
        if c in 'BH' and not emacoes and u.startswith('VULNERABILIDADES'): campo = 'vuln'; d['vuln'] = re.sub(r'^VULNERABILIDADES\s*', '', t); continue
        if c in 'BH' and not emacoes and u.startswith('ATRIBUTOS'): campo = None; continue
        m = re.match(r'AGI\s*([\d–—-]+)\s*FOR\s*([\d–—-]+)\s*INT\s*([\d–—-]+)\s*PRE\s*([\d–—-]+)\s*VIG\s*([\d–—-]+)', t)
        if m:
            for k, v in zip(('agi', 'for', 'int', 'pre', 'vig'), m.groups()): d['atr'][k] = int(v) if v.isdigit() else 0
            campo = None; continue
        if c in 'BH' and not emacoes and u.startswith('PERÍCIAS'):
            campo = 'per'; d['_per'] = re.sub(r'^PERÍCIAS\s*', '', t); continue
        if c in 'BH' and not emacoes and u.startswith('DESLOCAMENTO'):
            m = re.search(r'(\d+(?:[.,]\d+)?)\s*m', t); d['desloc'] = float(m.group(1).replace(',', '.')) if m else 9
            d['_desl'] = re.sub(r'^DESLOCAMENTO\s*', '', t); campo = None; continue
        if u == 'AÇÕES' or u.startswith('AÇÕES'):
            fecha(); emacoes = True; campo = None; continue
        if campo in ('resist', 'vuln') and c not in 'HK':
            d[campo] += ' ' + t; continue
        if campo == 'per' and c not in 'H':
            d['_per'] += ' ' + t; continue
        # --- habilidades / ações
        w0 = l[0]['text']
        if emacoes and w0 in ACOES and len(l) > 1 and classe(l[1]) in 'HW' or (emacoes and w0 in ACOES and any(classe(x) == 'H' for x in l)):
            fecha(); atk = None
            acao = ACOES[w0]; nm = txt([x for x in l if classe(x) == 'H'])
            atual = dict(n=titulo(nm), acao=acao, desc=''); continue
        if c == 'H' or (c == 'M' and False):
            nm = txt([x for x in l if classe(x) in 'HI'], '')
            nmH = txt([x for x in l if classe(x) == 'H'])
            alc = txt([x for x in l if classe(x) == 'I'])
            if emacoes and alc and atual is not None and acao:
                # cabeçalho de ataque; o TESTE vem na linha seguinte
                atk = dict(n=titulo(nmH), alc=alc, teste=0, dano='')
                d['ataques'].append(atk); continue
            if atual is not None and not atual['desc'] and atual.get('_h') and not emacoes:
                atual['n'] += ' ' + titulo(nmH); continue   # nome em duas linhas
            fecha(); atual = dict(n=titulo(nmH), acao='Passiva' if not emacoes else acao, desc='', _h=1); continue
        if c == 'K' and u.startswith('TESTE'):
            m = re.match(r'TESTE\s*(.*?)\s*\|\s*DANO\s*(.*)', t)
            if m and atk is not None and atk['dano'] == '':
                atk['teste'] = bonus(m.group(1)); atk['dano'] = m.group(2).strip()
                cr = re.search(r'cr[ií]tico\s*(x\d|\d+)', m.group(1))
                if cr: atk['alc'] = (atk['alc'] + ', ' if atk['alc'] else '') + 'crítico ' + cr.group(1)
            elif m:
                atk = dict(n=(atual or {}).get('n', 'Ataque'), alc='', teste=bonus(m.group(1)), dano=m.group(2).strip()); d['ataques'].append(atk)
            else:
                if atual is not None: atual['desc'] += ' ' + t
            continue
        if atual is not None:
            atual['desc'] += ' ' + t
    fecha()
    for h in d['habilidades']: h.pop('_h', None)
    d['habilidades'] = [h for h in d['habilidades'] if h['n'].lower() != 'agredir']
    for h in d['habilidades']:
        x = re.sub(r'(?<=[a-zà-ú])- (?=[a-zà-ú])', '', h['desc'])
        x = re.sub(r'(\s\d{3})+\s*$', '', x).strip()
        h['desc'] = x
    for a in d['ataques']:
        a['alc'] = re.sub(r'\s+(MÉDIO|GRANDE|PEQUENO|ENORME|COLOSSAL)(?=,|$)', '', a['alc'])
    d['sentidos'] = re.sub(r'^.*?(?=[A-ZÀ-Ú][a-zà-ú]{3,})', '', d['sentidos']).strip() if re.search(r'[A-ZÀ-Ú][a-zà-ú]{3,}', d['sentidos']) else ''
    # perícias
    per = d.pop('_per', '')
    ps = []
    for m in re.finditer(r'([A-ZÀ-Ú][A-ZÀ-Ú\- ]+?)\s+(\d*\s*O\s*(?:[+\-–−]\s*\d+)?)(?=\s+[A-ZÀ-Ú]{3,}|\s*,|\s*$)', per):
        ps.append(dict(n=titulo(m.group(1).strip()), b=bonus(' ' + m.group(2))))
    for q in ps:
        if q['n'] == 'Ciência': q['n'] = 'Ciências'
    d['pericias'] = ps; d['_per_txt'] = per
    d['def'] = d.pop('def_')
    d['desloc'] = d['desloc']
    d['_desl'] = d.get('_desl', '')
    return d

if __name__ == '__main__':
    pdf = pdfplumber.open(sys.argv[1])
    a = int(sys.argv[3]) if len(sys.argv) > 3 else 176
    z = int(sys.argv[4]) if len(sys.argv) > 4 else 292
    out = []
    for b in extrai(pdf, a, z):
        d = le(b)
        nm = titulo(b['nome'])
        el = SOBRE.get(nm) or (b['elementos'] or ['Outro'])[0]
        out.append(dict(pag=b['pag'], nome=nm, vd=b['vd'], elemento=el, elementos=b['elementos'], dados=d))
    json.dump(out, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
    print(len(out), 'criaturas')
