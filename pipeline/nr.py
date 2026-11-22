"""Buracos de reel 24, 26 e 28/11 (pedido do Gui via Growth, 22/11). ESQUELETO NOVO: legenda grande embaixo, selo POV/hora no topo,
barra de progresso; fundo de banco NUNCA usado; só música de banco; fim com CTA + "salva/manda pro grupo". Até 7 palavras por tela.
Uso: python3 nr.py [IDs]"""
import asyncio, subprocess, sys, json, shutil
from pathlib import Path
W = Path(__file__).resolve().parent.parent; N = W / 'n1'; sys.path.insert(0, str(N)); sys.argv = sys.argv[:1] + sys.argv[1:]
import kvx
K = kvx.K; OUT = W / 'gap'; MK = W.parent / 'mk'; BANCO = W
REG = json.loads((W.parent / 'social/pipeline/assets/banco/REGISTRO.json').read_text()); CLIP = {str(c['id']): c for c in REG['clips']}
LOGO = {'rz': K.svg(N / 'rz-logo-g.svg', h=46), 'rzc': K.svg(N / 'rz-logo-c.svg', h=46), 'qd': K.svg(W.parent / 'social/pipeline/assets/quiddo/quiddo-negativo.svg', h=50) if (W.parent / 'social/pipeline/assets/quiddo/quiddo-negativo.svg').exists() else '<b style="font-size:44px">Quiddo</b>',
        'rk': K.svg(K.SD / 'racketdna-logo-fundo-escuro.svg', h=40), 'sf': K.svg(K.SD / 'surfdna-logo-fundo-escuro.svg', h=40)}
COR = {'rz': ('#FFC23C', '#1A0B2E'), 'rzc': ('#FF5C93', '#2A0716'), 'qd': ('#FFC93C', '#0F3B2E'), 'rk': ('#DDF247', '#0A0A0A'), 'sf': ('#6CCFF6', '#0A0A0A')}
T = 11.0; CUTS = [0, 3.0, 6.0, 8.6, T]
CSS = K.FONTS + """*{margin:0;padding:0;box-sizing:border-box}html,body{background:transparent;width:1080px;height:1920px;overflow:hidden;font-family:'DM Sans',sans-serif;color:#fff}
.a{position:absolute}.an{animation-fill-mode:both;animation-play-state:paused}
.cap{font-family:'Bricolage Grotesque',Archivo,sans-serif;font-weight:800;letter-spacing:-.03em;line-height:1.08;text-align:center;color:#fff;text-shadow:0 6px 30px rgba(0,0,0,.65)}
.cap b{padding:0 14px;border-radius:12px}
@keyframes up{0%{opacity:0;transform:translateY(60px) scale(.96)}100%{opacity:1;transform:none}}
@keyframes vis{0%{visibility:visible}100%{visibility:visible}}@keyframes hide{0%{opacity:1}100%{opacity:0;visibility:hidden}}
@keyframes bar{0%{transform:scaleX(0)}100%{transform:scaleX(1)}}@keyframes pop{0%{opacity:0;transform:scale(.7)}100%{opacity:1;transform:none}}"""
an = lambda k, t, d=.45, x='': f'animation:{k} {d}s {t}s both paused{x};'
def seg(t0, t1, inner):
    return f'<div class="a" style="inset:0;{an("pop", t0, .01) if t0 > 0 else ""}"><div class="a" style="inset:0;{an("hide", t1, .01)}">{inner}</div></div>'
