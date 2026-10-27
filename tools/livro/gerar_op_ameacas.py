#!/usr/bin/env python3
"""Gera schema_etapa9c_ameacas.sql: as 18 'Ameaças da Realidade' (criminosos, cultistas, policiais e animais, livro p.284-289)
na tabela livro_inimigos (ids 50 em diante). Lê o TEXTO do livro (guardado no projeto privado, nunca no repositório).
Uso: python3 tools/livro/gerar_op_ameacas.py <texto-do-livro.md>   (o arquivo parte3 do projeto, com as marcas '=== PDF p.N ===')"""
import sys, os, re, json
sys.path.insert(0, os.path.dirname(__file__))
import extrair_op_inimigos as X
from extrair_op_inimigos import bonus
X.MIN |= {'em', 'na', 'no', 'nas', 'nos', 'com', 'para'}
titulo = X.titulo

NOMES = [('BANDIDO', 'Bandido'), ('CAPANGA', 'Capanga'), ('DEALUGUEL', 'Soldado de Aluguel'), ('ASSASSINO', 'Assassino'),
         ('MERCENÁRIO', 'Comandante Mercenário'), ('INICIADO', 'Iniciado'), ('INVESTIDO', 'Investido'), ('LÍDERDECULTO', 'Líder de Culto'),
         ('POLICIAL', 'Policial'), ('DEELITE', 'Policial de Elite'), ('CHEFEDEPOLÍCIA', 'Chefe de Polícia'), ('CÃODEGUARDA', 'Cão de Guarda'),
         ('ENXAMEDEABELHAS', 'Enxame de Abelhas'), ('ENXAMEDERATOS', 'Enxame de Ratos'), ('JACARÉ', 'Jacaré'), ('JAVAPORCO', 'Javaporco'),
         ('ONÇA-PINTADA', 'Onça-pintada'), ('SUCURI', 'Sucuri')]
ACOES = {'PADRÃO': 'Padrão', 'MOVIMENTO': 'Movimento', 'COMPLETA': 'Completa', 'REAÇÃO': 'Reação', 'LIVRE': 'Livre', 'PASSIVA': 'Passiva'}
TAM = {'PEQUENO': 'Pequeno', 'MÉDIO': 'Médio', 'GRANDE': 'Grande', 'ENORME': 'Enorme', 'COLOSSAL': 'Colossal', 'MINÚSCULO': 'Minúsculo'}

