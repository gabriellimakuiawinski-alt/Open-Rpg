from lib import *
d=seed(); CA=d['cA']
with sync_playwright() as p:
    b=p.chromium.launch()
    pj=abre(b,'J',d);pm=abre(b,'M',d);errs=[]
    for pg in (pj,pm):pg.on('pageerror',lambda e:errs.append(str(e)))
    pj.wait_for_timeout(1000)
    chk("jogador: cena clara no início",pj.evaluate("S.nt")==0)
    pgx.admin(f"update public.cenas set escuro=true,escuridao=.9,versao=coalesce(versao,0)+1 where id='{CA}'");emit(pj,'cenas','UPDATE',CA);emit(pm,'cenas','UPDATE',CA);pj.wait_for_timeout(600)
    chk("jogador recebe cena escura em tempo real",pj.evaluate("S.nt")==1)
    chk("mestre recebe cena escura em tempo real",pm.evaluate("S.nt")==1)
    pgx.admin(f"update public.tokens set dados=dados||'{{\"lo\":1,\"lz\":4}}'::jsonb where id='{d['tHeroi']}'");emit(pj,'tokens','UPDATE',d['tHeroi']);emit(pm,'tokens','UPDATE',d['tHeroi']);pj.wait_for_timeout(600)
    chk("luz do token chega ao jogador",pj.evaluate("lightsData().length")==1)
    chk("luz do token chega ao mestre",pm.evaluate("lightsData().length")==1)
    pgx.admin(f"update public.cenas set nevoa='[{{\"t\":\"r\",\"p\":[[400,200],[700,400]],\"c\":false}}]'::jsonb,paredes='[{{\"x1\":300,\"y1\":100,\"x2\":300,\"y2\":400,\"d\":0,\"o\":0}}]'::jsonb where id='{CA}'");emit(pj,'cenas','UPDATE',CA);emit(pm,'cenas','UPDATE',CA);pj.wait_for_timeout(600)
    chk("névoa chega ao jogador e ao mestre",pj.evaluate("S.fg.length")==1 and pm.evaluate("S.fg.length")==1)
    chk("paredes chegam aos dois",pj.evaluate("S.walls.length")==1 and pm.evaluate("S.walls.length")==1)
    pj.screenshot(path=S+'/fog_J.png');pm.screenshot(path=S+'/fog_M.png')
    chk("sem erros de script",not errs,errs)
    b.close()
report()
