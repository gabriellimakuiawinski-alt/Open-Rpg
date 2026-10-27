#!/usr/bin/env python3
"""Gera schema_etapa12_itens_fx.sql: acrescenta o campo 'fx' (resumo em etiquetas: Dano, Alcance, Efeito…) aos itens do catálogo
(livro_itens), para a pessoa entender o item sem ler a descrição. Textos em redação própria. Re-executável."""
import json
def l(*p): return [list(x) for x in p]
FX = {
 'explosivo': {
  'Granada de atordoamento': l(('Efeito','Atordoa 1 rodada'),('Uso','Empunhar e arremessar (ação padrão)'),('Alcance','Médio'),('Área','Raio de 6m'),('Teste','Fortitude DT Agi: só ofuscado e surdo 1 rodada')),
  'Granada de fragmentação': l(('Dano','8d6 perfuração'),('Uso','Empunhar e arremessar (ação padrão)'),('Alcance','Médio'),('Área','Raio de 6m'),('Teste','Reflexos DT Agi: metade')),
  'Granada de fumaça': l(('Efeito','Cega e dá camuflagem total'),('Duração','2 rodadas'),('Uso','Empunhar e arremessar (ação padrão)'),('Alcance','Médio'),('Área','Raio de 6m')),
  'Granada incendiária': l(('Dano','6d6 fogo + em chamas'),('Uso','Empunhar e arremessar (ação padrão)'),('Alcance','Médio'),('Área','Raio de 6m'),('Teste','Reflexos DT Agi: metade e evita as chamas')),
  'Mina antipessoal': l(('Dano','12d6 perfuração'),('Área','Cone de 6m'),('Ativação','Controle remoto, ação padrão, alcance longo'),('Teste','Reflexos DT Int: metade'),('Instalar','Ação completa, Tática DT 15'))},
 'protecao': {
  'Proteção leve': l(('Defesa','+5')),
  'Proteção pesada': l(('Defesa','+10'),('Resistência','2 a balístico, corte, impacto e perfuração'),('Penalidade','–5 em perícias com penalidade de carga')),
  'Escudo': l(('Defesa','+2 (soma com a proteção)'),('Uso','Empunhado em uma mão'))},
 'municao': {
  'Balas curtas': l(('Serve em','Pistolas, revólveres, submetralhadoras'),('Dura','2 cenas')),
  'Balas longas': l(('Serve em','Fuzis e metralhadoras'),('Dura','1 cena')),
  'Cartuchos': l(('Serve em','Espingardas'),('Dura','1 cena')),
  'Combustível': l(('Serve em','Lança-chamas'),('Dura','1 cena')),
  'Flechas': l(('Serve em','Arcos e bestas'),('Dura','A missão inteira (reaproveitáveis)')),
  'Foguete': l(('Serve em','Bazucas'),('Dura','1 disparo'))},
 'acessorio': {
  'Kit de perícia': l(('Efeito','Sem o kit, –5 no teste da perícia'),('Obs.','Um kit por perícia')),
  'Utensílio': l(('Bônus','+2 em uma perícia (menos Luta e Pontaria)'),('Uso','Precisa ser empunhado')),
  'Vestimenta': l(('Bônus','+2 em uma perícia (menos Luta e Pontaria)'),('Limite','Vale o bônus de até 2 vestimentas'),('Vestir','Ação completa'))},
 'operacional': {
  'Algemas': l(('Efeito','Pulsos presos: –5 em testes com as mãos e sem conjurar'),('Escapar','Acrobacia DT 30 (ou a chave)')),
  'Arpéu': l(('Prender','Pontaria DT 15'),('Bônus','+5 em Atletismo para subir')),
  'Bandoleira': l(('Efeito','Saca ou guarda um item como ação livre'),('Limite','1 vez por rodada')),
  'Binóculos': l(('Bônus','+5 em Percepção para ver longe')),
  'Bloqueador de sinal': l(('Efeito','Celulares não se conectam'),('Alcance','Médio')),
  'Cicatrizante': l(('Cura','2d8+2 PV'),('Ativação','Ação padrão'),('Alvo','Você ou ser adjacente')),
  'Corda': l(('Bônus','+5 em Atletismo para descer'),('Tamanho','10 metros')),
  'Equipamento de sobrevivência': l(('Bônus','+5 em Sobrevivência para acampar e se orientar, mesmo sem treino')),
  'Lanterna tática': l(('Efeito','Ofusca 1 rodada (e imune pelo resto da cena)'),('Ativação','Ação de movimento'),('Alcance','Curto')),
  'Máscara de gás': l(('Bônus','+10 em Fortitude contra efeitos de respiração')),
  'Mochila militar': l(('Efeito','+2 espaços de carga'),('Espaço','Não ocupa espaço')),
  'Óculos de visão térmica': l(('Efeito','Anula a penalidade por camuflagem')),
  'Pé de cabra': l(('Bônus','+5 em Força para arrombar'),('Combate','Vale como bastão')),
  'Pistola de dardos': l(('Efeito','Inconsciente até o fim da cena'),('Teste','Fortitude DT Agi: só desprevenido e lento 1 rodada'),('Carga','2 dardos')),
  'Pistola sinalizadora': l(('Dano','2d6 fogo'),('Alcance','Curto'),('Carga','2 cargas'),('Efeito','Sinal luminoso para chamar outros')),
  'Soqueira': l(('Dano','+1 em ataques desarmados')),
  'Spray de pimenta': l(('Efeito','Cego por 1d4 rodadas'),('Teste','Fortitude DT Agi evita'),('Ativação','Ação padrão, ser adjacente'),('Usos','2')),
  'Taser': l(('Dano','1d6 eletricidade + atordoado 1 rodada'),('Teste','Fortitude DT Agi evita'),('Ativação','Ação padrão, ser adjacente'),('Usos','2')),
  'Traje hazmat': l(('Bônus','+5 em resistência contra efeitos ambientais'),('Resistência','Químico 10'))},
 'modificacao': {
  'Certeira': l(('Efeito','+2 nos testes de ataque')), 'Cruel': l(('Efeito','+2 no dano')), 'Perigosa': l(('Efeito','+2 na margem de ameaça')),
  'Discreta': l(('Efeito','–1 espaço e +5 em Crime para ocultar')), 'Tática': l(('Efeito','Saca a arma como ação livre')),
  'Alongada': l(('Efeito','+2 nos testes de ataque')), 'Calibre Grosso': l(('Efeito','+1 dado de dano'),('Obs.','Usa munição de calibre grosso')),
  'Compensador': l(('Efeito','Sem penalidade de ataque ao disparar rajada')), 'Ferrolho Automático': l(('Efeito','A arma passa a ser automática (rajada)')),
  'Mira Laser': l(('Efeito','+2 na margem de ameaça')), 'Mira Telescópica': l(('Efeito','Alcance sobe 1 categoria e Ataque Furtivo em qualquer alcance')),
  'Silenciador': l(('Efeito','Reduz em 2d20 a penalidade de Furtividade após atacar')), 'Visão de Calor': l(('Efeito','Ignora a camuflagem do alvo')),
  'Dum Dum': l(('Efeito','+1 no multiplicador de crítico')), 'Explosiva': l(('Efeito','+2d6 de dano')),
  'Antibombas': l(('Efeito','+5 em resistência contra efeitos de área')), 'Blindada': l(('Efeito','Resistência a dano 5 e +1 espaço')),
  'Reforçada': l(('Efeito','Defesa +2 e +1 espaço')), 'Discreta (proteção)': l(('Efeito','–1 espaço e +5 em Crime para ocultar')),
  'Aprimorado': l(('Efeito','O bônus do acessório sobe para +5')), 'Discreto': l(('Efeito','–1 espaço e +5 em Crime para ocultar')),
  'Função adicional': l(('Efeito','+2 em uma perícia extra à sua escolha')), 'Instrumental': l(('Efeito','Funciona como kit de uma perícia escolhida'))},
 'paranormal': {}}
