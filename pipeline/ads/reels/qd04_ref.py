"""ADC-QD-04 v4 · professores no visual Sala de aula, na referência RZ-08. Uso: python3 qd04_ref.py <captura qd04_partida> <trabalho> [reel|feed|sq|all] [preview|podio]"""
import sys
from qd_ref import entrega
def cfg(m):
    return dict(id='ADC-QD-04', ver='v4', campeao=m['podio'] + CAMP, capa_t=1.7, foco=dict(rev=.38, rank=.36, pod=.47, fim=.6),
        num=dict(pts=PTS, jog=10, total=TOTAL), bichos=[('coruja.-.redondos.6', 'l'), ('tucano.bone.-.5', 'r'), ('capivara.bone.-.7', 'l'), ('sapo.-.escuros.4', 'r')],
        pal=dict(bg='#2E4A3A', bg0='rgba(46,74,58,0)', blob1='#FFE066', b1o=.3, blob2='#2B59C3', b2o=.5, ink='#1F2A24', txt='#F2F2EA', hl_bg='#FFE066', hl_fg='#1F2A24', scr='#F3E9D7',
                 ring='rgba(255,255,255,.95)', flash='#FFE066', wipe='#2B59C3', wipe2='#E5383B', wipe3='#F3E9D7', pill_bg='#FFE066', pill_fg='#1F2A24', logo='quiddo-negativo.svg', sym_op=.55),
        txt=dict(hook='A turma pedindo\n*mais uma.*', b='O celular entra\n*na aula.*', pts='pontos na hora.', jog='alunos jogando.',
                 d='Ranking a\n*cada pergunta.*', e='E a matéria\nvira *disputa.*', total='pontos no pódio.'))
PTS, TOTAL, CAMP = 952, 2865, 9.3  # números reais desta partida (confira na captura) e segundos entre a marca "podio" e a revelação do campeão no celular
if __name__ == '__main__': entrega(cfg, sys.argv)
