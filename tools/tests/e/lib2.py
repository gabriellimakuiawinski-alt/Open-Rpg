from lib import *
import os
BASE="file://"+os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..",".."))+"/"
def abre_pg(b,user,path,w=420,h=860,sess=False):
    ctx=b.new_context(viewport={"width":w,"height":h},device_scale_factor=2)
    ctx.route("**/@supabase/supabase-js@2**",lambda r:r.fulfill(status=200,content_type="application/javascript",body=MOCK))
    ctx.route("**/fonts.googleapis.com/**",lambda r:r.abort());ctx.route("**/fonts.gstatic.com/**",lambda r:r.abort())
    ctx.add_init_script("localStorage.setItem('me','%s')"%U[user])
    if sess: ctx.add_init_script("sessionStorage.setItem('open_rpg_abertura','1')")
    ctx.expose_function("pgcall",lambda s:json.dumps(pgx.handle(json.loads(s)),default=str))
    pg=ctx.new_page();pg.errs=[];pg.ctx=ctx;pg.user=user
    pg.on("pageerror",lambda e:pg.errs.append(str(e)))
    pg.on("console",lambda m:pg.errs.append(m.text) if m.type=="error" and "ERR_FAILED" not in m.text and "net::" not in m.text else None)
    pg.on("dialog",lambda dl:dl.accept())
    pg.goto(BASE+path)
    return pg
