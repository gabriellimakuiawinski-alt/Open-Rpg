import json,sys,time,zlib,struct,uuid
from playwright.sync_api import sync_playwright
import pgx
import os
HERE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.abspath(os.path.join(HERE,"..","..",".."))
S=HERE
os.makedirs("/tmp/open-rpg-shots",exist_ok=True)
import base64
MOCK=open(S+"/mock2.js").read().replace("__PIX__","data:image/png;base64,"+base64.b64encode(open(S+"/map.png","rb").read()).decode())
URL="file://"+ROOT+"/mesa.html"
ok=[];bad=[]
def chk(n,c,x=""):
    (ok if c else bad).append(n+(" -> "+str(x) if (not c and x!="") else ""))
def png(path,w=64,h=64,rgb=(200,80,80)):
    raw=b''.join(b'\x00'+bytes(rgb)*w for _ in range(h))
    def ch(t,d): c=struct.pack('>I',len(d))+t+d; return c+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
    open(path,'wb').write(b'\x89PNG\r\n\x1a\n'+ch(b'IHDR',struct.pack('>IIBBBBB',w,h,8,2,0,0,0))+ch(b'IDAT',zlib.compress(raw))+ch(b'IEND',b''))
U={k:str(uuid.UUID(f'{n:08x}-0000-4000-8000-000000000000')) for k,n in dict(M=1,A=2,J=3,K=4,X=5).items()}
def ids(prefix,n): return str(uuid.UUID(f'{prefix:02x}{n:06x}-0000-4000-8000-000000000000'))
def q(sql): return pgx.aj(sql)
def seed():
    pgx.admin("""truncate public.tokens, public.mapas_cena, public.arquivos, public.pastas, public.playlists, public.notas, public.personagens, public.cenas, public.membros, public.mesas, public.campanha_membros, public.campanhas, public.profiles cascade; delete from storage.objects; delete from auth.users;""")
    for k,v in U.items(): pgx.admin(f"insert into auth.users(id,email,raw_user_meta_data) values ('{v}','{k}@x','{{\"nome\":\"{k}\"}}')")
    pgx.admin(f"insert into public.campanhas(id,nome,mestre_id) values ('{ids(9,1)}','Campanha Teste','{U['M']}')")
    pgx.admin(f"insert into public.campanha_membros(campanha_id,user_id,papel) values ('{ids(9,1)}','{U['A']}','admin'),('{ids(9,1)}','{U['J']}','jogador'),('{ids(9,1)}','{U['K']}','jogador')")
    pgx.admin(f"insert into public.mesas(nome,mestre_id,campanha_id) values ('Mesa Teste','{U['M']}','{ids(9,1)}')")
    m=q("select to_jsonb(id::text) from public.mesas limit 1")
    d=dict(m=m,mapa=ids(1,1),gob=ids(1,2),chefe=ids(1,3),aud=ids(1,4),cA=ids(2,1),cB=ids(2,2),mc=ids(3,1),tGob=ids(4,1),tChefe=ids(4,2),tLacaio=ids(4,3),tHeroi=ids(4,4),tB=ids(4,5),fJ=ids(5,1),mcB=ids(3,2))
    A=lambda i,t,n:f"('{d[i]}','{m}','{t}','{n}','{m}/{d[i]}.png','image/png',10,'{U['M']}')"
    pgx.admin(f"insert into public.arquivos(id,mesa_id,tipo,nome,path,mime,tamanho,criado_por) values {A('mapa','mapa','Mapa 1')},{A('gob','chr','Goblin')},{A('chefe','chr','Chefe')}")
    pgx.admin(f"insert into public.arquivos(id,mesa_id,tipo,nome,path,mime,tamanho,criado_por) values ('{d['aud']}','{m}','aud','Musica','{m}/{d['aud']}.mp3','audio/mpeg',10,'{U['M']}')")
    for i in ('mapa','gob','chefe','aud'): pgx.admin(f"insert into storage.objects(bucket_id,name,owner) select 'mesa-arquivos',path,'{U['M']}' from public.arquivos where id='{d[i]}'")
    pgx.admin(f"insert into public.cenas(id,mesa_id,nome,ordem) values ('{d['cA']}','{m}','Cena A',0),('{d['cB']}','{m}','Cena B',1)")
    pgx.admin(f"insert into public.mapas_cena(id,cena_id,arquivo_id) values ('{d['mc']}','{d['cA']}','{d['mapa']}'),('{d['mcB']}','{d['cB']}','{d['mapa']}')")
    pgx.admin(f"insert into public.personagens(id,user_id,campanha_id,nome,dados) values ('{d['fJ']}','{U['J']}','{ids(9,1)}','Heroi do J','{{}}')")
    T=lambda i,n,x,y,extra='':f"('{d[i]}','{d['cA']}','{n}','{d['gob']}',{x},{y},'{U['M']}'{extra})"
    pgx.admin(f"""insert into public.tokens(id,cena_id,nome,imagem_id,x,y,criado_por,oculto,travado,personagem_id,dados) values
      ('{d['tGob']}','{d['cA']}','Goblin','{d['gob']}',100,100,'{U['M']}',false,false,null,'{{"hp":10,"pv":10,"mn":5,"mm":5,"ini":1,"bar":0,"sv":0,"lo":0,"lz":0,"la":60,"ld":0,"lm":"l"}}'),
      ('{d['tChefe']}','{d['cA']}','Chefe Secreto','{d['chefe']}',300,100,'{U['M']}',true,false,null,'{{"hp":50,"pv":50,"mn":5,"mm":5,"ini":1}}'),
      ('{d['tLacaio']}','{d['cA']}','Lacaio Travado','{d['gob']}',500,100,'{U['M']}',false,true,null,'{{"hp":3,"pv":3,"mn":0,"mm":0,"ini":1}}'),
      ('{d['tHeroi']}','{d['cA']}','Heroi','{d['gob']}',700,100,'{U['M']}',false,false,'{d['fJ']}','{{"hp":20,"pv":20,"mn":5,"mm":5,"ini":2}}'),
      ('{d['tB']}','{d['cB']}','Token da B','{d['gob']}',100,100,'{U['M']}',false,false,null,'{{"hp":1,"pv":1,"mn":0,"mm":0,"ini":1}}')""")
    pgx.admin(f"update public.mesas set cena_ativa='{d['cA']}' where id='{m}'")
    return d
