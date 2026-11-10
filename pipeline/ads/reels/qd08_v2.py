"""ADC-QD-08 v2 · Onboarding (linha corporativa). Look claro e acolhedor: creme + amarelo, celular protagonista, bichos do site. Sem pontos soltos."""
import sys
from qd_corp8 import roda
CAMP = 8.5
PAL = dict(bg='#FFF6E6', bg0='rgba(255,246,230,0)', blob1='#FFC83D', b1o=.55, blob2='#FF7A1A', b2o=.22, ink='#0E2A22', txt='#0E2A22', hl_bg='#FFC83D', hl_fg='#0E2A22', scr='#fff',
           ring='rgba(14,42,34,.85)', flash='#FFC83D', wipe='#FFC83D', wipe2='#FF7A1A', wipe3='#0E2A22', pill_bg='#0E2A22', pill_fg='#FFF6E6', logo='quiddo-cor.svg', sym_op=.55)
def cfg(m):
    return dict(id='ADC-QD-08', ver='v2', campeao=m['podio'] + CAMP, capa_t=1.5, rev_lag=2.0, foco=dict(rev=.43, rank=.39, pod=.47, fim=.52), rot0=(0, 14, -3),
        num=dict(), bichos=[('preguica.fone.-.2', 'l'), ('arara.festa.-.4', 'r'), ('sapo.flor.-.4', 'l'), ('mico.flor.-.7', 'r')],
        pal=PAL, still_t=m['q0_hero'] - .4, est_hook='Integração que\no novato *lembra.*',
        txt=dict(hook='Integração que\no novato *lembra.*', b='Cada novato no\n*seu celular.*', rev='Acertou? Ganha\npontos e *sobe.*',
                 d='Novato em\n*1º lugar.*', e='E o pódio\n*é do novato.*'))
if __name__ == '__main__': roda(cfg, sys.argv)
