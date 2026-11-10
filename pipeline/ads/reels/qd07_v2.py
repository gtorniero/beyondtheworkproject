"""ADC-QD-07 v2 · Reunião geral (linha corporativa). Look do KV aprovado: tinta + brilho mata, telão + celular juntos. Sem pontos soltos. Uso: ver qd_corp.py"""
import sys
from qd_corp8 import roda, tv_crop
CAMP, JOG = 8.5, 20
PAL = dict(bg='#0E2A22', bg0='rgba(14,42,34,0)', blob1='#0B5D45', b1o=.9, blob2='#13A07A', b2o=.35, ink='#0B0F0E', txt='#FFF6E6', hl_bg='#FFC83D', hl_fg='#0E2A22', scr='#fff',
           ring='rgba(255,255,255,.95)', flash='#FFC83D', wipe='#0B5D45', wipe2='#13A07A', wipe3='#FFF6E6', pill_bg='#FFC83D', pill_fg='#0E2A22', logo='quiddo-negativo.svg', sym_op=.35)
def cfg(m):
    return dict(id='ADC-QD-07', ver='v2', campeao=m['podio'] + CAMP, capa_t=1.5, rev_lag=2.0, foco=dict(rev=.43, rank=.39, pod=.47, fim=.52), rot0=(16, 4, 2),
        num=dict(), bichos=[('onca.coroa.-.2', 'l'), ('tucano.-.escuros.5', 'r'), ('capivara.-.escuros.1', 'l'), ('coruja.-.redondos.6', 'r')],
        pal=PAL, tv=tv_crop(f'{sys.argv[1]}/tv_q0_rev.png', f'{sys.argv[2]}/tv.png', .15, .02), tv_foco=(.04, .55), tv_sc=(1.0, 1.06), tv_phone=True, tv_top=dict(reel=700), tvp_w=350, tvp_dy=250,
        tvbig=(JOG, 'pessoas jogando juntas.', '', ''),
        still_t=m['q0_hero'] - .4, est_hook='Reunião geral com\n*todo mundo* acordado.',
        txt=dict(hook='Reunião geral\ncom *todo mundo*\nacordado.', b='Cada um no\n*seu celular.*', rev='Quem acerta,\n*ganha pontos.*',
                 d='', e='Quem acertou mais\n*leva o pódio.*'))
if __name__ == '__main__': roda(cfg, sys.argv)
