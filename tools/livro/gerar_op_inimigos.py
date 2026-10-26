#!/usr/bin/env python3
"""Gera schema_etapa9b_bestiario.sql: as criaturas do capítulo Ameaças do Livro de Regras de Ordem Paranormal
(v1.2, páginas 176 a 291 do PDF) na tabela global livro_inimigos (só leitura, atrás de login). Re-executável.
Uso (na raiz do repositório):  python3 tools/livro/gerar_op_inimigos.py <livro.pdf>
O PDF é do usuário e não fica no repositório. A leitura está em tools/livro/extrair_op_inimigos.py."""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import pdfplumber
import extrair_op_inimigos as X

pdf = pdfplumber.open(sys.argv[1] if len(sys.argv) > 1 else '/mnt/user-data/uploads/iniciativa-t20-ordem-paranormal-rpg-v1-2-vs-1-4.pdf')
LISTA = []
for b in X.extrai(pdf, 176, 291):
    d = X.le(b)
    nm = X.titulo(b['nome'])
    el = X.SOBRE.get(nm) or (b['elementos'] or ['Outro'])[0]
    # modelo do editor (inimigos.html)
    dados = dict(tamanho=d['tamanho'] or 'Médio', pv=d['pv'], def_=d['def'], desloc=d['desloc'], atr=d['atr'], fort=d['fort'], refl=d['refl'],
                 vont=d['vont'], ini=d['ini'], perc=d['perc'], pericias=d['pericias'], resist=d['resist'].strip(), vuln=d['vuln'].strip(),
                 sentidos=d['sentidos'], ataques=d['ataques'], habilidades=d['habilidades'], desc='')
    dados['def'] = dados.pop('def_')
    LISTA.append((nm, el, b['vd'], dados, b['pag']))

LISTA.sort(key=lambda x: (x[1], x[0]))
def q(s): return "'" + str(s).replace("'", "''") + "'"
out = ["""-- Etapa 9b — Bestiário do livro (Ordem Paranormal, Livro de Regras v1.2, capítulo Ameaças)
-- Tabela global livro_inimigos (só leitura, atrás de login). Re-executável. Rode DEPOIS de schema_etapa9_inimigos.sql.
-- Gerado por tools/livro/gerar_op_inimigos.py (não edite as linhas à mão).

create table if not exists public.livro_inimigos (
  id       int primary key,
  nome     text not null,
  elemento text not null default 'Outro',
  vd       text not null default '',
  pagina   int,
  dados    jsonb not null default '{}'::jsonb
);
create index if not exists livro_inimigos_idx on public.livro_inimigos(elemento, nome);
alter table public.livro_inimigos enable row level security;
drop policy if exists livro_inimigos_ler on public.livro_inimigos;
create policy livro_inimigos_ler on public.livro_inimigos for select to authenticated using (true);
revoke all on public.livro_inimigos from anon, authenticated;
grant select on public.livro_inimigos to authenticated;

insert into public.livro_inimigos(id, nome, elemento, vd, pagina, dados) values"""]
rows = []
for i, (nm, el, vd, dados, pag) in enumerate(LISTA, 1):
    rows.append(f"({i},{q(nm)},{q(el)},{q(vd)},{pag - 8},{q(json.dumps(dados, ensure_ascii=False))}::jsonb)")
out.append(',\n'.join(rows))
out.append("on conflict (id) do update set nome = excluded.nome, elemento = excluded.elemento, vd = excluded.vd, pagina = excluded.pagina, dados = excluded.dados;\n")
open('schema_etapa9b_bestiario.sql', 'w').write('\n'.join(out))
print(len(LISTA), 'criaturas ->', 'schema_etapa9b_bestiario.sql')
