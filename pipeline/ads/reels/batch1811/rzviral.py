"""18/11 (Gui): Retrozap mais imersivo e viral, grupo e casal, terminando em "Teste o seu grupo" / "Teste o de vocês". 3 look & feel:
A · CONVERSA (o chat estoura na tela, contador dispara, pôster entra)  B · STORIES DE PÔSTERES (pôsteres reais em tela cheia, swipe)
C · PLACAR AO VIVO (grupo vs. Brasil / um contra o outro, cara de transmissão esportiva).
Gancho no quadro 0, até 7 palavras por tela, conversa fictícia (Turma do Churras; Dani & Cris). Uso: python3 rzviral.py [IDs]"""
import asyncio, sys, subprocess, shutil, base64
from pathlib import Path
sys.argv = sys.argv[:1] + sys.argv[1:]
import kvx
K = kvx.K; H = kvx.HERE; OUT = H / 'out'
def b64(p): return 'data:image/jpeg;base64,' + base64.b64encode(Path(p).read_bytes()).decode()
PO = lambda n: b64(H / 'scr' / f'rzp_{n}.jpg')
LOGO = {'g': K.svg(H / 'rz-logo-g.svg', h=54), 'c': K.svg(H / 'rz-logo-c.svg', h=54)}
T = 12.0
CSS = K.FONTS + """*{margin:0;padding:0;box-sizing:border-box}body{width:1080px;height:1920px;overflow:hidden}
.st{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:'DM Sans',sans-serif;color:#fff}
.a{position:absolute}.bg{font-family:'Bricolage Grotesque',Archivo,sans-serif;font-weight:800;letter-spacing:-.035em;line-height:.95}
.an{animation-fill-mode:both;animation-timing-function:cubic-bezier(.2,.8,.2,1);animation-play-state:paused}
@keyframes pop{0%{opacity:0;transform:scale(.6)}70%{opacity:1;transform:scale(1.06)}100%{opacity:1;transform:none}}
@keyframes up{0%{opacity:0;transform:translateY(80px)}100%{opacity:1;transform:none}}
@keyframes out{0%{opacity:1}100%{opacity:0;visibility:hidden}}
@keyframes inR{0%{transform:translateX(1100px) rotate(6deg)}100%{transform:none}}
@keyframes outL{0%{transform:none}100%{transform:translateX(-1150px) rotate(-6deg)}}
@keyframes zoom{0%{transform:scale(1.0)}100%{transform:scale(1.12)}}
@keyframes shake{0%,100%{transform:none}20%{transform:translate(-14px,6px) rotate(-1deg)}40%{transform:translate(12px,-8px) rotate(1deg)}60%{transform:translate(-8px,4px)}80%{transform:translate(6px,-4px)}}
@keyframes bar{0%{transform:scaleX(0)}100%{transform:scaleX(1)}}
@keyframes prog{0%{transform:scaleX(0)}100%{transform:scaleX(1)}}
@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:.25}}
"""
def an(kind, t, d=.5, extra=''):
    return f'animation:{kind} {d}s {t}s both paused{extra};'
def seg(t0, t1, inner, style=''):  # bloco visível só entre t0 e t1
    return f'<div class="a" style="inset:0;{an("pop", t0, .01) if t0 > 0 else ""}{style}"><div class="a" style="inset:0;{an("out", t1, .01)}">{inner}</div></div>'
def counter(t0, t1, a, b, cls, style):  # número que conta (atualizado no seek)
    return f'<span class="cnt {cls}" data-t0="{t0}" data-t1="{t1}" data-a="{a}" data-b="{b}" style="{style}">{a}</span>'
