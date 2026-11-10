"""ADC-QD-04 v3 · Professores: a aula vira disputa, no visual Sala de aula do app.
Uso: python3 qd04.py <pasta da captura (qd_cap2.py qd04_partida.json)> <pasta de trabalho> [t_campeao] [preview]"""
import json, sys
from pathlib import Path
from qd_modelo import *
CAP, WORK = sys.argv[1], sys.argv[2]
m = json.loads((Path(CAP) / 'marcas.json').read_text())
camp = float(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3] != 'preview' else campeao_t(CAP, m)  # instante da revelação do campeão no celular (confira na folha; a detecção pode atrasar)
print('campeão em', camp)
STAR = '<svg viewBox="-2 -2 28 28"><path d="M12 1l3.2 7 7.6.8-5.7 5.1 1.7 7.5L12 17.6 5.2 21.4l1.7-7.5L1.2 8.8 8.8 8z" fill="#FFE066" stroke="#1F2A24" stroke-width="2" stroke-linejoin="round"/></svg>'
cfg = dict(m=m, campeao=camp, capa_t=1.6, frames=prepara(CAP, WORK, m, camp),
  pal=dict(bg='#2E4A3A', dot='rgba(255,255,255,.07)', bg2='#F3E9D7', dot2='rgba(46,74,58,.12)', ink='#1F2A24', txt='#F2F2EA', txt2='#1F2A24',
           hl_bg='#FFE066', hl_fg='#1F2A24', ring='rgba(255,255,255,.95)', flash='#FFE066', wipe='#2B59C3', wipe2='#FFE066',
           pill_bg='#FFE066', pill_fg='#1F2A24', logo='quiddo-negativo.svg', deco=STAR, deco_op=.95),
  txt=dict(hook='A turma *pedindo*\nmais uma pergunta.', b='O celular entra\n*na aula.*', c='Na hora, quem\n*entendeu.*', d='Ranking a\n*cada pergunta.*', e='E a matéria\nvira *disputa.*'))
if __name__ == '__main__':
    R = [i * .5 for i in range(40)]; Mo = [i * .45 for i in range(29)]
    entrega(cfg, 'ADC-QD-04', 'v3', Path(__file__).resolve().parent.parent.parent / 'out' / 'media', R, Mo, Path(WORK) / 'prev', so_preview='preview' in sys.argv)
