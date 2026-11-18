"""Lote 18/11 · Retrozap com os PÔSTERES reais do app (mapa astral, recibo do amor, boletim, ranking Top Brasil, procura-se, plantão, rádio).
Mesmo motor/visual do RK-05 (kvx/kv_dna); no lugar do celular entra o pôster 9:16 inclinado (e um segundo atrás, quando há).
Uso: python3 kvrz.py hero [IDs] | IDS=... FMTS=story python3 mstory.py (via kvrz)"""
import sys
sys.argv = sys.argv[:1] + sys.argv[1:]
import kvx
K = kvx.K; RS = K.RS
_body = kvx.body

def poster(src, w, x, y, rot=(-8, 3, 3.5), back=False):
    h = w * 16 / 9; ry, rx, rz = rot
    el = (f'<div class="abs" style="left:{x}px;top:{y}px;width:{w}px;height:{h:.0f}px;transform:perspective(2200px) rotateY({ry}deg) rotateX({rx}deg) rotateZ({rz}deg)">'
          f'<div style="width:100%;height:100%;border-radius:{w * .045:.0f}px;overflow:hidden;box-shadow:0 0 0 3px rgba(255,255,255,.25),0 0 120px rgba(255,255,255,{.10 if back else .22}),0 50px 110px rgba(0,0,0,.65);{"filter:brightness(.8);" if back else ""}">'
          f'<img src="{K.img(src)}" style="display:block;width:100%;height:100%"></div></div>')
    return f'<div style="position:absolute;inset:0;{K.A_("phin", .55 if back else .7, 1.1)}">{el}</div>' if K.CTX['anim'] else el

P = {  # pôster principal no mesmo lugar e tamanho do celular (a coluna de texto não muda)
    'feed45': (410, 615, 370), 'sq': (322, 698, 300), 'story': (392, 646, 640), '16x9': (430, 1385, 96), 'land': (230, 925, 40)}

def body(s, fmt):
    if 'po' not in s: return _body(s, fmt)
    s2 = dict(s, ph=K.PH('rzp_casal-recibo.jpg'))
    inner = _body(s2, fmt)
    # tira o celular gerado pelo corpo genérico (primeiro bloco) e põe os pôsteres
    ph = K.phone('rzp_casal-recibo.jpg', *(lambda L: (L['pw'], L['px'], L['py']))(
        {'feed45': dict(pw=420, px=610, py=380), 'sq': dict(pw=330, px=694, py=318), 'story': dict(pw=400, px=640, py=660),
         '16x9': dict(pw=440, px=1380, py=112), 'land': dict(pw=236, px=920, py=52)}[fmt]), kvx.ROT, 1.0, .5, 0.0)
    assert inner.startswith(ph), 'layout do celular mudou'
    w, x, y = P[fmt]; out = ''
    if len(s['po']) > 1 and fmt not in ('land',):
        out += poster(s['po'][1], w * .82, x + w * .30, y - w * .16, (-4, 3, 9), back=True)
    out += poster(s['po'][0], w, x, y)
    return out + inner[len(ph):]
kvx.body = body

