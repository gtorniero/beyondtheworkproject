"""ADC-RZ-01 v4 · "Seu WhatsApp de 2026 virou premiação." na referência RZ-08.
Abre no pódio explodindo → volta ao começo (escolher a conversa, leitura, turma) → desfile de troféus → CTA."""
from rz_ref import *
V = 'ADC-RZ-01-v4'
POD_JUMP, POD2_JUMP, RASPA_REV = 44.85, 59.55, 68.35


def build(fmt, FR):
    reel = fmt == 'reel'; T = 20.0 if reel else 12.0
    k = kit(fmt, T, FR, blobs=(CHIC, MANGA)); c, cam, rot, shot, txt = k.c, k.cam, k.rot, k.shot, k.txt
    # 1 · gancho: o pódio explode (salto em t=1.0)
    s0 = POD_JUMP - 1.0
    shot(0, 3.5, s0, [(0, cam(.5, .8, 1.75)), (.85, cam(.5, .8, 1.6), SNAP), (1.3, cam(.5, .31, 1.36)), (3.5, cam(.5, .31, 1.46))],
         [(0, rot(-16, 8, -2)), (1.3, rot(0, 0, 0))])
    c.add(c.flash(1.05, '#fff', .3, .7))
    txt('Seu WhatsApp\nde 2026 virou\n*premiação.*', -.3, 3.3, size=round(k.L['ts'] * .9), step=.06, dur=.4)
    k.ico('party-popper', 30, 1180, 1.2, 3.4, 200, -12); k.ico('medalha-1', 850, 760, 1.4, 3.4, 200, 10)
    def podcaster(t0, t1):
        j = t0 + 1.3
        shot(t0, t1, POD2_JUMP - 1.3, [(t0, cam(.5, .2, 1.7)), (t0 + .45, cam(.5, .2, 1.5)), (j - .1, cam(.5, .2, 1.55), SNAP), (j + .3, cam(.5, .3, 1.36)), (t1, cam(.5, .3, 1.44))], [(t0, rot(8, 0, 0)), (t0 + 1.7, rot(0, 0, 0))])
        c.add(c.flash(j + .05, '#fff', .28, .6))
        txt('Troféu de\n*Podcaster.*', t0 + .22, t1 - .15)
        k.ico('studio-microphone', 20, 1060, t0 + .5, t1 - .1, 200, -10); k.ico('headphone', 850, 1380, t0 + .8, t1 - .1, 200, 12)

    def leitura(t0, t1):
        shot(t0, t1, 8.35, [(t0, cam(.5, .38, 1.6)), (t0 + .4, cam(.5, .38, 1.42)), (t0 + 1.2, cam(.5, .38, 1.46), SNAP), (t0 + 1.6, cam(.5, .3, 1.3)), (t1, cam(.5, .3, 1.36))], [(t0, rot(-8, 0, 0)), (t0 + 1.4, rot(0, 0, 0))])
        k.num(0, 10505, t0 + .1, t0 + 1.2, 'mensagens *lidas.*', t1 - .2)

    c.add(c.wipe(3.5, PISC, .5, 'left'))
    if reel:
        # 2 · volta ao começo: escolher a conversa
        shot(3.5, 6.0, 1.85, [(3.5, cam(.5, .42, 1.7)), (3.95, cam(.5, .42, 1.45)), (4.7, cam(.5, .42, 1.48), SNAP), (5.1, cam(.3, .44, 1.75)), (5.55, cam(.3, .44, 1.78), SNAP), (5.8, cam(.5, .42, 1.5)), (6.0, cam(.5, .42, 1.52))], [(3.5, rot(10, 0, 0)), (5.0, rot(0, 0, 0))])
        txt('Você escolhe\na *conversa.*', 3.72, 5.85)
        c.add(c.flash(6.0, PISC, .2, .4)); leitura(6.0, 8.5)
        # 4 · desfile de troféus
        c.add(c.wipe(8.5, CHIC, .5, 'up')); podcaster(8.5, 11.4)
        r = RASPA_REV - 1.6; t_rev = 11.4 + 1.6
        shot(11.4, 14.2, r, [(11.4, cam(.5, .68, 1.85)), (11.8, cam(.5, .68, 1.62)), (t_rev - .05, cam(.5, .68, 1.7), SNAP), (t_rev + .35, cam(.5, .33, 1.4)), (14.2, cam(.5, .33, 1.46))], [(11.4, rot(-8, 0, 0)), (13.0, rot(0, 0, 0))])
        c.add(c.flash(11.4, GOIABA, .2, .45)); c.add(c.flash(t_rev + .05, '#fff', .28, .6))
        txt('Raspadinha do\n*Boca-Suja.*', 11.5, 14.05)
        k.ico('serious-face-with-symbols-covering-mouth', 850, 800, 11.8, 14.1, 200, 10)
        shot(14.2, 15.6, 87.2, [(14.2, cam(.5, .3, 1.7)), (14.55, cam(.5, .3, 1.5)), (15.6, cam(.5, .3, 1.56))], [(14.2, rot(-12, 4, 0)), (15.6, rot(-7, 2, 0))], rate=.4)
        c.add(c.flash(14.2, UVA, .2, .4)); txt('Coração\n*Mole.*', 14.28, 15.5)
        k.ico('heavy-black-heart', 30, 1240, 14.3, 15.5, 200, -10)
        shot(15.6, 17.0, 100.66, [(15.6, cam(.5, .42, 1.55)), (15.95, cam(.5, .42, 1.36)), (17.0, cam(.5, .42, 1.42))], [(15.6, rot(12, 4, 0)), (17.0, rot(7, 2, 0))], rate=.25)
        c.add(c.flash(15.6, PISC, .2, .4)); txt('E o *top 3*\ndo ano.', 15.68, 16.85)
        k.ico('ghost', 850, 1300, 15.7, 16.9, 200, 8)
        t_cta = 17.0
    else:
        leitura(3.5, 6.0); c.add(c.wipe(6.0, CHIC, .5, 'up')); podcaster(6.0, 9.0); t_cta = 9.0
    k.mount(t_cta)
    k.cta(t_cta, 'Faça a\nretrospectiva\ndo *seu grupo.*', blob=CHIC)
    return c


run(V, build, cover_t=1.6)