for el in ('Conhecimento','Energia','Morte','Sangue'):
    FX['paranormal'][f'Amarras de {el}'] = l(('Armadilha','Ação completa, 2 PE, área 3x3m: Reflexos DT Int ou fica imóvel'),('Laçar','Ação padrão, 1 PE, alcance curto: Vontade DT Agi ou fica paralisado'),('Manter','1 PE por rodada'),('Contra','Criaturas vulneráveis a '+el))
    FX['paranormal'][f'Componentes ritualísticos de {el}'] = l(('Efeito','Necessário para conjurar rituais de '+el))
    FX['paranormal'][f'Scanner de manifestação paranormal de {el}'] = l(('Efeito','Sabe a direção das manifestações de '+el),('Ativação','Ação padrão, 1 PE por rodada'),('Alcance','Longo'))
FX['paranormal'].update({
  'Câmera de aura paranormal': l(('Efeito','Foto revela auras paranormais (cor do elemento)'),('Ativação','Ação padrão, 1 PE')),
  'Emissor de pulsos paranormais': l(('Efeito','Atrai criaturas do elemento e afasta as do oposto'),('Ativação','Ação completa, 1 PE'),('Teste','Vontade DT Pre evita')),
  'Escuta de ruídos paranormais': l(('Efeito','Grava até 24 horas; ouvir dá +5 em Ocultismo para identificar criatura'),('Ativação','Ação completa, 2 PE')),
  'Medidor de estabilidade da membrana': l(('Efeito','Avalia a Membrana na área (exige Ocultismo treinado)'),('Obs.','Não dá resposta definitiva'))})
def q(s): return s.replace("'", "''")
out = ['-- Etapa 12 — Resumo em etiquetas (fx) nos itens do catálogo: Dano, Alcance, Efeito… (Livro de Regras v1.2).',
       '-- Re-executável. Rode DEPOIS de schema_etapa10_amaldicoados.sql. Gerado por tools/livro/gerar_op_itens_fx.py.', '']
n = 0
for g, d in FX.items():
    for nome, fx in d.items():
        out.append(f"update public.livro_itens set dados = dados || jsonb_build_object('fx', '{q(json.dumps(fx, ensure_ascii=False))}'::jsonb) where sistema = 'op' and grupo = '{g}' and nome = '{q(nome)}';"); n += 1
open('schema_etapa12_itens_fx.sql', 'w', encoding='utf-8').write('\n'.join(out) + '\n'); print(n, 'itens')
