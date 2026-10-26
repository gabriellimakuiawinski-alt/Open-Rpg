from lib import *
d=seed();png(S+'/tok.png')
M=q
def xy(tid): return M(f"select to_jsonb(array[x,y]) from public.tokens where id='{tid}'")
def row(pg,tid): return pg.evaluate(f"(()=>{{const t=S.tok.find(t=>t.id=='{tid}');return t?{{x:t.x,y:t.y,hid:t.hid,n:t.n,hp:t.hp}}:null}})()")
with sync_playwright() as p:
    b=p.chromium.launch()
    # ================= ADMIN =================
    pa=abre(b,'A',d);ev=pa.evaluate
    chk("admin: papel e classe",ev("ROLE")=='admin' and ev("GER&&!DONO&&document.body.classList.contains('adm')"))
    chk("admin: ve cenas e token oculto",ev("S.scenes.length")==2 and ev("S.tok.length")==4)
    hid=lambda sel:ev(f"(()=>{{const e=document.querySelector('{sel}');return !e||getComputedStyle(e).display=='none'}})()")
    chk("admin: sem musica, notas e obsidian",all(hid(s) for s in ["#mpb","#mm [data-a=m_nt]","#mm [data-a=m_obs]"]))
    chk("admin: tem nevoa/paredes/mapas",not any(hid(s) for s in ["[data-t=fog]","[data-t=wall]","#mm [data-a=m_maps]"]))
    pa.click("[data-a=rm]");chk("admin: painel sem opcoes da mesa (so mestre)",ev("!document.querySelector('#pl [data-cfg]')"))
    ev(f"(()=>{{sel=S.tok.find(t=>t.id=='{d['tChefe']}');tmOpen=true;ui();place()}})()")
    pa.fill("#tm [data-f=hp]","33");pa.wait_for_timeout(900)
    chk("admin edita token criado pelo mestre (update)",M(f"select to_jsonb((dados->>'hp')::int) from public.tokens where id='{d['tChefe']}'")==33)
    pa.click("[data-k=hid]");pa.wait_for_timeout(900)
    chk("admin revela token oculto",M(f"select to_jsonb(oculto) from public.tokens where id='{d['tChefe']}'")==False)
    ev(f"(()=>{{const t=S.tok.find(t=>t.id=='{d['tLacaio']}');t.x=640;t.y=260;save()}})()");pa.wait_for_timeout(900)
    chk("admin move token travado",xy(d['tLacaio'])==[640,260])
    ev("(()=>{S.fg.push({t:'r',p:[[5,5],[50,50]],c:0,w:1});save()})()");pa.wait_for_timeout(900)
    chk("admin edita nevoa",M(f"select to_jsonb(jsonb_array_length(nevoa)) from public.cenas where id='{d['cA']}'")==1)
    ev("sedit(null)");pa.fill('#e_n','Cena do admin');pa.check('#ew [data-mp]');pa.click('[data-a=e_ok]');pa.wait_for_timeout(1200)
    chk("admin cria cena com mapa",M("select to_jsonb(count(*)) from public.mapas_cena mc join public.cenas c on c.id=mc.cena_id where c.nome='Cena do admin'")==1)
    ev("(()=>{S.notes='x';S.pls.push({id:uid(),n:'p',t:[]});save()})()");pa.wait_for_timeout(900)
    chk("admin nao grava notas/playlists",M("select to_jsonb((select count(*) from public.notas)+(select count(*) from public.playlists))")==0)
    ev("fk='map'");pa.set_input_files('#fi',S+'/tok.png');pa.wait_for_timeout(1500)
    chk("admin envia mapa",M("select to_jsonb(count(*)) from public.arquivos where tipo='mapa' and criado_por='%s'"%U['A'])==1)
    chk("admin sem erros",not pa.errs,pa.errs)
    pa.ctx.close()
    # ================= JOGADOR K =================
    seed_after=d
    pk=abre(b,'K',d);ev=pk.evaluate
    pk.evaluate("S.v={x:0,y:0,z:1};draw()");pk.wait_for_timeout(100)
    xs,ys=pk.evaluate(f"(()=>{{const t=S.tok.find(t=>t.id=='{d['tHeroi']}'),r=cv.getBoundingClientRect(),g=S.gs;return[r.left+(t.x+g/2),r.top+(t.y+g/2)]}})()")
    pk.mouse.move(xs,ys);pk.mouse.down();pk.mouse.move(xs+60,ys+60,steps=4);pk.mouse.up();pk.wait_for_timeout(900)
    chk("jogador move token de outro jogador (regra do mestre)",xy(d['tHeroi'])==[750,150],xy(d['tHeroi']))
    pk.mouse.dblclick(xs+50,ys+50);pk.wait_for_timeout(300)
    chk("jogador nao edita token alheio mesmo vinculado a ficha de outro",pk.evaluate("document.getElementById('tm').classList.contains('hid')"))
    pk.ctx.close()
    # ================= TEMPO REAL =================
    d=seed()
    pj=abre(b,'J',d);pm=abre(b,'M',d)
    # mestre mexe -> jogador ve
    M_=lambda sql:pgx.run(U['M'],sql)
    r=M_(f"update public.tokens set x=800,y=300 where id='{d['tGob']}' returning 1;select '[]'::jsonb");emit(pj,'tokens','UPDATE',d['tGob']);pj.wait_for_timeout(200)
    chk("tempo real: jogador ve o token que o mestre moveu",row(pj,d['tGob'])['x']==800 and row(pj,d['tGob'])['y']==300,row(pj,d['tGob']))
    # mestre esconde -> versao sobe -> jogador refaz a cena
    M_(f"update public.tokens set oculto=true where id='{d['tHeroi']}'");emit(pj,'cenas','UPDATE',d['cA']);pj.wait_for_timeout(900)
    chk("tempo real: token ocultado some para o jogador",row(pj,d['tHeroi']) is None,row(pj,d['tHeroi']))
    M_(f"update public.tokens set oculto=false where id='{d['tHeroi']}'");emit(pj,'cenas','UPDATE',d['cA']);pj.wait_for_timeout(900)
    chk("tempo real: token revelado volta para o jogador",row(pj,d['tHeroi']) is not None)
    # mestre cria token -> aparece
    nt=ids(9,1)
    M_(f"insert into public.tokens(id,cena_id,nome,imagem_id,x,y,criado_por,dados) values ('{nt}','{d['cA']}','Recem chegado','{d['gob']}',900,500,'{U['M']}','{{\"hp\":4,\"pv\":4}}')");emit(pj,'tokens','INSERT',nt);pj.wait_for_timeout(300)
    chk("tempo real: token novo aparece para o jogador",row(pj,nt) and row(pj,nt)['n']=='Recem chegado',row(pj,nt))
    M_(f"delete from public.tokens where id='{nt}'");emit(pj,'tokens','DELETE',old=nt);pj.wait_for_timeout(300)
    chk("tempo real: token excluido some",row(pj,nt) is None)
    # jogador move -> mestre ve
    pgx.run(U['J'],f"select public.mover_token('{d['tGob']}', 150, 250)");emit(pm,'tokens','UPDATE',d['tGob']);pm.wait_for_timeout(200)
    chk("tempo real: mestre ve o jogador mover",row(pm,d['tGob'])['x']==150 and row(pm,d['tGob'])['y']==250,row(pm,d['tGob']))
    # mestre edita nevoa -> jogador ve
    M_(f"""update public.cenas set nevoa='[{{"t":"r","p":[[0,0],[10,10]],"c":0,"w":1}}]', escuro=true where id='{d['cA']}'""");emit(pj,'cenas','UPDATE',d['cA']);pj.wait_for_timeout(300)
    chk("tempo real: nevoa e escuro chegam ao jogador",pj.evaluate("S.fg.length==1&&S.nt==1"),pj.evaluate("[S.fg.length,S.nt]"))
    # nao sobrescreve alteracao local pendente
    pj.evaluate(f"(()=>{{const t=S.tok.find(t=>t.id=='{d['tGob']}');t.n='Editando…'}})()")
    # (nome so do dono; so verifica que o evento remoto nao apaga o local)
    M_(f"update public.tokens set x=1000 where id='{d['tGob']}'");emit(pj,'tokens','UPDATE',d['tGob']);pj.wait_for_timeout(200)
    chk("tempo real: alteracao local nao salva e preservada",pj.evaluate(f"S.tok.find(t=>t.id=='{d['tGob']}').n")=='Editando…')
    pj.evaluate(f"S.tok.find(t=>t.id=='{d['tGob']}').n='Goblin'")
    # imagem nova do jogador chega na biblioteca do mestre
    ev=pj.evaluate;ev("fk='chr'");pj.set_input_files('#fi',S+'/tok.png');pj.wait_for_timeout(1500)
    aid=M("select to_jsonb(id::text) from public.arquivos where nome='tok'")
    emit(pm,'arquivos','INSERT',aid);pm.wait_for_timeout(400)
    chk("tempo real: mestre ve imagem enviada pelo jogador",pm.evaluate(f"LIB.has('{aid}')"))
    # mestre troca de cena -> jogador acompanha
    M_(f"select public.ativar_cena('{d['cB']}')");emit(pj,'mesas','UPDATE',d['m']);pj.wait_for_timeout(1200)
    chk("tempo real: jogador acompanha a troca de cena",pj.evaluate("S.cur")==d['cB'] and pj.evaluate("S.tok.map(t=>t.n).join()")=='Token da B',pj.evaluate("[S.cur,S.tok.map(t=>t.n).join()]"))
    chk("tempo real: jogador carrega o mapa da nova cena",pj.evaluate("S.maps.length")==1 and pj.evaluate(f"LIB.has('{d['mapa']}')"))
    # mestre apaga a cena ativa dos jogadores -> espera
    chk("sem erros (jogador)",not pj.errs,pj.errs)
    chk("sem erros (mestre)",not pm.errs,pm.errs)
    pj.screenshot(path=S+'/j1.png')
    b.close()
report()