JS = """<script>function fmt(n){return Math.round(n).toLocaleString('pt-BR')}
function seek(t){document.getAnimations().forEach(a=>{a.currentTime=t*1000});
document.querySelectorAll('.cnt').forEach(e=>{const t0=+e.dataset.t0,t1=+e.dataset.t1,a=+e.dataset.a,b=+e.dataset.b;let k=Math.min(1,Math.max(0,(t-t0)/(t1-t0)));k=1-Math.pow(1-k,3);e.textContent=fmt(a+(b-a)*k)})}</script>"""
def page(body, bg): return f'<!doctype html><meta charset="utf-8"><style>{CSS}</style><div class="st" style="background:{bg}">{body}</div>{JS}'
def cta(txt, sub, c, ink, t0, logo):
    return seg(t0, 99, f"""<div class="a" style="inset:0;background:{ink}"></div>
      <div class="a" style="left:80px;top:300px;{an('up', t0, .4)}">{logo}</div>
      <div class="a bg" style="left:80px;top:430px;width:920px;font-size:150px;{an('up', t0 + .05, .45)}">{txt}</div>
      <div class="a" style="left:80px;top:1180px;width:920px;height:170px;border-radius:30px;background:{c};color:{ink};display:flex;align-items:center;justify-content:center;font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:66px;{an('pop', t0 + .35, .45)}">Teste agora →</div>
      <div class="a" style="left:80px;top:1390px;width:920px;text-align:center;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:42px;{an('up', t0 + .5, .4)}">retrozap.com.br</div>
      <div class="a" style="left:80px;top:1470px;width:920px;text-align:center;font-size:36px;color:#ffffffbb;{an('up', t0 + .6, .4)}">{sub}</div>""")

# ---------- A · CONVERSA ----------
def look_a(m):
    g = m == 'g'
    C, INK, BUB, ME = ('#FFC23C', '#120822', '#2A1A45', '#5B2BB5') if g else ('#FF5C93', '#22060F', '#3A1020', '#B3174F')
    hook = 'Abrimos o grupo.<br>Socorro.' if g else 'Abrimos a conversa<br>do casal.'
    msgs = ([('Pedrão', 'bora churras sábado?'), ('Lu', 'kkkkkkkkkk'), ('Pedrão', 'quem leva a carne?'), ('Caio', '👍'), ('Lu', 'MORTA kkkkk'), ('Juninho', 'alguém acordado? 3h'),
             ('Pedrão', 'cês viram isso?'), ('Tati', 'não vai dar hoje 😩'), ('Lu', 'kkkk socorro'), ('Pedrão', 'eu levo o carvão'), ('Bia', '🎤 áudio · 4:12'), ('Rafa', '...')] if g else
            [('Dani', 'bom dia, amor ☀️'), ('Cris', 'bom dia, vida'), ('Dani', 'te amo ❤️'), ('Cris', 'te amo mais'), ('Dani', 'pizza hoje? 🍕'), ('Cris', '🎤 áudio · 2:40'),
             ('Dani', 'chegou bem?'), ('Cris', 'perdão, esqueci'), ('Dani', 'saudade de você 🥺'), ('Cris', 'boa noite, amor'), ('Dani', 'te amo muito 💕'), ('Cris', 'neném 😍')])
    b = f'<div class="a" style="inset:0;background:{INK}"></div>'
    b += seg(0, 4.3, f'<div class="a bg" style="left:70px;top:150px;width:940px;font-size:96px;color:#fff">{hook}</div>')
    y = 470; inner = ''
    for i, (n, t) in enumerate(msgs):
        me = (n == 'Pedrão') if g else (n == 'Dani'); t0 = .15 + i * .33
        inner += (f'<div class="a" style="{"right" if me else "left"}:60px;top:{y}px;max-width:760px;padding:22px 30px;border-radius:30px;background:{ME if me else BUB};{an("pop", t0, .3)}">'
                  f'<div style="font-size:26px;font-weight:700;color:{C}">{n}</div><div style="font-size:44px;font-weight:600">{t}</div></div>')
        y += 120
    b += f'<div class="a" style="inset:0;{an("shake", 3.9, .5)}">{inner}</div>'
    # contador estoura por cima
    num = (10505, 'mensagens no grupo') if g else (17690, 'mensagens do casal')
    b += seg(4.3, 7.4, f'<div class="a" style="inset:0;background:{INK}ee"></div>'
             f'<div class="a bg" style="left:0;right:0;top:640px;text-align:center;font-size:250px;color:{C};{an("pop", 4.3, .4)}">{counter(4.3, 5.6, 0, num[0], "", "")}</div>'
             f'<div class="a bg" style="left:0;right:0;top:920px;text-align:center;font-size:84px;{an("up", 4.5, .4)}">{num[1]}</div>'
             f'<div class="a bg" style="left:0;right:0;top:1060px;text-align:center;font-size:64px;color:#ffffffcc;{an("up", 5.8, .4)}">{"e quem mandou mais?" if g else "e quem ama mais?"}</div>')
    pos = 'grupo-procura-se' if g else 'casal-recibo'
    b += seg(7.4, 9.9, f'<div class="a" style="inset:0;background:{C}"></div>'
             f'<div class="a" style="left:140px;top:260px;width:800px;height:1422px;border-radius:30px;overflow:hidden;box-shadow:0 40px 120px #0008;{an("inR", 7.4, .45)}"><img src="{PO(pos)}" style="width:100%;height:100%"></div>'
             f'<div class="a bg" style="left:0;right:0;top:110px;text-align:center;font-size:86px;color:{INK};{an("up", 7.5, .35)}">{"O fantasma ganhou pôster." if g else "Saiu o recibo do amor."}</div>')
    b += cta('Teste o seu grupo.' if g else 'Teste o de vocês.', '1º grupo grátis · nada sai do seu celular' if g else 'Nada sai do seu celular', C, INK, 9.9, LOGO[m])
    return page(b, INK)