C, G = 'rzc', 'rzg'
SPEC = {
 # CASAL (R$ 13,99 até 30/11; dezembro sai a versão R$ 8,99)
 'ADC-RZ-19-v1': dict(sp=C, title='O *mapa astral* do WhatsApp de vocês.', kick='Retrozap Casais', po=['rzp_casal-mapa-astral.jpg', 'rzp_casal-recibo.jpg'],
                      nums=[(RS + '13,99', 'pagamento único, no Pix ou no cartão')],
                      post='Sol em Tagarela, Lua em Áudio: tudo tirado da conversa de vocês. Nada sai do seu celular.'),
 'ADC-RZ-20-v1': dict(sp=C, title='Quem paga o jantar? *O recibo do amor diz.*', kick='Retrozap Casais', po=['rzp_casal-recibo.jpg', 'rzp_casal-placar.jpg'],
                      nums=[('"te amo"', 'quem mandou mais, quem puxou o papo, quem pediu desculpas: item por item'), (RS + '13,99', 'pagamento único')],
                      post='Nada sai do seu celular.'),
 'ADC-RZ-21-v1': dict(sp=C, title='Boletim do casal: *aprovados pra 2027?*', kick='Retrozap Casais', po=['rzp_casal-boletim.jpg', 'rzp_casal-mapa-astral.jpg'],
                      nums=[('10', 'em romantismo? Nota de cada um, tirada da conversa de vocês'), (RS + '13,99', 'pagamento único')],
                      post='Mais o mapa astral, o recibo do amor e o placar. Nada sai do seu celular.'),
 'ADC-RZ-22-v1': dict(sp=C, title='Vocês contra *os casais do Brasil.*', kick='Ranking Brasil', po=['rzp_casal-ranking.jpg', 'rzp_casal-placar.jpg'],
                      nums=[(RS + '13,99', 'pagamento único, no Pix ou no cartão')],
                      post='Mensagens, risadas, declarações de amor: veja em que vocês ficam no Top do Brasil. Só os números saem do celular, sem nomes nem textos.'),
 # GRUPO (1º grupo grátis)
 'ADC-RZ-23-v1': dict(sp=G, title='Seu grupo contra *o Brasil inteiro.*', kick='Ranking Brasil', po=['rzp_grupo-ranking.jpg', 'rzp_grupo-plantao.jpg'],
                      nums=[('Grátis', 'o 1º grupo, sem cadastro')],
                      post='Risada, madrugada, figurinhas: veja em que o seu grupo fica no Top do Brasil. Só os números saem do celular, sem nomes nem textos.'),
 'ADC-RZ-24-v1': dict(sp=G, title='Procura‑se: *o fantasma do seu grupo.*', kick='Retrozap', po=['rzp_grupo-procura-se.jpg', 'rzp_grupo-radio.jpg'],
                      nums=[('Grátis', 'o 1º grupo. Quem sumiu, quem fala mais, quem só manda kkkk.')],
                      post='Cada um ganha o seu pôster. Nada sai do seu celular.'),
 'ADC-RZ-25-v1': dict(sp=G, title='URGENTE: *seu grupo virou notícia.*', kick='Plantão do Zap', po=['rzp_grupo-plantao.jpg', 'rzp_grupo-diario.jpg'],
                      nums=[('Grátis', 'o 1º grupo, sem cadastro'), ('2026', 'em manchete: quem falou mais, o dia do caos, o fantasma')],
                      post='Nada sai do seu celular.'),
 'ADC-RZ-26-v1': dict(sp=G, title='As mais tocadas *do seu grupo.*', kick='Rádio Turma FM', po=['rzp_grupo-radio.jpg', 'rzp_grupo-procura-se.jpg'],
                      nums=[('#1', 'a gíria oficial do grupo, com quantas vezes cada um falou'), ('Grátis', 'o 1º grupo')],
                      post='Mais troféus, ranking e pôsteres. Nada sai do seu celular.'),
}
kvx.SPEC.update(SPEC); K.HERO.update({v: None for v in SPEC})

if __name__ == '__main__':
    import asyncio
    mode = sys.argv[1]; ids = sys.argv[2:] or list(SPEC)
    out = kvx.HERE / 'out'; out.mkdir(exist_ok=True)
    async def go():
        async with K.async_playwright() as p:
            b = await p.chromium.launch(); pg = await b.new_page()
            if mode == 'hero':
                for v in ids:
                    d = out / v; d.mkdir(parents=True, exist_ok=True)
                    for f in ('sq', 'story'):
                        W, H = K.FMT[f]; await K.shot(pg, kvx.page(v, f), d / f'{v}-{f}.png', W, H)
                    print(v, flush=True)
            else:
                fm = mode.split(',')
                jobs = [K.motion(b, v, f, out / v) for v in ids for f in fm]
                for v in ids: (out / v).mkdir(parents=True, exist_ok=True)
                for i in range(0, len(jobs), 6): await asyncio.gather(*jobs[i:i + 6])
            await b.close()
    asyncio.run(go())
