/* comum.js — conexão com o Supabase e login, compartilhado entre as páginas
   (ficha.html agora; mesa.html depois). A URL e a chave "publishable" são públicas
   por natureza: quem protege os dados são as regras do banco (schema.sql).
   NUNCA coloque aqui a chave "secret" / "service_role". */
(function () {
  const SUPABASE_URL = 'https://riltokltdqpccckpqmal.supabase.co';
  const SUPABASE_KEY = 'sb_publishable_j_yGg0oW5UdCar9Wkfg-zw_Baf8JMwL';

  if (!window.supabase || !window.supabase.createClient) { window.Mesa = null; return; }
  const db = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY, {
    auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true }
  });

  db.auth.onAuthStateChange(async (ev) => {
    if (ev === 'SIGNED_OUT') location.reload();
    if (ev === 'PASSWORD_RECOVERY') {
      const p = prompt('Digite a nova senha (mínimo 6 caracteres):');
      if (p) {
        const { error } = await db.auth.updateUser({ password: p });
        alert(error ? 'Não consegui trocar a senha: ' + traduz(error.message) : 'Senha alterada.');
      }
    }
  });

  function traduz(m) {
    m = String(m || '');
    if (/Invalid login credentials/i.test(m)) return 'E-mail ou senha incorretos.';
    if (/Email not confirmed/i.test(m)) return 'Confirme seu e-mail antes de entrar (veja a caixa de entrada e o spam).';
    if (/at least 6/i.test(m)) return 'A senha precisa ter pelo menos 6 caracteres.';
    if (/already registered/i.test(m)) return 'Este e-mail já tem conta. Use "Entrar".';
    if (/rate limit/i.test(m)) return 'Muitas tentativas seguidas. Espere um pouco e tente de novo.';
    if (/valid email|invalid format/i.test(m)) return 'E-mail inválido.';
    if (/fetch|network/i.test(m)) return 'Sem conexão com o servidor. Confira a internet.';
    return m;
  }

  function estilo() {
    if (document.getElementById('mx-css')) return;
    const s = document.createElement('style');
    s.id = 'mx-css';
    s.textContent = `
#mx-login{position:fixed;inset:0;z-index:100;background:#1b2221 radial-gradient(ellipse at 50% 20%,#2d3a37 0,transparent 70%);display:flex;align-items:center;justify-content:center;padding:16px;font:16px 'Hanken Grotesk',system-ui,sans-serif;color:#1f1b16;overflow:auto}
#mx-login .mx-box{position:relative;background:#f3ecd8;background-image:repeating-linear-gradient(180deg,transparent 0,transparent 31px,#4a6fa522 31px,#4a6fa522 32px);border-radius:3px;padding:34px 26px 24px;width:min(400px,100%);display:flex;flex-direction:column;gap:12px;box-shadow:0 2px 0 #0003,0 30px 50px -20px #000;transform:rotate(-.8deg);animation:mxj .7s cubic-bezier(.34,1.56,.64,1)}
@keyframes mxj{from{opacity:0;transform:translateY(60px) rotate(5deg)}}
#mx-login .mx-box::before{content:"";position:absolute;left:50%;top:-11px;width:84px;height:24px;margin-left:-42px;background:#dcc66ab8;transform:rotate(-3deg);box-shadow:0 1px 2px #0004}
#mx-login .mx-logo{width:70px;height:70px;margin:0 auto 2px}
#mx-login .mx-logo svg{width:100%;height:100%;overflow:visible}
#mx-login .mx-logo .t{fill:none;stroke:#1f1b16;stroke-width:2.8;stroke-linecap:round;stroke-linejoin:round}
#mx-login .mx-logo .o{fill:#f3ecd8;stroke:#1f1b16;stroke-width:2.2;transform-box:fill-box;transform-origin:center;animation:mxp 7s 2s infinite}
#mx-login .mx-logo .i{fill:#c42f23}#mx-login .mx-logo .p{fill:#111}
@keyframes mxp{0%,93%,100%{transform:scaleY(1)}96%{transform:scaleY(.08)}}
#mx-login h2{margin:0;text-align:center;font:400 30px 'Special Elite','Courier New',monospace;letter-spacing:.14em;text-transform:uppercase;color:#1f1b16}
#mx-login h2 b{font-weight:400;color:#b3261e}
#mx-login .mx-m{margin:0 0 6px;color:#51493b;text-align:center;font:700 21px/1.05 'Caveat','Segoe Print',cursive}
#mx-login input{background:transparent;color:#2b4a94;border:0;border-bottom:2px dashed #7a705d;border-radius:0;padding:10px 2px 7px;font:700 22px 'Caveat','Segoe Print',cursive;width:100%;transition:background .2s}
#mx-login input::placeholder{color:#7a705d99;font-weight:500}
#mx-login input:focus{outline:0;border-bottom:2px solid #b3261e;background:#c4473b12}
#mx-login button{position:relative;overflow:hidden;background:transparent;color:#51493b;border:0;border-radius:5px;padding:12px;cursor:pointer;font:400 15px 'Special Elite','Courier New',monospace;transition:transform .18s cubic-bezier(.34,1.56,.64,1),background .2s}
#mx-login button:hover{background:#00000012}
#mx-login button:focus-visible{outline:3px solid #dcc66a;outline-offset:2px}
#mx-login .mx-pri{background:#b3261e;color:#f3ecd8;letter-spacing:.14em;text-transform:uppercase;padding:15px 12px 14px;margin-top:6px;transform:rotate(-.5deg);box-shadow:0 5px 0 #6b160f,inset 0 0 0 2px #ffffff22}
#mx-login .mx-pri:hover{background:#d23a2c;transform:rotate(.4deg) translateY(-2px)}
#mx-login .mx-pri:active{transform:translateY(4px);box-shadow:0 1px 0 #6b160f,inset 0 0 0 2px #ffffff22}
#mx-login .mx-pri:disabled{opacity:.5}
#mx-login .mx-link{color:#51493b;font-size:13px;padding:6px;text-decoration:underline dashed;text-underline-offset:5px}
#mx-msg{min-height:20px;font:400 14px 'Special Elite',monospace;color:#b3261e}#mx-msg.ok{color:#3f7d4a}`;
    document.head.append(s);
    if(!document.querySelector('link[href*="Special+Elite"]')){const l=document.createElement('link');l.rel='stylesheet';l.href='https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=Hanken+Grotesk:wght@400;500;700&family=Special+Elite&display=swap';document.head.append(l)}
  }

  function telaLogin() {
    return new Promise((resolve) => {
      estilo();
      const o = document.createElement('div');
      o.id = 'mx-login';
      o.innerHTML = `<form class="mx-box" novalidate><div class="mx-logo"><svg viewBox="0 0 100 100" aria-hidden="true"><path class="t" d="M50 4 90 27 90 73 50 96 10 73 10 27ZM50 28 77 68 23 68ZM50 4V28M10 27 50 28 90 27M10 27 23 68M90 27 77 68M10 73 23 68M90 73 77 68M50 96 23 68M50 96 77 68"/><path class="o" d="M37.5 56Q50 45.5 62.5 56Q50 66.5 37.5 56Z"/><circle class="i" cx="50" cy="56" r="4.6"/><circle class="p" cx="50" cy="56" r="1.9"/></svg></div><h2>Open <b>RPG</b></h2>
<p class="mx-m">Entre para acessar suas mesas, campanhas e fichas.</p>
<input id="mx-nome" placeholder="Seu nome" autocomplete="nickname" style="display:none">
<input id="mx-email" type="email" placeholder="E-mail" autocomplete="email">
<input id="mx-senha" type="password" placeholder="Senha (mínimo 6 caracteres)" autocomplete="current-password">
<div id="mx-msg"></div>
<button type="submit" class="mx-pri">Entrar</button>
<button type="button" id="mx-alt">Criar conta</button>
<button type="button" id="mx-esq" class="mx-link">Esqueci a senha</button></form>`;
      document.body.append(o);
      const $ = (i) => o.querySelector('#' + i);
      const nome = $('mx-nome'), email = $('mx-email'), senha = $('mx-senha'),
        pri = o.querySelector('.mx-pri'), alt = $('mx-alt'), esq = $('mx-esq'), msg = $('mx-msg');
      let modo = 'entrar';
      const say = (t, ok) => { msg.textContent = t || ''; msg.className = ok ? 'ok' : ''; };
      const aplica = () => {
        nome.style.display = modo === 'criar' ? '' : 'none';
        pri.textContent = modo === 'criar' ? 'Criar conta' : 'Entrar';
        alt.textContent = modo === 'criar' ? 'Já tenho conta' : 'Criar conta';
        senha.autocomplete = modo === 'criar' ? 'new-password' : 'current-password';
      };
      const fim = (u) => { o.remove(); resolve(u); };
      alt.onclick = () => { modo = modo === 'criar' ? 'entrar' : 'criar'; say(''); aplica(); };
      esq.onclick = async () => {
        if (!email.value.trim()) return say('Digite seu e-mail acima e toque de novo.');
        const { error } = await db.auth.resetPasswordForEmail(email.value.trim(), { redirectTo: location.href.split('#')[0] });
        error ? say(traduz(error.message)) : say('Enviamos um link para redefinir a senha no seu e-mail.', true);
      };
      o.querySelector('form').onsubmit = async (e) => {
        e.preventDefault(); say('');
        const em = email.value.trim(), pw = senha.value;
        if (!em || !pw) return say('Preencha e-mail e senha.');
        pri.disabled = true;
        try {
          if (modo === 'criar') {
            const { data, error } = await db.auth.signUp({ email: em, password: pw, options: { data: { nome: nome.value.trim() } } });
            if (error) throw error;
            if (data.user && data.user.identities && !data.user.identities.length) { say('Este e-mail já tem conta. Use "Entrar".'); return; }
            if (data.session) return fim(data.session.user);
            say('Conta criada. Enviamos um e-mail de confirmação: confirme e depois volte aqui para entrar.', true);
            modo = 'entrar'; aplica();
          } else {
            const { data, error } = await db.auth.signInWithPassword({ email: em, password: pw });
            if (error) throw error;
            fim(data.session.user);
          }
        } catch (err) { say(traduz(err.message)); }
        finally { pri.disabled = false; }
      };
      email.focus();
    });
  }

  async function exigirLogin() {
    const { data } = await db.auth.getSession();
    if (data.session) return data.session.user;
    return telaLogin();
  }

  window.Mesa = { db, exigirLogin, sair: () => db.auth.signOut() };
})();
