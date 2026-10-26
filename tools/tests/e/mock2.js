(function(){
 const ME_ID=localStorage.getItem('me');
 const PIX='__PIX__';
 const call=async o=>{if(window.__offline)return{error:{message:'TypeError: Failed to fetch'}};return JSON.parse(await window.pgcall(JSON.stringify({...o,user:ME_ID})))};
 const blobs=new Map;window.__calls=[];
 function qb(table){
  const q={table,op:'select',cols:'*',F:[],ord:[],payload:null,ret:false,conflict:null};let one=0;
  const b={
   select(c){if(q.op=='select')q.cols=c||'*';else q.ret=true;return b},
   insert(p){q.op='insert';q.payload=p;return b},upsert(p,o){q.op='upsert';q.payload=p;q.conflict=o&&o.onConflict;return b},
   update(p){q.op='update';q.payload=p;return b},delete(){q.op='delete';return b},
   eq(k,v){q.F.push(['eq',k,v]);return b},in(k,v){q.F.push(['in',k,v]);return b},
   order(c,o){q.ord.push([c,!(o&&o.ascending===false)]);return b},
   maybeSingle(){one=1;return b},single(){one=2;return b},
   then(a,r){window.__calls.push(q.op+' '+table);return call({kind:'q',q}).then(res=>{if(res.error)return {data:null,error:res.error};let d=res.data;if(one)d=d&&d.length?d[0]:null;return{data:d,error:null}}).then(a,r)}};
  return b}
 const H=[];window.__H=H;
 window.__rtEmit=(table,p)=>H.filter(h=>h.table==table&&(h.event=='*'||h.event==p.eventType)).forEach(h=>h.cb(p));
 window.supabase={createClient(){return{
  from:qb,
  rpc:async(fn,args)=>{window.__calls.push('rpc '+fn);const r=await call({kind:'rpc',fn,args});return r.error?{data:null,error:r.error}:{data:r.data,error:null}},
  storage:{from(){return{
   async upload(path,blob){window.__calls.push('upload');const r=await call({kind:'up',path});if(r.error)return{data:null,error:r.error};blobs.set(path,URL.createObjectURL(blob));return{data:{path},error:null}},
   async remove(paths){const r=await call({kind:'rm',paths});if(r.error)return{data:null,error:r.error};paths.forEach(p=>blobs.delete(p));return{data:r.data,error:null}},
   async createSignedUrl(path){const r=await call({kind:'sign',paths:[path]});if(r.error)return{data:null,error:r.error};return{data:{signedUrl:blobs.get(path)||PIX},error:null}},
   async createSignedUrls(paths){const r=await call({kind:'sign',paths});if(r.error)return{data:null,error:r.error};return{data:r.data.map(n=>({path:n,signedUrl:blobs.get(n)||PIX,error:null})),error:null}}}}},
  channel(){const c={send(m){(window.__sentEv=window.__sentEv||[]).push(m);(window.__sent=window.__sent||[]).push(m.payload);return Promise.resolve('ok')},on(t,cfg,cb){if(t=='broadcast'){(window.__bcs=window.__bcs||{})[cfg.event]=cb;window.__bc=(window.__bcs.musica)||cb;return c}H.push({table:cfg.table,event:cfg.event,cb});return c},subscribe(cb){cb&&setTimeout(()=>cb('SUBSCRIBED'),0);return c}};return c},
  auth:{getSession:async()=>({data:{session:{user:{id:ME_ID,email:'u@x.com'}}}}),onAuthStateChange(){},signOut:async()=>{}}}}};
})();
