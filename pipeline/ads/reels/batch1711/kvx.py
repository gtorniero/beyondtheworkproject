"""Batch performance 17/11 · KV no look do ADC-RK-05 (o "pica" do Gui) para RACKET, SURF e RETROZAP.
Usa o motor de layout do kv_dna.py (pipeline/ads/reels) e acrescenta: temas por marca, layout genérico 4:5 e textos do brief.
Uso: python3 kvx.py <hero|adapt|motion> [IDs]   → out/<ID>/"""
import asyncio, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str((HERE / '../../social/pipeline/ads/reels').resolve()))
import kv_dna as K
from estudio import ff

K.SCR = HERE / 'scr'
K.FONTS += ff('Bricolage Grotesque', 'Bricolage-800.woff2', '800')
K.SP.update({
    'racket': dict(K.SP['racket'], cta='Fazer o teste'),
    'surf': dict(K.SP['surf'], cta='Fazer o teste'),
    'rzg': dict(c='#FFC23C', logo=str(HERE / 'rz-logo-g.svg'), cta='Fazer a do meu grupo', url='retrozap.com.br', fine='1º grupo grátis · sem cadastro.'),
    'rzc': dict(c='#FF5C93', logo=str(HERE / 'rz-logo-c.svg'), cta='Fazer a de vocês', url='retrozap.com.br', fine='Pagamento único · Pix ou cartão.'),
})
THEME = {'racket': ('#0A0A0A', '#0E4D64'), 'surf': ('#0A0A0A', '#0E4D64'), 'rzg': ('#1A0B2E', '#6B2FD6'), 'rzc': ('#2A0716', '#8A1240')}
RZCSS = "<style>.hd{font-family:'Bricolage Grotesque',Archivo,sans-serif!important;letter-spacing:-.03em!important}.num{font-family:'Bricolage Grotesque',Syne,sans-serif!important;letter-spacing:-.04em!important}.ph .scr{background:#1A0B2E}</style>"
RS = K.RS

PH = K.PH
SPEC = {
 # RACKET · didático
 'ADC-RK-11-v1': dict(sp='racket', title='Qual raquete é *a certa* pra você?', kick='Teste Racket DNA', ph=PH('racket_res.jpg'),
                      nums=[('3', 'raquetes do seu jogo, cada uma com o seu DNA Score'), ('183', 'raquetes medidas, cruzadas com o seu corpo, o seu braço e o seu jogo')],
                      post='Responda as perguntas e veja a prévia grátis.'),
 'ADC-RK-12-v1': dict(sp='racket', title='Antes de comprar raquete na Black Friday, *faça o teste.*', kick='Black Friday', ph=PH('racket_card.jpg'),
                      nums=[(RS + '19,99', 'relatório completo, pagamento único'), ('183', 'raquetes medidas, cruzadas com o seu jogo')],
                      post='Você vê a prévia grátis e só paga se quiser o relatório.'),
 # SURF (board) · didático
 'ADC-SF-11-v1': dict(sp='surf', title='Qual prancha é *a certa* pra você?', kick='Teste Surf DNA', ph=PH('surf_res.jpg'),
                      nums=[('3 min', 'para contar seu corpo, seu surf e o seu mar'), ('13', 'tipos de prancha disputam o seu resultado')],
                      post='Sai com medidas e litragem prontas para a loja ou o shaper.'),
 'ADC-SF-12-v1': dict(sp='surf', title='Antes de comprar prancha na Black Friday, *faça o teste.*', kick='Black Friday', ph=PH('surf_litros.jpg'),
                      nums=[(RS + '19,99', 'relatório completo. Uma prancha nova sai por R$ 1.500 a R$ 4.000.'), ('17', 'medidas na ficha técnica, prontas para qualquer shaper')],
                      post='Prévia grátis · 3 minutos · sem cadastro.'),
 # RETROZAP · literal
 'ADC-RZ-16-v1': dict(sp='rzg', title='Retrospectiva do seu WhatsApp em *3 passos.*', kick='Como funciona', ph=PH('g_podio.jpg'),
                      steps=[('1', 'Exporte a conversa do grupo no WhatsApp'), ('2', 'Escolha o arquivo no site'), ('3', 'Veja os troféus de cada um')],
                      post='Nada sai do seu celular.'),
 'ADC-RZ-17-v1': dict(sp='rzg', title='Retrospectiva do seu grupo do WhatsApp. *O que vem nela:*', kick='O que vem', ph=PH('g_tagarela.jpg'),
                      nums=[('8', 'troféus em disputa. Quem fala mais leva O Tagarela.'), ('Top 3', 'destaques do ano, com o número de cada um')],
                      chips=('Mensagens do ano', 'Quem fala mais', 'Troféus', 'Vídeo do grupo*'),
                      post='Nada sai do seu celular. *Vídeo no Premium.'),
 'ADC-RZ-18-v1': dict(sp='rzc', title='Retrospectiva do seu *namoro* no WhatsApp.', kick='Retrozap Casais', ph=PH('c_msgs.jpg'),
                      nums=[(RS + '13,99', 'pagamento único, no Pix ou no cartão'), ('8', 'troféus do casal: quem manda mais mensagem, quem é mais romântico')],
                      post='Nada sai do seu celular.'),
}
ROT = (-10, 4, 2.5)


