"""18/11 (Gui): "nos ads, faça uma versão com e sem preço; preço logo no começo não faz sentido; outro call to action: Teste o seu agora".
COM PREÇO (versão nova do mesmo AD): o preço sai do topo e vira o 2º número (aparece depois, no motion). SEM PREÇO (-SP): nenhum preço.
CTA novo em todos: "Teste o de vocês agora" / "Teste o do seu grupo agora" / "Teste o seu agora"."""
import sys
import kvrz, kvdna2
kvx = kvrz.kvx; K = kvx.K; RS = K.RS; PH = K.PH
K.SP.update({
    'rzc2': dict(K.SP['rzc'], cta='Teste o de vocês agora', fine='Pagamento único · Pix ou cartão.'),
    'rzg2': dict(K.SP['rzg'], cta='Teste o do seu grupo agora'),
    'racket2': dict(K.SP['racket'], cta='Teste o seu agora'),
    'surf2': dict(K.SP['surf'], cta='Teste o seu agora'),
})
kvx.THEME.update({'rzc2': kvx.THEME['rzc'], 'rzg2': kvx.THEME['rzg'], 'racket2': kvx.THEME['racket'], 'surf2': kvx.THEME['surf']})
_page = kvx.page
def page(v, fmt, anim=False):
    h = _page(v, fmt, anim)
    return h.replace('</style>', '</style>' + kvx.RZCSS, 1) if kvx.SPEC[v]['sp'] in ('rzc2', 'rzg2') else h
kvx.page = page; K.page = page

P13 = (RS + '13,99', 'pagamento único, no Pix ou no cartão')
T8 = ('8', 'troféus do casal: quem manda mais mensagem, quem é mais romântico')
base = kvx.SPEC
def var(old, new_id, sp, nums, post=None, **k):
    s = dict(base[old]); s.update(sp=sp, nums=nums, **k)
    if post is not None: s['post'] = post
    return new_id, s
V = dict([
 # RETROZAP CASAL
 var('ADC-RZ-18-v2', 'ADC-RZ-18-v3', 'rzc2', [T8, P13], 'Com o vídeo de vocês e grupos ilimitados. Nada sai do seu celular.'),
 var('ADC-RZ-18-v2', 'ADC-RZ-18-SP-v1', 'rzc2', [T8], 'Com o vídeo de vocês e grupos ilimitados. Nada sai do seu celular.'),
 var('ADC-RZ-19-v1', 'ADC-RZ-19-v2', 'rzc2', [('8', 'troféus do casal, mais o recibo do amor, o boletim e o placar'), P13]),
 var('ADC-RZ-19-v1', 'ADC-RZ-19-SP-v1', 'rzc2', [('8', 'troféus do casal, mais o recibo do amor, o boletim e o placar')]),
 var('ADC-RZ-20-v1', 'ADC-RZ-20-v2', 'rzc2', [base['ADC-RZ-20-v1']['nums'][0], P13]),
 var('ADC-RZ-20-v1', 'ADC-RZ-20-SP-v1', 'rzc2', [base['ADC-RZ-20-v1']['nums'][0]]),
 var('ADC-RZ-21-v1', 'ADC-RZ-21-v2', 'rzc2', [base['ADC-RZ-21-v1']['nums'][0], P13]),
 var('ADC-RZ-21-v1', 'ADC-RZ-21-SP-v1', 'rzc2', [base['ADC-RZ-21-v1']['nums'][0]]),
 var('ADC-RZ-22-v1', 'ADC-RZ-22-v2', 'rzc2', [('8', 'troféus do casal e o placar um contra o outro'), P13]),
 var('ADC-RZ-22-v1', 'ADC-RZ-22-SP-v1', 'rzc2', [('8', 'troféus do casal e o placar um contra o outro')]),
 # RACKET / SURF
 var('ADC-RK-17-v1', 'ADC-RK-17-v2', 'racket2', base['ADC-RK-17-v1']['nums']),
 var('ADC-RK-17-v1', 'ADC-RK-17-SP-v1', 'racket2', base['ADC-RK-17-v1']['nums'][:1], 'Faça o teste junto, em uns 3 minutos. Prévia grátis.'),
 var('ADC-SF-14-v1', 'ADC-SF-14-v2', 'surf2', base['ADC-SF-14-v1']['nums']),
 var('ADC-SF-14-v1', 'ADC-SF-14-SP-v1', 'surf2', base['ADC-SF-14-v1']['nums'][:1], 'Faça o teste junto com quem vai ganhar. Prévia grátis.'),
 var('ADC-SF-16-v1', 'ADC-SF-16-v2', 'surf2', base['ADC-SF-16-v1']['nums']),
 var('ADC-SF-16-v1', 'ADC-SF-16-SP-v1', 'surf2', [base['ADC-SF-16-v1']['nums'][0], ('17', 'medidas para conferir na prancha antes de pagar')]),
])
kvx.SPEC.update(V); K.HERO.update({v: None for v in V})

if __name__ == '__main__':
    import asyncio
    mode = sys.argv[1]; ids = sys.argv[2:] or list(V); out = kvx.HERE / 'out'
    async def go():
        async with K.async_playwright() as p:
            b = await p.chromium.launch(); pg = await b.new_page()
            if mode == 'hero':
                for v in ids:
                    d = out / v; d.mkdir(parents=True, exist_ok=True)
                    for f in ('sq', 'story'):
                        W, H = K.FMT[f]; await K.shot(pg, page(v, f), d / f'{v}-{f}.png', W, H)
                print(len(ids), flush=True)
            else:
                for v in ids: (out / v).mkdir(parents=True, exist_ok=True)
                jobs = [K.motion(b, v, f, out / v) for v in ids for f in mode.split(',')]
                for i in range(0, len(jobs), 8): await asyncio.gather(*jobs[i:i + 8])
            await b.close()
    asyncio.run(go())
