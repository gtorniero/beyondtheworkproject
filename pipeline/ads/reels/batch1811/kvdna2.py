"""Lote 18/11 · RACKET e SURF (board) DNA, mais ângulos no estilo RK-05 (pedido do Gui: "explore mais os ADs, mais importante de tudo").
Telas reais do teste (scr/). Números só do site. Uso: python3 kvdna2.py hero|story [IDs]"""
import sys, asyncio
import kvx
K = kvx.K; RS = K.RS; PH = K.PH
SPEC = {
 # RACKET
 'ADC-RK-15-v1': dict(sp='rkfree', title='Você joga com a raquete *errada?*', kick='Grátis', ph=PH('racket_troca.jpg'),
                      nums=[('Grátis', 'a avaliação da raquete que você já usa: DNA Score, peso e balanço comparados com o ideal pra você')],
                      post='Se quiser trocar, o relatório completo mostra as 3 que mais combinam.'),
 'ADC-RK-16-v1': dict(sp='rkfree', title='A sua raquete, *nota por nota.*', kick='Grátis', ph=PH('racket_free_ficha.jpg', 1.0, .0),
                      nums=[('Grátis', 'sua ficha ideal: peso, cabeça, swingweight e balanço'), ('183', 'raquetes medidas para comparar')],
                      post='Leve para a loja ou compare com a sua.'),
 'ADC-RK-17-v1': dict(sp='racket', title='Raquete de presente? *Acerte no Natal.*', kick='Natal', ph=PH('racket_res.jpg'),
                      nums=[('3', 'raquetes que mais combinam com o jogo de quem vai ganhar'), (RS + '19,99', 'relatório completo, pagamento único')],
                      post='Faça o teste junto, em uns 3 minutos. Prévia grátis.'),
 'ADC-RK-18-v1': dict(sp='racket', title='Raquete certa, *setup errado?*', kick='Corda e tensão', ph=PH('racket_card.jpg', 1.18, .25),
                      nums=[('279.990', 'combinações de raquete, grip, corda, espessura e tensão'), ('1', 'é a sua, no relatório completo')],
                      chips=('Raquete', 'Grip', 'Corda', 'Tensão'), post='Prévia grátis · relatório completo R$ 19,99.'),
 'ADC-RK-19-v1': dict(sp='racket', title='O seu perfil de jogo *em um hexágono.*', kick='Perfil de jogo', ph=PH('racket_radar.jpg', 1.0, .0),
                      nums=[('6', 'eixos: potência, controle, spin, conforto, manobra e estabilidade'), ('183', 'raquetes comparadas com o seu perfil')],
                      post='Veja a sua atual contra a recomendada. Prévia grátis.'),
 # SURF (board)
 'ADC-SF-13-v1': dict(sp='surf', title='Sua prancha tem *os litros certos?*', kick='Litragem', ph=PH('surf_litros.jpg'),
                      nums=[('34,2&nbsp;L', 'para 70 kg no nível intermediário. E para você?'), ('3 min', 'pra descobrir os seus')],
                      post='Prévia grátis · sem cadastro.'),
 'ADC-SF-14-v1': dict(sp='surf', title='Prancha de presente? *Acerte as medidas.*', kick='Natal', ph=PH('surf_res.jpg'),
                      nums=[('17', 'medidas na ficha técnica, prontas para a loja ou o shaper'), (RS + '19,99', 'relatório completo, pagamento único')],
                      post='Faça o teste junto com quem vai ganhar. Prévia grátis.'),
 'ADC-SF-15-v1': dict(sp='surf', title='Vai encomendar no shaper? *Leve a ficha.*', kick='Sob medida', ph=PH('surf_medidas.jpg', 1.0, .18),
                      nums=[('17', 'medidas: comprimento, largura, espessura, litros e mais'), ('13', 'tipos de prancha disputam o seu resultado')],
                      post='Prévia grátis · 3 minutos · sem cadastro.'),
 'ADC-SF-16-v1': dict(sp='surf', title='Prancha usada? *Confira antes de pagar.*', kick='Antes de comprar', ph=PH('surf_cards.jpg'),
                      nums=[('416', 'tamanhos de 35 modelos comparados com o seu surf'), (RS + '19,99', 'contra R$ 1.500 a R$ 4.000 de uma prancha')],
                      post='Prévia grátis · 3 minutos.'),
}
kvx.SPEC.update(SPEC); K.HERO.update({v: None for v in SPEC})

if __name__ == '__main__':
    mode = sys.argv[1]; ids = sys.argv[2:] or list(SPEC); out = kvx.HERE / 'out'
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
                for v in ids: (out / v).mkdir(parents=True, exist_ok=True)
                jobs = [K.motion(b, v, f, out / v) for v in ids for f in mode.split(',')]
                for i in range(0, len(jobs), 6): await asyncio.gather(*jobs[i:i + 6])
            await b.close()
    asyncio.run(go())
