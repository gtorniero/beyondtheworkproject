"""ADC-QD-08 v1 · Onboarding / integração de novos (linha corporativa). Uso: ver qd_corp.py"""
import sys
from qd_corp import roda, PAL, tv_crop
PTS, TOTAL, CAMP, JOG = 950, 1891, 8.5, 12  # números reais desta partida (TV e celular gravados) e s entre "podio" e o campeão no celular
def cfg(m):
    return dict(id='ADC-QD-08', ver='v1', campeao=m['podio'] + CAMP, capa_t=1.5, rev_lag=2.0, foco=dict(rev=.43, rank=.39, pod=.47, fim=.52),
        num=dict(pts=PTS, jog=JOG, total=TOTAL), bichos=[('preguica.fone.-.2', 'l'), ('arara.festa.-.4', 'r'), ('sapo.flor.-.4', 'l'), ('mico.flor.-.7', 'r')],
        pal=PAL, tv=tv_crop(f'{sys.argv[1]}/tv_q0_rank.png', f'{sys.argv[2]}/tv.png', .13, .02), tv_foco=(.04, .55), tvbig=(JOG, 'novatos jogando.', '', ''),
        still_t=m['podio'] + CAMP + 2.5, est_hook='Integração que\no novato *lembra.*',
        txt=dict(hook='Integração que\no novato *lembra.*', b='Cada novato no\n*seu celular.*', pts='pontos na hora.', jog='pessoas jogando.',
                 d='', e='E o pódio\n*é do novato.*', total='pontos no pódio.'))
if __name__ == '__main__': roda(cfg, sys.argv)