# ---------- B · STORIES DE PÔSTERES ----------
def look_b(m):
    g = m == 'g'
    C, INK = ('#FFC23C', '#120822') if g else ('#FF5C93', '#22060F')
    seq = ([('grupo-procura-se', 'Quem sumiu do grupo?'), ('grupo-radio', 'A gíria oficial do ano'), ('grupo-plantao', 'O grupo virou notícia'), ('grupo-ranking', 'Seu grupo contra o Brasil')] if g else
           [('casal-mapa-astral', 'O mapa astral de vocês'), ('casal-recibo', 'Quem paga o jantar?'), ('casal-boletim', 'Aprovados pra 2027?'), ('casal-ranking', 'Vocês contra o Brasil')])
    n = len(seq); d = 2.3; b = f'<div class="a" style="inset:0;background:{INK}"></div>'
    for i, (p, cap) in enumerate(seq):
        t0, t1 = i * d, (i + 1) * d
        img = (f'<div class="a" style="inset:0;{an("inR", t0, .35) if i else ""}"><div class="a" style="inset:0;{an("outL", t1 - .3, .35) if i < n - 1 else ""}">'
               f'<div class="a" style="left:0;top:380px;width:1080px;height:1540px;overflow:hidden"><div class="a" style="inset:0;{an("zoom", t0, d, ";animation-timing-function:linear;transform-origin:50% 0")}"><img src="{PO(p)}" style="width:1080px;height:1920px"></div></div>'
               f'<div class="a" style="left:0;right:0;top:0;height:380px;background:{INK}"></div>'
               f'<div class="a bg" style="left:60px;top:170px;width:960px;font-size:88px;{an("up", t0 + .25, .35) if i else ""}">{cap}</div></div></div>')
        b += f'<div class="a" style="inset:0;z-index:{i + 1}">{img}</div>'
    bars = ''.join(f'<div style="flex:1;height:8px;border-radius:4px;background:#ffffff55;overflow:hidden"><div style="height:100%;background:#fff;transform-origin:left;{an("prog", i * d, d, ";animation-timing-function:linear")}"></div></div>' for i in range(n))
    b += f'<div class="a" style="left:40px;right:40px;top:60px;display:flex;gap:10px;z-index:20">{bars}</div>'
    b += f'<div class="a" style="left:40px;top:90px;z-index:20;display:flex;align-items:center;gap:16px;font-weight:700;font-size:30px">{LOGO[m]}</div>'
    b += f'<div class="a" style="z-index:30;inset:0">{cta("Teste o seu grupo." if g else "Teste o de vocês.", "1º grupo grátis · nada sai do seu celular" if g else "Nada sai do seu celular", C, INK, n * d, LOGO[m])}</div>'
    return page(b, INK)

