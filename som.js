/* som.js — sons do Open RPG, todos gerados na hora (nenhum arquivo de áudio).
   Som.fx('pasta'|'carimbo'|'tachinha'|'papel'|'lapis'|'dado'|'aba'|'abre'|'fecha'|'postit'|'cracha'|'tecla')
   Som.musica(true|false), Som.efeitos(true|false), Som.volume(0..1)
   O navegador só libera áudio depois do primeiro toque: tudo começa no primeiro gesto. */
(function(){
const LS={get:(k,d)=>{try{const v=localStorage.getItem(k);return v==null?d:v}catch(e){return d}},set:(k,v)=>{try{localStorage.setItem(k,v)}catch(e){}}};
const AC=window.AudioContext||window.webkitAudioContext;
const st={fx:LS.get('orpg_efeitos','1')==='1',mus:LS.get('orpg_musica','1')==='1',vol:+LS.get('orpg_volume','0.6')};
let ctx=null,master=null,fxBus=null,musBus=null,verb=null,ruido=null,liberado=false,motor=null;

function cria(){
  if(ctx||!AC)return ctx;
  ctx=new AC();
  master=ctx.createGain();master.gain.value=st.vol;
  const comp=ctx.createDynamicsCompressor();comp.threshold.value=-18;comp.ratio.value=3;
  master.connect(comp);comp.connect(ctx.destination);
  fxBus=ctx.createGain();fxBus.gain.value=st.fx?.9:0;fxBus.connect(master);
  musBus=ctx.createGain();musBus.gain.value=0;musBus.connect(master);
  // reverberação: resposta ao impulso feita de ruído que decai (sala grande e escura)
  verb=ctx.createConvolver();const n=ctx.sampleRate*3.6,ir=ctx.createBuffer(2,n,ctx.sampleRate);
  for(let c=0;c<2;c++){const d=ir.getChannelData(c);for(let i=0;i<n;i++)d[i]=(Math.random()*2-1)*Math.pow(1-i/n,3.2)}
  verb.buffer=ir;const vg=ctx.createGain();vg.gain.value=.55;verb.connect(vg);vg.connect(musBus);
  // ruído branco reaproveitável
  ruido=ctx.createBuffer(1,ctx.sampleRate*2,ctx.sampleRate);const r=ruido.getChannelData(0);for(let i=0;i<r.length;i++)r[i]=Math.random()*2-1;
  return ctx}

/* ---------------- blocos de som ---------------- */
const T=()=>ctx.currentTime;
function env(g,t,a,pico,dur,fim=.0001){g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(pico,t+a);g.gain.exponentialRampToValueAtTime(fim,t+dur)}
function chiado(t,{tipo='bandpass',f=2500,f2=null,q=1,dur=.15,vol=.4,a=.004,saida=fxBus}={}){
  const s=ctx.createBufferSource();s.buffer=ruido;s.playbackRate.value=.8+Math.random()*.4;
  const fl=ctx.createBiquadFilter();fl.type=tipo;fl.frequency.setValueAtTime(f,t);if(f2)fl.frequency.exponentialRampToValueAtTime(f2,t+dur);fl.Q.value=q;
  const g=ctx.createGain();env(g,t,a,vol,dur);s.connect(fl);fl.connect(g);g.connect(saida);
  s.start(t,Math.random()*1.5);s.stop(t+dur+.05)}
function tom(t,{f=200,f2=null,tipo='sine',dur=.15,vol=.4,a=.003,saida=fxBus}={}){
  const o=ctx.createOscillator();o.type=tipo;o.frequency.setValueAtTime(f,t);if(f2)o.frequency.exponentialRampToValueAtTime(f2,t+dur);
  const g=ctx.createGain();env(g,t,a,vol,dur);o.connect(g);g.connect(saida);o.start(t);o.stop(t+dur+.05)}
function farfalha(t,dur,base=2600,vol=.22){ // papel: várias micro-rajadas
  const n=4+Math.floor(dur*30);for(let i=0;i<n;i++){const tt=t+Math.random()*dur;chiado(tt,{f:base*(.6+Math.random()*.9),q:.9,dur:.02+Math.random()*.05,vol:vol*(.4+Math.random()*.6)})}}

const SONS={
  papel(t){farfalha(t,.16)},
  lapis(t){chiado(t,{tipo:'highpass',f:5200,dur:.03,vol:.18})},
  tachinha(t){tom(t,{f:2100,f2:1300,tipo:'triangle',dur:.04,vol:.22});chiado(t+.005,{tipo:'highpass',f:3500,dur:.03,vol:.2});tom(t+.03,{f:520,f2:380,dur:.08,vol:.12})},
  pasta(t){tom(t,{f:110,f2:55,dur:.16,vol:.55});chiado(t,{tipo:'lowpass',f:1400,dur:.12,vol:.35});farfalha(t+.06,.28,2200,.2)},
  carimbo(t){tom(t,{f:150,f2:42,dur:.2,vol:.75});chiado(t,{tipo:'lowpass',f:900,dur:.08,vol:.5});chiado(t+.002,{tipo:'highpass',f:2400,dur:.025,vol:.25});tom(t+.09,{f:900,f2:600,tipo:'triangle',dur:.03,vol:.06})},
  aba(t){chiado(t,{f:700,f2:3200,q:.7,dur:.22,vol:.28,a:.03});farfalha(t+.1,.1,3000,.12)},
  abre(t){farfalha(t,.12,2000,.2);chiado(t+.05,{f:600,f2:2400,q:.6,dur:.3,vol:.22,a:.05})},
  fecha(t){chiado(t,{f:2600,f2:600,q:.6,dur:.22,vol:.2,a:.02});tom(t+.18,{f:95,f2:60,dur:.1,vol:.2})},
  postit(t){chiado(t,{tipo:'highpass',f:1500,f2:4500,dur:.12,vol:.12,a:.02});tom(t+.1,{f:700,f2:500,tipo:'triangle',dur:.04,vol:.05})},
  cracha(t){tom(t,{f:2600,tipo:'square',dur:.012,vol:.06});tom(t+.05,{f:3100,tipo:'square',dur:.01,vol:.05});chiado(t,{tipo:'highpass',f:4000,dur:.04,vol:.1})},
  tecla(t){chiado(t,{tipo:'bandpass',f:1800+Math.random()*600,q:2,dur:.03,vol:.3});tom(t,{f:180,f2:90,dur:.04,vol:.15})},
  dado(t){let tt=t,gap=.05;for(let i=0;i<7;i++){const v=.3*(1-i/8);tom(tt,{f:500+Math.random()*500,f2:260,tipo:'triangle',dur:.03,vol:v*.5});chiado(tt,{f:1500+Math.random()*900,q:3,dur:.03,vol:v});tt+=gap*(1+Math.random()*.6);gap*=1.28}}
};

/* ---------------- trilha: ambiente sombrio de investigação ----------------
   drone grave em Lá, acordes lentos em Lá menor harmônico, caixinha de música
   esparsa, chiado de fita e um pulso distante de vez em quando. */
const NOTA=n=>440*Math.pow(2,(n-69)/12);
const ACORDES=[[45,57,60,64,71],[41,53,57,60,64],[38,50,53,57,62],[40,52,56,59,65],[45,57,60,64,67],[46,53,58,62,65]]; // Am(9) F Dm E(b9) Am Bb
const ESCALA=[69,71,72,74,76,77,80,81,83,84]; // Lá menor harmônico, região aguda
function Motor(){
  let vivo=true,timers=[],ia=0,oscDr=[];
  const pad=ctx.createGain();pad.gain.value=.5;
  const lp=ctx.createBiquadFilter();lp.type='lowpass';lp.frequency.value=700;lp.Q.value=.5;
  const lfo=ctx.createOscillator(),lg=ctx.createGain();lfo.frequency.value=.05;lg.gain.value=260;lfo.connect(lg);lg.connect(lp.frequency);lfo.start();
  pad.connect(lp);lp.connect(musBus);lp.connect(verb);
  // drone
  [[33,'sawtooth',.05],[45,'triangle',.07],[45.07,'triangle',.05]].forEach(([n,tp,v])=>{const o=ctx.createOscillator(),g=ctx.createGain(),f=ctx.createBiquadFilter();
    o.type=tp;o.frequency.value=NOTA(n);f.type='lowpass';f.frequency.value=260;g.gain.value=v;o.connect(f);f.connect(g);g.connect(musBus);g.connect(verb);o.start();oscDr.push(o)});
  // chiado de fita
  const hs=ctx.createBufferSource();hs.buffer=ruido;hs.loop=true;const hf=ctx.createBiquadFilter();hf.type='bandpass';hf.frequency.value=5000;hf.Q.value=.4;const hg=ctx.createGain();hg.gain.value=.012;
  hs.connect(hf);hf.connect(hg);hg.connect(musBus);hs.start();oscDr.push(hs);
  const agenda=(fn,ms)=>{const id=setTimeout(()=>{if(vivo)fn()},ms);timers.push(id)};
  function acorde(){
    const t=T()+.05,dur=11,ac=ACORDES[ia++%ACORDES.length];
    ac.forEach((n,i)=>{const o=ctx.createOscillator(),g=ctx.createGain();o.type=i==0?'sine':'triangle';o.frequency.value=NOTA(n);o.detune.value=(Math.random()-.5)*10;
      g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(i==0?.12:.05,t+3.5);g.gain.setValueAtTime(i==0?.12:.05,t+dur-4);g.gain.exponentialRampToValueAtTime(.0001,t+dur);
      o.connect(g);g.connect(pad);o.start(t);o.stop(t+dur+.1)});
    agenda(acorde,(dur-3)*1000)}
  function caixinha(){
    if(Math.random()<.7){const t=T()+.02,n=ESCALA[Math.floor(Math.random()*ESCALA.length)],v=.05+Math.random()*.03;
      [[1,v],[2.76,v*.25],[5.4,v*.08]].forEach(([k,vv])=>{const o=ctx.createOscillator(),g=ctx.createGain();o.frequency.value=NOTA(n)*k;env(g,t,.004,vv,2.4/k+.4);o.connect(g);g.connect(musBus);g.connect(verb);o.start(t);o.stop(t+3)});
      if(Math.random()<.35){const n2=ESCALA[Math.floor(Math.random()*ESCALA.length)],t2=t+.35+Math.random()*.3,o=ctx.createOscillator(),g=ctx.createGain();o.frequency.value=NOTA(n2);env(g,t2,.004,v*.7,2);o.connect(g);g.connect(verb);g.connect(musBus);o.start(t2);o.stop(t2+2.5)}}
    agenda(caixinha,2600+Math.random()*4200)}
  function pulso(){ // batida distante, como um coração ou um passo no andar de cima
    const t=T()+.05;[0,.32].forEach(d=>{const o=ctx.createOscillator(),g=ctx.createGain();o.frequency.setValueAtTime(62,t+d);o.frequency.exponentialRampToValueAtTime(38,t+d+.25);env(g,t+d,.01,d?.08:.12,.35);o.connect(g);g.connect(musBus);g.connect(verb);o.start(t+d);o.stop(t+d+.4)});
    agenda(pulso,18000+Math.random()*24000)}
  acorde();agenda(caixinha,3000);agenda(pulso,9000);
  return{parar(){vivo=false;timers.forEach(clearTimeout);const t=T();oscDr.forEach(o=>{try{o.stop(t+2.6)}catch(e){}});try{lfo.stop(t+2.6)}catch(e){}}}}

function aplicaMus(){
  if(!ctx||!liberado)return;
  const t=T();musBus.gain.cancelScheduledValues(t);musBus.gain.setValueAtTime(musBus.gain.value,t);
  if(st.mus&&!document.hidden){if(!motor)motor=Motor();musBus.gain.linearRampToValueAtTime(.22,t+4)}
  else{musBus.gain.linearRampToValueAtTime(0,t+1.5);if(motor){const m=motor;motor=null;setTimeout(()=>{if(!motor)m.parar()},1800)}}}

function libera(){
  if(liberado||!AC)return;cria();liberado=true;
  if(ctx.state==='suspended')ctx.resume();
  aplicaMus()}
['pointerdown','keydown','touchstart'].forEach(ev=>addEventListener(ev,libera,{once:false,passive:true,capture:true}));
document.addEventListener('visibilitychange',()=>{if(!ctx)return;if(document.hidden){musBus.gain.setTargetAtTime(0,T(),.3);setTimeout(()=>{if(document.hidden&&ctx.state==='running')ctx.suspend()},900)}else{ctx.resume().then(aplicaMus)}});

let ult={};
window.Som={
  fx(nome){if(!st.fx||!AC)return;libera();if(!ctx||!SONS[nome])return;const agora=performance.now();if(ult[nome]&&agora-ult[nome]<45)return;ult[nome]=agora;
    if(ctx.state==='suspended')ctx.resume();try{SONS[nome](T()+.005)}catch(e){}},
  musica(v){st.mus=!!v;LS.set('orpg_musica',st.mus?'1':'0');aplicaMus()},
  efeitos(v){st.fx=!!v;LS.set('orpg_efeitos',st.fx?'1':'0');if(fxBus)fxBus.gain.setTargetAtTime(st.fx?.9:0,T(),.05)},
  volume(v){st.vol=Math.max(0,Math.min(1,+v));LS.set('orpg_volume',st.vol);if(master)master.gain.setTargetAtTime(st.vol,T(),.05)},
  estado:()=>({...st,tocando:!!motor,disponivel:!!AC})
};
})();
