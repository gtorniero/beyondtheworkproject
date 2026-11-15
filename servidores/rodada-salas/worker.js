// Rodada · servidor das salas ao vivo (salas.beyondthework.com.br).
// Cada sala é um Durable Object que guarda quem está conectado e a "presença" de cada um
// (o anfitrião publica o estado da partida; os jogadores publicam o apelido e o resultado).
// A cada mudança, todo mundo recebe a lista completa. Nada é gravado em banco: a sala some quando esvazia.

const NOME_SALA = /^rd-[a-z]{3,12}-[a-z0-9]{4}$/;
const PEER = /^[a-z0-9]{8,24}$/;
const JOGOS = ['cidade', 'pisca', 'infiltrado', 'quem'];
const MAX_PESSOAS = 40;
const MAX_PRESENCA = 32 * 1024;
const ORIGENS = ['https://beyondthework.com.br', 'https://www.beyondthework.com.br', 'https://beyondthework.pages.dev'];

const cors = (req) => {
  const o = req.headers.get('Origin') || '';
  const ok = ORIGENS.includes(o) || /^https:\/\/[a-z0-9-]+\.beyondthework\.pages\.dev$/.test(o) || /^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(o);
  return ok ? { 'Access-Control-Allow-Origin': o, Vary: 'Origin' } : {};
};
const json = (req, obj, status = 200) => new Response(JSON.stringify(obj), { status, headers: { 'content-type': 'application/json', 'cache-control': 'no-store', ...cors(req) } });

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    const p = url.pathname.split('/').filter(Boolean);
    if (req.method === 'OPTIONS') return new Response(null, { headers: { ...cors(req), 'Access-Control-Allow-Methods': 'GET', 'Access-Control-Max-Age': '86400' } });
    // GET /sala/<nome>?peer=<id>  (WebSocket)
    if (p[0] === 'sala' && p.length === 2) {
      const nome = p[1].toLowerCase();
      if (!NOME_SALA.test(nome)) return json(req, { erro: 'sala' }, 400);
      if (req.headers.get('Upgrade') !== 'websocket') return json(req, { erro: 'websocket' }, 426);
      const o = req.headers.get('Origin') || '';
      if (o && !cors(req)['Access-Control-Allow-Origin']) return json(req, { erro: 'origem' }, 403);
      return env.SALAS.get(env.SALAS.idFromName(nome)).fetch(req);
    }
    // GET /codigo/<CODIGO> → em qual jogo há uma sala aberta com esse código
    if (p[0] === 'codigo' && p.length === 2 && /^[A-Za-z0-9]{4}$/.test(p[1])) {
      const c = p[1].toLowerCase();
      const r = await Promise.all(JOGOS.map(async (g) => {
        try { const x = await env.SALAS.get(env.SALAS.idFromName(`rd-${g}-${c}`)).fetch('https://sala/info'); const j = await x.json(); return j.anfitriao ? g : null; } catch { return null; }
      }));
      return json(req, { jogo: r.find(Boolean) || null });
    }
    if (url.pathname === '/') return json(req, { ok: true, servico: 'Rodada · salas ao vivo' });
    return json(req, { erro: 'nao_encontrado' }, 404);
  },
};

export class Sala {
  constructor(ctx, env) {
    this.ctx = ctx;
    // responde ao "ping" do celular sem acordar a sala
    this.ctx.setWebSocketAutoResponse(new WebSocketRequestResponsePair('{"t":"ping"}', '{"t":"pong"}'));
  }

  async fetch(req) {
    const url = new URL(req.url);
    if (url.pathname === '/info') {
      const anfitriao = this.ctx.getWebSockets().some((ws) => { const a = ws.deserializeAttachment(); return a && a.presence && a.presence.r === 'h'; });
      return new Response(JSON.stringify({ anfitriao }), { headers: { 'content-type': 'application/json' } });
    }
    const peer = (url.searchParams.get('peer') || '').toLowerCase();
    if (!PEER.test(peer)) return new Response('peer', { status: 400 });
    const abertos = this.ctx.getWebSockets();
    // mesma pessoa reconectando: fecha a conexão antiga e guarda a presença dela
    let presenca = null;
    for (const ws of this.ctx.getWebSockets(peer)) { const a = ws.deserializeAttachment(); if (a && a.presence) presenca = a.presence; try { ws.close(4000, 'substituida'); } catch {} }
    if (abertos.length - this.ctx.getWebSockets(peer).length >= MAX_PESSOAS && !presenca) return new Response('cheia', { status: 429 });
    const [cliente, servidor] = Object.values(new WebSocketPair());
    this.ctx.acceptWebSocket(servidor, [peer]);
    servidor.serializeAttachment({ peer, presence: presenca, vivo: true });
    this.envia(servidor, { t: 'ola', peer });
    this.espalha();
    return new Response(null, { status: 101, webSocket: cliente });
  }

  lista() {
    const vistos = new Map();
    for (const ws of this.ctx.getWebSockets()) {
      const a = ws.deserializeAttachment();
      if (!a || !a.vivo) continue;
      vistos.set(a.peer, { peer: a.peer, presence: a.presence || null });
    }
    return [...vistos.values()];
  }

  envia(ws, msg) { try { ws.send(JSON.stringify(msg)); } catch {} }

  espalha() {
    const msg = JSON.stringify({ t: 'peers', peers: this.lista() });
    for (const ws of this.ctx.getWebSockets()) { const a = ws.deserializeAttachment(); if (a && a.vivo) { try { ws.send(msg); } catch {} } }
  }

  async webSocketMessage(ws, data) {
    if (typeof data !== 'string' || data.length > MAX_PRESENCA) return;
    let m; try { m = JSON.parse(data); } catch { return; }
    if (m && m.t === 'presence' && m.p && typeof m.p === 'object') {
      const a = ws.deserializeAttachment() || {};
      a.presence = m.p; a.vivo = true;
      ws.serializeAttachment(a);
      this.espalha();
    }
  }

  async webSocketClose(ws) { this.sai(ws); }
  async webSocketError(ws) { this.sai(ws); }
  sai(ws) {
    const a = ws.deserializeAttachment();
    if (a) { a.vivo = false; try { ws.serializeAttachment(a); } catch {} }
    try { ws.close(1000, 'tchau'); } catch {}
    this.espalha();
  }
}
