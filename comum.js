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
#mx-login{position:fixed;inset:0;z-index:100;background:#1d2133;display:flex;align-items:center;justify-content:center;padding:16px;font:15px Roboto,system-ui,sans-serif;color:#fff}
#mx-login .mx-box{background:#2a2e44;border-radius:24px;padding:24px;width:min(400px,100%);display:flex;flex-direction:column;gap:10px;box-shadow:0 8px 32px #0009}
#mx-login h2{margin:0;font-weight:500;font-size:24px;color:#fff;text-transform:none;letter-spacing:0}
#mx-login .mx-m{margin:0 0 4px;color:#9aa0bd}
#mx-login input{background:#1d2133;color:#fff;border:1px solid #454b6b;border-radius:12px;padding:12px;font:inherit;font-size:16px;width:100%}
#mx-login input:focus-visible,#mx-login button:focus-visible{outline:2px solid #bb99ff}
#mx-login button{background:transparent;color:#fff;border:0;border-radius:14px;padding:12px;cursor:pointer;font:inherit}
#mx-login button:hover{background:#ffffff14}
#mx-login .mx-pri{background:linear-gradient(90deg,#bb99ff,#e0a8f0);color:#1d1030;font-weight:700}
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
      o.innerHTML = `<form class="mx-box" novalidate><h2>Mesa RPG</h2>
<p class="mx-m">Entre na sua conta para acessar suas fichas.</p>
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