def steps(items, x, y, w, size=120, ls=30, gap=40):
    out = ''
    for n, t in items:
        tt = K.t_num(K.CTX['ni']); K.CTX['ni'] += 1
        out += (f'<div class="abs" style="left:{x}px;top:{y}px;width:{w}px;display:flex;align-items:center;gap:26px;{K.A_("rise", tt)}">'
                f'<div class="num" style="font-size:{size}px;min-width:{size * .7:.0f}px">{n}</div><div class="lab" style="font-size:{ls}px">{t}</div></div>')
        y += size + gap
    return out


def body(s, fmt):
    """Corpo genérico: celular à direita, números/passos à esquerda."""
    ph = s['ph']
    L = {  # phone w,x,y · coluna x,y,w · tamanhos
        'feed45': dict(pw=420, px=610, py=380, cx=64, cy=430, cw=520, n1=190, n2=118, ls=28, st=118, sls=31, post=28, chip=24),
        'sq': dict(pw=330, px=694, py=318, cx=56, cy=345, cw=590, n1=150, n2=104, ls=24, st=92, sls=26, post=24, chip=21),
        'story': dict(pw=400, px=640, py=660, cx=64, cy=690, cw=540, n1=200, n2=136, ls=30, st=130, sls=33, post=30, chip=24),
        '16x9': dict(pw=440, px=1380, py=112, cx=90, cy=470, cw=1150, n1=190, n2=150, ls=27, st=110, sls=30, post=29, chip=24),
        'land': dict(pw=236, px=920, py=52, cx=40, cy=268, cw=700, n1=120, n2=0, ls=21, st=0, sls=0, post=0, chip=0),
    }[fmt]
    b = K.phone(ph['src'], L['pw'], L['px'], L['py'], ROT, ph['zoom'], .5, ph['fy'])
    x, y, w = L['cx'], L['cy'], L['cw']
    if fmt == 'land':
        n = s['nums'][0] if 'nums' in s else (s['steps'][2][0], s['steps'][2][1])
        if 'steps' in s: return b + steps(s['steps'][:3], x, y - 60, w, 64, 20, 10)
        return b + K.num(n[0], n[1], x, y, w, L['n1'], L['ls'])
    if fmt == '16x9':
        if 'steps' in s: b += steps(s['steps'], x, 400, w, 96, L['sls'], 24)
        else:
            for i, n in enumerate(s['nums'][:2]): b += K.num(n[0], n[1], x + i * 600, y, 540, L['n1'], L['ls'])
        if s.get('post'): b += K.sub(s['post'], x, 790, w, L['post'])
        return b
    if 'steps' in s:
        b += steps(s['steps'], x, y, w, L['st'], L['sls'], 34 if fmt != 'sq' else 22)
        y += len(s['steps']) * (L['st'] + (34 if fmt != 'sq' else 22)) + 10
    else:
        for i, n in enumerate(s['nums'][:2]):
            size = L['n1'] if i == 0 else L['n2']
            b += K.num(n[0], n[1], x, y, w, size, L['ls'])
            y += size * .88 + L['ls'] * 2.6 + (60 if fmt != 'sq' else 34)
            if i == 0: b += K.rule(x, y - 30, w - 40)
    if s.get('chips') and fmt in ('feed45', '16x9'): b += K.chips(s['chips'], x, y - 20, w, L['chip']); y += 95
    if s.get('post'): b += K.sub(s['post'], x, y, w, L['post'])
    return b


