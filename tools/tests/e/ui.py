from lib import *
d=seed()
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=abre(b,'M',d);pg.wait_for_timeout(900)
    pg.click("[data-a=rm]");pg.wait_for_timeout(500);pg.screenshot(path=S+'/u1_painel.png')
    pg.click("[data-a=rm]")
    pg.evaluate(f"(()=>{{sel=S.tok.find(t=>t.id=='{d['tGob']}');tmOpen=true;ui();place()}})()");pg.wait_for_timeout(500);pg.screenshot(path=S+'/u2_token.png')
    pg.evaluate("sel=null;selM=null;tmOpen=false;ui();place()")
    pg.click("[data-a=dm]");pg.wait_for_timeout(500);pg.screenshot(path=S+'/u3_menu.png')
    pg.click("[data-a=m_maps]");pg.wait_for_timeout(700);pg.screenshot(path=S+'/u4_modal.png')
    pg.keyboard.press('Escape')
    pg.evaluate("M=null;mrender()");pg.click("[data-a=da]");pg.wait_for_timeout(700);pg.screenshot(path=S+'/u5_dock.png')
    pg.evaluate("tool='fog';ui();opts()") if False else None
    b.close()
