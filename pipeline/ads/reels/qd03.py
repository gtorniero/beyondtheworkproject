"""ADC-QD-03 v3 · Chá-bar: "Quem conhece mais os noivos?" no visual Amor do app.
Uso: python3 qd03.py <pasta da captura (qd_cap2.py qd03_partida.json)> <pasta de trabalho> [t_campeao] [preview]"""
import json, sys
from pathlib import Path
from qd_modelo import *
CAP, WORK = sys.argv[1], sys.argv[2]
m = json.loads((Path(CAP) / 'marcas.json').read_text())
camp = float(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3] != 'preview' else campeao_t(CAP, m)  # instante da revelação do campeão no celular (confira na folha; a detecção pode atrasar)
print('campeão em', camp)
HEART = '<svg viewBox="-3 -3 38 36"><path d="M23.6,0c-3.4,0-6.3,2.7-7.6,5.6C14.7,2.7,11.8,0,8.4,0C3.8,0,0,3.8,0,8.4c0,9.4,9.5,11.9,16,21.2c6.1-9.3,16-12.1,16-21.2C32,3.8,28.2,0,23.6,0z" fill="{f}" stroke="#5A1027" stroke-width="2.6" stroke-linejoin="round"/></svg>'
cfg = dict(m=m, campeao=camp, capa_t=1.6, frames=prepara(CAP, WORK, m, camp),
  pal=dict(bg='#8E1B3E', dot='rgba(255,143,177,.22)', bg2='#FFE3EA', dot2='rgba(255,143,177,.45)', ink='#5A1027', txt='#FFF6E6', txt2='#5A1027',
           hl_bg='#FFD1DC', hl_fg='#8E1B3E', ring='rgba(255,255,255,.95)', flash='#FFD1DC', wipe='#E5383B', wipe2='#FF8FB1',
           pill_bg='#FFE3EA', pill_fg='#5A1027', logo='quiddo-negativo.svg', deco=HEART.replace('{f}', '#E5383B'), deco_op=.95),
  txt=dict(hook='Quem conhece\n*mais* os noivos?', b='Cada um no\n*seu celular.*', c='Acertou?\nSai *na hora.*', d='Ranking a\n*cada pergunta.*', e='E o pódio\nvira *festa.*'))
if __name__ == '__main__':
    R = [i * .5 for i in range(40)]; Mo = [i * .45 for i in range(29)]
    entrega(cfg, 'ADC-QD-03', 'v3', Path(__file__).resolve().parent.parent.parent / 'out' / 'media', R, Mo, Path(WORK) / 'prev', so_preview='preview' in sys.argv)
