"""ADC-QD-01 v5 · treinamento corporativo no visual Escritório, na referência RZ-08. Uso: python3 qd01_v5.py <captura qd01_partida> <trabalho> [reel|feed|sq|all] [preview|podio]"""
import sys
from qd_ref5 import entrega
def cfg(m):
    return dict(id='ADC-QD-01', ver='v5', campeao=m['podio'] + CAMP, capa_t=1.5, rev_lag=2.0, foco=dict(rev=.43, rank=.39, pod=.47, fim=.52),
        num=dict(pts=PTS, jog=8, total=TOTAL), bichos=[('sapo.flor.-.4', 'l'), ('tucano.-.escuros.5', 'r'), ('coruja.-.redondos.6', 'l'), ('onca.coroa.-.2', 'r')],
        pal=dict(bg='#1E1B3A', bg0='rgba(30,27,58,0)', blob1='#4C6EF5', b1o=.6, blob2='#F06595', b2o=.4, ink='#120F26', txt='#FFF6E6', hl_bg='#FFC83D', hl_fg='#120F26', scr='#EEEAFB',
                 ring='rgba(255,255,255,.95)', flash='#FFC83D', wipe='#4C6EF5', wipe2='#F06595', wipe3='#EEEAFB', pill_bg='#FFC83D', pill_fg='#120F26', logo='quiddo-negativo.svg', sym_op=.5),
        txt=dict(hook='Treinamento com\n*a sala ligada.*', b='A sala responde\n*pelo celular.*', pts='pontos na hora.', jog='pessoas jogando.',
                 d='Ranking a\n*cada pergunta.*', e='Na hora, você vê\n*quem entendeu.*', total='pontos no pódio.'))
PTS, TOTAL, CAMP = 959, 1914, 8.5  # números reais desta partida e segundos entre a marca "podio" e a revelação do campeão no celular
if __name__ == '__main__': entrega(cfg, sys.argv)
