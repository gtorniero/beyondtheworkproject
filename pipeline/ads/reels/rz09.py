"""ADC-RZ-09 v1 · versão CASAL do RZ-02 v3 (big numbers), na identidade Casa Casal.
Retrospectiva de casal real do site (captura_casal.py + gera_casal.py): Gran Finale do casal → números gigantes → troféus → vídeo do casal → CTA."""
from rz_ref_casal import *
V = 'ADC-RZ-09-v1'
N_MSG, N_AUD, N_RIS, N_DEC = 113.8, 117.75, 121.6, 125.55   # instante em que cada contador real começa a rodar na tela
TAGARELA, CORACAO, VIDEO = 41.3, 59.9, 138.6


def build(fmt, FR):
    reel = fmt == 'reel'; T = 20.0 if reel else 12.0
    k = kit(fmt, T, FR, blobs=(ROSA, PESSEGO)); c, cam, rot, shot, txt = k.c, k.cam, k.rot, k.shot, k.txt
    # 1 · gancho: a pergunta e o número real rodando (começa em t=1.9)
    s0 = N_MSG - 1.9
    shot(0, 4.6, s0, [(0, cam(.5, .5, .92)), (.9, cam(), SNAP), (1.5, cam(), SNAP), (1.95, cam(.5, .33, 1.7)), (4.6, cam(.5, .33, 1.8))],
         [(0, rot(20, 10, 3)), (.9, rot(6, 3, 0)), (1.9, rot(0, 0, 0))])
    txt('Quantas mensagens\nvocês trocaram\nem *2026*?', -.3, 2.0, size=round(k.L['ts'] * .84), step=.05, dur=.4)
    k.num(0, 10524, 2.05, 3.5, 'mensagens em *2026.*', 4.4)
    c.add(c.flash(3.55, CEREJA, .3, .35))
    k.ico('love-letter', 30, 1150, 2.3, 4.4, 200, -10)
    # 2 · declarações de amor
    c.add(c.wipe(4.6, CEREJA, .5, 'up'))
    shot(4.6, 7.2, N_DEC - .25, [(4.6, cam(.5, .3, 1.85)), (5.05, cam(.5, .3, 1.6)), (7.2, cam(.5, .33, 1.7))], [(4.6, rot(-8, 0, 0)), (6.2, rot(0, 0, 0))])
    k.num(0, 677, 4.8, 6.0, '*"te amo"* e cia.', 7.05, fmt_='int')
    k.ico('heavy-black-heart', 850, 1300, 5.0, 7.0, 200, 10)
    if reel:
        # 3 · risadas
        shot(7.2, 9.6, N_RIS - .2, [(7.2, cam(.5, .3, 1.8)), (7.6, cam(.5, .3, 1.55)), (9.6, cam(.5, .33, 1.64))], [(7.2, rot(8, 0, 0)), (8.6, rot(0, 0, 0))])
        c.add(c.flash(7.2, ROSA1, .2, .5))
        k.num(0, 865, 7.35, 8.4, '*risadas* no ano.', 9.45, fmt_='int')
        k.ico('face-with-tears-of-joy', 30, 1250, 7.6, 9.4, 200, -12)
        # 4 · áudios
        c.add(c.wipe(9.6, PESSEGO, .5, 'left'))
        shot(9.6, 12.2, N_AUD - .2, [(9.6, cam(.5, .3, 1.8)), (10.05, cam(.5, .3, 1.55)), (12.2, cam(.5, .33, 1.64))], [(9.6, rot(-10, 0, 0)), (11.2, rot(0, 0, 0))])
        k.num(0, 726, 9.8, 11.0, '*áudios* trocados.', 12.05, fmt_='int')
        k.ico('headphone', 850, 760, 10.1, 12.0, 200, 8)
        # 5 · prova: troféus do casal e vídeo
        shot(12.2, 13.8, TAGARELA, [(12.2, cam(.5, .42, 1.55)), (12.55, cam(.5, .42, 1.36)), (13.8, cam(.5, .42, 1.42))], [(12.2, rot(12, 4, 0)), (13.8, rot(7, 2, 0))], rate=.5)
        c.add(c.flash(12.2, ROSA1, .2, .5)); txt('Quem *fala*\nmais.', 12.28, 13.7)
        shot(13.8, 15.4, CORACAO, [(13.8, cam(.5, .42, 1.6)), (14.15, cam(.5, .42, 1.4)), (15.4, cam(.5, .42, 1.46))], [(13.8, rot(-12, 4, 0)), (15.4, rot(-7, 2, 0))], rate=.5)
        c.add(c.flash(13.8, CEREJA, .2, .35)); txt('Quem manda\nmais *coração.*', 13.88, 15.3)
        shot(15.4, 17.0, VIDEO, [(15.4, cam(.5, .55, 1.62)), (15.75, cam(.5, .55, 1.42)), (17.0, cam(.5, .55, 1.48))], [(15.4, rot(0, 8, 0)), (17.0, rot(0, 3, 0))])
        c.add(c.flash(15.4, ROSA1, .2, .5)); txt('E o *vídeo*\nde vocês.', 15.48, 16.85)
        t_cta = 17.0
    else:
        shot(7.2, 9.0, TAGARELA, [(7.2, cam(.5, .42, 1.55)), (7.55, cam(.5, .42, 1.36)), (9.0, cam(.5, .42, 1.42))], [(7.2, rot(12, 4, 0)), (9.0, rot(7, 2, 0))], rate=.5)
        c.add(c.flash(7.2, ROSA1, .2, .5)); txt('Quem *fala*\nmais.', 7.28, 8.85)
        t_cta = 9.0
    k.mount(t_cta)
    k.cta(t_cta, 'Façam a\nretrospectiva\n*de vocês.*', blob=ROSA)
    return c


run(V, build, cover_t=3.7)
