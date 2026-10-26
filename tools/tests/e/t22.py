# Tabletop: girar token com a roda do mouse + ficha/inventário pelo menu do token
from lib import *
d=seed()
M=q
def pos(pg,tid):
    return pg.evaluate(f"(()=>{{const t=S.tok.find(t=>t.id=='{tid}'),r=cv.getBoundingClientRect(),g=S.gs,v=S.v;return[r.left+v.x+(t.x+t.z*g/2)*v.z,r.top+v.y+(t.y+t.z*g/2)*v.z]}})()")
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=abre(b,'M',d);ev=pg.evaluate
    ev("S.v={x:0,y:0,z:1};draw()");pg.wait_for_timeout(100)
    r0=ev(f"(S.tok.find(t=>t.id=='{d['tGob']}').r)||0")
    x,y=pos(pg,d['tGob']);pg.mouse.move(x,y);pg.mouse.down();pg.mouse.move(x+30,y+30,steps=3)
    pg.mouse.wheel(0,-100);pg.wait_for_timeout(100);pg.mouse.wheel(0,-100);pg.wait_for_timeout(100)
    zoom=ev("S.v.z")
    pg.mouse.up();pg.wait_for_timeout(900)
    r1=ev(f"(S.tok.find(t=>t.id=='{d['tGob']}').r)||0")
    chk("roda do mouse gira o token em passos de 15 graus enquanto arrasta",(r1-r0)%360==(-30)%360,(r0,r1))
    chk("a roda não dá zoom enquanto arrasta o token",zoom==1,zoom)
    pg.mouse.wheel(0,-100);pg.wait_for_timeout(150)
    chk("sem arrastar, a roda continua dando zoom",ev("S.v.z")>1,ev("S.v.z"))
    chk("rotação gravada no banco",M(f"select to_jsonb(rot) from public.tokens where id='{d['tGob']}'")==r1 and r1!=0,r1)
    # ficha no menu do token
    ev(f"sel=S.tok.find(t=>t.id=='{d['tHeroi']}');tmTab='g';ui()");pg.wait_for_timeout(300)
    txt=ev("document.getElementById('tm').innerText")
    chk("menu do token mostra a ficha ligada",'Ficha de' in txt,txt[:200])
    chk("menu tem Rolar, Abrir ficha e Inventário","Rolar" in txt and "Abrir ficha" in txt and "Inventário" in txt)
    # dar um item de arma e um consumível à ficha, depois usar pelo tabletop
    pgx.admin("""update public.personagens set dados = jsonb_build_object('inv', jsonb_build_object('items', jsonb_build_array(
      jsonb_build_object('id','i1','n','Faca','tipo','arma','qtd',1,'eq',false,'catg',0,'esp',1,'arma',jsonb_build_object('dano','1d4','crit','19','per','Luta')),
      jsonb_build_object('id','i2','n','Cicatrizante','tipo','consumivel','qtd',2,'eq',false,'catg',1,'esp',1)))) where id='%s'"""%d['fJ'])
    pg.reload();pg.wait_for_function("document.getElementById('cs')&&/salvo/.test(document.getElementById('cs').textContent)",timeout=15000)
    ev("S.v={x:0,y:0,z:1};draw()");x,y=pos(pg,d["tHeroi"]);pg.mouse.dblclick(x,y);pg.wait_for_timeout(500)
    ev("tmTab='g';ui()");pg.wait_for_timeout(300)
    chk("inventário da ficha aparece no menu","Faca" in ev("document.getElementById('tm').innerText"))
    pg.click('#tm [data-mf="atk"]');pg.wait_for_timeout(300)
    chk("Atacar escreve no log da mesa",'Faca ataque' in ev("document.getElementById('log').innerText"))
    pg.click('#tm [data-mf="dano"]');pg.wait_for_timeout(300)
    chk("Dano escreve no log",'dano 1d4' in ev("document.getElementById('log').innerText"))
    pg.click('#tm [data-mf="eq"] >> nth=0');pg.wait_for_timeout(900)
    chk("Equipar grava na ficha (banco)",M(f"select to_jsonb((dados->'inv'->'items'->0->>'eq')) from public.personagens where id='{d['fJ']}'")=='true')
    pg.click('#tm [data-mf="usar"]');pg.wait_for_timeout(900)
    chk("Usar gasta uma unidade do item",M(f"select to_jsonb((dados->'inv'->'items'->1->>'qtd')::int) from public.personagens where id='{d['fJ']}'")==1)
    chk("sem erros",not [e for e in pg.errs if 'net::' not in e],pg.errs)
    b.close()
report()
