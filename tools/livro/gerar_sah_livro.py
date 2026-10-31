#!/usr/bin/env python3
"""Gera schema_etapa15_sah_livro.sql (+ _celular.sql, uma linha só): o resto do Sobrevivendo ao Horror —
origens, poderes gerais, poderes e trilhas de classe, classe Sobrevivente, poderes paranormais, rituais, bestiário e regras.
Dados em sah_habilidades.py, sah_ameacas.py e sah_regras.py (redação própria). Uso: python3 tools/livro/gerar_sah_livro.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from sah_habilidades import H
from sah_ameacas import A
from sah_regras import R

q = lambda s: "'" + str(s).replace("'", "''") + "'"
nul = lambda v: 'null' if v is None else (str(v) if isinstance(v, int) else q(v))
J = lambda d: q(json.dumps(d, ensure_ascii=False)) + '::jsonb'

refs = set(); hv = []
for i, h in enumerate(H):
    assert h['ref'] not in refs, h['ref']; refs.add(h['ref'])
    hv.append(f"({q(h['ref'])},'op','sah',{nul(h['classe'])},{q(h['grupo'])},{nul(h['trilha'])},{nul(h['nex'])},{5000 + i},{q(h['nome'])},{nul(h['circulo'])},{nul(h['elemento'])},{J(h['dados'])})")
av = [f"({101 + k},{q(n)},{q(el)},{q(vd)},{pag},'sah',{J(d)})" for k, (n, el, vd, pag, d) in enumerate(A)]
rv = []
for i, (g, sub, nome, texto, pag) in enumerate(R):
    rv.append(f"({q('op:sah:' + g + ':' + nome)},'op','sah',{q(g)},{q(sub)},{q(nome)},{6000 + i},{pag},{q(texto)},{J({'comp': 'sah'})})")

SQL = """-- Etapa 15 — Sobrevivendo ao Horror: habilidades, bestiário e regras (complemento 'sah')
-- Rode DEPOIS do schema_etapa13_sah_itens.sql. Re-executável. Gerado por tools/livro/gerar_sah_livro.py (não edite à mão).
-- Origens, poderes gerais (classe 'geral'), poderes e trilhas de classe, classe Sobrevivente, poderes paranormais e rituais
-- em livro_habilidades; criaturas e Ameaças da Realidade em livro_inimigos (ids 101+); regras novas e opcionais em livro_regras.

alter table public.livro_habilidades drop constraint if exists livro_habilidades_grupo_check;
alter table public.livro_habilidades add constraint livro_habilidades_grupo_check check (grupo in ('classe', 'poder', 'trilha', 'ritual', 'origem', 'paranormal'));
create index if not exists livro_habilidades_fonte_idx on public.livro_habilidades(fonte);
alter table public.livro_inimigos add column if not exists fonte text not null default 'livro-basico';
alter table public.livro_regras drop constraint if exists livro_regras_grupo_check;
alter table public.livro_regras add constraint livro_regras_grupo_check check (grupo in ('condicao', 'perigo', 'regra', 'jogo', 'opcional'));

insert into public.livro_habilidades(ref, sistema, fonte, classe, grupo, trilha, nex, ordem, nome, circulo, elemento, dados) values
""" + ',\n'.join(hv) + """
on conflict (ref) do update set sistema = excluded.sistema, fonte = excluded.fonte, classe = excluded.classe, grupo = excluded.grupo, trilha = excluded.trilha,
  nex = excluded.nex, ordem = excluded.ordem, nome = excluded.nome, circulo = excluded.circulo, elemento = excluded.elemento, dados = excluded.dados;

insert into public.livro_inimigos(id, nome, elemento, vd, pagina, fonte, dados) values
""" + ',\n'.join(av) + """
on conflict (id) do update set nome = excluded.nome, elemento = excluded.elemento, vd = excluded.vd, pagina = excluded.pagina, fonte = excluded.fonte, dados = excluded.dados;

insert into public.livro_regras(ref, sistema, fonte, grupo, subgrupo, nome, ordem, pagina, texto, dados) values
""" + ',\n'.join(rv) + """
on conflict (ref) do update set sistema = excluded.sistema, fonte = excluded.fonte, grupo = excluded.grupo, subgrupo = excluded.subgrupo,
  nome = excluded.nome, ordem = excluded.ordem, pagina = excluded.pagina, texto = excluded.texto, dados = excluded.dados;
"""
raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
open(os.path.join(raiz, 'schema_etapa15_sah_livro.sql'), 'w', encoding='utf-8').write(SQL)
linha = ' '.join(l.strip() for l in SQL.split('\n') if l.strip() and not l.strip().startswith('--'))
open(os.path.join(raiz, 'schema_etapa15_sah_livro_celular.sql'), 'w', encoding='utf-8').write(linha + '\n')
c = {}
for h in H: k = (h['classe'] or '-', h['grupo']); c[k] = c.get(k, 0) + 1
print(len(H), 'habilidades', c); print(len(A), 'inimigos;', len(R), 'regras')