G = {
    'feed45': (K.G45, dict(tsize=96, ty=150, tw=960, maxh=230)),
    'sq': (dict(pad=56, logo_y=46, logo_h=44, kick_y=60, kick=19, cta_b=46, cta=30, cta_p=(16, 26), url=20, fine=18, blob=(260, 640, 560, 700)), dict(tsize=80, ty=112, tw=968, maxh=180)),
    'story': (dict(pad=64, logo_y=270, logo_h=52, kick_y=286, kick=22, cta_b=380, cta=40, cta_p=(24, 36), url=25, fine=23, blob=(700, 860, 1150, 900)), dict(tsize=108, ty=360, tw=952, maxh=360)),
    'land': (dict(pad=40, logo_y=32, logo_h=34, kick_y=0, kick=0, cta_b=32, cta=23, cta_p=(12, 20), url=16, fine=15, blob=(120, 460, 300, 500)), dict(tsize=54, ty=84, tw=800, maxh=118)),
    '16x9': (dict(pad=90, logo_y=70, logo_h=56, kick_y=88, kick=22, cta_b=80, cta=38, cta_p=(22, 34), url=25, fine=23, blob=(200, 860, 500, 900)), dict(tsize=96, ty=170, tw=1180, maxh=230)),
}


def page(v, fmt, anim=False):
    K.CTX['anim'] = anim; K.CTX['ni'] = 0
    s = SPEC[v]; K.INK, K.PETROL = THEME[s['sp']]
    g, t = G[fmt]; W, H = K.FMT[fmt]
    html = K.frame(s['sp'], body(s, fmt), s['title'], t['tsize'], ty=t['ty'], tw=t['tw'], kick=s['kick'], W=W, H=H, g=g, maxh=t['maxh'])
    if s['sp'].startswith('rz'): html = html.replace('</style>', '</style>' + RZCSS, 1)
    if anim:  # gancho no quadro 0: título, logo e kicker já na tela
        import re as _re
        html = _re.sub(r'(class="abs hd"[^>]*?style="[^"]*?)animation:rise[^;]*;', r'\1', html)
        html = html.replace(K.A_('fade', 0, .6), '')
        html = html.replace('class="cv" data-to', 'class="cvx" data-to') if False else _re.sub(r'<span class="cv"([^>]*data-dec="2")', r'<span class="price"\1', html)  # preço nunca conta: aparece já certo
    return html


K.page = page
K.HERO = {v: None for v in SPEC}

if __name__ == '__main__':
    mode = sys.argv[1]; ids = sys.argv[2:] or list(SPEC)
    out = HERE / 'out'; out.mkdir(exist_ok=True)
    if mode == 'hero':  # todos os estáticos de uma vez
        async def go():
            async with K.async_playwright() as p:
                b = await p.chromium.launch(); pg = await b.new_page()
                for v in ids:
                    d = out / v; d.mkdir(parents=True, exist_ok=True)
                    for f in ('sq', 'story', 'feed45', 'land', '16x9'):
                        W, H = K.FMT[f]; await K.shot(pg, page(v, f), d / f'{v}-{f}.png', W, H)
                    print(v, flush=True)
                await b.close()
        asyncio.run(go())
    else:
        asyncio.run(K.main('motion', ids, out))
