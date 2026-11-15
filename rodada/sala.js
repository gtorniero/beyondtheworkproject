/* Rodada · conexão com as salas ao vivo (salas.beyondthework.com.br).
   Oferece claude.use('room') com a mesma cara que os jogos já usam:
   room.join(nome) → sala com peers(), onPeers(cb, erro), presence(obj) e leave().
   'db' e 'user' não existem fora do Claude: os jogos caem no modo deste aparelho. */
(function(){
'use strict';
if (window.claude && window.claude.use) return;
var SERVIDOR = (function(){
  /* teste local: ?salas=ws://127.0.0.1:8787 (fica guardado nesta aba) */
  try {
    var q = new URLSearchParams(location.search).get('salas') || sessionStorage.getItem('rz-salas');
    if (q && /^ws:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(q)) { sessionStorage.setItem('rz-salas', q); return q; }
  } catch (e) {}
  return 'wss://salas.beyondthework.com.br';
})();
var HTTP = SERVIDOR.replace(/^ws/, 'http');
function idNovo(){ var a = 'abcdefghijklmnopqrstuvwxyz0123456789', s = ''; try { var b = new Uint8Array(16); crypto.getRandomValues(b); for (var i = 0; i < 16; i++) s += a[b[i] % 36]; } catch (e) { for (var j = 0; j < 16; j++) s += a[Math.floor(Math.random() * 36)]; } return s; }
function meuId(nome){ var k = 'rz-peer:' + nome, v = null; try { v = sessionStorage.getItem(k); } catch (e) {} if (!v || !/^[a-z0-9]{8,24}$/.test(v)) { v = idNovo(); try { sessionStorage.setItem(k, v); } catch (e) {} } return v; }

function join(nome){
  nome = String(nome).toLowerCase();
  var eu = meuId(nome), ws = null, lista = [], cbs = [], errs = [], minha = null, saiu = false, tentativas = 0, timerPing = null, desde = 0;
  var mapa = function(){ return lista.map(function(p){ return { peer: p.peer, kind: 'viewer', presence: p.presence, sameTab: p.peer === eu }; }); };
  var avisa = function(){ var ch = { peers: mapa() }; cbs.forEach(function(f){ try { f(ch); } catch (e) { console.error(e); } }); };
  var falha = function(){ errs.forEach(function(f){ try { f(); } catch (e) {} }); };
  return new Promise(function(ok, nao){
    var primeiro = true;
    function abre(){
      if (saiu) return;
      try { ws = new WebSocket(SERVIDOR + '/sala/' + encodeURIComponent(nome) + '?peer=' + eu); } catch (e) { if (primeiro) { primeiro = false; nao(e); } return; }
      ws.onopen = function(){ tentativas = 0; desde = 0; if (minha) envia(minha); clearInterval(timerPing); timerPing = setInterval(function(){ try { ws.send('{"t":"ping"}'); } catch (e) {} }, 25000); };
      ws.onmessage = function(ev){
        var m; try { m = JSON.parse(ev.data); } catch (e) { return; }
        if (m.t === 'peers' && Array.isArray(m.peers)) {
          lista = m.peers;
          if (primeiro) { primeiro = false; ok(sala); }
          avisa();
        }
      };
      ws.onclose = function(ev){
        clearInterval(timerPing);
        if (saiu || ev.code === 4000) return;
        if (primeiro && tentativas >= 2) { primeiro = false; nao(new Error('sem_conexao')); return; }
        if (!desde) desde = Date.now();
        if (Date.now() - desde > 30000) { falha(); desde = Date.now(); }
        tentativas++;
        setTimeout(abre, Math.min(8000, 500 * Math.pow(2, Math.min(tentativas, 4))));
      };
    }
    function envia(p){ try { if (ws && ws.readyState === 1) ws.send(JSON.stringify({ t: 'presence', p: p })); } catch (e) {} }
    var sala = {
      peers: mapa,
      onPeers: function(cb, err){ if (cb) cbs.push(cb); if (err) errs.push(err); },
      presence: function(p){ minha = p; envia(p); return Promise.resolve(); },
      leave: function(){ saiu = true; clearInterval(timerPing); try { ws && ws.close(1000, 'tchau'); } catch (e) {} return Promise.resolve(); }
    };
    /* voltou do WhatsApp ou destravou a tela: reconecta na hora */
    document.addEventListener('visibilitychange', function(){ if (!saiu && document.visibilityState === 'visible' && ws && ws.readyState > 1) { tentativas = 0; abre(); } });
    abre();
  });
}

var ROOM = { join: join };
window.claude = {
  use: function(n){ return n === 'room' ? Promise.resolve(ROOM) : Promise.reject(new Error('indisponivel')); }
};
/* qual jogo tem uma sala aberta com este código (usado na entrada da Rodada) */
window.RodadaSalas = {
  jogoDoCodigo: function(c){ return fetch(HTTP + '/codigo/' + encodeURIComponent(c)).then(function(r){ return r.json(); }).then(function(j){ return j.jogo || null; }); }
};
})();
