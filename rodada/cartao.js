/* Rodada · card de colocação do dia (1080×1350) para salvar e mandar no WhatsApp.
   RodadaCard.mount(el, dados) desenha a imagem, mostra o botão de WhatsApp e o de copiar o texto. */
(function(){
'use strict';
var esc=function(t){return String(t==null?'':t).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})};
var TEMAS={
  um:{bg:'#FFF7EA',ink:'#1C1530',ink2:'#5F5873',acc:'#E8A317',accTxt:'#8A6100',soft:'#F6EBCB',line:'#EDE3CF'},
  mom:{bg:'#F2FBF6',ink:'#0F2A1E',ink2:'#4E6B5D',acc:'#009C58',accTxt:'#00703F',soft:'#DDF5E8',line:'#CFEBDC'}
};
var D="'Bricolage Grotesque','Figtree',system-ui,sans-serif";
function rr(c,x,y,w,h,r){c.beginPath();c.moveTo(x+r,y);c.arcTo(x+w,y,x+w,y+h,r);c.arcTo(x+w,y+h,x,y+h,r);c.arcTo(x,y+h,x,y,r);c.arcTo(x,y,x+w,y,r);c.closePath()}
function logoUm(c,x,y,s,T){
  c.save();c.font='800 '+s+'px '+D;c.fillStyle=T.ink;c.textBaseline='alphabetic';
  var w=c.measureText('1%').width;
  c.strokeStyle=T.acc;c.lineWidth=s*0.12;c.lineCap='round';c.beginPath();c.arc(x+w*0.5,y-s*0.42+w*0.62,w*0.62,Math.PI*1.25,Math.PI*1.75);c.stroke();
  c.fillText('1%',x,y+s*0.62);c.restore();return w;
}
function logoMom(c,x,y,s,T){
  c.save();var r1=s*0.36,r2=s*0.16;
  c.fillStyle=T.acc;c.beginPath();c.arc(x+r1,y+s*0.5-r1+s*0.2,r1,0,Math.PI*2);c.fill();
  c.strokeStyle=T.acc;c.lineWidth=s*0.07;c.beginPath();c.arc(x+r1*2+s*0.08+r2,y+s*0.5+s*0.2-r2,r2-s*0.035,0,Math.PI*2);c.stroke();
  var tx=x+r1*2+s*0.12+r2*2+s*0.12;
  c.fillStyle=T.ink;c.font='800 '+(s*0.62)+'px '+D;c.fillText('mais',tx,y+s*0.42);
  c.fillStyle=T.ink2;c.font='500 '+(s*0.3)+'px '+D;c.fillText('ou menos',tx,y+s*0.78);
  c.restore();
}
function ring(c,x,y,r,w){[['#E23D77',-80],['#E8A317',40],['#009C58',160]].forEach(function(a){c.strokeStyle=a[0];c.lineWidth=w;c.lineCap='round';c.beginPath();var st=a[1]*Math.PI/180;c.arc(x,y,r,st,st+1.55);c.stroke()})}
function draw(d){
  var T=TEMAS[d.jogo]||TEMAS.um,W=1080,H=1350,cv=document.createElement('canvas');cv.width=W;cv.height=H;var c=cv.getContext('2d');
  c.fillStyle=T.bg;c.fillRect(0,0,W,H);
  c.fillStyle=T.soft;c.beginPath();c.arc(W-60,120,260,0,Math.PI*2);c.fill();
  // topo
  if(d.jogo==='mom')logoMom(c,80,80,150,T);else logoUm(c,80,96,150,T);
  c.textAlign='right';c.fillStyle=T.ink2;c.font='600 34px '+D;c.fillText(d.topo||'',W-80,120);
  if(d.sub){c.fillStyle=T.ink;c.font='800 40px '+D;c.fillText(d.sub,W-80,172)}
  c.textAlign='left';
  // placar
  c.fillStyle=T.ink;c.font='800 300px '+D;var sc=String(d.placar[0]),wsc=c.measureText(sc).width;c.fillText(sc,72,560);
  c.fillStyle=T.ink2;c.font='800 120px '+D;c.fillText('/'+d.placar[1],72+wsc+10,560);
  c.font='500 44px '+D;c.fillStyle=T.ink2;c.fillText(d.detalhe||'',80,630);
  // bolinhas
  var n=d.pips.length,gap=18,pw=Math.min(78,(W-160-gap*(n-1))/n);
  d.pips.forEach(function(ok,i){var cx=80+pw/2+i*(pw+gap),cy=720;c.beginPath();c.arc(cx,cy,pw/2,0,Math.PI*2);if(ok){c.fillStyle=T.acc;c.fill()}else{c.strokeStyle=T.line;c.lineWidth=7;c.stroke()}});
  // caixas de colocação
  var boxes=[d.grupo,d.brasil].filter(Boolean),bw=(W-160-24)/2,by=820,bh=250;
  if(!boxes.length)boxes=[{rot:'Sua sequência',val:(d.sequencia||1)+(d.sequencia===1?' dia':' dias'),nota:'Jogue todo dia para subir'}];
  boxes.forEach(function(b,i){var bx=boxes.length===1?80:80+i*(bw+24),w=boxes.length===1?W-160:bw;
    c.fillStyle='#FFFFFF';rr(c,bx,by,w,bh,36);c.fill();c.strokeStyle=T.line;c.lineWidth=3;rr(c,bx,by,w,bh,36);c.stroke();
    c.fillStyle=T.ink2;c.font='700 30px '+D;c.fillText(String(b.rot).toUpperCase(),bx+40,by+66);
    c.fillStyle=T.accTxt;var vs=96;c.font='800 '+vs+'px '+D;while(vs>48&&c.measureText(String(b.val)).width>w-70){vs-=2;c.font='800 '+vs+'px '+D}c.fillText(b.val,bx+40,by+168);
    if(b.nota){c.fillStyle=T.ink2;var fs=30;c.font='500 '+fs+'px '+D;while(fs>18&&c.measureText(b.nota).width>w-70){fs--;c.font='500 '+fs+'px '+D}c.fillText(b.nota,bx+40,by+218)}
  });
  // rodapé
  c.strokeStyle=T.line;c.lineWidth=3;c.beginPath();c.moveTo(80,1140);c.lineTo(W-80,1140);c.stroke();
  if(d.sequencia&&(d.grupo||d.brasil)){c.fillStyle=T.ink;c.font='700 38px '+D;c.fillText(d.sequencia+(d.sequencia===1?' dia seguido':' dias seguidos'),80,1210)}
  c.fillStyle=T.ink2;c.font='500 34px '+D;c.fillText(d.chamada||'Bora uma rodada?',80,1270);
  ring(c,W-300,1232,24,10);c.fillStyle=T.ink;c.font='800 54px '+D;c.fillText('r',W-350,1250);c.fillText('dada',W-268,1250);
  c.fillStyle=T.ink2;c.font='500 26px '+D;c.textAlign='right';c.fillText(d.site||'beyondthework.com.br/rodada',W-80,1296);c.textAlign='left';
  return cv.toDataURL('image/png');
}
function mount(el,d){
  var go=function(){
    var src;try{src=draw(d)}catch(e){src=null}
    var wa='https://wa.me/?text='+encodeURIComponent(d.texto);
    el.innerHTML='<div class="rcard-share" style="display:grid;gap:12px;justify-items:center">'+
      (src?'<img src="'+src+'" alt="Card do seu resultado de hoje" style="width:100%;max-width:400px;border-radius:20px;box-shadow:0 10px 30px rgba(0,0,0,.12)">':'')+
      '<p style="margin:0;font-size:13px;opacity:.75;text-align:center">No celular, toque e segure a imagem para salvar. No computador, clique com o botão direito.</p>'+
      '<a href="'+esc(wa)+'" target="_blank" rel="noopener" style="display:flex;align-items:center;justify-content:center;gap:10px;width:100%;max-width:400px;border-radius:14px;padding:15px 18px;background:#25D366;color:#073B1F;font:800 16px '+D+';text-decoration:none"><svg width="22" height="22" style="flex:none" viewBox="0 0 32 32" aria-hidden="true"><path fill="#fff" d="M16 3.2C9 3.2 3.3 8.8 3.3 15.7c0 2.3.6 4.5 1.8 6.4L3.2 28.8l6.9-1.8c1.8 1 3.9 1.5 6 1.5 7 0 12.7-5.6 12.7-12.6S23 3.2 16 3.2z"/><path fill="#25D366" d="M16 5.4c5.8 0 10.5 4.6 10.5 10.3S21.8 26.1 16 26.1c-1.9 0-3.7-.5-5.3-1.4l-.4-.2-4 1 1.1-3.9-.3-.4c-1-1.6-1.5-3.5-1.5-5.4C5.6 10 10.3 5.4 16 5.4z"/><path fill="#fff" d="M12.3 10.2c-.2-.5-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.7s1.2 3.2 1.4 3.4c.2.2 2.3 3.6 5.6 4.9 2.8 1.1 3.4.9 4 .8.6-.1 2-.8 2.2-1.6.3-.8.3-1.5.2-1.6-.1-.1-.3-.2-.7-.4l-2.2-1.1c-.3-.1-.5-.2-.8.2l-1 1.2c-.2.2-.4.3-.7.1-.3-.2-1.4-.5-2.7-1.7-1-.9-1.7-2-1.9-2.3-.2-.3 0-.5.1-.7l.5-.6c.2-.2.2-.4.3-.6.1-.2 0-.4 0-.6l-1-2.4z"/></svg>Mandar no WhatsApp</a>'+
      '<button type="button" class="rc-copy" style="width:100%;max-width:400px;border-radius:14px;padding:13px 18px;background:transparent;border:2px solid currentColor;color:inherit;font:700 15px '+D+';cursor:pointer;opacity:.85">Copiar o texto</button>'+
      '<pre class="rc-txt" style="display:none;white-space:pre-wrap;font:500 14px/1.5 ui-monospace,monospace;margin:0;text-align:left;width:100%;max-width:400px">'+esc(d.texto)+'</pre></div>';
    var b=el.querySelector('.rc-copy');b.addEventListener('click',function(){
      var ok=function(){b.textContent='Copiado! Cole no grupo.'};
      var fb=function(){var p=el.querySelector('.rc-txt');p.style.display='block';var r=document.createRange();r.selectNodeContents(p);var s=getSelection();s.removeAllRanges();s.addRange(r);b.textContent='Texto selecionado: copie e cole'};
      try{navigator.clipboard.writeText(d.texto).then(ok,fb)}catch(e){fb()}
    });
  };
  try{Promise.all([document.fonts.load("800 100px 'Bricolage Grotesque'"),document.fonts.load("500 40px 'Bricolage Grotesque'"),document.fonts.load("700 30px 'Bricolage Grotesque'"),document.fonts.load("600 30px 'Bricolage Grotesque'")]).then(go,go)}catch(e){go()}
}
window.RodadaCard={mount:mount,draw:draw};
})();