# ---------- C · PLACAR AO VIVO ----------
def look_c(m):
    g = m == 'g'
    C, INK, AC = ('#FFD84D', '#0E4D33', '#16613F') if g else ('#FF5C93', '#22060F', '#3A1020')
    b = f'<div class="a" style="inset:0;background:{INK}"></div>'
    b += (f'<div class="a" style="left:60px;top:120px;display:flex;align-items:center;gap:18px;font-family:\'JetBrains Mono\',monospace;font-weight:700;font-size:30px;letter-spacing:.12em">'
          f'<span style="width:22px;height:22px;border-radius:50%;background:#FF3B30;{an("blink", 0, 1, ";animation-iteration-count:12;animation-timing-function:steps(1)")}"></span>AO VIVO · {"GRUPO x BRASIL" if g else "DANI x CRIS"}</div>')
    if g:
        b += f'<div class="a bg" style="left:60px;top:200px;width:960px;font-size:118px">Seu grupo<br>contra o <span style="color:{C}">Brasil.</span></div>'
        rows = [('Risada', 31, 2), ('Madrugada', 40, 7), ('Figurinhas', 15, 5), ('Mensagens', 8, 4)]
        y = 560
        for i, (k, a, top) in enumerate(rows):
            t0 = .6 + i * 1.1
            b += (f'<div class="a" style="left:60px;top:{y}px;width:960px;height:220px;border-radius:28px;background:{AC};{an("up", t0, .35)}">'
                  f'<div class="a" style="left:40px;top:40px;font-size:52px;font-weight:700">{k}</div>'
                  f'<div class="a bg" style="right:40px;top:26px;font-size:120px;color:{C}">Top {counter(t0, t0 + .9, 60, top, "", "")}%</div>'
                  f'<div class="a" style="left:40px;right:40px;bottom:36px;height:14px;border-radius:7px;background:#ffffff22"><div style="height:100%;border-radius:7px;background:{C};transform-origin:left;width:{100 - top}%;{an("bar", t0, .9)}"></div></div></div>')
            y += 250
        b += seg(5.6, 9.8, f'<div class="a" style="inset:0;background:{C}"></div>'
                 f'<div class="a bg" style="left:0;right:0;top:330px;text-align:center;font-size:110px;color:{INK};{an("pop", 5.6, .4)}">PÓDIO DO<br>BRASIL</div>'
                 f'<div class="a" style="left:190px;top:620px;width:700px;height:1244px;border-radius:30px;overflow:hidden;box-shadow:0 40px 120px #0006;{an("up", 6.0, .5)}"><img src="{PO("grupo-ranking")}" style="width:100%;height:100%"></div>')
    else:
        b += f'<div class="a bg" style="left:60px;top:200px;width:960px;font-size:118px">Quem ama<br><span style="color:{C}">mais?</span></div>'
        rows = [('Mensagens', 9982, 7708), ('"Te amo"', 830, 295), ('Boa noite', 387, 300), ('Puxou o papo', 541, 85)]
        y = 560
        for i, (k, a, c2) in enumerate(rows):
            t0 = .6 + i * 1.1; tot = a + c2
            b += (f'<div class="a" style="left:60px;top:{y}px;width:960px;height:220px;border-radius:28px;background:{AC};{an("up", t0, .35)}">'
                  f'<div class="a" style="left:0;right:0;top:26px;text-align:center;font-size:40px;font-weight:700;color:#ffffffcc">{k}</div>'
                  f'<div class="a bg" style="left:40px;top:70px;font-size:96px;color:{C}">{counter(t0, t0 + .9, 0, a, "", "")}</div>'
                  f'<div class="a bg" style="right:40px;top:70px;font-size:96px">{counter(t0, t0 + .9, 0, c2, "", "")}</div>'
                  f'<div class="a" style="left:40px;right:40px;bottom:30px;height:14px;border-radius:7px;background:#ffffff33;overflow:hidden"><div style="height:100%;background:{C};transform-origin:left;width:{a / tot * 100:.0f}%;{an("bar", t0, .9)}"></div></div></div>')
            y += 250
        b += (f'<div class="a bg" style="left:60px;top:500px;font-size:44px;color:{C}">DANI</div><div class="a bg" style="right:60px;top:500px;font-size:44px">CRIS</div>')
        b += seg(5.6, 9.8, f'<div class="a" style="inset:0;background:{C}"></div>'
                 f'<div class="a bg" style="left:0;right:0;top:330px;text-align:center;font-size:150px;color:{INK};{an("pop", 5.6, .4)}">5 x 0</div>'
                 f'<div class="a" style="left:190px;top:560px;width:700px;height:1244px;border-radius:30px;overflow:hidden;box-shadow:0 40px 120px #0006;{an("up", 6.0, .5)}"><img src="{PO("casal-placar")}" style="width:100%;height:100%"></div>')
    b += cta('Teste o seu grupo.' if g else 'Teste o de vocês.', '1º grupo grátis · só os números saem do celular' if g else 'Nada sai do seu celular', C, INK, 9.8, LOGO[m])
    return page(b, INK)