def abre(b,user,d,wait=True):
    ctx=b.new_context(viewport={"width":1100,"height":800})
    ctx.route("**/@supabase/supabase-js@2**",lambda r:r.fulfill(status=200,content_type="application/javascript",body=MOCK))
    ctx.add_init_script("localStorage.setItem('me','%s')"%U[user])
    ctx.expose_function("pgcall",lambda s:json.dumps(pgx.handle(json.loads(s)),default=str))
    pg=ctx.new_page();pg.errs=[];pg.ctx=ctx;pg.user=user
    pg.on("pageerror",lambda e:pg.errs.append(str(e)))
    pg.on("console",lambda m:pg.errs.append(m.text) if m.type=="error" else None)
    pg.on("dialog",lambda dl:dl.accept())
    pg.goto(URL+"?mesa="+d['m'])
    if wait: pg.wait_for_function("document.getElementById('cs')&&/salvo/.test(document.getElementById('cs').textContent)",timeout=15000)
    return pg
def emit(pg,table,ev,row=None,old=None,as_user=None):
    """simula o Realtime: só entrega se o usuário da página enxerga a linha (RLS)"""
    if ev!='DELETE':
        t=table
        r=pgx.run(U[pg.user],f"select coalesce(jsonb_agg(to_jsonb(rr_)),'[]'::jsonb) from public.{t} rr_ where id='{row}'")
        if not r.get('data'): return False
        pg.evaluate("([t,p])=>window.__rtEmit(t,p)",[table,{"eventType":ev,"new":r['data'][0],"old":{}}])
    else:
        pg.evaluate("([t,p])=>window.__rtEmit(t,p)",[table,{"eventType":"DELETE","new":{},"old":{"id":old}}])
    return True
def report():
    print("PASSOU:",len(ok));[print("  ok  ",x) for x in ok]
    print("FALHOU:",len(bad));[print("  XX  ",x) for x in bad]
    sys.exit(1 if bad else 0)
