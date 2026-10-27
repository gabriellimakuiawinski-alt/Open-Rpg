#!/usr/bin/env python3
"""Gera schema_etapa11_regras.sql: condições, perigos (ambiente, armadilhas, doenças, venenos) e regras de cálculo
do Livro de Regras de Ordem Paranormal v1.2 (cap. 7 'Perigos', págs. 290-293, e Apêndice, págs. 310-313).
Textos resumidos pelo Claude (mecânica completa, redação própria). Uso: python3 tools/livro/gerar_op_regras.py"""
import json, os

R = []
def add(grupo, sub, nome, texto, pag, dados=None): R.append((grupo, sub, nome, texto, pag, dados or {}))
def cond(nome, tipo, texto): add('condicao', tipo, nome, texto, 310 if nome <= 'Envenenado' else 311, {'tipo': tipo})

# ---------------------------------------------------------------- condições (Apêndice, p.310-311)
cond('Abalado', 'medo', '–1 dado em testes. Abalado de novo vira apavorado.')
cond('Agarrado', 'paralisia', 'Desprevenido e imóvel, –1 dado em ataques e só ataca com armas leves. Ataque à distância contra agarrado tem 50% de chance de acertar o alvo errado.')
cond('Alquebrado', 'mental', 'Habilidades e rituais custam +1 PE.')
cond('Apavorado', 'medo', '–2 dados em testes de perícia e deve fugir da fonte do medo (pode parar ao perdê-la de vista ou passar de alcance médio). Se não puder fugir, não pode se aproximar dela.')
cond('Asfixiado', 'outra', 'Não respira. Prende o fôlego por rodadas igual a Vigor; depois Fortitude por rodada (DT 5, +5 por teste anterior). Falhou: inconsciente e perde 1d6 PV por rodada até respirar ou morrer.')
cond('Atordoado', 'mental', 'Desprevenido e não pode fazer ações.')
cond('Caído', 'outra', '–2 dados em ataques corpo a corpo e deslocamento 1,5m. –5 de Defesa contra corpo a corpo, +5 contra ataques à distância.')
cond('Cego', 'sentidos', 'Desprevenido e lento, sem Percepção para observar, –2 dados em perícias de Agilidade ou Força. Alvos dos seus ataques têm camuflagem total. Escuridão total conta como cego, salvo percepção no escuro.')
cond('Confuso', 'mental', 'No início do turno role 1d6: 1 move-se em direção sorteada (1d8); 2-3 não age e balbucia; 4-5 ataca o ser mais próximo (ou a si mesmo, só o dano); 6 a condição termina.')
cond('Debilitado', 'outra', '–2 dados em testes de Agilidade, Força e Vigor. Debilitado de novo vira inconsciente.')
cond('Desprevenido', 'outra', '–5 na Defesa e –1 dado em Reflexos. Fica assim contra inimigos que não percebe.')
cond('Doente', 'outra', 'Sob efeito de uma doença.')
cond('Em Chamas', 'outra', 'No início dos turnos sofre 1d6 de fogo. Ação padrão apaga com as mãos; imersão em água também apaga.')
cond('Enjoado', 'outra', 'Só pode fazer uma ação padrão ou de movimento por rodada (não as duas).')
cond('Enredado', 'paralisia', 'Lento, vulnerável e –1 dado em ataques.')
cond('Envenenado', 'outra', 'O efeito depende do veneno: outra condição (fraco, enjoado...) ou dano recorrente. Sem outra indicação, dura a cena. Dano recorrente de envenenado sempre acumula.')
cond('Esmorecido', 'mental', '–2 dados em Intelecto e Presença.')
cond('Exausto', 'fadiga', 'Debilitado, lento e vulnerável. Exausto de novo vira inconsciente.')
cond('Fascinado', 'mental', '–2 dados em Percepção e só pode observar o que o fascinou. Qualquer ação hostil contra ele anula; balançá-lo gasta ação padrão.')
cond('Fatigado', 'fadiga', 'Fraco e vulnerável. Fatigado de novo vira exausto.')
cond('Fraco', 'outra', '–1 dado em testes de Agilidade, Força e Vigor. Fraco de novo vira debilitado.')
cond('Frustrado', 'mental', '–1 dado em Intelecto e Presença. Frustrado de novo vira esmorecido.')
cond('Imóvel', 'paralisia', 'Todos os deslocamentos viram 0m.')
cond('Inconsciente', 'outra', 'Indefeso, sem ações nem reações. Acordar balançando gasta ação padrão.')
cond('Indefeso', 'outra', 'Desprevenido, –10 na Defesa, falha automática em Reflexos e pode sofrer golpe de misericórdia.')
cond('Lento', 'paralisia', 'Deslocamentos pela metade (arredonda para baixo em 1,5m); não corre nem investe.')
cond('Machucado', 'outra', 'Menos da metade dos PV totais.')
cond('Morrendo', 'outra', 'Com 0 PV. Três turnos morrendo na mesma cena (não precisam ser seguidos) e você morre. Só termina com Medicina (DT 20) ou efeito específico.')
cond('Ofuscado', 'sentidos', '–1 dado em ataques e Percepção.')
cond('Paralisado', 'paralisia', 'Imóvel e indefeso; só faz ações puramente mentais.')
cond('Pasmo', 'mental', 'Não pode fazer ações.')
cond('Petrificado', 'outra', 'Inconsciente e com resistência a dano 10.')
cond('Sangrando', 'outra', 'No início dos turnos faz Vigor (DT 20). Passou: estabiliza e a condição acaba. Falhou: perde 1d6 PV e continua sangrando.')
cond('Surdo', 'sentidos', 'Sem Percepção para ouvir, –2 dados em Iniciativa e condição ruim para conjurar rituais.')
cond('Surpreendido', 'outra', 'Não ciente dos inimigos: desprevenido e sem ações.')
cond('Vulnerável', 'outra', '–2 de Defesa.')

