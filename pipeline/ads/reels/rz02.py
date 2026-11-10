"""ADC-RZ-02 v3 · big numbers: "Quantas mensagens seu grupo mandou em 2026?" na referência RZ-08.
Números reais do Gran Finale rodando em corpo gigante → ano a ano → top 3 → card → CTA."""
from rz_ref import *
V = 'ADC-RZ-02-v3'
N_START = 90.25  # o contador de mensagens de 2026 começa a rodar na tela real


def build(fmt, FR):
    reel = fmt == 'reel'; T = 20.0 if reel else 12.0
    k = kit(fmt, T, FR, blobs=(PISC, UVA)); c, cam, rot, shot, txt = k.c, k.cam, k.rot, k.shot, k.txt
    # 1 · gancho: a pergunta, e o número real rodando (começa em t=1.9)
    s0 = N_START - 1.9
    shot(0, 4.6, s0, [(0, cam(.5, .5, .92)), (.9, cam(), SNAP), (1.5, cam(), SNAP), (1.95, cam(.5, .36, 1.7)), (4.6, cam(.5, .36, 1.8))],
         [(0, rot(20, 10, 3)), (.9, rot(6, 3, 0)), (1.9, rot(0, 0, 0))])
    txt('Quantas mensagens\nseu grupo mandou\nem *2026*?', -.3, 2.0, size=round(k.L['ts'] * .84), step=.05, dur=.4)
    k.num(0, 7249, 2.05, 3.5, 'mensagens em *2026.*', 4.4)
    c.add(c.flash(3.55, MANGA, .3, .5))
    k.ico('speech-balloon', 30, 1150, 2.3, 4.4, 200, -10)
    # 2 · áudios
    c.add(c.wipe(4.6, CHIC, .5, 'up'))
    shot(4.6, 7.2, 94.3, [(4.6, cam(.5, .36, 1.85)), (5.05, cam(.5, .36, 1.6)), (7.2, cam(.5, .4, 1.7))], [(4.6, rot(-8, 0, 0)), (6.2, rot(0, 0, 0))])
    k.num(0, 421, 4.8, 6.0, '*áudios* no ano.', 7.05, fmt_='int')
    k.ico('headphone', 850, 1300, 5.0, 7.0, 200, 10)
    if reel:
        # 3 · curiosidades
        shot(7.2, 9.6, 99.47, [(7.2, cam(.5, .45, 1.8)), (7.6, cam(.5, .52, 1.5)), (8.3, cam(.5, .54, 1.52), SNAP), (8.7, cam(.5, .62, 1.75)), (9.6, cam(.5, .62, 1.8))], [(7.2, rot(8, 0, 0)), (8.6, rot(0, 0, 0))], rate=.17)
        c.add(c.flash(7.2, PISC, .2, .4))
        k.num(0, 636, 7.35, 8.4, 'vezes *"bora".*', 9.45, fmt_='int')
        k.ico('call-me-hand', 30, 1250, 7.6, 9.4, 200, -12)
        # 4 · ano a ano
        c.add(c.wipe(9.6, GOIABA, .5, 'left'))
        shot(9.6, 12.2, 18.3, [(9.6, cam(.5, .8, 1.8)), (10.05, cam(.5, .78, 1.55)), (12.2, cam(.5, .78, 1.64))], [(9.6, rot(-10, 0, 0)), (11.2, rot(0, 0, 0))])
        txt('De 3.256\npara *7.249.*', 9.82, 12.05)
        k.ico('chart-with-upwards-trend', 850, 760, 10.1, 12.0, 200, 8)
        # 5 · prova: top 3, mídias, card
        shot(12.2, 13.8, 100.66, [(12.2, cam(.5, .42, 1.55)), (12.55, cam(.5, .42, 1.36)), (13.8, cam(.5, .42, 1.42))], [(12.2, rot(12, 4, 0)), (13.8, rot(7, 2, 0))], rate=.25)
        c.add(c.flash(12.2, UVA, .2, .4)); txt('O *top 3*\ndo ano.', 12.28, 13.7)
        shot(13.8, 15.4, 104.2, [(13.8, cam(.5, .6, 1.6)), (14.15, cam(.5, .6, 1.4)), (15.4, cam(.5, .6, 1.46))], [(13.8, rot(-12, 4, 0)), (15.4, rot(-7, 2, 0))])
        c.add(c.flash(13.8, MANGA, .2, .4)); txt('Tudo em\n*vídeo.*', 13.88, 15.3)
        shot(15.4, 17.0, 49.6, [(15.4, cam(.5, .33, 1.62)), (15.75, cam(.5, .33, 1.42)), (17.0, cam(.5, .33, 1.48))], [(15.4, rot(0, 8, 0)), (17.0, rot(0, 3, 0))])
        c.add(c.flash(15.4, PISC, .2, .4)); txt('*Card* pronto\npro grupo.', 15.48, 16.85)
        t_cta = 17.0
    else:
        shot(7.2, 9.0, 100.66, [(7.2, cam(.5, .42, 1.55)), (7.55, cam(.5, .42, 1.36)), (9.0, cam(.5, .42, 1.42))], [(7.2, rot(12, 4, 0)), (9.0, rot(7, 2, 0))], rate=.25)
        c.add(c.flash(7.2, UVA, .2, .4)); txt('E o *top 3*\ndo ano.', 7.28, 8.85)
        t_cta = 9.0
    k.mount(t_cta)
    k.cta(t_cta, 'Faça a\nretrospectiva\n2026 do\n*seu grupo.*', blob=PISC)
    return c


run(V, build, cover_t=3.7)
