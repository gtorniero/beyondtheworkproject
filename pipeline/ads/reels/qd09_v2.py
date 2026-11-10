"""ADC-QD-09 v2 · Treinamento para ser lembrado (linha corporativa). Look verde mata, TV do instrutor em destaque, % que acertou gigante. Sem pontos."""
import sys
from qd_corp8 import roda, tv_crop
CAMP = 8.5
PAL = dict(bg='#0B5D45', bg0='rgba(11,93,69,0)', blob1='#13A07A', b1o=.75, blob2='#FFC83D', b2o=.28, ink='#0E2A22', txt='#FFF6E6', hl_bg='#FFC83D', hl_fg='#0E2A22', scr='#fff',
           ring='rgba(255,255,255,.95)', flash='#FFF6E6', wipe='#13A07A', wipe2='#FFC83D', wipe3='#0E2A22', pill_bg='#FFC83D', pill_fg='#0E2A22', logo='quiddo-negativo.svg', sym_op=.4)
def cfg(m):
    return dict(id='ADC-QD-09', ver='v2', campeao=m['podio'] + CAMP, capa_t=1.5, rev_lag=2.0, foco=dict(rev=.43, rank=.39, pod=.44, fim=.44), rot0=(-4, 0, 0),
        num=dict(), bichos=[('coruja.-.redondos.6', 'l'), ('jabuti.palha.redondos.3', 'r'), ('tucano.bone.-.5', 'l'), ('gato.coroa.-.6', 'r')],
        pal=PAL, tv=tv_crop(f'{sys.argv[1]}/tv_q0_rev.png', f'{sys.argv[2]}/tv.png', .15, .02), tv_foco=(.5, .55), tv_sc=(1.04, 1.14), tv_long=True, tv_top=dict(reel=800, feed=520, sq=420), big_em=dict(reel=2.4, feed=2.0, sq=1.6),
        tvbig=(93, 'acertaram na hora.', '', '%'),
        still_t=m['q0_hero'] - .4, est_hook='Treinamento para\nser *lembrado.*',
        txt=dict(hook='Treinamento\npara ser\n*lembrado.*', b='Quiz no fim,\n*pelo celular.*', rev='', d='', e='Você vê na hora\n*quem entendeu.*'))
if __name__ == '__main__': roda(cfg, sys.argv)
