var __defProp = Object.defineProperty;
var __name = (target, value) => __defProp(target, "name", { value, configurable: true });

// worker.js
var NOME_SALA = /^rd-[a-z]{3,12}-[a-z0-9]{4}$/;
var PEER = /^[a-z0-9]{8,24}$/;
var JOGOS = ["cidade", "pisca", "infiltrado", "quem"];
var MAX_PESSOAS = 40;
var MAX_PRESENCA = 32 * 1024;
var ORIGENS = ["https://beyondthework.com.br", "https://www.beyondthework.com.br", "https://beyondthework.pages.dev"];
var cors = /* @__PURE__ */ __name((req) => {
  const o = req.headers.get("Origin") || "";
  const ok = ORIGENS.includes(o) || /^https:\/\/[a-z0-9-]+\.beyondthework\.pages\.dev$/.test(o) || /^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(o);
  return ok ? { "Access-Control-Allow-Origin": o, Vary: "Origin" } : {};
}, "cors");
var json = /* @__PURE__ */ __name((req, obj, status = 200) => new Response(JSON.stringify(obj), { status, headers: { "content-type": "application/json", "cache-control": "no-store", ...cors(req) } }), "json");
var worker_default = {
  async fetch(req, env) {
    const url = new URL(req.url);
    const p = url.pathname.split("/").filter(Boolean);
    if (req.method === "OPTIONS") return new Response(null, { headers: { ...cors(req), "Access-Control-Allow-Methods": "GET", "Access-Control-Max-Age": "86400" } });
    if (p[0] === "sala" && p.length === 2) {
      const nome = p[1].toLowerCase();
      if (!NOME_SALA.test(nome)) return json(req, { erro: "sala" }, 400);
      if (req.headers.get("Upgrade") !== "websocket") return json(req, { erro: "websocket" }, 426);
      const o = req.headers.get("Origin") || "";
      if (o && !cors(req)["Access-Control-Allow-Origin"]) return json(req, { erro: "origem" }, 403);
      return env.SALAS.get(env.SALAS.idFromName(nome)).fetch(req);
    }
    if (p[0] === "codigo" && p.length === 2 && /^[A-Za-z0-9]{4}$/.test(p[1])) {
      const c = p[1].toLowerCase();
      const r = await Promise.all(JOGOS.map(async (g) => {
        try {
          const x = await env.SALAS.get(env.SALAS.idFromName(`rd-${g}-${c}`)).fetch("https://sala/info");
          const j = await x.json();
          return j.anfitriao ? g : null;
        } catch {
          return null;
        }
      }));
      return json(req, { jogo: r.find(Boolean) || null });
    }
    if (url.pathname === "/") return json(req, { ok: true, servico: "Rodada \xB7 salas ao vivo" });
    return json(req, { erro: "nao_encontrado" }, 404);
  }
};
var Sala = class {
  static {
    __name(this, "Sala");
  }
  constructor(ctx, env) {
    this.ctx = ctx;
    this.ctx.setWebSocketAutoResponse(new WebSocketRequestResponsePair('{"t":"ping"}', '{"t":"pong"}'));
  }
  async fetch(req) {
    const url = new URL(req.url);
    if (url.pathname === "/info") {
      const anfitriao = this.ctx.getWebSockets().some((ws) => {
        const a = ws.deserializeAttachment();
        return a && a.presence && a.presence.r === "h";
      });
      return new Response(JSON.stringify({ anfitriao }), { headers: { "content-type": "application/json" } });
    }
    const peer = (url.searchParams.get("peer") || "").toLowerCase();
    if (!PEER.test(peer)) return new Response("peer", { status: 400 });
    const abertos = this.ctx.getWebSockets();
    let presenca = null;
    for (const ws of this.ctx.getWebSockets(peer)) {
      const a = ws.deserializeAttachment();
      if (a && a.presence) presenca = a.presence;
      try {
        ws.close(4e3, "substituida");
      } catch {
      }
    }
    if (abertos.length - this.ctx.getWebSockets(peer).length >= MAX_PESSOAS && !presenca) return new Response("cheia", { status: 429 });
    const [cliente, servidor] = Object.values(new WebSocketPair());
    this.ctx.acceptWebSocket(servidor, [peer]);
    servidor.serializeAttachment({ peer, presence: presenca, vivo: true });
    this.envia(servidor, { t: "ola", peer });
    this.espalha();
    return new Response(null, { status: 101, webSocket: cliente });
  }
  lista() {
    const vistos = /* @__PURE__ */ new Map();
    for (const ws of this.ctx.getWebSockets()) {
      const a = ws.deserializeAttachment();
      if (!a || !a.vivo) continue;
      vistos.set(a.peer, { peer: a.peer, presence: a.presence || null });
    }
    return [...vistos.values()];
  }
  envia(ws, msg) {
    try {
      ws.send(JSON.stringify(msg));
    } catch {
    }
  }
  espalha() {
    const msg = JSON.stringify({ t: "peers", peers: this.lista() });
    for (const ws of this.ctx.getWebSockets()) {
      const a = ws.deserializeAttachment();
      if (a && a.vivo) {
        try {
          ws.send(msg);
        } catch {
        }
      }
    }
  }
  async webSocketMessage(ws, data) {
    if (typeof data !== "string" || data.length > MAX_PRESENCA) return;
    let m;
    try {
      m = JSON.parse(data);
    } catch {
      return;
    }
    if (m && m.t === "presence" && m.p && typeof m.p === "object") {
      const a = ws.deserializeAttachment() || {};
      a.presence = m.p;
      a.vivo = true;
      ws.serializeAttachment(a);
      this.espalha();
    }
  }
  async webSocketClose(ws) {
    this.sai(ws);
  }
  async webSocketError(ws) {
    this.sai(ws);
  }
  sai(ws) {
    const a = ws.deserializeAttachment();
    if (a) {
      a.vivo = false;
      try {
        ws.serializeAttachment(a);
      } catch {
      }
    }
    try {
      ws.close(1e3, "tchau");
    } catch {
    }
    this.espalha();
  }
};

