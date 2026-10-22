/* mesa-icones.js — troca emojis por ícones de traço */
/* ---------- ícones no lugar dos emojis (troca em qualquer painel, inclusive os criados depois) ---------- */
(function(){
const S_=(p)=>`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${p}</svg>`;
const IC={
'🏠':'<path d="M3 11 12 3l9 8"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
'📜':'<path d="M7 3h10a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2Z"/><path d="M9 8h6M9 12h6M9 16h4"/>',
'📢':'<path d="M3 10v4h4l7 5V5L7 10Z"/><path d="M17.5 8.5a5 5 0 0 1 0 7"/>',
'✕':'<path d="M6 6l12 12M18 6 6 18"/>',
'🔒':'<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
'🔓':'<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 7.5-2"/>',
'🗑':'<path d="M4 7h16M10 7V4h4v3M6 7l1 13h10l1-13M10 11v6M14 11v6"/>',
'💀':'<path d="M12 3a8 8 0 0 0-5 14v3h10v-3a8 8 0 0 0-5-14Z"/><circle cx="9" cy="12" r="1.4"/><circle cx="15" cy="12" r="1.4"/><path d="M10 20v-2M14 20v-2"/>',
'🙈':'<path d="M3 3l18 18"/><path d="M10.6 6.1A9.5 9.5 0 0 1 12 6c5 0 8.5 4 9.5 6a14 14 0 0 1-3 3.8M6.5 7.6A14 14 0 0 0 2.5 12C3.5 14 7 18 12 18c1.3 0 2.5-.3 3.6-.8"/><path d="M9.9 9.9a3 3 0 0 0 4.2 4.2"/>',
'❤':'<path d="M12 20s-8-4.9-8-10.5A4.5 4.5 0 0 1 12 7a4.5 4.5 0 0 1 8 2.5C20 15.1 12 20 12 20Z"/>',
'📺':'<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/>',
'🔦':'<path d="M7 3h10l-1 5H8Z"/><path d="M8 8l-1 3h10l-1-3M10 11v10h4V11"/>',
'🏮':'<circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/>',
'⎘':'<rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2"/>',
'🌙':'<path d="M20 14.5A8.5 8.5 0 1 1 9.5 4a7 7 0 0 0 10.5 10.5Z"/>',
'📁':'<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/>',
'🔄':'<path d="M20 11a8 8 0 0 0-14-4L4 9M4 4v5h5M4 13a8 8 0 0 0 14 4l2-2M20 20v-5h-5"/>',
'⏭':'<path d="M5 5l9 7-9 7Z"/><path d="M18 5v14"/>',
'☁':'<path d="M7 18a4.5 4.5 0 0 1-.5-9A6 6 0 0 1 18 10a4 4 0 0 1-.5 8Z"/>',
'⚠':'<path d="M12 3 2 20h20Z"/><path d="M12 10v5M12 18v.5"/>',
'🔊':'<path d="M3 10v4h4l6 4V6L7 10Z"/><path d="M16 9a4 4 0 0 1 0 6M18.5 6.5a8 8 0 0 1 0 11"/>',
'☐':'<rect x="4" y="4" width="16" height="16" rx="2"/>',
'☑':'<rect x="4" y="4" width="16" height="16" rx="2"/><path d="m8 12 3 3 5-6"/>',
'✓':'<path d="m5 12 5 5 9-10"/>'
};
const re=new RegExp('('+Object.keys(IC).join('|')+')️?','g');
const SKIP=new Set(['SCRIPT','STYLE','TEXTAREA','INPUT','OPTION','SELECT','TITLE']);
function troca(root){
  const w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT,{acceptNode:n=>{
    if(!n.nodeValue||!re.test(n.nodeValue)){re.lastIndex=0;return NodeFilter.FILTER_REJECT}re.lastIndex=0;
    const p=n.parentElement;return p&&!SKIP.has(p.tagName)&&!p.closest('.mdv,#obt,#obc,canvas')?NodeFilter.FILTER_ACCEPT:NodeFilter.FILTER_REJECT}});
  const L=[];while(w.nextNode())L.push(w.currentNode);
  L.forEach(n=>{
    const f=document.createDocumentFragment();let last=0,t=n.nodeValue,m;re.lastIndex=0;
    while((m=re.exec(t))){f.append(t.slice(last,m.index));const i=document.createElement('i');i.className='ie';i.innerHTML=S_(IC[m[1]]);f.append(i);last=m.index+m[0].length}
    f.append(t.slice(last));n.replaceWith(f)})}
let q=0;const go=()=>{q=0;obs.disconnect();try{troca(document.body)}finally{obs.observe(document.body,{childList:true,subtree:true,characterData:true})}};
const obs=new MutationObserver(()=>{if(!q)q=requestAnimationFrame(go)});
go();
})();
