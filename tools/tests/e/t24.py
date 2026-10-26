# modificações equipadas na arma: efeito no ataque/dano/crítico, sem espaço, limite pela patente, remover
from lib2 import *
d=seed()
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=abre_pg(b,'J','ficha.html?id='+d['fJ']);pg.wait_for_timeout(2000);ev=pg.evaluate
    chk("armaEf: Cruel +2, Perigosa 19→17, Dum Dum x2→x3",ev("""(()=>{const S=SIS,a=(dano,crit,m)=>S.armaEf({arma:{dano,crit},mods:m.map(n=>({n}))});
      const c=a('1d10','19',['Cruel','Perigosa']),e=a('2d6','x2',['Dum Dum','Explosiva','Calibre Grosso']),z=a('1d6','19',['Certeira','Alongada']);
      return c.dano=='1d10+2'&&c.crit=='17'&&e.crit=='x3'&&e.dano=='3d6+2d6'&&z.atk==4})()"""))
    pg.click('[data-tab=g]');pg.fill('[data-p="op.pp"]','50');pg.press('[data-p="op.pp"]','Tab');pg.wait_for_timeout(400);pg.wait_for_timeout(300)
    pg.click('[data-tab=i]');pg.click('[data-act="op-cat"]');pg.wait_for_timeout(400)
    pg.fill('#catq','katana');pg.locator('#md .cat-i:has-text("Katana")').click();pg.wait_for_timeout(300)
    pg.click('[data-act="op-cat"]');pg.click('#md [data-ab="modificacao"]');pg.locator('#md .cat-i:has-text("Cruel")').click();pg.wait_for_timeout(300)
    pg.locator('#md .cat-i:has-text("Katana")').click();pg.wait_for_timeout(400)
    it="curF().inv.items.find(i=>i.n=='Katana')"
    chk("Cruel fica na arma, sem espaço extra, categoria +1",ev(f"(()=>{{const i={it};return i.esp==2&&i.catg==2&&i.mods.length==1&&i.mods[0].n=='Cruel'}})()"))
    chk("lista de modificações aparece no item",pg.locator('.modt:has-text("Cruel")').count()==1)
    pg.click('[data-tab=c]');pg.wait_for_timeout(200)
    chk("card de ataque mostra o dano com a modificação",'1d10+2' in pg.inner_text('.arma'),pg.inner_text('.arma'))
    pg.click('[data-tab=i]');pg.click('[data-act="op-modx"]');pg.wait_for_timeout(300)
    chk("remover volta categoria e tira a modificação",ev(f"(()=>{{const i={it};return i.catg==1&&i.mods.length==0}})()"))
    pg.click('[data-tab=g]');pg.fill('[data-p="op.pp"]','0');pg.press('[data-p="op.pp"]','Tab');pg.wait_for_timeout(400)
    pg.click('[data-tab=i]');pg.click('[data-act="op-cat"]');pg.click('#md [data-ab="modificacao"]');pg.locator('#md .cat-i:has-text("Perigosa")').click();pg.wait_for_timeout(300)
    pg.locator('#md .cat-i:has-text("Katana")').click();pg.wait_for_timeout(300)
    chk("Recruta não pode: patente bloqueia categoria II",ev(f"(()=>{{const i={it};return i.catg==1&&i.mods.length==0}})()"))
    chk("avisa a patente",'patente' in pg.inner_text('body') and 'Não dá para aplicar' in pg.inner_text('body'))
    chk("sem erros",not pg.errs,pg.errs)
    b.close()
report()
