from lib import *
d=seed()
with sync_playwright() as p:
    b=p.chromium.launch();pg=abre(b,'M',d);pg.wait_for_timeout(900)
    print(pg.evaluate("['dcb','mpb'].map(i=>JSON.stringify(document.getElementById(i).getBoundingClientRect()))"), pg.viewport_size)
