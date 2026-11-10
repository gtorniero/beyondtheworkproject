"""ADC-SF-03 v1 · SURF DNA na referência (dna_ref.py). Captura: dna_capture.py surf → quadros 30 fps."""
from dna_ref import main
main(dict(v='ADC-SF-03-v1', color='#6CCFF6', logo='surfdna-logo-fundo-escuro.svg', icon='surfdna-icone-sem-fundo-cor.svg', url='sportdna.com.br/surf', cta_k='13 tipos · 416 tamanhos · 422 casos reais',
    hook='Sua prancha\né a *certa?*', hook_tap=5.35, hook_f=(.3, .43),
    i2='O teste pergunta\ncomo você *surfa.*', i2_tap=14.25, i2_f=(.5, .48),
    motor='Aí o motor\n*cruza tudo.*', ana=30.58, ana_rate=.33, n_main=(416, 'int', 'tamanhos comparados medida por medida'),
    kick='Por trás do motor', wall_hd='Não é *chute.*', wall=[(422, 'int', 'casos reais na calibração'), (13, 'int', 'tipos de prancha na disputa'), (17, 'int', 'medidas na ficha técnica')],
    top_hd='As *3* que mais\ncombinam.', top=34.0, rows=(.40, .52, .635), btn=.72, pcts=(96, 88, 84),
    why_hd='E o *porquê*\nde cada uma.', card=43.2, card_f=(.5, .40), chip_k='Seu DNA de surf', chip='Surfista de curvas<br>de onda pequena'))
