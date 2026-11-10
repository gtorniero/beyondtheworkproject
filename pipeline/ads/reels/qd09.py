"""ADC-QD-09 v1 · Treinamento com quiz no fim (fixação) (linha corporativa). Uso: ver qd_corp.py"""
import sys
from qd_corp import roda, PAL, tv_crop
PTS, TOTAL, CAMP, JOG = 949, 1895, 8.5, 93  # números reais desta partida (TV e celular gravados) e s entre "podio" e o campeão no celular
def cfg(m):
    return dict(id='ADC-QD-09', ver='v1', campeao=m['podio'] + CAMP, capa_t=1.5, rev_lag=2.0, foco=dict(rev=.43, rank=.39, pod=.47, fim=.52),
        num=dict(pts=PTS, jog=JOG, total=TOTAL), bichos=[('coruja.-.redondos.6', 'l'), ('jabuti.palha.redondos.3', 'r'), ('tucano.bone.-.5', 'l'), ('gato.coroa.-.6', 'r')],
        pal=PAL, tv=tv_crop(f'{sys.argv[1]}/tv_q0_rev.png', f'{sys.argv[2]}/tv.png', .15, .02), tv_foco=(.04, .55), tvbig=(JOG, 'acertaram na hora.', '', '%'),
        still_t=m['podio'] + CAMP + 2.5, est_hook='Treinamento\nque *fixa.*',
        txt=dict(hook='Treinamento\nque *fixa.*', b='Quiz no fim,\n*pelo celular.*', pts='pontos na hora.', jog='pessoas jogando.',
                 d='', e='Você vê na hora\n*quem entendeu.*', total='pontos no pódio.'))
if __name__ == '__main__': roda(cfg, sys.argv)
