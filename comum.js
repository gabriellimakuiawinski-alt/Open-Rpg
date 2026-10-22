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
#mx-login{position:fixed;inset:0;z-index:100;background:radial-gradient(circle at 50% 28%,#232850 0,#12142a 65%);display:flex;align-items:center;justify-content:center;padding:16px;font:15px Roboto,system-ui,sans-serif;color:#fff}
#mx-login .mx-box{background:#242946;border-radius:28px;padding:26px 24px;width:min(400px,100%);display:flex;flex-direction:column;gap:10px;box-shadow:0 18px 50px -12px #000c}
#mx-login .mx-logo{width:74px;height:74px;margin:0 auto 4px;filter:drop-shadow(0 0 14px rgba(185,155,255,.45))}
#mx-login .mx-logo svg{width:100%;height:100%;overflow:visible}
#mx-login .mx-logo .t{fill:none;stroke:#b99bff;stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round}
#mx-login .mx-logo .o{fill:#12142a;stroke:#b99bff;stroke-width:2;transform-box:fill-box;transform-origin:center;animation:mxp 7s 2s infinite}
#mx-login .mx-logo .i{fill:#b99bff}#mx-login .mx-logo .p{fill:#12142a}
@keyframes mxp{0%,93%,100%{transform:scaleY(1)}96%{transform:scaleY(.08)}}
#mx-login h2{text-align:center}
#mx-login h2{margin:0;font-weight:800;font-size:28px;color:#fff;text-transform:none;letter-spacing:-.01em;font-family:'Bricolage Grotesque',system-ui,sans-serif}
#mx-login h2 b{color:#b99bff}
#mx-login .mx-m{margin:0 0 6px;color:#9aa0bd;text-align:center}
#mx-login input{background:#1d2133;color:#fff;border:1px solid #454b6b;border-radius:12px;padding:12px;font:inherit;font-size:16px;width:100%}
#mx-login input:focus-visible,#mx-login button:focus-visible{outline:2px solid #bb99ff}
#mx-login button{background:transparent;color:#fff;border:0;border-radius:14px;padding:12px;cursor:pointer;font:inherit}
#mx-login button:hover{background:#ffffff14}
#mx-login .mx-pri{background:linear-gradient(90deg,#b99bff,#d1a8f5);color:#1d1030;font-weight:700}
#mx-login .mx-pri:hover{background:linear-gradient(90deg,#c9adff,#e8b8f5)}
#mx-login .mx-pri:disabled{opacity:.5}
#mx-login .mx-link{color:#9aa0bd;font-size:13px;padding:6px}
#mx-msg{min-height:20px;font-size:14px;color:#ff8a8a}#mx-msg.ok{color:#8be28b}`;
    document.head.append(s);
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
