"""ADC-QD-07 v1 · Reunião geral / kickoff (linha corporativa). Uso: ver qd_corp.py"""
import sys
from qd_corp import roda, PAL, tv_crop
PTS, TOTAL, CAMP, JOG = 954, 1900, 8.5, 20  # números reais desta partida (TV e celular gravados) e s entre "podio" e o campeão no celular
def cfg(m):
    return dict(id='ADC-QD-07', ver='v1', campeao=m['podio'] + CAMP, capa_t=1.5, rev_lag=2.0, foco=dict(rev=.43, rank=.39, pod=.47, fim=.52),
        num=dict(pts=PTS, jog=JOG, total=TOTAL), bichos=[('onca.coroa.-.2', 'l'), ('tucano.-.escuros.5', 'r'), ('capivara.-.escuros.1', 'l'), ('coruja.-.redondos.6', 'r')],
        pal=PAL, tv=tv_crop(f'{sys.argv[1]}/tv_q0_rev.png', f'{sys.argv[2]}/tv.png', .15, .02), tv_foco=(.04, .55), tvbig=(JOG, 'pessoas na sala.', '', ''),
        still_t=m['podio'] + CAMP + 2.5, est_hook='Reunião geral com\n*todo mundo* acordado.',
        txt=dict(hook='Reunião geral\ncom *todo mundo*\nacordado.', b='Cada um no\n*seu celular.*', pts='pontos na hora.', jog='pessoas jogando.',
                 d='', e='E o pódio sai\n*na hora.*', total='pontos no pódio.'))
if __name__ == '__main__': roda(cfg, sys.argv)