txt = open(sys.argv[1], encoding='utf-8').read()
a = txt.index('=== PDF p.292 '); z = txt.index('PERIGOS', a)
txt = re.sub('[\ue000-\uf8ff]', ' ', txt)
L = [re.sub(r' {2,}', '  ', l.rstrip()) for l in txt[a:z].split('\n') if l.strip() and not l.startswith('===') and not re.fullmatch(r'\d{3}', l.strip())]
# cabeçalhos: 'NOME VD n'
cab = [(i, re.match(r'^(.*?) VD (\d+)$', l)) for i, l in enumerate(L)]
cab = [(i, m.group(1).strip(), m.group(2)) for i, m in cab if m]
assert len(cab) == 18, len(cab)
def parse(bloco, nome, vd, pag):
    d = dict(tamanho='Médio', pv=0, desloc=9, atr=dict(agi=0, **{'for': 0}, int=0, pre=0, vig=0), fort=0, refl=0, vont=0, ini=0, perc=0,
             pericias=[], resist='', vuln='', sentidos='', ataques=[], habilidades=[], desc='')
    # cabeçalho da ficha: da linha do tipo até o DESLOCAMENTO (junta as linhas, que quebram de forma irregular)
    it = next(k for k, l in enumerate(bloco) if re.match(r'^(PESSOA|ANIMAL(?: \(ENXAME\))?)\s+(PEQUENO|MÉDIO|GRANDE|ENORME|COLOSSAL|MINÚSCULO)$', l.strip().upper()))
    KW = ('SENTIDOS', 'DEFESA', 'PONTOS', 'PERÍCIAS', 'DESLOCAMENTO', 'AGI', 'PESSOA', 'ANIMAL')
    fim_h = len(bloco)
    for k in range(it + 1, len(bloco)):
        l = bloco[k].strip()
        if l.upper().startswith('AÇÕES') or (re.match(r'^[A-ZÀ-Ú]{4,}(?: [A-ZÀ-Ú]{3,})*\s+\S', l) and not l.startswith(KW)):
            fim_h = k; break
    H = re.sub(r'\s+', ' ', ' '.join(x.strip() for x in bloco[it:fim_h]))
    fim_h -= 1
    m = re.match(r'^(?:PESSOA|ANIMAL(?: \(ENXAME\))?)\s+(\S+)', H.upper()); d['tamanho'] = TAM.get(m.group(1), 'Médio') if m else 'Médio'
    m = re.search(r'SENTIDOS Percepção (.*?) \| Iniciativa (\S+)(.*?) DEFESA (\d+)', H)
    if not m: print('SEM SENTIDOS', nome, H)
    d['perc'] = bonus(' ' + m.group(1)); d['ini'] = bonus(' ' + m.group(2)); d['sentidos'] = m.group(3).strip(); d['def'] = int(m.group(4))
    m = re.search(r'Fortitude (.*?) \| Reflexos (.*?) \| Vontade (\S+)(.*?) PONTOS DE VIDA (\d+)', H)
    d['fort'], d['refl'], d['vont'] = (bonus(' ' + x) for x in m.groups()[:3]); d['pv'] = int(m.group(5))
    ex = m.group(4).strip()
    for mm in re.finditer(r'(Resistências?|Imunidades?|Vulnerabilidades?)\s+(.*?)(?=\s*(?:Resistência|Imunidade|Vulnerabilidade)|$)', ex):
        k = 'vuln' if mm.group(1).startswith('Vuln') else 'resist'
        d[k] = (d[k] + '; ' if d[k] else '') + (('Imune: ' if mm.group(1).startswith('Imun') else '') + (lambda x: x[:1].upper() + x[1:])(re.sub(r'^a\s+', '', mm.group(2).strip())))
    m = re.search(r'AGI (\d+) FOR (\d+) INT (\d+) PRE (\d+) VIG (\d+)', H)
    if not m: print('FALHOU', nome, H)
    for k, v in zip(('agi', 'for', 'int', 'pre', 'vig'), m.groups()): d['atr'][k] = int(v)
    m = re.search(r'PERÍCIAS (.*?)(?= DESLOCAMENTO| AGI |$)', H)
    if m:
        for p in re.split(r',\s*', m.group(1)):
            mm = re.match(r'^(.*?)\s+(\d*O.*)$', p.strip())
            if mm: d['pericias'].append(dict(n=mm.group(1).strip(), b=bonus(' ' + mm.group(2))))
    m = re.search(r'DESLOCAMENTO (\d+(?:[.,]\d+)?)\s*m(?: \| \d+)?(.*?)(?= AGI | PERÍCIAS |$)', H)
    d['desloc'] = float(m.group(1).replace(',', '.'))
    extra = re.sub(r'^[,\s]+', '', m.group(2)).strip()
    extra = re.sub(r'\s*\|\s*\d+', '', extra)
    corpo = bloco[fim_h + 1:]
    emacoes = False; hab = dict(n='Deslocamento especial', acao='Passiva', desc=extra[0].upper() + extra[1:]) if extra else None; i = 0; n = len(corpo)
    def fecha():
        nonlocal hab
        if hab and hab['desc'].strip():
            hab['desc'] = re.sub(r'(?<=[a-zà-ú])- (?=[a-zà-ú])', '', re.sub(r'\s+', ' ', hab['desc'].strip())); d['habilidades'].append(hab)
        hab = None
    while i < n:
        t = corpo[i].strip(); i += 1; u = t.upper()
        if u.startswith('AÇÕES'):
            fecha(); emacoes = True; continue
        m = re.match(r'^(PADRÃO|MOVIMENTO|COMPLETA|REAÇÃO|LIVRE|PASSIVA)\s+(.+)$', u)
        if emacoes and m:
            fecha()
            if m.group(2).strip() == 'AGREDIR':
                cab_atk = corpo[i].strip(); i += 1
                mm = re.match(r'^([A-ZÀ-Ú\- ]+?)\s+((?:Corpo a corpo|À distância).*)$', cab_atk)
                nm, alc = (titulo(mm.group(1)), mm.group(2).strip()) if mm else (titulo(cab_atk), '')
                alc = re.sub(r'\s{2,}', ', ', alc)
                alc = re.sub(r'[\s,]*,[\s,]*', ', ', alc)
                alc = re.sub(r'\s+(CURTO|MÉDIO|LONGO)$', lambda k: ', ' + k.group(1).capitalize(), alc)
                alc = re.sub(r',\s*(CURTO|MÉDIO|LONGO)', lambda k: ', ' + k.group(1).capitalize(), alc)
                j = ''
                while i < n and 'Dano' not in j: j += ' ' + corpo[i].strip(); i += 1
                while i < n and not re.search(r'(balístico|corte|impacto|perfuração|mental|fogo|químico|veneno|Sangue|Morte|Energia|Conhecimento)\s*$', j.strip(), re.I) and re.match(r'^[a-zà-ú]', corpo[i].strip()): j += ' ' + corpo[i].strip(); i += 1
                mt = re.search(r'Teste\s+(.*?)\s*\|\s*Dano\s+(.*)$', j)
                cr = re.search(r'cr[ií]tico\s*([\dx/]+)', j)
                if mt: d['ataques'].append(dict(n=nm, alc=re.sub(r',\s*,', ',', alc + (', crítico ' + cr.group(1) if cr else '')), teste=bonus(' ' + mt.group(1)), dano=mt.group(2).strip()))
                continue
            hab = dict(n=titulo(m.group(2).strip()), acao=ACOES[m.group(1)], desc=''); continue
        m = re.match(r'^([A-ZÀ-Ú]{4,}(?: [A-ZÀ-Ú]{2,})*)\s+(.+)$', t)
        if m and not re.match(r'^(CULTISTAS|ANIMAIS|FORÇAS|CRIMINOSOS)\b', t):
            fecha(); hab = dict(n=titulo(m.group(1)), acao='Passiva', desc=m.group(2)); continue
        if re.match(r'^(CULTISTAS|ANIMAIS|FORÇAS DA LEI|CRIMINOSOS|AMEAÇAS DA REALIDADE)', t): fecha(); i = n; continue
        if hab is not None: hab['desc'] += ' ' + t; continue
    fecha()
    for h in list(d['habilidades']):          # ataques escritos como habilidade (Cauda, Garras...)
        mm = re.match(r'^((?:Corpo a corpo|À distância)[^T]*?)?\s*Teste\s+(.*?)\s*\|\s*Dano\s+(.*)$', h['desc'])
        if mm:
            cr = re.search(r'cr[ií]tico\s*([\dx/]+)', mm.group(2))
            d['ataques'].append(dict(n=h['n'], alc=((mm.group(1) or 'Corpo a corpo').strip() + (', crítico ' + cr.group(1) if cr else '')), teste=bonus(' ' + mm.group(2)),
                                     dano=re.sub(r'(\d)(impacto|corte|perfuração|balístico|mental|fogo|químico)', r'\1 \2', mm.group(3).strip())))
            d['habilidades'].remove(h)
    return d
