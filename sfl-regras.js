/* sfl-regras.js — regras do Search For Light (SFL 2), sistema próprio do mestre.
   Estende window.SIS (sistemas.js) e usa os dados de sfl-dados.js (window.SFLD).
   Teste: rola N d20 (N = atributo), fica o maior; o atributo NÃO soma. Resultado = maior dado + treino da perícia.
   Valores marcados [PROPOSTA] nos documentos (docs/sfl/) são ponto de partida e podem mudar. */
(function () {
  'use strict';
  const S = window.SIS, D = window.SFLD || { classes: [], origens: [], poderes: [], armas: [] }, n0 = S.n0;
  S.SISTEMAS.sfl = { n: 'Search For Light', d: 'Ficha automática: atributo dá os dados, perícia soma o treino, Vida, Fôlego, Medo e Infecção.' };

  const ATR = [['cor', 'Corpo', 'COR'], ['ref', 'Reflexo', 'REF'], ['men', 'Mente', 'MEN'], ['pre', 'Presença', 'PRE']];
  const PERICIAS = [['Atletismo', 'cor'], ['Furtividade', 'ref'], ['Parkour', 'ref'], ['Percepção', 'men'], ['Investigação', 'men'], ['Técnica', 'men'], ['Medicina', 'men'], ['Sobrevivência', 'men'],
    ['Persuasão', 'pre'], ['Intimidação', 'pre'], ['Vontade', 'pre'], ['Contundente', 'cor'], ['Cortante', 'cor'], ['Arremesso', 'ref'], ['Tiro', 'ref']];
  const TREINO = [[0, 'Leigo'], [3, 'Treinado +3'], [6, 'Veterano +6'], [9, 'Expert +9']];
  const FAIXAS = [[0, 'Controlado', 'sem efeitos'], [3, 'Inquieto', 'sintomas leves; poderes +2 no teste'], [6, 'Instável', 'ao usar poder, teste de Vontade DT 18'], [9, 'Limiar', 'o Ódio assume']];
  const faixaInf = v => FAIXAS.filter(f => v >= f[0]).pop();
  const BENEFICIOS = [['atr', '+1 atributo (máximo 5)'], ['per', 'Subir uma perícia de nível'], ['arma', 'Treinar uma arma especial (ou subir o treino)'], ['vida', '+1 de Vida máxima por ponto de Corpo']];
  const classe = id => D.classes.find(c => c.id == id) || null;
  const origem = id => D.origens.find(o => o.id == id) || null;
  const linha = id => D.poderes.find(p => p.id == id) || null;
  const familia = n => /^Arco/.test(n) ? 'Arco' : /^Besta/.test(n) ? 'Besta' : n;
  const ESPECIAIS = [...new Set(D.armas.filter(a => a.cat == 'especial').map(a => familia(a.n)))];

  /* ---------- crítico: "19–20 ×2" -> {m:19, x:2}; "n/a" -> null ---------- */
  function critDe(txt) {
    const m = /(\d+)(?:\s*[–-]\s*\d+)?\s*×\s*(\d+)/.exec(String(txt || ''));
    return m ? { m: +m[1], x: +m[2] } : null;
  }

  /* garante a estrutura de uma ficha SFL sem apagar nada que já exista */
  function preparar(f) {
    if (!f.sfl || typeof f.sfl != 'object') f.sfl = {};
    const s = f.sfl;
    if (s.classe === undefined) s.classe = ''; if (s.origem === undefined) s.origem = ''; if (s.trilha === undefined) s.trilha = '';
    s.marco = Math.max(0, Math.min(8, Math.round(n0(s.marco))));
    if (!Array.isArray(s.perClasse)) s.perClasse = [];
    if (!Array.isArray(s.esc)) s.esc = [];
    if (!Array.isArray(s.armas)) s.armas = [];            // treinos de arma especial [{f:'Arco', t:3}]
    if (!s.bonus || typeof s.bonus != 'object') s.bonus = {};
    if (s.linha === undefined) s.linha = '';
    /* ficha vinda de outro sistema: guarda o que havia e começa com o modelo do SFL */
    if (!Array.isArray(f.attrs)) f.attrs = [];
    if (!ATR.every(([id]) => f.attrs.some(a => a.id == id))) {
      if (f.attrs.length && !f.altSis) f.altSis = { attrs: f.attrs, skills: f.skills, stats: f.stats };
      f.attrs = ATR.map(([id, n]) => ({ id, n, v: 1 }));
    } else f.attrs = ATR.map(([id, n]) => f.attrs.find(a => a.id == id) || { id, n, v: 1 });
    if (!Array.isArray(f.skills) || !PERICIAS.every(([n]) => f.skills.some(k => k.n == n))) f.skills = PERICIAS.map(([n, a]) => ({ id: S.uid(), n, a, t: 0, o: 0 }));
    const antes = Array.isArray(f.stats) ? f.stats : [];
    const mk = (id, n, c, ex) => antes.find(x => x.id == id) || Object.assign({ id, n, cur: 0, max: 0, c }, ex || {});
    f.stats = [mk('pv', 'Vida', '#ee4444'), mk('pe', 'Fôlego', '#e8b53a'), mk('medo', 'Medo', '#8a8f98'), mk('inf', 'Infecção', '#8bd04a')];
    f.stats[0].n = 'Vida'; f.stats[1].n = 'Fôlego';
    if (!f.inv || !Array.isArray(f.inv.items)) f.inv = { items: [] };
    if (!Array.isArray(f.poderes)) f.poderes = [];
    return f;
  }

  const atr = (f, id) => { const a = (f.attrs || []).find(a => a.id == id); return a ? n0(a.v) : 0 };

  /* tudo que a ficha calcula sozinha */
  function derivar(f) {
    const s = f.sfl, C = classe(s.classe), O = origem(s.origem), b = s.bonus || {};
    const cor = atr(f, 'cor'), ref = atr(f, 'ref');
    const pvMax = Math.max(1, 10 + cor * 2 + (C && C.id == 'combatente' ? 4 : 0) + n0(b.pv) + s.esc.filter(e => e.k == 'vida').reduce((t, e) => t + n0(e.n), 0));
    const folMax = Math.max(0, 5 + ref + (C && C.id == 'batedor' ? 2 : 0) + n0(b.fol));
    const slots = Math.max(0, 5 + cor + (C && C.id == 'tecnico' ? 2 : 0) + n0(b.slots));
    const itens = ((f.inv && f.inv.items) || []).filter(it => it && n0(it.qtd === undefined ? 1 : it.qtd) > 0);
    const usado = itens.reduce((t, it) => t + n0(it.esp) * (it.qtd === undefined ? 1 : n0(it.qtd)), 0);
    const arm = itens.filter(it => it.tipo == 'armadura' && it.eq).sort((x, y) => n0(y.red) - n0(x.red))[0];
    const nTrilha = Math.ceil(s.marco / 2), nEsc = Math.floor(s.marco / 2);
    const extrasAtr = s.esc.filter(e => e.k == 'atr').length;
    const pontos = f.attrs.reduce((t, a) => t + n0(a.v), 0);
    const nivelPoder = !s.linha ? 0 : s.marco >= 8 ? 3 : s.marco >= 4 ? 2 : 1;
    const fonte = new Set([...(O ? O.pericias : []), ...s.perClasse]);
    const inf = n0((f.stats.find(x => x.id == 'inf') || {}).cur);
    const armasMax = 1 + (s.origem == 'militar' ? 1 : 0);
    return { C, O, pvMax, folMax, slots, usado, sobre: usado > slots, armadura: arm ? n0(arm.red) : 0, armaduraNome: arm ? arm.n : '',
      nTrilha, nEsc, escPend: nEsc - s.esc.length, pontos, pontosMax: 10 + extrasAtr, nivelPoder, fonte, inf, faixa: faixaInf(inf), armasMax,
      trilha: C && C.trilhas.find(t => t.id == s.trilha) || null };
  }

  /* aplica a regra: máximos, perícias vindas de origem e classe. Devolve mensagens curtas. */
  function aplicar(f) {
    preparar(f);
    const s = f.sfl, msg = [];
    if (s.classeUlt !== undefined && s.classeUlt !== s.classe) { s.perClasse = []; s.trilha = ''; s.esc = s.esc.filter(e => e.k != 'hab') }
    s.classeUlt = s.classe;
    const D_ = derivar(f);
    const ult = s.ult || {}, alvo = { pv: D_.pvMax, pe: D_.folMax, medo: 5, inf: 10 };
    Object.entries(alvo).forEach(([id, mx]) => {
      const st = f.stats.find(x => x.id == id); if (!st) return;
      const antes = ult[id] === undefined ? n0(st.max) : n0(ult[id]);
      if (n0(st.max) != mx || ult[id] === undefined) {
        const novo = ult[id] === undefined && !n0(st.max) && !n0(st.cur), dif = mx - antes;
        if (novo) st.cur = (id == 'medo' || id == 'inf') ? 0 : mx;
        else if (dif > 0 && id != 'medo' && id != 'inf') { st.cur = n0(st.cur) + dif; if (ult[id] !== undefined) msg.push(`+${dif} ${st.n} máximo`) }
        else if (n0(st.cur) > mx) st.cur = mx;
        st.max = mx;
      }
      ult[id] = mx;
    });
    s.ult = ult;
    f.skills.forEach(k => { if (D_.fonte.has(k.n) && n0(k.t) < 3) k.t = 3 });
    return { D: D_, msg };
  }

  /* ---------- testes ---------- */
  const d20 = () => 1 + Math.floor(Math.random() * 20);
  /* atributo + dados extras (vantagem +1, desvantagem -1); reserva < 1 rola 2 e fica com o menor */
  function teste(at, extra, bonus) {
    const pool = n0(at) + n0(extra), q = pool >= 1 ? pool : 2, r = Array.from({ length: q }, d20), d = pool >= 1 ? Math.max(...r) : Math.min(...r);
    return { r, d, total: d + n0(bonus), q, baixo: pool < 1 };
  }
  const treinoDe = (f, nome) => { const k = f.skills.find(x => x.n == nome); return k ? n0(k.t) + n0(k.o) : 0 };
  const treinoArma = (f, fam) => { const a = (f.sfl.armas || []).find(x => x.f == fam); return a ? n0(a.t) : 0 };

  /* ataque de uma arma do inventário: dados, bônus, margem de crítico */
  function ataque(f, it) {
    const a = it.arma || {}, cat = a.cat || 'contundente', esp = cat == 'especial', fam = a.fam || familia(it.n || '');
    const melee = cat == 'contundente' || cat == 'cortante';
    const dados = atr(f, melee ? 'cor' : 'ref');
    const nome = { contundente: 'Contundente', cortante: 'Cortante', arremesso: 'Arremesso', tiro: 'Tiro' }[cat];
    const treinada = !esp || (f.sfl.armas || []).some(x => x.f == fam);
    const bonus = esp ? treinoArma(f, fam) : treinoDe(f, nome);
    return { dados: dados + (treinada ? 0 : -1), bonus: treinada ? bonus : 0, treinada, crit: critDe(a.crit), melee, rotulo: esp ? fam : nome };
  }

  function danoRolar(f, it, crit) {
    const a = it.arma || {}, c = critDe(a.crit), mult = crit ? Math.max(1, c ? c.x : 2) : 1;
    const m = /(\d*)d(\d+)\s*([+-]\s*\d+)?/.exec(String(a.dano || '')); if (!m) return null;
    const q = (+m[1] || 1) * mult, fc = +m[2], fixo = m[3] ? +m[3].replace(/\s+/g, '') : 0;
    const r = Array.from({ length: Math.min(100, q) }, () => 1 + Math.floor(Math.random() * fc));
    const corpo = (a.cat == 'contundente' || a.cat == 'cortante') ? atr(f, 'cor') : 0;
    return { r, soma: r.reduce((t, x) => t + x, 0) + fixo + corpo, corpo, fixo, q, fc, mult };
  }

  /* ---------- catálogo (loja e inventário) ---------- */
  const geral = (n, esp, tipo, extra) => Object.assign({ ref: 'sfl:' + n, n, tipo: tipo || 'geral', esp, qtd: 1 }, extra || {});
  const CAT = D.armas.map(a => ({ ref: 'sfl:' + a.n, n: a.n, tipo: 'arma', esp: /2 mãos/.test(a.n) ? 2 : 1, qtd: 1, desc: a.traco === 'n/a' ? '' : a.traco,
    arma: { dano: a.dano, crit: a.crit, cat: a.cat, fam: a.cat == 'especial' ? familia(a.n) : '', traco: a.traco, efeito: a.efeito, esp: a.cat == 'especial' } }))
    .concat([
      geral('Armadura leve', 1, 'armadura', { red: 1, sub: 'leve', desc: 'Reduz 1 de dano.' }),
      geral('Armadura média', 2, 'armadura', { red: 2, sub: 'média', desc: 'Reduz 2 de dano.' }),
      geral('Armadura pesada', 3, 'armadura', { red: 3, sub: 'pesada', desc: 'Reduz 3 de dano; desvantagem em Parkour e Furtividade.' }),
      geral('Escudo', 2, 'armadura', { red: 0, sub: 'escudo', desc: 'Bloqueio usa ÷3 do teste.' }),
      geral('Bandagem', 0.5, 'consumivel', { desc: 'Medicina DT 15: recupera 1d4 PV (uma vez por ferimento).' }),
      geral('Pilha UV', 0.5, 'consumivel', { desc: 'Alimenta lanterna ou lâmpada UV.' }),
      geral('Lanterna UV', 1, 'geral', { desc: 'Usa pilha UV. Machuca voláteis.' }),
      geral('Ração', 0.5, 'consumivel', { desc: 'Comida para um dia.' }),
      geral('Munição (pente)', 0.5, 'consumivel', { desc: 'Um Suprimento de munição.' }),
      geral('Rádio', 1, 'geral', { desc: 'Capta transmissões das facções.' }),
      geral('Kit de ferramentas', 1, 'geral', { desc: 'Reparos e Técnica.' }),
      geral('Estabilizador', 0.5, 'consumivel', { desc: 'Raro: baixa 2 de Infecção.' })
    ]);
  S.CATALOGO.sfl = CAT;

  /* símbolo do dinheiro: SFL usa euro, a moeda da Estônia, a não ser que o mestre escolha outro */
  S.moedaDe = camp => { const m = camp && camp.config && camp.config.moeda; return camp && camp.sistema == 'sfl' ? (m && m != 'R$' ? m : '€') : (m || 'R$') };

  S.sfl = { ATR, PERICIAS, TREINO, FAIXAS, faixaInf, BENEFICIOS, ESPECIAIS, classe, origem, linha, familia, critDe, preparar, derivar, aplicar, teste, treinoDe, treinoArma, ataque, danoRolar, atr, CAT, dados: D };
})();
