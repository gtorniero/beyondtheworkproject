/* Rodada Ao Vivo · motor comum dos jogos de cartas secretas.
   Dois modos: "cada um no seu celular" (sala com código, via room) e "um celular só" (passa o celular).
   Protocolo: o anfitrião publica o estado da rodada na própria presença; jogadores publicam só o apelido. */
(function(){
'use strict';
var esc=function(t){return String(t==null?'':t).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})};
/* sorteio com crypto (sem viés) quando disponível */
var rand=function(n){try{var c=window.crypto||window.msCrypto,b=new Uint32Array(1),lim=Math.floor(4294967296/n)*n;do{c.getRandomValues(b)}while(b[0]>=lim);return b[0]%n}catch(e){return Math.floor(Math.random()*n)}};
var shuffle=function(a){a=a.slice();for(var i=a.length-1;i>0;i--){var j=rand(i+1);var t=a[i];a[i]=a[j];a[j]=t}return a};
var ALPHA='ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
var newCode=function(){var s='';for(var i=0;i<4;i++)s+=ALPHA[rand(ALPHA.length)];return s};
var store={get:function(k,d){try{var v=localStorage.getItem('rav:'+k);return v==null?d:v}catch(e){return d}},set:function(k,v){try{localStorage.setItem('rav:'+k,v)}catch(e){}}};
var HUB='https://beyondthework.com.br/rodada/',PREF={cidade:'cd',pisca:'pi',infiltrado:'in'};
var mmss=function(ms){var s=Math.max(0,Math.ceil(ms/1000));return Math.floor(s/60)+':'+String(s%60).padStart(2,'0')};