# ---------------------------------------------------------------- perigos: ambiente (p.290-293)
def per(sub, nome, texto, pag): add('perigo', sub, nome, texto, pag)
per('Ambiente', 'Ácido', '1d6 de dano químico por rodada de exposição. Imersão total: 10d6 por rodada, e o dano persiste por mais uma rodada.', 290)
per('Ambiente', 'Calor e frio', 'Acima de 50 °C ou abaixo de –10 °C: Fortitude por dia (DT 5, +5 por teste anterior); falhou, 1d6 de fogo ou frio que só cura ao sair do clima. Acima de 60 °C ou abaixo de –20 °C: teste por minuto.', 290)
per('Ambiente', 'Neblina', 'Camuflagem. Neblina espessa: camuflagem a criaturas a 1,5m e camuflagem total a mais de 1,5m.', 290)
per('Ambiente', 'Chuva', '–5 em Percepção e os mesmos efeitos de vento forte.', 290)
per('Ambiente', 'Granizo', 'Como chuva, mais 1 de dano de impacto em todos no início de cada rodada.', 290)
per('Ambiente', 'Neve', 'Como chuva, e cria terreno difícil.', 290)
per('Ambiente', 'Tempestade', '–2 dados em Percepção e os efeitos de vendaval. No início da rodada role 1d10: com 1, um ser aleatório é atingido por raio (8d12 de eletricidade).', 291)
per('Ambiente', 'Vento forte', '–1 dado em ataques à distância e 50% de chance por rodada de apagar chamas ou dissipar névoas.', 291)
per('Ambiente', 'Vendaval', '–2 dados em ataques à distância. Apaga chamas e dissipa névoas.', 291)
per('Ambiente', 'Furacão', 'Ataques à distância impossíveis. No início da rodada, seres Médios ou menores fazem Fortitude (DT 15) ou caem, são arrastados 1d4 x 1,5m e sofrem 1d6 de impacto por 1,5m.', 291)
per('Ambiente', 'Tornado', 'Ataques à distância impossíveis. No início da rodada, seres Grandes ou menores fazem Fortitude (DT 25) ou caem, são arrastados 1d12 x 1,5m em direção aleatória e sofrem 1d6 de impacto por 1,5m.', 291)
per('Ambiente', 'Eletricidade', 'Dano por rodada conforme a fonte: mínima 1d6 (bateria), baixa 2d8 (caixa de fusíveis), média 4d10 (cerca elétrica), alta 8d12 (raio).', 292)
per('Ambiente', 'Fome e sede', 'Aguenta um dia. Depois, Fortitude por dia (DT 15, +1 por teste anterior): 1ª falha fraco, 2ª debilitado, 3ª inconsciente, 4ª letal. Só se cura com comida e bebida.', 292)
per('Ambiente', 'Fumaça', 'Fortitude no início de cada turno (DT 10, +1 por teste anterior); falhou, perde o turno tossindo. Duas falhas seguidas: perde 1d6 PV. Quem não respira é imune. Dá camuflagem.', 292)
per('Ambiente', 'Lava', '2d6 de fogo por rodada de exposição. Imersão total: 20d6 por rodada, e o dano persiste por mais uma rodada.', 292)
per('Ambiente', 'Queda', '1d6 de impacto a cada 1,5m, máximo 40d6 (60m). Na água, reduza 6m (–4d6). Objeto pesado que cai em alguém causa o mesmo; objeto muito pesado, o dobro.', 292)
per('Ambiente', 'Fogo', 'Exposto a chamas: Reflexos (DT 15) ou fica em chamas (1d6 de fogo por turno). Fogo de efeito instantâneo (ritual, explosivo) não dura o bastante para incendiar alguém, salvo se a descrição disser.', 292)
per('Ambiente', 'Sono', 'Uma noite sem dormir não tem custo, mas sem recuperar PV e PE. Depois, Fortitude por dia (DT 15, +1 por teste): falhou, fatigado; já fatigado, exausto; já exausto, inconsciente até dormir 8 horas.', 293)
per('Ambiente', 'Sufocamento', 'Prende a respiração por rodadas igual a Vigor. Depois, Fortitude por rodada (DT 5, +5 por teste): falhou, inconsciente e perde 1d6 PV por rodada até respirar ou morrer.', 293)

