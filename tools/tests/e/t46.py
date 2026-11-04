# Mapas de interior: marcar local, ligar mapa, tirar telhado, salvar, jogador vê, RLS do arquivo
from lib import *
d=seed()
M=q
m2=ids(1,9)
pgx.admin(f"insert into public.arquivos(id,mesa_id,tipo,nome,path,mime,tamanho,criado_por) values ('{m2}','{d['m']}','mapa','Interior Casa','{d['m']}/{m2}.png','image/png',10,'{U['M']}')")
pgx.admin(f"insert into storage.objects(bucket_id,name,owner) values ('mesa-arquivos','{d['m']}/{m2}.png','{U['M']}')")
def scr(pg,x,y):
    return pg.evaluate(f"(()=>{{const r=cv.getBoundingClientRect(),v=S.v;return[r.left+v.x+{x}*v.z,r.top+v.y+{y}*v.z]}})()")
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=abre(b,'M',d);ev=pg.evaluate
    ev("S.v={x:0,y:0,z:1};draw()");pg.wait_for_timeout(100)
    pg.click('[data-t=int]');pg.wait_for_timeout(100)
    chk("ferramenta Interior abre o painel",'interiores' in ev("document.getElementById('opt').innerText").lower())
    x0,y0=scr(pg,300,300);x1,y1=scr(pg,500,450)
    pg.mouse.move(x0,y0);pg.mouse.down();pg.mouse.move(x1,y1,steps=5);pg.mouse.up();pg.wait_for_timeout(200)
    chk("arrastar abre a escolha do mapa",not ev("document.getElementById('ed').classList.contains('hid')"))
    pg.check(f'#ew input[name=int_m][value="{m2}"]');pg.click('#ew [data-int=ok]');pg.wait_for_timeout(1200)
    chk("interior criado com telhado ligado",ev("S.ints.length==1&&S.ints[0].t==1&&S.ints[0].i=='%s'"%m2),ev("JSON.stringify(S.ints)"))
    chk("retângulo na grade",ev("S.ints[0].x==300&&S.ints[0].y==300&&S.ints[0].w==200&&S.ints[0].h==150"),ev("JSON.stringify(S.ints)"))
    chk("salvo no banco",M("select to_jsonb(jsonb_array_length(interiores)) from public.cenas where id='%s'"%d['cA'])==1)
    # toque duplo tira o telhado
    x,y=scr(pg,400,380);pg.mouse.click(x,y);pg.mouse.click(x,y,delay=10);pg.wait_for_timeout(100)
    pg.mouse.dblclick(x,y);pg.wait_for_timeout(900)
    t=ev("S.ints[0].t")
    chk("dois toques alternam o telhado",t in (0,1),t)
    if t==1: pg.click('#opt [data-int=roof]');pg.wait_for_timeout(900)
    chk("telhado tirado",ev("S.ints[0].t")==0)
    chk("telhado gravado no banco",M("select to_jsonb(interiores->0->'t') from public.cenas where id='%s'"%d['cA'])==0)
    pg.click('[data-t=sel]');pg.wait_for_timeout(1200)
    # jogador
    pj=abre(b,'J',d);pj.wait_for_timeout(800)
    chk("jogador recebe o interior",pj.evaluate("(S.ints||[]).length")==1 and pj.evaluate("S.ints[0].t")==0,pj.evaluate("JSON.stringify(S.ints)"))
    chk("jogador não vê marcas nem botão",pj.evaluate("getComputedStyle(document.querySelector('[data-t=int]')).display")=='none')
    chk("imagem do interior liberada ao jogador",pj.evaluate("!!LIB.get('%s')"%m2))
    # volta o telhado e confere desfazer
    pg.click('[data-t=int]');pg.click('#opt [data-int=roof]');pg.wait_for_timeout(300)
    chk("pôr telhado de novo",ev("S.ints[0].t")==1)
    pg.click('#undo');pg.wait_for_timeout(300)
    chk("desfazer volta o telhado",ev("S.ints[0].t")==0,ev("S.ints[0].t"))
    pg.click('#opt [data-int=del]');pg.wait_for_timeout(900)
    print(ev("S.ints.length"),M("select to_jsonb(interiores) from public.cenas where id='%s'"%d['cA']))
    chk("remover interior",ev("S.ints.length")==0 and M("select to_jsonb(jsonb_array_length(interiores)) from public.cenas where id='%s'"%d['cA'])==0)
    pg.wait_for_timeout(100)
    chk("sem erros de script",not [e for e in pg.errs if 'ERR_TUNNEL' not in e and 'Failed to load resource' not in e],pg.errs[:3])
    b.close()
report()