// ../../../../../tmp/claude-0/-home-claude/2a0f0e4e-1534-5972-89cf-361ec61c35ee/scratchpad/wr/node_modules/wrangler/templates/middleware/middleware-ensure-req-body-drained.ts
var drainBody = /* @__PURE__ */ __name(async (request, env, _ctx, middlewareCtx) => {
  try {
    return await middlewareCtx.next(request, env);
  } finally {
    try {
      if (request.body !== null && !request.bodyUsed) {
        const reader = request.body.getReader();
        while (!(await reader.read()).done) {
        }
      }
    } catch (e) {
      console.error("Failed to drain the unused request body.", e);
    }
  }
}, "drainBody");
var middleware_ensure_req_body_drained_default = drainBody;

// ../../../../../tmp/claude-0/-home-claude/2a0f0e4e-1534-5972-89cf-361ec61c35ee/scratchpad/wr/node_modules/wrangler/templates/middleware/middleware-miniflare3-json-error.ts
function reduceError(e) {
  return {
    name: e?.name,
    message: e?.message ?? String(e),
    stack: e?.stack,
    cause: e?.cause === void 0 ? void 0 : reduceError(e.cause)
  };
}
__name(reduceError, "reduceError");
var jsonError = /* @__PURE__ */ __name(async (request, env, _ctx, middlewareCtx) => {
  try {
    return await middlewareCtx.next(request, env);
  } catch (e) {
    const error = reduceError(e);
    const body = JSON.stringify(error);
    const headers = {
      "Content-Type": "application/json",
      "MF-Experimental-Error-Stack": "true"
    };
    const encoded = encodeURIComponent(body);
    if (encoded.length <= 8192) {
      headers["MF-Experimental-Error-Stack-Payload"] = encoded;
    }
    return new Response(body, { status: 500, headers });
  }
}, "jsonError");
var middleware_miniflare3_json_error_default = jsonError;

// .wrangler/tmp/bundle-Z5BSo8/middleware-insertion-facade.js
var __INTERNAL_WRANGLER_MIDDLEWARE__ = [
  middleware_ensure_req_body_drained_default,
  middleware_miniflare3_json_error_default
];
var middleware_insertion_facade_default = worker_default;