# ---------------------------------------------------------------- armadilhas (p.290)
per('Armadilhas', 'Alarme', 'Sinal sonoro ou numa central, avisando intrusos. Investigação/Crime DT 20.', 290)
per('Armadilhas', 'Arame farpado', 'Terreno difícil; 1d6+2 de corte em quem atravessa. Investigação/Crime DT 20.', 290)
per('Armadilhas', 'Armadilha de caça', 'Prende a perna: 4d6 de corte, lento até curar e imóvel enquanto preso (Reflexos DT 20 reduz à metade e evita as condições). Soltar exige Força DT 15; cada falha causa 1d6 de corte.', 290)
per('Armadilhas', 'Descarga elétrica', '6d6 de eletricidade em todos a até 3m; Reflexos DT 20 reduz à metade (quem ativou não tem teste). Investigação/Crime DT 25.', 290)
per('Armadilhas', 'Fosso camuflado', 'Queda de 3m (2d6); Reflexos DT 20 evita; Atletismo DT 20 para subir. Investigação ou Sobrevivência/Crime DT 20.', 290)

# ---------------------------------------------------------------- doenças (p.291-292)
per('Doenças', 'Como funcionam as doenças', 'Ao contato, teste de resistência (em geral Fortitude): passou, resistiu; falhou, infectado no estágio I. No fim de cada cena repita o teste: falhou, avança um estágio. Dois sucessos seguidos curam. Penalidades e condições acabam com a cura.', 291)
per('Doenças', 'Febre Hemorrágica', 'Mordida de ratos, Fortitude DT 15. I: fraco. II: debilitado. III+: ao sofrer dano de corte, balístico ou perfuração fica sangrando.', 291)
per('Doenças', 'Mente Embaralhada', 'Implantação mental, Vontade DT 20. I: Intelecto –1. II: no início do turno, Intelecto DT 15 ou perde a ação de movimento. III+: mente parcialmente controlada por quem implantou; vê todos como ameaça.', 291)
per('Doenças', 'Putrefação Acelerada', 'Inalação, Fortitude DT 20. I: Vigor –1. II: Vigor –2 no total e deslocamento pela metade. III: Vigor 0, deslocamento 1,5m e uma lesão permanente.', 291)
per('Doenças', 'Sangue Quente', 'Contato, Fortitude DT 15. I: +1 em Força e Agilidade. II: confuso. III: confuso e vulnerável a todo tipo de dano.', 291)
per('Doenças', 'Vírus do Infecticídio', 'Contato, Fortitude DT 30; só cura com testes feitos abaixo de 0 °C. I: PV máximos –2d10 (se zerar, morre). II: mais –2d10. III+: mais –2d10 e passa a transmitir o vírus por contato.', 292)

# ---------------------------------------------------------------- venenos (p.293)
per('Venenos', 'Como funcionam os venenos', 'Exposto, faz Fortitude (DT do veneno); falhou, sofre o efeito (alguns têm efeito reduzido, entre parênteses, mesmo se passar). Tipos: contato (ataque que acerta ou toque), ferimento (ataque que causa 1+ de dano), inalação (frasco em alcance curto libera cubo de 3m; prender o fôlego não evita) e ingestão. Aplicar em arma é ação padrão e dura até acertar ou fim da cena.', 293)
for n, t, dt, e in [('Arsênico', 'ingestão', 15, '1d12 de dano por rodada durante 1d4 rodadas'), ('Beladona', 'ferimento', 20, 'vítima fica fraca'),
    ('Clorofórmio', 'inalação', 25, 'inconsciente (enjoada por 1 rodada se passar)'), ('Curare', 'ferimento', 20, 'imóvel (lenta se passar) por 1d6 rodadas'),
    ('Estricnina', 'ferimento', 25, '2d12 de dano por rodada por 2d4 rodadas (metade do dano se passar)'), ('Inseticida', 'inalação', 15, 'vítima fica enjoada'),
    ('Lixo químico', 'contato', 20, 'debilitada (fraca se passar)'), ('Peçonha fraca', 'ferimento', 15, '1d12 de dano (metade se passar)'),
    ('Peçonha mortal', 'ferimento', 25, 'cai com 0 PV (10d6 de dano se passar)'), ('Peçonha potente', 'ferimento', 20, '1d12 por rodada por 1d4 rodadas (metade se passar)'),
    ('Sonífero', 'ingestão', 20, 'inconsciente (enjoada por 1 rodada se passar)')]:
    per('Venenos', n, f'Veneno de {t}, Fortitude DT {dt}: {e}.', 293)