def page(spec):
    m = spec['m']; c, ink = COR[m]; b = ''
    b += f'<div class="a" style="left:0;right:0;bottom:0;height:900px;background:linear-gradient(rgba(0,0,0,0),rgba(0,0,0,.72))"></div>'
    if spec.get('lay', 1) != 2: b += f'<div class="a" style="left:60px;right:60px;top:70px;height:8px;border-radius:4px;background:rgba(255,255,255,.3);overflow:hidden"><div style="height:100%;background:{c};transform-origin:left;{an("bar", 0, T, ";animation-timing-function:linear")}"></div></div>'
    if spec.get('lay', 1) == 1: b += f'<div class="a" style="left:60px;top:110px;display:flex;align-items:center;gap:18px"><span style="background:{c};color:{ink};font-family:\'JetBrains Mono\',monospace;font-weight:700;font-size:30px;padding:8px 16px;border-radius:10px">{spec["tag"]}</span></div>'
    lay = spec.get('lay', 1)
    for i, (t, hl) in enumerate(spec['lines']):
        t0, t1 = CUTS[i], CUTS[i + 1]; anim = an("up", t0 + .1, .4) if i else ""
        if lay == 1:
            txt = t.replace('*', f'<b style="background:{c};color:{ink}">', 1).replace('*', '</b>', 1)
            b += seg(t0, t1, f'<div class="a cap" style="left:70px;right:70px;bottom:{360 if i != 1 else 420}px;font-size:{96 if len(t) < 34 else 84}px;{anim}">{txt}</div>')
        elif lay == 2:
            txt = t.replace('*', f'<span style="color:#fff;background:{ink};padding:0 12px;border-radius:10px">', 1).replace('*', '</span>', 1)
            b += seg(t0, t1, f'<div class="a" style="left:60px;right:60px;top:300px;background:{c};color:{ink};border-radius:30px;padding:44px 48px;box-shadow:0 30px 80px rgba(0,0,0,.45);{anim}">'
                     f'<div style="font-family:\'JetBrains Mono\',monospace;font-weight:700;font-size:28px;letter-spacing:.1em;opacity:.75">{i + 1}/3</div>'
                     f'<div style="font-family:\'Bricolage Grotesque\',sans-serif;font-weight:800;font-size:{88 if len(t) < 34 else 76}px;letter-spacing:-.03em;line-height:1.05;margin-top:12px">{txt}</div></div>')
        else:
            txt = t.replace('*', f'<span style="color:{c}">', 1).replace('*', '</span>', 1)
            b += seg(t0, t1, f'<div class="a" style="inset:0;background:rgba(0,0,0,.45)"></div><div class="a cap" style="left:60px;right:60px;top:720px;font-size:{120 if len(t) < 30 else 100}px;{anim}">{txt}</div>')
    e1, e2, e3 = spec['end']
    if lay == 1:
        endbg, etxt, ebtn, ebtc = ink, '#fff', c, ink
    elif lay == 2:
        endbg, etxt, ebtn, ebtc = c, ink, ink, c
    else:
        endbg, etxt, ebtn, ebtc = ink, '#fff', '#fff', ink
    b += seg(CUTS[3], 99, f'<div class="a" style="inset:0;background:{endbg}"></div><div class="a" style="left:80px;top:330px;{"filter:invert(1);" if lay == 2 and m in ("rk","sf","qd") else ""}">{LOGO[m]}</div>'
             f'<div class="a cap" style="left:80px;right:80px;top:{470 if lay != 3 else 700}px;text-align:{"left" if lay != 3 else "center"};font-size:104px;text-shadow:none;color:{etxt};{an("up", CUTS[3], .4)}">{e1}</div>'
             f'<div class="a" style="left:80px;right:80px;top:1180px;height:150px;border-radius:{28 if lay != 3 else 75}px;background:{ebtn};color:{ebtc};display:flex;align-items:center;justify-content:center;font-weight:800;font-size:58px;{an("pop", CUTS[3] + .3, .4)}">{e2}</div>'
             f'<div class="a" style="left:80px;right:80px;top:1380px;text-align:center;font-weight:700;font-size:42px;color:{etxt};{an("up", CUTS[3] + .5, .4)}">{e3}</div>')
    return f'<!doctype html><meta charset="utf-8"><style>{CSS}</style><div class="a" style="inset:0">{b}</div><script>function seek(t){{document.getAnimations().forEach(a=>a.currentTime=t*1000)}}</script>'
def bg(spec, out):
    tmp = OUT / f'tmp-{spec["id"]}'; shutil.rmtree(tmp, ignore_errors=True); tmp.mkdir(); segs = []
    m = spec['m']; ink = COR[m][1]
    for i, (cid, t0) in enumerate(spec['clips'] + [(None, 0)]):
        du = CUTS[i + 1] - CUTS[i]; sg = tmp / f's{i}.mp4'
        if cid:
            c = CLIP[cid]; src = BANCO / c['file']
            vf = ('crop=ih*9/16:ih,' if c['orientation'] == 'horizontal' else '') + "scale=1180:-2,zoompan=z='min(zoom+0.0006,1.08)':d=1:s=1080x1920:fps=30,eq=saturation=1.05"
            subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', str(t0), '-i', str(src), '-t', str(du), '-vf', vf, '-an', '-c:v', 'libx264', '-crf', '17', '-pix_fmt', 'yuv420p', '-r', '30', str(sg)], check=True)
        else:
            subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'lavfi', '-i', f'color=c=0x{ink[1:]}:s=1080x1920:r=30:d={du}', '-c:v', 'libx264', '-crf', '17', '-pix_fmt', 'yuv420p', str(sg)], check=True)
        segs.append(sg)
    (tmp / 'l.txt').write_text(''.join(f"file '{s}'\n" for s in segs))
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', str(tmp / 'l.txt'), '-c:v', 'libx264', '-crf', '17', '-pix_fmt', 'yuv420p', '-r', '30', str(out)], check=True)
    shutil.rmtree(tmp)
