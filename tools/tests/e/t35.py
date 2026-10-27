# Grau de treinamento conforme o livro: 2+Int (combatente), 5+Int (especialista), 3+Int (ocultista); NEX 70% sobe treinado ou veterano
from lib2 import *
d=seed()
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=abre_pg(b,'J','ficha.html?id='+d['fJ']);pg.wait_for_timeout(2000);ev=pg.evaluate
    ev("curF().skills.forEach(s=>s.t=0);[0,1,2,3].forEach(i=>curF().skills[i].t=5);curF().skills[4].t=10;render()");pg.wait_for_timeout(300)
    for cl,base in (('combatente',2),('especialista',5),('ocultista',3)):
        ev("(()=>{const f=curF();f.op.classe='%s';render();OP.treinar(f,{modo:'grau',nex:35})})()"%cl);pg.wait_for_timeout(300)
        intl=ev("curF().attrs.find(a=>a.id=='int').v")
        txt=pg.inner_text('#md')
        chk("%s: contador 0 / %d"%(cl,base+intl),'0 / %d'%(base+intl) in txt,(base,intl,txt[:160]))
        pg.click('#md [data-x]');pg.wait_for_timeout(200)
    ev("OP.treinar(curF(),{modo:'grau',nex:70})");pg.wait_for_timeout(300)
    chk("NEX 70%: treinadas e veteranas sobem",pg.locator('#md .cat-i:not(.off)').count()==5,pg.locator('#md .cat-i:not(.off)').count())
    pg.click('#md [data-x]')
    ev("OP.treinar(curF(),{modo:'grau',nex:35})");pg.wait_for_timeout(300)
    chk("NEX 35%: veterana não sobe a Expert",pg.locator('#md .cat-i:not(.off)').count()==4 and 'NEX 70' in pg.locator('#md .cat-i').nth(4).inner_text())
    chk("sem erros",not pg.errs,pg.errs);pg.ctx.close()
    report()