LISTA = []
for k, (i, h, vd) in enumerate(cab):
    fim = cab[k + 1][0] if k + 1 < len(cab) else len(L)
    bloco = L[i + 1:fim]
    chave = h.replace(' ', '')
    nome = dict(NOMES).get(chave)
    assert nome, h
    # nomes em duas linhas ('SOLDADO' / 'DEALUGUEL', 'POLICIAL' / 'DEELITE'): a 1ª linha cai no fim do bloco anterior
    while bloco and bloco[-1].strip() in ('SOLDADO', 'POLICIAL', 'COMANDANTE', 'ANIMAIS', 'AMEAÇAS DA REALIDADE', 'CULTISTAS', 'FORÇAS DA LEI', 'ENXAME'): bloco = bloco[:-1]
    LISTA.append((nome, vd, parse(bloco, nome, vd, 0)))
def q(s): return "'" + str(s).replace("'", "''") + "'"
rows = [f"({50 + k},{q(n)},'Outro',{q(vd)},{[284, 284, 284, 285, 285, 286, 286, 286, 287, 287, 287, 288, 288, 288, 288, 289, 289, 289][k]},{q(json.dumps(d, ensure_ascii=False))}::jsonb)" for k, (n, vd, d) in enumerate(LISTA)]
raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
open(os.path.join(raiz, 'schema_etapa9c_ameacas.sql'), 'w', encoding='utf-8').write("""-- Etapa 9c — Ameaças da Realidade do livro (criminosos, cultistas, policiais e animais; livro p.284 a 289)
-- Acrescenta 18 criaturas em livro_inimigos. Rode DEPOIS de schema_etapa9b_bestiario.sql. Re-executável.
-- Gerado por tools/livro/gerar_op_ameacas.py (não edite as linhas à mão).

insert into public.livro_inimigos(id, nome, elemento, vd, pagina, dados) values
""" + ',\n'.join(rows) + """
on conflict (id) do update set nome = excluded.nome, elemento = excluded.elemento, vd = excluded.vd, pagina = excluded.pagina, dados = excluded.dados;
""")
for n, vd, d in LISTA: print(n, vd, 'PV', d['pv'], 'DEF', d.get('def'), 'atq', [(a['n'], a['teste'], a['dano']) for a in d['ataques']], 'hab', [h['n'] for h in d['habilidades']])
