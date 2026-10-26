import json,re,subprocess
PSQL=['psql','-h','/tmp/pgtest','-p','54329','-U','postgres','-d','e2e','-X','-q','-A','-t','-v','ON_ERROR_STOP=1']
PK={'notas':'mesa_id'}
def lit(v):
    if v is None: return 'NULL'
    if isinstance(v,bool): return 'true' if v else 'false'
    if isinstance(v,(int,float)): return repr(v)
    if isinstance(v,(list,dict)): v=json.dumps(v)
    return "'"+str(v).replace("'","''")+"'"
def admin(sql):
    p=subprocess.run(PSQL,input=sql,capture_output=True,text=True)
    if p.returncode: raise RuntimeError(p.stderr)
    return [l for l in p.stdout.split('\n') if l.strip()]
def aj(sql):  # admin json scalar
    r=admin(sql); return json.loads(r[-1]) if r else None
def run(user,stmt):
    script=f"begin;\nset local role authenticated;\nselect set_config('request.jwt.claim.sub',{lit(user)},true);\n{stmt};\ncommit;"
    p=subprocess.run(PSQL,input=script,capture_output=True,text=True)
    if p.returncode:
        m=re.search(r'ERROR:\s+(.*)',p.stderr); return {'error':{'code':'P0001','message':(m.group(1).strip() if m else p.stderr.strip())}}
    ls=[l for l in p.stdout.split('\n') if l.strip()]
    try: return {'data':json.loads(ls[-1]) if ls else None}
    except Exception: return {'data':None}
def where(F):
    w=[]
    for op,k,v in F:
        w.append(f"{k} = {lit(v)}" if op=='eq' else f"{k} in ({', '.join(lit(x) for x in v) or 'NULL'})")
    return (' where '+' and '.join(w)) if w else ''
def agg(inner): return f"with r as ({inner}) select coalesce(jsonb_agg(to_jsonb(r)),'[]'::jsonb) from r"
def handle(req):
    u=req['user'];k=req['kind']
    if k=='q':
        q=req['q'];t=q['table'];op=q['op']
        if op=='select':
            o=(' order by '+', '.join(c+('' if a else ' desc') for c,a in q['ord'])) if q['ord'] else ''
            cols=re.sub(r"(\w+):(\w+)->(\w+)",r"\2->'\3' as \1",q['cols'])
            return run(u,agg(f"select {cols} from public.{t}{where(q['F'])}{o}"))
        if op in('insert','upsert'):
            rows=q['payload'] if isinstance(q['payload'],list) else [q['payload']]
            cols=list(rows[0].keys());cs=', '.join(cols)
            s=f"insert into public.{t} ({cs}) select {cs} from json_populate_recordset(null::public.{t}, {lit(json.dumps(rows))})"
            if op=='upsert':
                pk=q.get('conflict') or PK.get(t,'id');s+=f" on conflict ({pk}) do update set "+', '.join(f"{c}=excluded.{c}" for c in cols if c!=pk)
            return run(u,agg(s+' returning *'))
        if op=='update':
            cols=list(q['payload'].keys());cs=', '.join(cols)
            return run(u,agg(f"update public.{t} set ({cs}) = (select {cs} from json_populate_record(null::public.{t}, {lit(json.dumps(q['payload']))})){where(q['F'])} returning *"))
        if op=='delete':
            return run(u,agg(f"delete from public.{t}{where(q['F'])} returning *"))
    if k=='rpc':
        a=', '.join(f"{n}=>{lit(v)}" for n,v in (req.get('args') or {}).items())
        return run(u,f"select to_jsonb(public.{req['fn']}({a})::text)")
    if k=='up':
        return run(u,f"insert into storage.objects(bucket_id,name,owner) values ('mesa-arquivos',{lit(req['path'])},{lit(u)}) returning 1;select '[]'::jsonb")
    if k=='rm':
        return run(u,agg(f"delete from storage.objects where bucket_id='mesa-arquivos' and name in ({', '.join(lit(x) for x in req['paths'])}) returning name"))
    if k=='sign':
        return run(u,f"select coalesce(jsonb_agg(name),'[]'::jsonb) from storage.objects where bucket_id='mesa-arquivos' and name in ({', '.join(lit(x) for x in req['paths'])})")
    return {'error':{'message':'?'+k}}
