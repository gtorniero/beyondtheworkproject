"""ADC-QD-03 v4 · chá-bar no visual Amor, na referência RZ-08. Uso: python3 qd03_ref.py <captura qd03_partida> <trabalho> [reel|feed|sq|all] [preview|podio]"""
import sys
from qd_ref import entrega
def cfg(m):
    return dict(id='ADC-QD-03', ver='v4', campeao=m['podio'] + CAMP, capa_t=1.7, foco=dict(rev=.24, rank=.22, pod=.5, fim=.62),
        num=dict(pts=PTS, jog=8, total=TOTAL), bichos=[('tucano.-.coracao.5', 'l'), ('onca.flor.-.2', 'r'), ('capivara.-.coracao.1', 'l'), ('jabuti.palha.redondos.3', 'r')],
        pal=dict(bg='#8E1B3E', bg0='rgba(142,27,62,0)', blob1='#FF8FB1', blob2='#E5383B', ink='#5A1027', txt='#FFF6E6', hl_bg='#FFD1DC', hl_fg='#8E1B3E', scr='#FFE3EA',
                 ring='rgba(255,255,255,.95)', flash='#FFD1DC', wipe='#E5383B', wipe2='#FF8FB1', wipe3='#FFF6E6', pill_bg='#FFE3EA', pill_fg='#5A1027', logo='quiddo-negativo.svg',
                 sym_cor=['#FF8FB1', '#FFD1DC', '#FF8FB1', '#FFD1DC'], sym_op=.4),
        txt=dict(hook='Quem conhece\n*mais* os noivos?', b='Cada um no\n*seu celular.*', pts='pontos na hora.', jog='convidados jogando.',
                 d='Ranking a\n*cada pergunta.*', e='E o pódio\nvira *festa.*', total='pontos no pódio.'))
PTS, TOTAL, CAMP = 954, 2866, 8.8  # números reais desta partida (confira na captura) e segundos entre a marca "podio" e a revelação do campeão no celular
if __name__ == '__main__': entrega(cfg, sys.argv)
