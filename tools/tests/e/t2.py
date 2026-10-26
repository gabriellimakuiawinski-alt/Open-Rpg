from lib import *
d=seed();png(S+'/tok.png')
M=lambda s:q(s)
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=abre(b,'M',d);ev=pg.evaluate
    # --- enviar imagem ---
    ev("fk='chr'");pg.set_input_files('#fi',S+'/tok.png');pg.wait_for_timeout(1500)
    n=M("select to_jsonb(count(*)) from public.arquivos where tipo='chr'")
    chk("upload: arquivo gravado (3 chr)",n==3,n)
    r=M("select to_jsonb(a) from public.arquivos a where nome='tok'")
    chk("upload: miniatura, mime, dono",r and str(r.get('miniatura')).startswith('data:image/') and r['mime']=='image/png' and r['criado_por']==U['M'] and r['tamanho']>50,r and {k:str(v)[:30] for k,v in r.items()})
    chk("upload: arquivo no storage",M(f"select to_jsonb(count(*)) from storage.objects where name='{r['path']}'")==1)
    nid=r['id']
    chk("upload: sem _pend na biblioteca",ev(f"!LIB.get('{nid}')._pend"))
    # --- novo token ---
    ev(f"addTok('{nid}')");pg.wait_for_timeout(900)
    t=M(f"select to_jsonb(t) from public.tokens t where imagem_id='{nid}'")
    chk("token novo gravado com dono e dados",t and t['criado_por']==U['M'] and t['dados']['hp']==10 and t['categoria']=='chr' and t['cena_id']==d['cA'],t)
    tid=t['id']
    # --- mover ---
    ev(f"(()=>{{const t=S.tok.find(t=>t.id=='{tid}');t.x=250;t.y=350;save()}})()");pg.wait_for_timeout(900)
    chk("mover grava x,y",M(f"select to_jsonb(array[x,y]) from public.tokens where id='{tid}'")==[250,350])
    # --- painel: ocultar, travar, vincular ficha ---
    ev(f"(()=>{{sel=S.tok.find(t=>t.id=='{tid}');tmOpen=true;ui();place()}})()")
    v0=M(f"select to_jsonb(versao) from public.cenas where id='{d['cA']}'")
    pg.click("[data-k=hid]");pg.wait_for_timeout(900)
    chk("ocultar grava oculto=true",M(f"select to_jsonb(oculto) from public.tokens where id='{tid}'")==True)
    v1=M(f"select to_jsonb(versao) from public.cenas where id='{d['cA']}'")
    chk("ocultar sobe a versao da cena",v1>v0,(v0,v1))
    pg.click("[data-k=lk]");pg.wait_for_timeout(900)
    chk("travar grava travado=true",M(f"select to_jsonb(travado) from public.tokens where id='{tid}'")==True)
    pg.select_option("select[data-f=pj]",d['fJ']);pg.wait_for_timeout(900)
    chk("vincular ficha grava personagem_id",M(f"select to_jsonb(personagem_id::text) from public.tokens where id='{tid}'")==d['fJ'])
    pg.fill("#tm [data-f=hp]","7");pg.wait_for_timeout(900)
    chk("editar PV grava em dados",M(f"select to_jsonb((dados->>'hp')::int) from public.tokens where id='{tid}'")==7)
    # --- névoa, paredes, escuro, grade ---
    ev("(()=>{S.fg.push({t:'r',p:[[0,0],[100,100]],c:0,w:1});S.walls.push({x1:0,y1:0,x2:100,y2:0,d:0});S.nt=1;S.dl=.5;S.gs=64;S.grid=false;S.fcol='#112233';S.fa=.8;save()})()");pg.wait_for_timeout(900)
    c=M(f"select to_jsonb(c) from public.cenas c where id='{d['cA']}'")
    chk("nevoa gravada",len(c['nevoa'])==1 and c['nevoa'][0]['t']=='r',c['nevoa'])
    chk("paredes/escuro/grade gravados",len(c['paredes'])==1 and c['escuro'] is True and c['escuridao']==0.5 and c['grade_px']==64 and c['grade_visivel'] is False and c['nevoa_cor']=='#112233' and c['nevoa_opacidade']==0.8,c)
    # --- excluir token pelo painel ---
    ev(f"(()=>{{sel=S.tok.find(t=>t.id=='{tid}');tmOpen=true;ui();place()}})()")
    pg.click("[data-k=del]");pg.wait_for_timeout(900)
    chk("excluir token remove do banco",M(f"select to_jsonb(count(*)) from public.tokens where id='{tid}'")==0)
    # --- nova cena com o mapa ---
    ev("sedit(null)");pg.fill('#e_n','Cena Nova');pg.check('#ew [data-mp]');pg.click('[data-a=e_ok]');pg.wait_for_timeout(1200)
    cn=M("select to_jsonb(c) from public.cenas c where nome='Cena Nova'")
    chk("cena nova criada",cn is not None)
    chk("cena nova tem o mapa",M(f"select to_jsonb(count(*)) from public.mapas_cena where cena_id='{cn['id']}'")==1)
    chk("cena nova nao e a ativa",M(f"select to_jsonb(cena_ativa::text) from public.mesas")==d['cA'])
    chk("pilula mostra (oculta)","oculta" in ev("document.getElementById('rmb').textContent"),ev("document.getElementById('rmb').textContent"))
    pg.click("[data-a=rm]");pg.click("[data-a=ativar]");pg.wait_for_timeout(900)
    chk("ativar cena",M("select to_jsonb(cena_ativa::text) from public.mesas")==cn['id'])
    # --- renomear cena existente / mapa travado ---
    ev(f"edit('{d['cB']}')");pg.fill('#e_n','Cena B renomeada');pg.click('[data-a=e_ok]');pg.wait_for_timeout(900)
    chk("renomear cena",M(f"select to_jsonb(nome) from public.cenas where id='{d['cB']}'")=='Cena B renomeada')
    # --- notas e playlist (so mestre) ---
    ev("(()=>{S.notes='segredo do mestre';const q={id:uid(),n:'Combate',t:['"+d['aud']+"']};S.pls.push(q);save()})()");pg.wait_for_timeout(900)
    chk("notas gravadas",M(f"select to_jsonb(texto) from public.notas where mesa_id='{d['m']}'")=='segredo do mestre')
    chk("playlist gravada com faixa",M("select to_jsonb(faixas::text[]) from public.playlists where nome='Combate'")==[d['aud']])
    # --- pasta ---
    ev("(()=>{S.fl.push({id:uid(),n:'Monstros',k:'chr'});save()})()");pg.wait_for_timeout(900)
    chk("pasta gravada",M("select to_jsonb(tipo) from public.pastas where nome='Monstros'")=='chr')
    gid=ev(f"(()=>{{const i=LIB.get('{nid}');i.fid=S.fl[0].id;return sv(i).then(()=>1)}})()")
    chk("mover imagem para a pasta",M(f"select to_jsonb(pasta_id::text) from public.arquivos where id='{nid}'")==ev("S.fl[0].id"))
    # --- trocar categoria chr->prop ---
    ev(f"(()=>{{const i=LIB.get('{nid}');i.k='prop';return sv(i)}})()");pg.wait_for_timeout(700)
    chk("trocar categoria chr->prop",M(f"select to_jsonb(tipo) from public.arquivos where id='{nid}'")=='prop')
    # --- excluir imagem usada ---
    ev(f"del('{nid}');LIB.delete('{nid}')");pg.wait_for_timeout(900)
    chk("excluir imagem: linha e objeto somem",M(f"select to_jsonb((select count(*) from public.arquivos where id='{nid}')+(select count(*) from storage.objects where name like '%{nid}%'))")==0)
    # --- recarregar: tudo volta ---
    pg.reload();pg.wait_for_function("document.getElementById('cs')&&/salvo/.test(document.getElementById('cs').textContent)",timeout=15000)
    chk("recarregar: 3 cenas",ev("S.scenes.length")==3,ev("S.scenes.length"))
    chk("recarregar: abre na cena ativa lembrada",ev("S.cur")==cn['id'] or ev("S.cur")==d['cA'])
    ev(f"loadScene('{d['cA']}')");pg.wait_for_timeout(500)
    chk("recarregar: nevoa/paredes/grade voltam",ev("S.fg.length==1&&S.walls.length==1&&S.nt==1&&S.gs==64&&S.grid===false&&S.fcol=='#112233'&&S.fa==.8&&S.dl==.5"))
    chk("recarregar: notas e playlist",ev("S.notes=='segredo do mestre'&&S.pls.length==1&&S.fl.length==1"))
    chk("sem erros de console",not pg.errs,pg.errs)
    b.close()
report()