SPEC = {'ADC-RZ-27-v1': (look_a, 'g'), 'ADC-RZ-28-v1': (look_a, 'c'), 'ADC-RZ-29-v1': (look_b, 'g'), 'ADC-RZ-30-v1': (look_b, 'c'),
        'ADC-RZ-31-v1': (look_c, 'g'), 'ADC-RZ-32-v1': (look_c, 'c')}

async def render(b, v):
    f, m = SPEC[v]; html = f(m); d = OUT / v; d.mkdir(parents=True, exist_ok=True); fr = d / '_fr'; fr.mkdir(exist_ok=True)
    pg = await b.new_page(viewport={'width': 1080, 'height': 1920}); await pg.set_content(html); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
    for i in range(int(T * 30)):
        await pg.evaluate(f'seek({i / 30})'); await pg.screenshot(path=str(fr / f'{i:05d}.jpg'), type='jpeg', quality=90)
    for t, nm in ((0, 'hook'), (5.2, 'meio'), (8.6, 'poster'), (11.5, 'fim')):
        await pg.evaluate(f'seek({t})'); await pg.screenshot(path=str(d / f'{v}-{nm}.png'))
    await pg.close()
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-framerate', '30', '-i', str(fr / '%05d.jpg'), '-an', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '19', '-movflags', '+faststart', str(d / f'{v}-motion-story.mp4')], check=True)
    shutil.rmtree(fr); print(v, flush=True)

async def stills(b, v):
    f, m = SPEC[v]; d = OUT / v; d.mkdir(parents=True, exist_ok=True)
    pg = await b.new_page(viewport={'width': 1080, 'height': 1920}); await pg.set_content(f(m)); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
    for t, nm in ((0, 'hook'), (5.2, 'meio'), (8.6, 'poster'), (11.5, 'fim')):
        await pg.evaluate(f'seek({t})'); await pg.screenshot(path=str(d / f'{v}-{nm}.png'))
    await pg.close()

if __name__ == '__main__':
    mode = sys.argv[1]; ids = sys.argv[2:] or list(SPEC)
    async def go():
        async with K.async_playwright() as p:
            b = await p.chromium.launch()
            await asyncio.gather(*[(render if mode == 'motion' else stills)(b, v) for v in ids])
            await b.close()
    asyncio.run(go())
