// Só para o navegador aceitar "instalar". Não guarda nada: tudo vem da rede, então nunca fica versão velha.
self.addEventListener('install',()=>self.skipWaiting());
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('fetch',()=>{});