# ---------------------------------------------------------------- cálculos e acúmulo (Apêndice p.312-313)
def reg(nome, texto, pag): add('regra', 'Cálculos e bônus', nome, texto, pag)
reg('Arredondamento', 'Divisões arredondam para baixo, salvo indicação contrária (7 de dano pela metade = 3).', 312)
reg('Ordem das contas', 'Faça multiplicações e divisões antes de somas e subtrações. O teste de resistência é sempre o primeiro a ser aplicado; por último vem a resistência a dano.', 312)
reg('Multiplicações', 'Vários multiplicadores se combinam em um só: o primeiro vale inteiro e cada outro soma o seu valor –1 (x2 e x2 dão x3, não x4).', 312)
reg('Acumulando bônus', 'Bônus de fontes diferentes acumulam; da mesma fonte, não. O mesmo vale para penalidades, e bônus e penalidades se somam entre si. As fontes são habilidades, itens, rituais e aliados.', 312)
reg('Exceções de acúmulo', 'Habilidades de classe e origem acumulam entre si (exceto da mesma habilidade). Bônus de Defesa de proteção, escudo e itens paranormais acumulam, mas não se usam duas proteções ou dois escudos; demais bônus de itens não acumulam. Rituais não acumulam entre si, nem aliados. O mesmo atributo não conta duas vezes na mesma característica.', 312)
reg('Condições juntas', 'Várias condições aplicam todos os seus efeitos; efeitos iguais não acumulam, vale o mais severo (desprevenido e vulnerável dão –5 na Defesa, não –7). As condições acabam no fim da cena, salvo indicação.', 313)
reg('Chance de falha', 'Chances de falha de fontes diferentes (como camuflagem) acumulam até 75%; sempre sobra 1 chance em 4 de acertar.', 313)
reg('Fortificação', 'Chance de evitar crítico e ataque furtivo (como a maldição Letárgica) sempre acumula, sem limite; 100% ou mais é imunidade.', 313)
reg('Cura acelerada, PV temporários e resistência a dano', 'Acumulam, exceto quando as fontes não acumulam. Proteção pesada (RD 2) com Ódio Incontrolável (RD 5 a balístico, corte, impacto e perfuração) reduz esses danos em 7 e o resto em 2.', 313)

raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
q = lambda s: "'" + s.replace("'", "''") + "'"
vals = []
for i, (g, sub, nome, texto, pag, d) in enumerate(R):
    vals.append(f"({q('op:regra:' + g + ':' + nome)},'op','livro-basico',{q(g)},{q(sub)},{q(nome)},{i + 1},{pag},{q(texto)},{q(json.dumps(d, ensure_ascii=False))}::jsonb)")
SQL = """-- Etapa 11 — Condições, perigos e regras de cálculo do livro (Ordem Paranormal, Livro de Regras v1.2)
-- Tabela global livro_regras (só leitura, atrás de login). Re-executável.
-- Gerado por tools/livro/gerar_op_regras.py (não edite as linhas à mão).

create table if not exists public.livro_regras (
  ref      text primary key,
  sistema  text not null default 'op',
  fonte    text not null default 'livro-basico',
  grupo    text not null check (grupo in ('condicao', 'perigo', 'regra')),
  subgrupo text,
  nome     text not null,
  ordem    int  not null default 0,
  pagina   int,
  texto    text not null default '',
  dados    jsonb not null default '{}'::jsonb
);
create index if not exists livro_regras_idx on public.livro_regras(sistema, grupo, ordem);
alter table public.livro_regras enable row level security;
drop policy if exists livro_regras_ler on public.livro_regras;
create policy livro_regras_ler on public.livro_regras for select to authenticated using (true);
revoke all on public.livro_regras from anon, authenticated;
grant select on public.livro_regras to authenticated;

insert into public.livro_regras(ref, sistema, fonte, grupo, subgrupo, nome, ordem, pagina, texto, dados) values
""" + ',\n'.join(vals) + """
on conflict (ref) do update set sistema = excluded.sistema, fonte = excluded.fonte, grupo = excluded.grupo, subgrupo = excluded.subgrupo,
  nome = excluded.nome, ordem = excluded.ordem, pagina = excluded.pagina, texto = excluded.texto, dados = excluded.dados;
"""
with open(os.path.join(raiz, 'schema_etapa11_regras.sql'), 'w', encoding='utf-8') as fh:
    fh.write(SQL)
print(len(R), 'linhas')