function start(cfg){
  var app=document.getElementById('app');
  var S={screen:'home',mode:'online',n:cfg.def||cfg.min,opts:{},names:'',nick:store.get('nick',''),code:'',joinCode:'',
    isHost:false,rm:null,myPeer:null,peers:[],G:null,passIdx:0,passShown:false,cardOn:false,step:0,dur:(cfg.timer?cfg.timer.def*60000:0),
    err:'',joinErr:'',waitLong:false,hostGone:false,crossed:{}};
  (cfg.opts||[]).forEach(function(o){S.opts[o.id]=o.def});
  S.modo=cfg.modes?cfg.modes[0].id:null;
  try{var hm=location.hash.match(/^#([A-Za-z0-9]{4})$/);if(hm)S.joinCode=hm[1].toUpperCase()}catch(e){}
  var roomNs=null,roomKnown=false,SK='rav:sess:'+cfg.id;
  var sess={get:function(){try{return JSON.parse(sessionStorage.getItem(SK)||'null')}catch(e){return null}},set:function(o){try{sessionStorage.setItem(SK,JSON.stringify(o))}catch(e){}},del:function(){try{sessionStorage.removeItem(SK)}catch(e){}}};
  try{claude.use('room').then(function(r){roomNs=r;roomKnown=true;if(!retoma())render()},function(){roomKnown=true;render()})}catch(e){roomKnown=true}
  var ticker=setInterval(function(){var t=document.getElementById('avTimer');if(t&&S.G&&S.G.t0){var left=S.G.t0+S.G.dur-Date.now();t.textContent=left>0?mmss(left):'Tempo!'}},250);

  function mixHtml(n){
    if(n<cfg.min||n>cfg.max)return '<p class="small">'+esc(cfg.nome)+' é para '+cfg.min+' a '+cfg.max+' pessoas.</p>';
    var r=cfg.setup(n,S.opts).roles,c={};r.forEach(function(k){c[k]=(c[k]||0)+1});
    return '<div class="mix">'+Object.keys(cfg.cards).filter(function(k){return c[k]}).map(function(k){var d=cfg.cards[k];return '<span><i style="background:'+d.c+'">'+c[k]+'</i>'+esc(c[k]>1?(d.plural||d.nome):d.nome)+'</span>'}).join('')+'</div>';
  }
  function cardHtml(role,G,opts,pl){
    opts=opts||{};var d=cfg.card(role,G||{},pl||null);
    return '<div class="rc'+(opts.up?' on':'')+'" '+(opts.tap?'role="button" tabindex="0" aria-label="Sua carta: toque para mostrar ou esconder" id="myCard"':'aria-label="Carta '+esc(d.nome)+'"')+' style="--c:'+d.c+';--cbg:'+d.cbg+';--cink:'+d.cink+'">'+
      '<div class="flip"><div class="side back" aria-hidden="true">'+cfg.backSvg+'</div>'+
      '<div class="side front"><div class="top"><span>'+esc(cfg.cardTop!=null?cfg.cardTop:cfg.nome)+'</span><span>Rodada</span></div><div class="ico" aria-hidden="true">'+d.icon+'</div><div class="nm">'+esc(d.nome)+'</div><div class="ln">'+esc(d.linha)+'</div>'+(d.xt?'<div class="xt">'+esc(d.xt)+'</div>':'')+'</div></div></div>';
  }
  function peopleHtml(list,meId){return '<div class="people">'+list.map(function(p){return '<span class="'+(p.id===meId?'me':'')+(S.G&&S.G.out.indexOf(p.id)>=0?' out':'')+'">'+esc(p.nick)+(p.id===meId?' (você)':'')+'</span>'}).join('')+'</div>'}
  function roleChip(k){var d=cfg.cards[k];return '<span class="role" style="background:'+d.c+'">'+esc(d.nome)+'</span>'}

  /* ---------- telas ---------- */
  function home(){
    var online=S.mode==='online',canRoom=!!roomNs;
    var h='<section class="panel"><div class="tag">Como jogar</div>'+(typeof cfg.rules==='function'?cfg.rules(S.modo):cfg.rules)+'</section>';
    h+='<section class="panel"><div class="tag">Começar uma partida</div>'+
      '<div class="seg" role="group" aria-label="Como vão jogar"><button data-act="mode" data-v="online" aria-pressed="'+online+'">Cada um no seu celular<span>O anfitrião cria a sala; a turma entra com o código.</span></button><button data-act="mode" data-v="pass" aria-pressed="'+(!online)+'">Um celular só<span>Passa de mão em mão; cada um vê a sua carta.</span></button></div>'+
      (cfg.modes?'<div class="tag">Modo de jogo</div><div class="seg" role="group" aria-label="Modo de jogo">'+cfg.modes.map(function(m){return '<button data-act="modo" data-v="'+m.id+'" aria-pressed="'+(S.modo===m.id)+'">'+esc(m.nome)+'<span>'+esc(m.desc)+'</span></button>'}).join('')+'</div>':'')+
      '<div class="tag">Quantas pessoas'+(cfg.hostPlays?'':' (sem contar '+esc(cfg.hostLabel.toLowerCase())+')')+'</div>'+
      '<div class="stepper"><button data-act="n" data-v="-1" aria-label="Menos uma pessoa">−</button><b id="nVal">'+S.n+'</b><button data-act="n" data-v="1" aria-label="Mais uma pessoa">+</button><span class="small">de '+cfg.min+' a '+cfg.max+'</span></div>'+
      mixHtml(S.n)+
      (cfg.optsTitle?'<div class="tag">'+esc(cfg.optsTitle)+'</div>':'')+(cfg.opts||[]).map(function(o){return '<label class="chk"><input type="checkbox" data-act="opt" data-v="'+o.id+'"'+(S.opts[o.id]?' checked':'')+'>'+esc(o.label)+'</label>'}).join('')+
      (cfg.timer?'<div class="tag">Tempo da rodada</div><div class="mix">'+cfg.timer.opts.map(function(m){return '<button class="btn sec" style="width:auto;padding:8px 14px'+(S.dur===m*60000?';border-color:var(--acc)':'')+'" data-act="dur" data-v="'+m+'" aria-pressed="'+(S.dur===m*60000)+'">'+m+' min</button>'}).join('')+'</div>':'');
    if(online){
      h+='<label for="avNick">Seu apelido<input type="text" id="avNick" maxlength="18" value="'+esc(S.nick)+'" placeholder="Como a turma te chama"></label>';
      h+='<button class="btn" data-act="create"'+(canRoom?'':' disabled')+'>Criar sala</button>';
      if(roomKnown&&!canRoom)h+='<p class="small">As salas ao vivo não estão disponíveis nesta visualização. Use "Um celular só".</p>';
    }else{
      h+='<label for="avNames">Nomes, separados por vírgula (opcional)<input type="text" id="avNames" value="'+esc(S.names)+'" placeholder="Ana, Beto, Cris…"></label>';
      h+='<button class="btn" data-act="pass"'+(S.n<cfg.min||S.n>cfg.max?' disabled':'')+'>Começar a distribuir</button>';
      if(!cfg.hostPlays)h+='<p class="small">'+esc(cfg.hostLabel)+' segura o celular e não recebe carta.</p>';
    }
    h+='<p class="err" role="status">'+esc(S.err)+'</p></section>';
    h+='<section class="panel"><div class="tag">Recebeu um código?</div><div class="row"><label for="avCode">Código da sala<input type="text" class="code" id="avCode" maxlength="4" value="'+esc(S.joinCode)+'" placeholder="KX7Q" autocomplete="off"></label><label for="avNick2">Seu apelido<input type="text" id="avNick2" maxlength="18" value="'+esc(S.nick)+'" placeholder="Seu apelido"></label></div><button class="btn sec" data-act="join"'+(canRoom?'':' disabled')+'>Entrar na sala</button><p class="err" role="status">'+esc(S.joinErr)+'</p></section>';
    h+='<section class="panel"><div class="tag">As cartas</div><div class="gallery">'+cfg.gallery().map(function(g){return cardHtml(g[0],g[1],{up:true})}).join('')+'</div></section>';
    return h;
  }
  function modoAtual(){for(var i=0;i<(cfg.modes||[]).length;i++)if(cfg.modes[i].id===S.modo)return cfg.modes[i];return cfg.modes?cfg.modes[0]:null}
  function lobby(){
    var ps=players(),n=ps.length+(cfg.hostPlays?1:0),ok=n>=cfg.min&&n<=cfg.max;
    var inv='Bora jogar '+cfg.nome+' na Rodada? Entra na sala com o código '+S.code+': '+HUB+'#'+(PREF[cfg.id]||'')+S.code;
    var h='<section class="panel" style="text-align:center;justify-items:center"><div class="tag">Sala criada · mande o código para a turma</div><div class="bigcode" aria-label="Código da sala">'+esc(S.code)+'</div><a href="https://wa.me/?text='+encodeURIComponent(inv)+'" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;gap:8px;border-radius:14px;padding:13px 18px;background:#25D366;color:#073B1F;font-weight:800;text-decoration:none;width:100%"><svg width="22" height="22" style="flex:none" viewBox="0 0 32 32" aria-hidden="true"><path fill="#fff" d="M16 3.2C9 3.2 3.3 8.8 3.3 15.7c0 2.3.6 4.5 1.8 6.4L3.2 28.8l6.9-1.8c1.8 1 3.9 1.5 6 1.5 7 0 12.7-5.6 12.7-12.6S23 3.2 16 3.2z"/><path fill="#25D366" d="M16 5.4c5.8 0 10.5 4.6 10.5 10.3S21.8 26.1 16 26.1c-1.9 0-3.7-.5-5.3-1.4l-.4-.2-4 1 1.1-3.9-.3-.4c-1-1.6-1.5-3.5-1.5-5.4C5.6 10 10.3 5.4 16 5.4z"/><path fill="#fff" d="M12.3 10.2c-.2-.5-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.7s1.2 3.2 1.4 3.4c.2.2 2.3 3.6 5.6 4.9 2.8 1.1 3.4.9 4 .8.6-.1 2-.8 2.2-1.6.3-.8.3-1.5.2-1.6-.1-.1-.3-.2-.7-.4l-2.2-1.1c-.3-.1-.5-.2-.8.2l-1 1.2c-.2.2-.4.3-.7.1-.3-.2-1.4-.5-2.7-1.7-1-.9-1.7-2-1.9-2.3-.2-.3 0-.5.1-.7l.5-.6c.2-.2.2-.4.3-.6.1-.2 0-.4 0-.6l-1-2.4z"/></svg>Mandar convite no WhatsApp</a><p class="small">O link já abre o jogo com o código preenchido. Ou a pessoa abre esta página, toca em "Recebeu um código?" e digita '+esc(S.code)+'.</p></section>';
    h+='<section class="panel"><div class="tag">Na sala · '+n+' de '+S.n+(cfg.hostPlays?' (com você)':'')+'</div>'+(ps.length?peopleHtml(ps,null):'<p class="small">Esperando a turma entrar…</p>')+mixHtml(n)+
      '<button class="btn" data-act="deal"'+(ok?'':' disabled')+'>Distribuir as cartas</button>'+(ok?'':'<p class="small">Faltam '+Math.max(0,cfg.min-n)+' para o mínimo de '+cfg.min+'.</p>')+
      '<button class="btn sec" data-act="leave">Cancelar sala</button></section>';
    return h;
  }
  function wait(){
    var hp=hostPeer();
    var h='<section class="panel" style="text-align:center;justify-items:center"><div class="tag">Você está na sala</div><div class="bigcode">'+esc(S.code)+'</div><p class="muted">'+(hp?'Esperando o anfitrião distribuir as cartas.':S.waitLong?'Ninguém abriu a sala '+esc(S.code)+' ainda. Confira o código com o anfitrião.':'Procurando a sala…')+'</p></section>';
    h+='<section class="panel"><div class="tag">Quem já entrou</div>'+peopleHtml(players(),S.myPeer)+'<button class="btn sec" data-act="leave">Sair da sala</button></section>';
    return h;
  }
  function pass(){
    var G=S.G,p=G.pl[S.passIdx];
    if(!S.passShown)return '<section class="panel" style="text-align:center;justify-items:center;padding:32px 18px"><div class="tag">Carta '+(S.passIdx+1)+' de '+G.pl.length+'</div><h2>Passe o celular para '+esc(p.nick)+'</h2><p class="muted">Só '+esc(p.nick)+' pode olhar a próxima tela.</p><button class="btn" data-act="pshow">Sou '+esc(p.nick)+', ver minha carta</button></section>';
    return '<section style="display:grid;gap:12px;--rcoff:178px">'+cardHtml(p.role,G,{up:true},p)+'<p class="hint">Decore e esconda antes de passar.</p><button class="btn" data-act="pnext">'+(S.passIdx<G.pl.length-1?'Esconder e passar':(cfg.hostPlays?'Esconder e começar':'Esconder e devolver para '+esc(cfg.hostLabel.toLowerCase())))+'</button></section>';
  }
  function game(){
    var G=S.G,host=S.isHost||S.mode==='pass',me=myEntry(),h='';
    var win=host&&cfg.vitoria?cfg.vitoria(G):(G.win||null);
    if(win)h+='<div class="win" role="status">'+esc(win)+'</div>';
    if(S.hostGone)h+='<p class="err">O anfitrião saiu da sala.</p>';
    if(me){
      var out=G.out.indexOf(me.id)>=0;
      h+='<section style="display:grid;gap:10px;--rcoff:'+(out?150:120)+'px">'+(out?'<p class="err" style="text-align:center">Você está fora desta rodada. Fique quieto e assista.</p>':'')+cardHtml(me.role,G,{tap:true,up:S.cardOn},me)+'<p class="hint">Toque na carta para '+(S.cardOn?'esconder':'ver')+'.</p></section>';
    }
    if(cfg.timer)h+='<section class="panel" style="justify-items:center"><div class="tag">Tempo</div><div class="timer" id="avTimer">'+(G.t0?mmss(G.t0+G.dur-Date.now()):mmss(G.dur||S.dur))+'</div>'+(host&&!G.t0?'<button class="btn" data-act="timer">Começar o tempo</button>':'')+'</section>';
    if(cfg.extra)h+=cfg.extra(G,me,S.crossed,host);
    if(host){
      if(cfg.steps){h+='<section class="panel"><div class="tag">Roteiro de '+esc(cfg.hostLabel.toLowerCase())+'</div><ol class="script">'+cfg.steps.map(function(s,i){return '<li class="'+(i===S.step?'now':i<S.step?'done':'')+'">'+esc(s[0])+(s[1]?'<small>'+esc(s[1])+'</small>':'')+'</li>'}).join('')+'</ol><div class="row"><button class="btn sec" data-act="step" data-v="-1">Voltar</button><button class="btn" data-act="step" data-v="1">'+(S.step>=cfg.steps.length-1?'Nova noite':'Próximo')+'</button></div></section>'}
      if(cfg.outs!==false){
        h+='<section class="panel"><div class="tag">'+(cfg.hostSeesRoles?'Cartas da mesa · só você vê':'Quem saiu')+'</div><div class="list">'+G.pl.map(function(p){var o=G.out.indexOf(p.id)>=0;return '<div class="'+(o?'out':'')+'"><span class="who">'+esc(p.nick)+(me&&p.id===me.id?' (você)':'')+'</span>'+(cfg.hostSeesRoles?roleChip(p.role):'<span></span>')+'<button data-act="out" data-v="'+esc(p.id)+'">'+(o?'Voltar':'Saiu')+'</button></div>'}).join('')+'</div></section>';
      }
      h+='<section class="panel"><button class="btn" data-act="reveal">Revelar todas as cartas</button><button class="btn sec" data-act="again">Nova rodada, mesmas pessoas</button><button class="btn sec" data-act="end">Encerrar</button></section>';
    }else h+='<p class="small" style="text-align:center">O anfitrião revela as cartas no fim da rodada.</p>';
    return h;
  }
  function rev(){
    var G=S.G,host=S.isHost||S.mode==='pass';
    var h='<section class="panel"><div class="tag">Fim da rodada · as cartas</div>'+(cfg.revealExtra?cfg.revealExtra(G):'')+'<div class="list">'+G.pl.map(function(p){return '<div class="'+(G.out.indexOf(p.id)>=0?'out':'')+'"><span class="who">'+esc(p.nick)+'</span>'+roleChip(p.role)+'<span></span></div>'}).join('')+'</div></section>';
    if(host)h+='<section class="panel"><button class="btn" data-act="again">Nova rodada, mesmas pessoas</button><button class="btn sec" data-act="end">Encerrar</button></section>';
    else h+='<p class="small" style="text-align:center">Esperando o anfitrião começar a próxima.</p>';
    return h;
  }
  function render(){
    var f={home:home,lobby:lobby,wait:wait,pass:pass,game:game,rev:rev}[S.screen]||home;
    document.body.classList.toggle('av-in',S.screen!=='home');var bk=document.querySelector('.back');if(bk){if(S.screen==='home'){bk.textContent='← Todos os jogos da Rodada';bk.removeAttribute('data-av')}else{bk.textContent='← Voltar ao início de '+cfg.nome;bk.setAttribute('data-av','1')}}
    var y=window.scrollY;app.innerHTML=f();if(S.keepScroll)window.scrollTo(0,y);S.keepScroll=false;
  }
  function go(s){S.screen=s;S.cardOn=false;window.scrollTo(0,0);render()}

  /* ---------- sala ---------- */
  function players(){return S.peers.filter(function(p){return p.kind==='viewer'&&p.presence&&p.presence.r==='p'}).map(function(p){return {id:p.peer,nick:String(p.presence.nick||'Jogador').slice(0,18)}})}
  function hostPeer(){for(var i=0;i<S.peers.length;i++){var p=S.peers[i];if(p.presence&&p.presence.r==='h'&&p.presence.g===cfg.id&&!p.sameTab)return p}return null}
  function myEntry(){var G=S.G;if(!G)return null;if(S.mode==='pass')return null;for(var i=0;i<G.pl.length;i++)if(G.pl[i].id===S.myPeer)return G.pl[i];return null}
  function packG(G){return {r:'h',g:cfg.id,ph:G.ph,ep:G.ep,pl:G.pl.map(function(p){return [p.id,p.nick,p.role]}),dt:G.data,out:G.out,t0:G.t0,dur:G.dur,win:cfg.vitoria?cfg.vitoria(G):null}}
  function unpack(hp){return {ph:hp.ph,ep:hp.ep,pl:(hp.pl||[]).map(function(a){return {id:String(a[0]),nick:String(a[1]).slice(0,18),role:String(a[2])}}).filter(function(p){return cfg.cards[p.role]}),data:hp.dt||{},out:Array.isArray(hp.out)?hp.out.map(String):[],t0:+hp.t0||0,dur:+hp.dur||0,win:hp.win?String(hp.win).slice(0,80):null}}
  function sync(){if(S.isHost&&S.rm){var o=S.G?packG(S.G):{r:'h',g:cfg.id,ph:'lobby',ep:0};sess.set({code:S.code,host:true,nick:S.nick,G:S.G,step:S.step,n:S.n,opts:S.opts,dur:S.dur,modo:S.modo,hist:S.hist});S.rm.presence(o).catch(function(){S.err='Não deu para atualizar a sala.';render()})}}
  function onPeers(ch){
    S.peers=ch.peers;
    if(!S.myPeer){for(var i=0;i<ch.peers.length;i++)if(ch.peers[i].sameTab){S.myPeer=ch.peers[i].peer;break}}
    if(!S.isHost){
      var hp=hostPeer();
      if(hp){S.hostGone=false;var P=hp.presence;
        if(P.ph==='jogo'||P.ph==='rev'){var prevEp=S.G&&S.G.ep;S.G=unpack(P);var scr=P.ph==='jogo'?'game':'rev';if(S.screen!==scr||prevEp!==S.G.ep){if(prevEp!==S.G.ep){S.crossed={}}go(scr);return}}
        else if(S.screen!=='wait'){go('wait');return}
      }else if(S.G&&(S.screen==='game'||S.screen==='rev'))S.hostGone=true;
    }
    S.keepScroll=true;render();
  }
  function joinRoom(code,asHost){
    if(!roomNs)return Promise.reject();
    return roomNs.join('rd-'+cfg.id+'-'+code.toLowerCase()).then(function(rm){
      S.rm=rm;S.code=code;S.isHost=asHost;S.peers=rm.peers();
      rm.onPeers(onPeers,function(){S.err='A conexão com a sala caiu.';render()});
      return rm.presence(asHost?{r:'h',g:cfg.id,ph:'lobby',ep:0}:{r:'p',nick:S.nick||'Jogador'});
    });
  }
  /* recarregou a página no meio da partida: volta para a mesma sala, com a mesma identidade */
  function retoma(){
    var o=sess.get();if(!o||!/^[A-Z0-9]{4}$/.test(o.code||''))return false;
    S.nick=o.nick||S.nick;S.mode='online';
    if(o.host){if(o.G)S.G=o.G;S.step=o.step||0;if(o.n)S.n=o.n;if(o.opts)S.opts=o.opts;if(o.dur)S.dur=o.dur;if(o.modo)S.modo=o.modo;if(o.hist)S.hist=o.hist}
    joinRoom(o.code,!!o.host).then(function(){
      if(o.host){var mp=S.rm.peers().filter(function(q){return q.sameTab})[0];if(mp)S.myPeer=mp.peer;sync();enter(S.G?(S.G.ph==='rev'?'rev':'game'):'lobby')}
      else enter('wait');
    },function(){sess.del();render()});
    return true;
  }
  function doHome(){sess.del();var r=S.rm;S.rm=null;S.isHost=false;S.G=null;S.peers=[];S.myPeer=null;if(r)r.leave().catch(function(){});go('home')}
  /* voltar do celular/navegador: dentro do jogo, volta para o início do jogo, não para a Rodada */
  var pushed=false;
  function enter(s){if(S.screen==='home'&&s!=='home'&&!pushed){try{history.pushState({av:1},'');pushed=true}catch(e){}}go(s)}
  function toHome(){if(pushed){pushed=false;try{history.back();return}catch(e){}}doHome()}
  window.addEventListener('popstate',function(){pushed=false;if(S.screen!=='home')doHome()});

  /* Distribui os papéis especiais (infiltrado, assassino, detetive...) para quem teve menos vezes,
     e nunca para quem teve um na rodada anterior, quando dá. Vale para sala e para "um celular só". */
  function distribui(list,roles){
    var cont={};roles.forEach(function(r){cont[r]=(cont[r]||0)+1});
    var comum=Object.keys(cont).sort(function(a,b){return cont[b]-cont[a]})[0];
    if(!S.hist){try{S.hist=JSON.parse(sessionStorage.getItem(HK)||'null')}catch(e){}}
    var H=S.hist;if(!H||typeof H.vezes!=='object'||Array.isArray(H.ultima))H=S.hist={vezes:{},ultima:{}};
    var chave=function(p){return S.mode==='pass'?'n:'+String(p.nick).toLowerCase():'i:'+p.id};
    var out=list.map(function(){return comum}),livre=list.map(function(){return true}),novas={};
    /* cada papel especial, um por vez: ninguém repete o mesmo papel da rodada anterior,
       e quem teve menos vezes aquele papel tem preferência. O resto é sorteio. */
    shuffle(roles.filter(function(r){return r!==comum})).forEach(function(r){
      var cand=shuffle(list.map(function(p,i){return i}).filter(function(i){return livre[i]}));
      cand.sort(function(x,y){var kx=chave(list[x]),ky=chave(list[y]),u=H.ultima[r]||[];
        var rx=u.indexOf(kx)>=0?1:0,ry=u.indexOf(ky)>=0?1:0;
        return (rx-ry)||(((H.vezes[kx]||{})[r]||0)-((H.vezes[ky]||{})[r]||0))});
      var i=cand[0];out[i]=r;livre[i]=false;var k=chave(list[i]);
      H.vezes[k]=H.vezes[k]||{};H.vezes[k][r]=(H.vezes[k][r]||0)+1;(novas[r]=novas[r]||[]).push(k);
    });
    H.ultima=novas;try{sessionStorage.setItem(HK,JSON.stringify(H))}catch(e){}return out;
  }
  function deal(list){
    var n=list.length,su=cfg.setup(n,S.opts,S.modo),roles=distribui(list,su.roles);
    var G={ph:'jogo',ep:(S.G?S.G.ep+1:1)+rand(1000)*1000,pl:list.map(function(p,i){return {id:p.id,nick:p.nick,role:roles[i]}}),data:su.data||{},out:[],t0:0,dur:S.dur};
    if(cfg.modes)G.data.modo=S.modo;if(cfg.afterDeal)cfg.afterDeal(G,S.opts,S.modo);
    S.G=G;S.step=0;S.crossed={};
  }

  /* ---------- ações ---------- */
  app.addEventListener('click',function(e){
    var b=e.target.closest('[data-act]');
    if(!b){var c=e.target.closest('#myCard');if(c){S.cardOn=!S.cardOn;c.classList.toggle('on',S.cardOn);var hn=c.parentNode.querySelector('.hint');if(hn)hn.textContent='Toque na carta para '+(S.cardOn?'esconder':'ver')+'.'}return}
    var a=b.dataset.act,v=b.dataset.v;
    if(a==='opt')return;
    S.err='';
    if(a==='mode'){S.mode=v;render()}
    else if(a==='modo'){S.modo=v;if(cfg.onModo)cfg.onModo(v,S);S.keepScroll=true;render()}
    else if(a==='n'){S.n=Math.max(cfg.min,Math.min(cfg.max,S.n+(+v)));S.keepScroll=true;render()}
    else if(a==='dur'){S.dur=(+v)*60000;S.keepScroll=true;render()}
    else if(a==='create'){
      S.nick=(document.getElementById('avNick').value.trim()||'Anfitrião').slice(0,18);store.set('nick',S.nick);S.mode='online';
      b.disabled=true;var code=newCode();
      joinRoom(code,true).then(function(){sess.set({code:code,host:true,nick:S.nick});enter('lobby')},function(){S.err='Não deu para criar a sala agora. Tente de novo ou use "Um celular só".';render()});
    }
    else if(a==='join'){
      var code=(document.getElementById('avCode').value||'').toUpperCase().replace(/[^A-Z0-9]/g,'');
      S.nick=(document.getElementById('avNick2').value.trim()||'').slice(0,18);
      if(code.length!==4){S.joinErr='O código tem 4 letras ou números.';render();return}
      if(!S.nick){S.joinErr='Escreva seu apelido para a turma saber quem é você.';render();return}
      store.set('nick',S.nick);S.joinErr='';S.mode='online';b.disabled=true;S.waitLong=false;
      joinRoom(code,false).then(function(){sess.set({code:code,host:false,nick:S.nick});enter('wait');setTimeout(function(){if(S.screen==='wait'&&!hostPeer()){S.waitLong=true;render()}},8000)},function(){S.joinErr='Não deu para entrar agora. Tente de novo.';render()});
    }
    else if(a==='leave'||a==='end'){toHome()}
    else if(a==='deal'){
      if(!S.myPeer&&S.rm){var mp=S.rm.peers().filter(function(q){return q.sameTab})[0];if(mp)S.myPeer=mp.peer}
      var list=players();if(cfg.hostPlays)list=[{id:S.myPeer,nick:S.nick||'Anfitrião'}].concat(list);
      if(list.length<cfg.min||list.length>cfg.max)return;
      deal(list);sync();go('game');
    }
    else if(a==='pass'){
      var names=(document.getElementById('avNames').value||'').split(',').map(function(s){return s.trim().slice(0,18)}).filter(Boolean);
      S.names=names.join(', ');
      var list=[];for(var i=0;i<S.n;i++)list.push({id:'p'+i,nick:names[i]||('Jogador '+(i+1))});
      deal(list);S.passIdx=0;S.passShown=false;enter('pass');
    }
    else if(a==='pshow'){S.passShown=true;window.scrollTo(0,0);render()}
    else if(a==='pnext'){S.passShown=false;if(S.passIdx<S.G.pl.length-1){S.passIdx++;go('pass')}else go('game')}
    else if(a==='timer'){S.G.t0=Date.now();S.G.dur=S.G.dur||S.dur;sync();S.keepScroll=true;render()}
    else if(a==='out'){var k=S.G.out.indexOf(v);if(k>=0)S.G.out.splice(k,1);else S.G.out.push(v);sync();S.keepScroll=true;render()}
    else if(a==='step'){var nx=S.step+(+v);if(nx>=cfg.steps.length)nx=0;S.step=Math.max(0,nx);S.keepScroll=true;render()}
    else if(a==='reveal'){S.G.ph='rev';sync();go('rev')}
    else if(a==='again'){
      var list2=S.G.pl.map(function(p){return {id:p.id,nick:p.nick}});
      if(S.mode==='online'){var live=players().map(function(p){return p.id});list2=list2.filter(function(p){return p.id===S.myPeer||live.indexOf(p.id)>=0});players().forEach(function(p){if(!list2.some(function(q){return q.id===p.id}))list2.push(p)})}
      if(list2.length<cfg.min){S.err='Saiu gente: faltam pessoas para outra rodada.';render();return}
      deal(list2);
      if(S.mode==='pass'){S.passIdx=0;S.passShown=false;go('pass')}else{sync();go('game')}
    }
    else if(a==='cross'){S.crossed[v]=!S.crossed[v];b.classList.toggle('x',!!S.crossed[v]);b.setAttribute('aria-pressed',!!S.crossed[v])}
  });
  app.addEventListener('change',function(e){var t=e.target;if(t.dataset&&t.dataset.act==='opt'){S.opts[t.dataset.v]=t.checked;S.keepScroll=true;render()}});
  app.addEventListener('input',function(e){var t=e.target;
    if(t.id==='avNick'||t.id==='avNick2')S.nick=t.value;
    if(t.id==='avNames')S.names=t.value;
    if(t.id==='avCode'){t.value=t.value.toUpperCase().replace(/[^A-Z0-9]/g,'').slice(0,4);S.joinCode=t.value}
  });
  app.addEventListener('keydown',function(e){var c=e.target.closest&&e.target.closest('#myCard');if(c&&(e.key==='Enter'||e.key===' ')){e.preventDefault();c.click()}});
  document.addEventListener('click',function(e){var bk=e.target.closest&&e.target.closest('.back[data-av]');if(bk){e.preventDefault();toHome()}});
  render();
}
window.RodadaAoVivo={start:start,esc:esc,shuffle:shuffle,rand:rand};
})();
