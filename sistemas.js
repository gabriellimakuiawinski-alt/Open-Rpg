/* sistemas.js — sistemas de RPG do Open RPG (ficha, loja e mesa usam o mesmo arquivo).
   Cada campanha escolhe um sistema:
   - 'op'      Ordem Paranormal: a ficha se calcula sozinha (PV/PE/SAN pelo NEX, Defesa pelo que está
               equipado, carga, patente, luz para a mesa, avisos de novas habilidades).
   - 'modular' tudo editável à mão, sem regras automáticas.
   Aqui só existe mecânica (números e nomes curtos). Textos dos livros não entram no repositório. */
(function () {
  'use strict';
  const SISTEMAS = {
    op: { n: 'Ordem Paranormal', d: 'Ficha automática: NEX, PV/PE/SAN, Defesa, carga e luz se calculam sozinhos.' },
    modular: { n: 'Modular', d: 'Ficha livre: você cria e edita todos os campos, barras e listas.' }
  };
  const ATR = [['agi', 'AGI', 'Agilidade'], ['for', 'FOR', 'Força'], ['int', 'INT', 'Intelecto'], ['pre', 'PRE', 'Presença'], ['vig', 'VIG', 'Vigor']];
  const PERICIAS = [['Acrobacia', 'agi'], ['Adestramento', 'pre'], ['Artes', 'pre'], ['Atletismo', 'for'], ['Atualidades', 'int'], ['Ciências', 'int'], ['Crime', 'agi'], ['Diplomacia', 'pre'], ['Enganação', 'pre'], ['Fortitude', 'vig'], ['Furtividade', 'agi'], ['Iniciativa', 'agi'], ['Intimidação', 'pre'], ['Intuição', 'pre'], ['Investigação', 'int'], ['Luta', 'for'], ['Medicina', 'int'], ['Ocultismo', 'int'], ['Percepção', 'pre'], ['Pilotagem', 'agi'], ['Pontaria', 'agi'], ['Profissão', 'int'], ['Reflexos', 'agi'], ['Religião', 'pre'], ['Sobrevivência', 'int'], ['Tática', 'int'], ['Tecnologia', 'int'], ['Vontade', 'pre']];
  const TREINO = [[0, 'Destreinado'], [5, 'Treinado +5'], [10, 'Veterano +10'], [15, 'Expert +15']];

  /* ---------- classes: [inicial, por nível] (+ atributo quando indicado) ---------- */
  const CLASSES = {
    combatente: { n: 'Combatente', pv: [20, 4], pe: [2, 2], san: [12, 3], pd: [6, 3], poder: 'Poder de combatente',
      ex: { 5: 'Ataque especial (2 PE, +5)', 25: 'Ataque especial (3 PE, +10)', 55: 'Ataque especial (4 PE, +15)', 85: 'Ataque especial (5 PE, +20)' } },
    especialista: { n: 'Especialista', pv: [16, 3], pe: [3, 3], san: [16, 4], pd: [8, 4], poder: 'Poder de especialista',
      ex: { 5: 'Eclético e Perito (2 PE, +1d6)', 25: 'Perito (3 PE, +1d8)', 40: 'Engenhosidade (veterano)', 55: 'Perito (4 PE, +1d10)', 75: 'Engenhosidade (expert)', 85: 'Perito (5 PE, +1d12)' } },
    ocultista: { n: 'Ocultista', pv: [12, 2], pe: [4, 4], san: [20, 5], pd: [10, 5], poder: 'Poder de ocultista',
      ex: { 5: 'Escolhido pelo Outro Lado (1º círculo)', 25: 'Escolhido pelo Outro Lado (2º círculo)', 55: 'Escolhido pelo Outro Lado (3º círculo)', 85: 'Escolhido pelo Outro Lado (4º círculo)' } },
    criatura: { n: 'Criatura', oculta: true, pv: [0, 0], pe: [0, 0], san: [0, 0], pd: [0, 0], poder: 'Habilidade', ex: {} },
    sobrevivente: { n: 'Sobrevivente', estagio: true, pv: [8, 2], pe: [2, 1], san: [8, 2], pd: [4, 2], poder: 'Habilidade',
      ex: { 1: 'Empenho', 2: 'Trilha (1ª habilidade)', 3: 'Aumento de atributo', 4: 'Trilha (2ª habilidade)', 5: 'Cicatrizado' } }
  };
  const NEX = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 99];
  /* marcos comuns às 3 classes de agente: [tipo, rótulo] */
  const MARCOS = { 10: [['trilha', 'Habilidade de trilha']], 15: [['poder']], 20: [['atr', 'Aumento de atributo']], 30: [['poder']],
    35: [['grau', 'Grau de treinamento']], 40: [['trilha', 'Habilidade de trilha']], 45: [['poder']], 50: [['atr', 'Aumento de atributo'], ['vers', 'Versatilidade']],
    60: [['poder']], 65: [['trilha', 'Habilidade de trilha']], 70: [['grau', 'Grau de treinamento']], 75: [['poder']], 80: [['atr', 'Aumento de atributo']],
    90: [['poder']], 95: [['atr', 'Aumento de atributo']], 99: [['trilha', 'Habilidade de trilha']] };
  const PATENTES = [[0, 'Recruta', 'Baixo', [2, 0, 0, 0]], [20, 'Operador', 'Médio', [3, 1, 0, 0]], [50, 'Agente especial', 'Médio', [3, 2, 1, 0]],
    [100, 'Oficial de operações', 'Alto', [3, 3, 2, 1]], [200, 'Agente de elite', 'Ilimitado', [3, 3, 3, 2]]];
  const CIRCULO_PE = { 1: 1, 2: 3, 3: 6, 4: 10 };
  const ROMANO = ['0', 'I', 'II', 'III', 'IV'];
  /* alvos de efeitos automáticos (habilidades, homebrews e itens) */
  const ALVOS = [['pv', 'PV máximos'], ['pe', 'PE máximos'], ['san', 'SAN máxima'], ['def', 'Defesa'], ['desloc', 'Deslocamento (m)'], ['carga', 'Espaços de carga'], ['res', 'Testes de resistência']]
    .concat(PERICIAS.map(([n]) => ['per:' + n, 'Perícia: ' + n]));

  const n0 = v => { v = +v; return isFinite(v) ? v : 0 };
  const av = (f, id) => { const a = (f.attrs || []).find(a => a.id == id); return a ? n0(a.v) : 0 };
  const uid = () => Math.random().toString(36).slice(2, 9);
  const temQtd = it => it && (it.qtd === undefined || it.qtd === '' || n0(it.qtd) > 0);

  function nivel(op) {
    const C = CLASSES[op.classe] || CLASSES.combatente;
    if (C.estagio) return Math.max(1, Math.min(5, Math.round(n0(op.estagio) || 1)));
    const x = n0(op.nex) || 5; return x >= 99 ? 20 : Math.max(1, Math.min(19, Math.floor(x / 5)));
  }
  const nexDoNivel = n => n >= 20 ? 99 : n * 5;

  /* marcos atingidos ao chegar no nível n */
  function marcos(classe, n) {
    const C = CLASSES[classe] || CLASSES.combatente, out = [];
    if (C.estagio) { if (C.ex[n]) out.push({ k: n == 3 ? 'atr' : n == 2 || n == 4 ? 'trilha' : 'classe', t: C.ex[n] }); return out }
    const x = nexDoNivel(n);
    if (C.ex[x]) out.push({ k: 'classe', t: C.ex[x] });
    (MARCOS[x] || []).forEach(([k, t]) => out.push({ k, t: k == 'poder' ? C.poder : t }));
    if (classe == 'ocultista' && x > 5) out.push({ k: 'ritual', t: 'Aprender um ritual (de qualquer círculo que você já lance; não conta no limite de rituais)' });   // livro p.33
    return out;
  }

  /* efeitos automáticos: habilidades (inclui homebrew) + itens equipados com bônus */
  function efeitos(f, n) {
    const E = {}, per = {}, soma = (a, v) => { if (a.startsWith('per:')) per[a.slice(4)] = (per[a.slice(4)] || 0) + v; else E[a] = (E[a] || 0) + v };
    (f.poderes || []).forEach(p => { if (p.off) return; (p.ef || []).forEach(e => { if (e && e.a) soma(e.a, n0(e.v) * (e.nv ? n : 1)) }) });
    /* bônus de itens em perícia não se acumulam: vale o maior */
    const itPer = {};
    ((f.inv && f.inv.items) || []).forEach(it => {
      if (!temQtd(it) || (it.precisaEq && !it.eq)) return;
      (it.ef || []).forEach(e => { if (!e || !e.a) return; const v = n0(e.v);
        if (e.a.startsWith('per:')) { const k = e.a.slice(4); itPer[k] = Math.max(itPer[k] || 0, v) } else E[e.a] = (E[e.a] || 0) + v });
    });
    Object.entries(itPer).forEach(([k, v]) => per[k] = (per[k] || 0) + v);
    return { E, per };
  }

  /* ---------- tudo que a ficha de Ordem Paranormal calcula sozinha ---------- */
  function derivar(f, cfg) {
    cfg = cfg || {};
    const op = f.op || {}, C = CLASSES[op.classe] || CLASSES.combatente, n = nivel(op), A = id => av(f, id);
    const { E, per } = efeitos(f, n), b = op.bonus || {};
    const prog = (t, at) => t[0] + at + (n - 1) * (t[1] + (C.estagio ? 0 : at));
    const pvMax = Math.max(1, prog(C.pv, A('vig')) + (E.pv || 0) + n0(b.pv));
    let peMax, sanMax, pdMax = 0;
    if (cfg.determinacao) { pdMax = Math.max(0, prog(C.pd, A('pre')) + (E.pe || 0) + n0(b.pe)); peMax = pdMax; sanMax = 0 }
    else { peMax = Math.max(0, prog(C.pe, A('pre')) + (E.pe || 0) + n0(b.pe)); sanMax = Math.max(0, C.san[0] + (n - 1) * C.san[1] + (E.san || 0) + n0(b.san)) }
    if (C.criatura) { peMax = 0; sanMax = 0; pdMax = 0 }
    const itens = ((f.inv && f.inv.items) || []).filter(temQtd);
    const forca = A('for'), cap = (forca > 0 ? forca * 5 : 2) + (E.carga || 0) + n0(b.carga);
    const usado = itens.reduce((t, it) => t + n0(it.esp) * (it.qtd === undefined ? 1 : n0(it.qtd)), 0);
    const sobre = usado > cap, maxCarga = cap * 2;
    /* Defesa: 10 + AGI + 1 proteção (a melhor equipada) + escudo equipado + efeitos */
    const prot = itens.filter(it => it.tipo == 'protecao' && it.eq);
    const arm = prot.filter(it => it.sub != 'escudo').sort((a, b) => n0(b.def) - n0(a.def))[0];
    const esc = prot.filter(it => it.sub == 'escudo').sort((a, b) => n0(b.def) - n0(a.def))[0];
    const det = [['Base', 10], ['AGI', A('agi')]];
    if (arm) det.push([arm.n || 'Proteção', n0(arm.def)]);
    if (esc) det.push([esc.n || 'Escudo', n0(esc.def)]);
    if (E.def) det.push(['Habilidades', E.def]);
    if (n0(b.def)) det.push(['Outros', n0(b.def)]);
    if (sobre) det.push(['Sobrecarga', -5]);
    const def = det.reduce((t, x) => t + x[1], 0);
    const desloc = 9 + (E.desloc || 0) + n0(b.desloc) - (sobre ? 3 : 0);
    const limPE = C.estagio ? 1 : n;
    const pp = n0(op.pp), pat = PATENTES.filter(p => pp >= p[0]).pop();
    const porCat = [0, 0, 0, 0, 0];
    itens.forEach(it => { const c = Math.max(0, Math.min(4, Math.round(n0(it.catg)))); if (c) porCat[c] += it.qtd === undefined ? 1 : Math.max(0, Math.round(n0(it.qtd))) });
    const excesso = [1, 2, 3, 4].filter(c => porCat[c] > pat[3][c - 1]).map(c => `${porCat[c]} itens de categoria ${ROMANO[c]} (limite ${pat[3][c - 1]})`);
    const pesadaSemProf = arm && arm.sub == 'pesada' && !(f.poderes || []).some(p => /prote[cç][aã]o pesada/i.test(p.n || ''));
    return { n, nex: C.estagio ? null : nexDoNivel(n), estagio: C.estagio ? n : null, classe: C, pvMax, peMax, sanMax, pdMax, determinacao: !!cfg.determinacao,
      def, defDet: det, desloc, cap, usado, sobre, maxCarga, limPE, patente: pat, porCat, excesso, per, E, res: E.res || 0,
      dtRitual: 10 + limPE + A('pre'), luz: luz(f), pesadaSemProf };
  }

  /* melhor luz que o inventário oferece: c = lanterna (cone), l = lampião (raio). Em metros. */
  function luz(f) {
    const r = { c: 0, l: 0, cn: '', ln: '' };
    ((f.inv && f.inv.items) || []).forEach(it => {
      if (!temQtd(it) || !it.luz || typeof it.luz != 'object') return;
      const t = it.luz.t == 'c' ? 'c' : it.luz.t == 'l' ? 'l' : null, m = n0(it.luz.m);
      if (t && m > r[t]) { r[t] = m; r[t + 'n'] = it.n || '' }
    });
    return r;
  }

  /* garante a estrutura de uma ficha de Ordem Paranormal (não apaga nada que já exista) */
  function prepararOP(f) {
    if (!f.op || typeof f.op != 'object') {
      const info = k => { const x = (f.info || []).find(i => (i.n || '').toLowerCase() == k); return x ? String(x.v || '') : '' };
      const cl = info('classe').toLowerCase(), nx = parseInt(info('nex'), 10);
      f.op = { classe: CLASSES[cl] ? cl : 'combatente', nex: NEX.includes(nx) ? nx : 5, estagio: 1, origem: info('origem'), trilha: info('trilha'), pp: 0, bonus: {}, avisos: [] };
    }
    const op = f.op; op.bonus = op.bonus || {}; op.avisos = Array.isArray(op.avisos) ? op.avisos : [];
    if (!CLASSES[op.classe]) op.classe = 'combatente';
    if (!Array.isArray(f.attrs)) f.attrs = [];
    ATR.forEach(([id, n]) => { if (!f.attrs.some(a => a.id == id)) f.attrs.push({ id, n, v: 1 }) });
    if (!Array.isArray(f.stats)) f.stats = [];
    [['pv', 'PV', '#ee4444'], ['pe', 'PE', '#b980ff'], ['san', 'SAN', '#44aaff']].forEach(([id, n, c]) => { if (!f.stats.some(s => s.id == id)) f.stats.push({ id, n, cur: 0, max: 0, c }) });
    if (!Array.isArray(f.skills) || !f.skills.length) f.skills = PERICIAS.map(([n, a]) => ({ id: uid(), n, a, t: 0, o: 0 }));
    if (!f.inv || !Array.isArray(f.inv.items)) f.inv = { items: [] };
    if (!Array.isArray(f.poderes)) f.poderes = [];
    return f;
  }

  /* aplica a regra na ficha: atualiza máximos (e soma no atual quando o máximo sobe),
     cria avisos de NEX. Devolve mensagens curtas para mostrar ao jogador. */
  function aplicar(f, cfg) {
    prepararOP(f);
    const D = derivar(f, cfg), op = f.op, msg = [];
    const st = id => f.stats.find(s => s.id == id);
    const alvo = { pv: D.pvMax, pe: D.peMax, san: D.sanMax };
    const ult = op.ult || {};
    Object.entries(alvo).forEach(([id, mx]) => {
      const s = st(id); if (!s) return;
      if (id == 'pe') s.n = D.determinacao ? 'PD' : 'PE';
      const antes = ult[id] === undefined ? n0(s.max) : n0(ult[id]);
      if (n0(s.max) != mx || ult[id] === undefined) {
        const novo = ult[id] === undefined && !n0(s.max) && !n0(s.cur); // ficha nova: começa cheia
        const dif = mx - antes;
        if (novo) s.cur = mx;
        else if (dif > 0) { s.cur = n0(s.cur) + dif; if (ult[id] !== undefined) msg.push(`+${dif} ${s.n} máximo`) }
        else if (n0(s.cur) > mx) s.cur = mx;
        s.max = mx;
      }
      ult[id] = mx;
    });
    op.ult = ult;
    /* avisos de NEX / estágio */
    const n = D.n, visto = n0(op.visto) || 0;
    if (!visto) op.visto = n;
    else if (n > visto) {
      for (let lv = visto + 1; lv <= n; lv++) marcos(op.classe, lv).forEach(m => op.avisos.push({ id: uid(), nv: lv, k: m.k, t: m.t }));
      msg.push(D.estagio ? `Estágio ${n}!` : `NEX ${D.nex}%!`);
      op.visto = n;
    } else if (n < visto) { op.avisos = op.avisos.filter(a => a.nv <= n); op.visto = n }
    /* info antiga (cabeçalho genérico) acompanha, para quem abre a ficha em outro lugar */
    const setInfo = (k, v) => { const x = (f.info || []).find(i => (i.n || '').toLowerCase() == k); if (x) x.v = v };
    setInfo('classe', D.classe.n); setInfo('nex', D.estagio ? 'Estágio ' + D.estagio : D.nex + '%'); setInfo('defesa', String(D.def)); setInfo('deslocamento', D.desloc + ' m');
    setInfo('origem', op.origem || ''); setInfo('trilha', op.trilha || ''); setInfo('patente', D.patente[1]);
    return { D, msg };
  }

  /* ---------- dados: "2d6+3", "1d12", "3d4-1" ---------- */
  /* efeito das modificações de arma (por nome). atk = bônus no ataque; dano = texto somado; dado = +dados do mesmo tipo; marg = margem de ameaça; mult = multiplicador */
  const MODEF = { 'Certeira': { atk: 2 }, 'Alongada': { atk: 2 }, 'Cruel': { dano: '+2' }, 'Perigosa': { marg: 2 }, 'Mira Laser': { marg: 2 }, 'Dum Dum': { mult: 1 }, 'Explosiva': { dano: '+2d6' }, 'Calibre Grosso': { dado: 1 }, 'Lancinante': { dano: '+1d8' }, 'Erosiva': { dano: '+1d8' } };
  const modNome = m => typeof m == 'string' ? m : (m && m.n) || '';
  function armaEf(it) {
    const a = it.arma || {}, r = { dano: a.dano || '', crit: a.crit || '', atk: n0(a.atk), mods: [] };
    (it.mods || []).forEach(m => { const e = MODEF[modNome(m)]; if (!e) return; r.mods.push(modNome(m));
      if (e.atk) r.atk += e.atk;
      if (e.dado && r.dano) r.dano = r.dano.replace(/(\d*)d(\d+)/i, (x, q, d) => ((+q || 1) + e.dado) + 'd' + d);
      if (e.dano && r.dano) r.dano += e.dano;
      if (e.marg || e.mult) { const c = String(r.crit).replace(/\s+/g, '').match(/^(\d+)?\/?(?:x(\d+))?$/i);
        if (c) { const mg = Math.max(2, (c[1] ? +c[1] : 20) - (e.marg || 0)), mu = (c[2] ? +c[2] : 2) + (e.mult || 0);
          r.crit = mg < 20 ? (mu != 2 ? mg + '/x' + mu : String(mg)) : 'x' + mu } } });
    return r;
  }
  function rolar(expr) {
    const s = String(expr || '').replace(/\s+/g, '').toLowerCase(); if (!s) return null;
    let total = 0; const partes = [];
    const re = /([+-]?)(\d*)d(\d+)|([+-]?)(\d+)/g; let m, ok = false;
    while ((m = re.exec(s))) {
      ok = true;
      if (m[3]) { const q = Math.min(100, +(m[2] || 1)), fc = +m[3], sg = m[1] == '-' ? -1 : 1, r = [];
        for (let i = 0; i < q; i++) r.push(1 + Math.floor(Math.random() * fc));
        total += sg * r.reduce((a, b) => a + b, 0); partes.push((sg < 0 ? '-' : '') + `[${r.join(',')}]`) }
      else { const v = (m[4] == '-' ? -1 : 1) * +m[5]; total += v; partes.push(String(v)) }
    }
    return ok ? { total, txt: partes.join(' ') } : null;
  }
  /* teste de perícia de OP: nº de d20 = atributo (0 = 2 dados, fica o menor) */
  function teste(at, bonus) {
    const q = at > 0 ? at : 2, r = Array.from({ length: q }, () => 1 + Math.floor(Math.random() * 20));
    const d = at > 0 ? Math.max(...r) : Math.min(...r); return { r, d, total: d + (bonus || 0) };
  }

  /* ---------- catálogo base de Ordem Paranormal (só números) ---------- */
  const W = (n, catg, dano, crit, alc, td, esp, per) => ({ ref: 'op:' + n, n, tipo: 'arma', catg, esp, arma: { dano, crit, alc, td, per } });
  const G = (n, catg, esp, x) => Object.assign({ ref: 'op:' + n, n, tipo: 'geral', catg, esp }, x || {});
  const CATALOGO = { op: [
    { ref: 'op:Proteção leve', n: 'Proteção leve', tipo: 'protecao', sub: 'leve', def: 5, catg: 1, esp: 2 },
    { ref: 'op:Proteção pesada', n: 'Proteção pesada', tipo: 'protecao', sub: 'pesada', def: 10, catg: 2, esp: 5 },
    { ref: 'op:Escudo', n: 'Escudo', tipo: 'protecao', sub: 'escudo', def: 2, catg: 1, esp: 2 },
    G('Celular', 0, 1, { luz: { t: 'c', m: 4.5 } }),
    G('Lanterna', 0, 1, { luz: { t: 'c', m: 9 } }),
    G('Lanterna tática', 1, 1, { luz: { t: 'c', m: 18 } }),
    G('Vela', 0, 0.5, { luz: { t: 'l', m: 3 } }),
    G('Lampião', 0, 1, { luz: { t: 'l', m: 6 } }),
    G('Lampião de camping (LED)', 1, 1, { luz: { t: 'l', m: 9 } }),
    W('Faca', 0, '1d4', '19', 'Curto', 'C', 1, 'Luta'), W('Martelo', 0, '1d6', 'x2', '', 'I', 1, 'Luta'), W('Punhal', 0, '1d4', 'x3', '', 'P', 1, 'Luta'),
    W('Bastão', 0, '1d6', 'x2', '', 'I', 1, 'Luta'), W('Machete', 0, '1d6', '19', '', 'C', 1, 'Luta'), W('Lança', 0, '1d6', 'x2', 'Curto', 'P', 1, 'Luta'),
    W('Cajado', 0, '1d6', 'x2', '', 'I', 2, 'Luta'), W('Arco', 0, '1d6', 'x3', 'Médio', 'P', 2, 'Pontaria'), W('Besta', 0, '1d8', '19', 'Médio', 'P', 2, 'Pontaria'),
    W('Pistola', 1, '1d12', '18', 'Curto', 'B', 1, 'Pontaria'), W('Revólver', 1, '2d6', '19/x3', 'Curto', 'B', 1, 'Pontaria'), W('Fuzil de caça', 1, '2d8', '19/x3', 'Médio', 'B', 2, 'Pontaria'),
    W('Machadinha', 0, '1d6', 'x3', 'Curto', 'C', 1, 'Luta'), W('Nunchaku', 0, '1d8', 'x2', '', 'I', 1, 'Luta'), W('Corrente', 0, '1d8', 'x2', '', 'I', 1, 'Luta'),
    W('Espada', 1, '1d8', '19', '', 'C', 1, 'Luta'), W('Florete', 1, '1d6', '18', '', 'C', 1, 'Luta'), W('Machado', 1, '1d8', 'x3', '', 'C', 1, 'Luta'), W('Maça', 1, '2d4', 'x2', '', 'I', 1, 'Luta'),
    W('Acha', 1, '1d12', 'x3', '', 'C', 2, 'Luta'), W('Gadanho', 1, '2d4', 'x4', '', 'C', 2, 'Luta'), W('Katana', 1, '1d10', '19', '', 'C', 2, 'Luta'), W('Marreta', 1, '3d4', 'x2', '', 'I', 2, 'Luta'),
    W('Montante', 1, '2d6', '19', '', 'C', 2, 'Luta'), W('Motosserra', 1, '3d6', 'x2', '', 'C', 2, 'Luta'), W('Arco composto', 1, '1d10', 'x3', 'Médio', 'P', 2, 'Pontaria'),
    W('Balestra', 1, '1d12', '19', 'Médio', 'P', 2, 'Pontaria'), W('Submetralhadora', 1, '2d6', '19/x3', 'Curto', 'B', 1, 'Pontaria'), W('Espingarda', 1, '4d6', 'x3', 'Curto', 'B', 2, 'Pontaria'),
    W('Fuzil de assalto', 2, '2d10', '19/x3', 'Médio', 'B', 2, 'Pontaria'), W('Fuzil de precisão', 3, '2d10', '19/x3', 'Longo', 'B', 2, 'Pontaria'), W('Metralhadora', 2, '2d12', '19/x3', 'Médio', 'B', 2, 'Pontaria'),
    G('Balas curtas', 0, 1, { tipo: 'municao' }), G('Balas longas', 1, 1, { tipo: 'municao' }), G('Cartuchos', 1, 1, { tipo: 'municao' }), G('Flechas', 0, 1, { tipo: 'municao' }),
    G('Kit de perícia', 0, 1), G('Utensílio', 1, 1), G('Vestimenta', 1, 1), G('Algemas', 0, 1), G('Arpéu', 0, 1), G('Bandoleira', 1, 1), G('Binóculos', 0, 1),
    G('Cicatrizante', 1, 1, { tipo: 'consumivel' }), G('Corda', 0, 1), G('Equipamento de sobrevivência', 0, 2), G('Máscara de gás', 0, 1), G('Mochila militar', 1, 0, { ef: [{ a: 'carga', v: 2 }] }),
    G('Pé de cabra', 0, 1), G('Spray de pimenta', 1, 1), G('Taser', 1, 1), G('Granada de fumaça', 0, 1, { tipo: 'consumivel' }), G('Granada de atordoamento', 0, 1, { tipo: 'consumivel' })
  ], modular: [] };
  const TIPOS_ITEM = [['geral', 'Geral'], ['arma', 'Arma'], ['protecao', 'Proteção'], ['municao', 'Munição'], ['consumivel', 'Consumível'], ['paranormal', 'Paranormal']];

  /* Calculador de VD (Valor de Desafio) de criaturas.
     Não existe regra publicada: a fórmula foi ajustada nas 48 criaturas do bestiário do livro (o Anfitrião, VD 413, ficou de fora).
     VD ≈ -304,6 + 78,25 × ln(PV) + 1,547 × (Fortitude + Reflexos + Vontade), arredondado ao passo de 20 (mínimo 20).
     Na conferência cruzada o erro médio foi ~25; metade das criaturas cai a 1 passo do VD do livro. É uma estimativa.
     Habilidades, imunidades e dano dos ataques não entram na conta. */
  function calcVD(d) {
    d = d || {};
    const pv = Math.max(1, n0(d.pv)), sv = n0(d.fort) + n0(d.refl) + n0(d.vont);
    const bruto = -304.6 + 78.25 * Math.log(pv) + 1.547 * sv;
    const vd = Math.max(20, Math.round(bruto / 20) * 20);
    return { bruto: Math.round(bruto), vd, min: Math.max(20, vd - 40), max: vd + 40 };
  }
  // criaturas do livro mais parecidas (PV, defesa e testes de resistência); lista = [{nome, vd, dados}]
  function parecidos(d, lista, n) {
    d = d || {};
    const lp = Math.log(Math.max(1, n0(d.pv))), sv = n0(d.fort) + n0(d.refl) + n0(d.vont), df = n0(d.def);
    return (lista || []).map(e => {
      const x = e.dados || {}, dist = Math.pow((Math.log(Math.max(1, n0(x.pv))) - lp) / 0.5, 2) + Math.pow((n0(x.fort) + n0(x.refl) + n0(x.vont) - sv) / 10, 2) + Math.pow((n0(x.def) - df) / 8, 2);
      return { e, dist };
    }).sort((a, b) => a.dist - b.dist).slice(0, n || 3).map(x => x.e);
  }

  /* Dificuldade do combate - regra do Livro de Regras (cap. Ameaças, "Construindo combates", p. 177):
     soma-se o VD de todas as ameaças e compara-se com a soma do NEX de todos os personagens do grupo.
     Igual ao NEX do grupo = equilibrado; perto da metade = fácil; perto de 1,5 vez = difícil.
     Evitar menos da metade ou mais de 1,5 vez. Jogadores veteranos enfrentam uma categoria abaixo (difícil = VD de 2 vezes o NEX).
     Os cortes entre as categorias (0,75 e 1,25) são interpretação nossa: o livro só dá os pontos 0,5 / 1 / 1,5. */
  function nexDaFicha(op, info) {
    const C = op && CLASSES[op.classe];
    if (C) { if (C.estagio || C.criatura) return null; return n0(op.nex) || 5 }
    const i = (info || []).find(i => String(i.n || '').toLowerCase() == 'nex'), m = i && /(\d+)/.exec(String(i.v));
    return m ? +m[1] : null;
  }
  function dificuldade(nex, vd, vet) {
    nex = n0(nex); vd = n0(vd); const k = vet ? 0.75 : 1, r = nex > 0 ? vd / nex : 0, re = r * k;
    const alvo = m => Math.round(nex * m / k);
    const alvos = { facil: alvo(0.5), equilibrado: alvo(1), dificil: alvo(1.5), max: alvo(1.5) };
    let nivel, texto;
    if (nex <= 0) { nivel = 'sem-grupo'; texto = 'Sem NEX no grupo' }
    else if (vd <= 0) { nivel = 'vazio'; texto = 'Sem inimigos' }
    else if (re < 0.5) { nivel = 'facil-demais'; texto = 'Fácil demais (evite)' }
    else if (re < 0.75) { nivel = 'facil'; texto = 'Fácil' }
    else if (re <= 1.25) { nivel = 'equilibrado'; texto = 'Equilibrado' }
    else if (re <= 1.5) { nivel = 'dificil'; texto = 'Difícil' }
    else { nivel = 'dificil-demais'; texto = 'Difícil demais (evite)' }
    return { nex, vd, razao: r, nivel, texto, alvos };
  }

  window.SIS = { SISTEMAS, ATR, PERICIAS, TREINO, CLASSES, NEX, PATENTES, CIRCULO_PE, ROMANO, ALVOS, CATALOGO, TIPOS_ITEM,
    nivel, marcos, derivar, aplicar, prepararOP, luz, rolar, teste, uid, n0, armaEf, modNome, MODEF, calcVD, parecidos, nexDaFicha, dificuldade,
    sistemaDe: (camp, f) => (camp && SISTEMAS[camp.sistema] ? camp.sistema : camp ? 'op' : (f && SISTEMAS[f.sistema] ? f.sistema : 'op')),
    cfgDe: camp => (camp && camp.config && typeof camp.config == 'object' ? camp.config : {}) };
})();
