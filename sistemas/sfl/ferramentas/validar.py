#!/usr/bin/env python3
"""Confere os dados do Search For Light antes de publicar.
Uso (na raiz do repositório): python3 sistemas/sfl/ferramentas/validar.py
Sai com erro (código 1) se achar problema."""
import json, pathlib, sys, collections

D = pathlib.Path(__file__).resolve().parents[1] / 'dados'
erros, avisos = [], []
load = lambda n: json.loads((D / n).read_text(encoding='utf-8'))

ALVOS = {'vidaMax', 'folegoMax', 'espacos', 'espacosGrupo', 'prontos', 'metros', 'armasEspeciais', 'infeccao',
         'margemCritico', 'espacosArma'}
RARIDADES = {'Comum', 'Incomum', 'Raro', 'Fabricável', None}

regras, per, ori, cla, inf = load('regras.json'), load('pericias.json'), load('origens.json'), load('classes.json'), load('infectados.json')
armas, itens, mods, hp = load('armas.json'), load('itens.json'), load('modificacoes.json'), load('habilidade-propria.json')

versoes = {n: load(n).get('versao') for n in [p.name for p in D.glob('*.json')]}
if len(set(versoes.values())) != 1:
    erros.append(f'versões diferentes entre os arquivos: {versoes}')

PER = {p['id'] for p in per['pericias']}
if len(PER) != 15:
    erros.append(f'esperava 15 perícias, há {len(PER)}')


def unicos(lista, onde):
    c = collections.Counter(x['id'] for x in lista)
    for k, v in c.items():
        if v > 1:
            erros.append(f'id repetido em {onde}: {k}')


def efeitos(obj, onde):
    for e in obj.get('efeitos', []):
        if e.get('soma') not in ALVOS:
            erros.append(f'{onde}: efeito com alvo desconhecido {e}')
        if not isinstance(e.get('valor'), (int, float)):
            erros.append(f'{onde}: efeito sem valor numérico {e}')


unicos(ori['origens'], 'origens')
for o in ori['origens']:
    if len(o['pericias']) != 2:
        erros.append(f"origem {o['id']}: precisa de 2 perícias")
    for p in o['pericias']:
        if p not in PER:
            erros.append(f"origem {o['id']}: perícia inexistente {p}")
    efeitos(o, f"origem {o['id']}")

unicos(cla['classes'], 'classes')
for c in cla['classes']:
    for p in c['pericias']:
        if p not in PER:
            erros.append(f"classe {c['id']}: perícia inexistente {p}")
    if len(c['habilidades']) != 9:
        avisos.append(f"classe {c['id']}: {len(c['habilidades'])} habilidades (o padrão é 9)")
    if len(c['trilhas']) != 3 or any(len(t['habilidades']) != 4 for t in c['trilhas']):
        erros.append(f"classe {c['id']}: precisa de 3 trilhas com 4 habilidades")
    unicos(c['habilidades'], f"habilidades de {c['id']}")
    efeitos(c, f"classe {c['id']}")
    for h in c['habilidades'] + [h for t in c['trilhas'] for h in t['habilidades']]:
        efeitos(h, f"{c['id']}/{h['id']}")

unicos(inf['classes'], 'classes de infectado')
for c in inf['classes']:
    if sorted(c['niveis']) != ['1', '2', '3'] or any(len(v) != 3 for v in c['niveis'].values()):
        erros.append(f"infectado {c['id']}: precisa de 3 opções nos níveis 1, 2 e 3")
    for v in c['niveis'].values():
        for h in v:
            if 'custo' not in h:
                erros.append(f"infectado {c['id']}/{h['id']}: poder sem custo em Infecção")
    if len(c['trilhas']) != 3 or any(len(t['habilidades']) != 4 for t in c['trilhas']):
        erros.append(f"infectado {c['id']}: precisa de 3 trilhas com 4 habilidades")

unicos(armas['armas'], 'armas')
for a in armas['armas']:
    if a['raridade'] not in RARIDADES:
        erros.append(f"arma {a['id']}: raridade inválida {a['raridade']}")
    if a['espacos'] is not None and not 0 <= a['espacos'] <= 3:
        erros.append(f"arma {a['id']}: espaços fora de 0 a 3")
    if a['categoria'] == 'arremesso' and a['limiteMods']:
        erros.append(f"arma {a['id']}: arremesso não leva modificação")
    if a['categoria'] != 'especial' and a['pericia'] not in PER:
        erros.append(f"arma {a['id']}: perícia inexistente {a['pericia']}")

unicos(itens['itens'], 'itens')
for i in itens['itens']:
    if i['raridade'] not in RARIDADES:
        erros.append(f"item {i['id']}: raridade inválida {i['raridade']}")
    efeitos(i, f"item {i['id']}")

ARMAS = {a['id'] for a in armas['armas']}
unicos(mods['modificacoes'], 'modificações')
for m in mods['modificacoes']:
    for x in m['para'].get('ids', []) + m['para'].get('exceto', []):
        if x not in ARMAS:
            erros.append(f"modificação {m['id']}: arma inexistente {x}")
    efeitos(m, f"modificação {m['id']}")

# contagens úteis para o balanceamento
cont = collections.Counter(p for o in ori['origens'] for p in o['pericias'])
for p in PER:
    if cont[p] < 2:
        avisos.append(f'perícia {p} aparece em só {cont[p]} origem(ns)')

print(f"SFL v{regras['versao']}: {len(ori['origens'])} origens, {len(cla['classes'])} classes, {len(inf['classes'])} classes de infectado, "
      f"{len(armas['armas'])} armas, {len(itens['itens'])} itens, {len(mods['modificacoes'])} modificações")
print('Origens por perícia:', ', '.join(f'{k} {v}' for k, v in sorted(cont.items())))
for a in avisos:
    print('AVISO:', a)
for e in erros:
    print('ERRO:', e)
sys.exit(1 if erros else 0)