SPEC = [
 dict(id='R-R16', lay=1, m='rz', dia='24/11', tag='SEXTA · 23H', clips=[('6704', 2), ('41173', 1), ('36783', 3)], track=('1076', 25),
      lines=[('*214 mensagens* não lidas no grupo.', 1), ('Tudo sobre o *churrasco.*', 1), ('Que ninguém *confirmou.*', 1)],
      end=('Todo grupo tem uma *história.*'.replace('*', ''), 'Faça a do seu grupo →', 'Manda pro grupo que mais fala 📲')),
 dict(id='R-R17', lay=2, m='rzc', dia='26/11', tag='DOMINGO · 22H', clips=[('21292', 0.5), ('23865', 1), ('26555', 4)], track=('801', 40),
      lines=[('Quem manda mais *boa noite?*', 1), ('Ela jura que *é ela.*', 1), ('A conversa diz *outra coisa.*', 1)],
      end=('A retrospectiva de vocês dois.', 'Faça a de vocês →', 'Manda pro seu amor e tira a prova ❤️')),
 dict(id='R-R18', lay=3, m='rz', dia='28/11', tag='DEZEMBRO CHEGANDO', clips=[('5655', 1), ('45462', 2), ('44562', 1)], track=('1005', 30),
      lines=[('Grupo da família: *ativado.*', 1), ('Bom dia da tia *às 6h.*', 1), ('E quem leva *a farofa?*', 1)],
      end=('A retrospectiva do grupo da família.', '1º grupo grátis →', 'Manda no grupo da família 🎄')),
 dict(id='D-R16', lay=1, m='rk', dia='24/11', tag='POV', clips=[('13999', 6), ('23946', 1), ('869', 4)], track=('859', 10),
      lines=[('Você ia comprar *raquete hoje.*', 1), ('Seu amigo: *"qual o peso dela?"*', 1), ('Você não *sabia.*', 1)],
      end=('Antes de comprar, faça o teste.', 'Teste o seu agora →', '🔖 Salva pra quando for comprar')),
 dict(id='D-R17', lay=2, m='sf', dia='26/11', tag='POV', clips=[('1065', 1), ('1042', 3), ('1220', 2)], track=('644', 20),
      lines=[('Primeira prancha, *escolhida pela cor.*', 1), ('No mar, ela *não rema.*', 1), ('Era *litragem*, não cor.', 1)],
      end=('Descubra os seus litros antes.', 'Teste o seu agora →', '🔖 Salva pra quando for comprar')),
 dict(id='D-R18', lay=3, m='rk', dia='28/11', tag='POV', clips=[('880', 2), ('23639', 0.5), ('14057', 1)], track=('1063', 15),
      lines=[('Treina *2x por semana.*', 1), ('Joga com a raquete *do ídolo.*', 1), ('E o golpe *chega atrasado.*', 1)],
      end=('A raquete certa pro seu jogo.', 'Teste o seu agora →', '🔖 Salva pra quando for comprar')),
 dict(id='Q-R15', lay=2, m='qd', dia='26/11', tag='TREINAMENTO · SLIDE 47', clips=[('12892', 0.5), ('49288', 2), ('9069', 1)], track=('830', 10),
      lines=[('Treinamento, *slide 47.*', 1), ('Metade da sala *no celular.*', 1), ('E se o celular *fosse o jogo?*', 1)],
      end=('Quiz no telão, todo mundo responde.', 'Faça o seu. Teste grátis.', 'Manda pra quem organiza o treinamento 📲')),
 dict(id='Q-R16', lay=3, m='qd', dia='28/11', tag='ÚLTIMA AULA', clips=[('24259', 1), ('49155', 3), ('23669', 1)], track=('5', 10),
      lines=[('Última aula *antes das férias.*', 1), ('Ninguém presta *atenção.*', 1), ('Até o quiz *começar.*', 1)],
      end=('A revisão vira jogo no telão.', 'Faça o seu. Teste grátis.', 'Manda pra um professor 🍎')),
]
async def render(b, spec):
    v = spec['id']; d = OUT / v; d.mkdir(exist_ok=True); fr = d / 'fr'; shutil.rmtree(fr, ignore_errors=True); fr.mkdir()
    pg = await b.new_page(viewport={'width': 1080, 'height': 1920}); await pg.set_content(page(spec)); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
    for i in range(int(T * 30)):
        await pg.evaluate(f'seek({i / 30})'); await pg.screenshot(path=str(fr / f'{i:04d}.png'), omit_background=True)
    await pg.close()
    bgp = d / 'bg.mp4'; await asyncio.to_thread(bg, spec, bgp)
    tid, ss = spec['track']
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(bgp), '-framerate', '30', '-i', str(fr / '%04d.png'), '-ss', str(ss), '-i', str(MK / f'{tid}.mp3'),
      '-filter_complex', f'[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v];[2:a]atrim=0:{T},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.3,afade=t=out:st={T - 1.6}:d=1.6,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,aformat=channel_layouts=stereo[a]',
      '-map', '[v]', '-map', '[a]', '-t', str(T), '-c:v', 'libx264', '-crf', '19', '-r', '30', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(d / f'{v}.mp4')], check=True)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', '0.2', '-i', str(d / f'{v}.mp4'), '-frames:v', '1', str(d / f'{v}-capa.png')], check=True)
    shutil.rmtree(fr); print(v, flush=True)
async def main(ids):
    async with K.async_playwright() as p:
        b = await p.chromium.launch(); S = [s for s in SPEC if not ids or s['id'] in ids]
        for i in range(0, len(S), 4): await asyncio.gather(*[render(b, s) for s in S[i:i + 4]])
        await b.close()
if __name__ == '__main__': asyncio.run(main(sys.argv[1:]))
