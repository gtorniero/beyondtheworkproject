"""ADC-RZ-01 v5 · foco em RETROSPECTIVA do WhatsApp (Gui, 10/11: "ninguém entende 'seu WhatsApp virou premiação'").
A retrospectiva como experiência, do começo ao fim: gancho no pódio → escolhe o grupo → Ato I → troféus → Gran Finale → card → CTA."""
from rz_ref import *
V = 'ADC-RZ-01-v5'
POD_JUMP, RASPA_REV, N_START = 44.85, 68.35, 90.25


def build(fmt, FR):
    reel = fmt == 'reel'; T = 20.0 if reel else 12.0
    k = kit(fmt, T, FR, blobs=(UVA, MANGA)); c, cam, rot, shot, txt = k.c, k.cam, k.rot, k.shot, k.txt
    # 1 · gancho: o pódio aparece (salto em t=1.0) sob a promessa "retrospectiva"
    shot(0, 3.5, POD_JUMP - 1.0, [(0, cam(.5, .8, 1.75)), (.85, cam(.5, .8, 1.6), SNAP), (1.3, cam(.5, .31, 1.36)), (3.5, cam(.5, .31, 1.46))],
         [(0, rot(-16, 8, -2)), (1.3, rot(0, 0, 0))])
    c.add(c.flash(1.05, '#fff', .3, .7))
    txt('A *retrospectiva*\ndo seu grupo\nno WhatsApp.', -.3, 3.3, size=round(k.L['ts'] * .9), step=.06, dur=.4)
    k.ico('calendar', 850, 1240, 1.2, 3.4, 200, 10)

    def trofeus(t0, t1):
        rev = t0 + 1.6
        shot(t0, t1, RASPA_REV - 1.6, [(t0, cam(.5, .68, 1.85)), (t0 + .4, cam(.5, .68, 1.62)), (rev - .05, cam(.5, .68, 1.7), SNAP), (rev + .35, cam(.5, .33, 1.4)), (t1, cam(.5, .33, 1.46))], [(t0, rot(-8, 0, 0)), (t0 + 1.6, rot(0, 0, 0))])
        c.add(c.flash(rev + .05, '#fff', .28, .6))
        txt('Depois, os\n*troféus.*', t0 + .1, t1 - .15)
        k.ico('trophy' if (RZ / 'icones-grupo' / 'trophy.svg').exists() else 'party-popper', 30, 1220, t0 + .4, t1 - .1, 200, -10)

    def finale(t0, t1):
        shot(t0, t1, N_START - .6, [(t0, cam(.5, .45, 1.2)), (t0 + .5, cam(.5, .36, 1.5), SNAP), (t1, cam(.5, .36, 1.62))], [(t0, rot(10, 4, 0)), (t0 + 1.2, rot(0, 0, 0))])
        txt('No fim, o\n*Gran Finale.*', t0 + .1, t1 - .15)
        k.ico('drum-with-drumsticks', 850, 1300, t0 + .4, t1 - .1, 200, 10)

    if reel:
        c.add(c.wipe(3.5, PISC, .5, 'left'))
        shot(3.5, 6.0, 10.0, [(3.5, cam(.5, .3, 1.75)), (3.95, cam(.5, .3, 1.5)), (6.0, cam(.5, .36, 1.56))], [(3.5, rot(10, 0, 0)), (5.0, rot(0, 0, 0))])
        txt('Escolhe o\n*grupo.*', 3.72, 5.85)
        k.ico('busts-in-silhouette' if (RZ / 'icones-grupo' / 'busts-in-silhouette.svg').exists() else 'speech-balloon', 30, 1300, 3.9, 5.9, 200, -10)
        c.add(c.flash(6.0, UVA, .2, .4))
        shot(6.0, 8.5, 18.2, [(6.0, cam(.5, .3, 1.7)), (6.4, cam(.5, .3, 1.45)), (8.5, cam(.5, .36, 1.52))], [(6.0, rot(-10, 0, 0)), (7.4, rot(0, 0, 0))])
        txt('Ato I: quem é\no *seu grupo.*', 6.1, 8.35)
        k.ico('busts-in-silhouette' if (RZ / 'icones-grupo' / 'busts-in-silhouette.svg').exists() else 'eyes', 850, 1300, 6.4, 8.4, 200, 10)
        c.add(c.wipe(8.5, CHIC, .5, 'up')); trofeus(8.5, 11.4)
        c.add(c.wipe(11.4, GOIABA, .5, 'left')); finale(11.4, 14.2)
        shot(14.2, 17.0, 49.6, [(14.2, cam(.5, .33, 1.62)), (14.6, cam(.5, .33, 1.42)), (17.0, cam(.5, .33, 1.5))], [(14.2, rot(0, 8, 0)), (17.0, rot(0, 3, 0))])
        c.add(c.flash(14.2, PISC, .2, .4)); txt('E um *card*\npro grupo.', 14.3, 16.85)
        t_cta = 17.0
    else:
        c.add(c.wipe(3.5, CHIC, .5, 'up')); trofeus(3.5, 6.2)
        c.add(c.wipe(6.2, GOIABA, .5, 'left')); finale(6.2, 9.0); t_cta = 9.0
    k.mount(t_cta)
    k.cta(t_cta, 'Faça a\nretrospectiva\ndo *seu grupo.*', blob=UVA)
    return c


run(V, build, cover_t=1.8)