// ../../../../../tmp/claude-0/-home-claude/2a0f0e4e-1534-5972-89cf-361ec61c35ee/scratchpad/wr/node_modules/wrangler/templates/middleware/common.ts
var __facade_middleware__ = [];
function __facade_register__(...args) {
  __facade_middleware__.push(...args.flat());
}
__name(__facade_register__, "__facade_register__");
function __facade_invokeChain__(request, env, ctx, dispatch, middlewareChain) {
  const [head, ...tail] = middlewareChain;
  const middlewareCtx = {
    dispatch,
    next(newRequest, newEnv) {
      return __facade_invokeChain__(newRequest, newEnv, ctx, dispatch, tail);
    }
  };
  return head(request, env, ctx, middlewareCtx);
}
__name(__facade_invokeChain__, "__facade_invokeChain__");
function __facade_invoke__(request, env, ctx, dispatch, finalMiddleware) {
  return __facade_invokeChain__(request, env, ctx, dispatch, [
    ...__facade_middleware__,
    finalMiddleware
  ]);
}
__name(__facade_invoke__, "__facade_invoke__");

// .wrangler/tmp/bundle-Z5BSo8/middleware-loader.entry.ts
var __Facade_ScheduledController__ = class ___Facade_ScheduledController__ {
  constructor(scheduledTime, cron, noRetry) {
    this.scheduledTime = scheduledTime;
    this.cron = cron;
    this.#noRetry = noRetry;
  }
  scheduledTime;
  cron;
  static {
    __name(this, "__Facade_ScheduledController__");
  }
  #noRetry;
  noRetry() {
    if (!(this instanceof ___Facade_ScheduledController__)) {
      throw new TypeError("Illegal invocation");
    }
    this.#noRetry();
  }
};
function wrapExportedHandler(worker) {
  if (__INTERNAL_WRANGLER_MIDDLEWARE__ === void 0 || __INTERNAL_WRANGLER_MIDDLEWARE__.length === 0) {
    return worker;
  }
  for (const middleware of __INTERNAL_WRANGLER_MIDDLEWARE__) {
    __facade_register__(middleware);
  }
  const fetchDispatcher = /* @__PURE__ */ __name(function(request, env, ctx) {
    if (worker.fetch === void 0) {
      throw new Error("Handler does not export a fetch() function.");
    }
    return worker.fetch(request, env, ctx);
  }, "fetchDispatcher");
  return {
    ...worker,
    fetch(request, env, ctx) {
      const dispatcher = /* @__PURE__ */ __name(function(type, init) {
        if (type === "scheduled" && worker.scheduled !== void 0) {
          const controller = new __Facade_ScheduledController__(
            Date.now(),
            init.cron ?? "",
            () => {
            }
          );
          return worker.scheduled(controller, env, ctx);
        }
      }, "dispatcher");
      return __facade_invoke__(request, env, ctx, dispatcher, fetchDispatcher);
    }
  };
}
__name(wrapExportedHandler, "wrapExportedHandler");
function wrapWorkerEntrypoint(klass) {
  if (__INTERNAL_WRANGLER_MIDDLEWARE__ === void 0 || __INTERNAL_WRANGLER_MIDDLEWARE__.length === 0) {
    return klass;
  }
  for (const middleware of __INTERNAL_WRANGLER_MIDDLEWARE__) {
    __facade_register__(middleware);
  }
  return class extends klass {
    #fetchDispatcher = /* @__PURE__ */ __name((request, env, ctx) => {
      this.env = env;
      this.ctx = ctx;
      if (super.fetch === void 0) {
        throw new Error("Entrypoint class does not define a fetch() function.");
      }
      return super.fetch(request);
    }, "#fetchDispatcher");
    #dispatcher = /* @__PURE__ */ __name((type, init) => {
      if (type === "scheduled" && super.scheduled !== void 0) {
        const controller = new __Facade_ScheduledController__(
          Date.now(),
          init.cron ?? "",
          () => {
          }
        );
        return super.scheduled(controller);
      }
    }, "#dispatcher");
    fetch(request) {
      return __facade_invoke__(
        request,
        this.env,
        this.ctx,
        this.#dispatcher,
        this.#fetchDispatcher
      );
    }
  };
}
__name(wrapWorkerEntrypoint, "wrapWorkerEntrypoint");
var WRAPPED_ENTRY;
if (typeof middleware_insertion_facade_default === "object") {
  WRAPPED_ENTRY = wrapExportedHandler(middleware_insertion_facade_default);
} else if (typeof middleware_insertion_facade_default === "function") {
  WRAPPED_ENTRY = wrapWorkerEntrypoint(middleware_insertion_facade_default);
}
var middleware_loader_entry_default = WRAPPED_ENTRY;
export {
  Sala,
  __INTERNAL_WRANGLER_MIDDLEWARE__,
  middleware_loader_entry_default as default
};
//# sourceMappingURL=worker.js.map
