"""ADC-RN-03 v2 · RUN DNA na referência (dna_ref.py). Captura: rn_capture.py → quadros 30 fps."""
from dna_ref import main
main(dict(v='ADC-RN-03-v2', color='#FF8A3D', logo='rundna-logo-fundo-escuro.svg', icon='rundna-icone-sem-fundo-cor.svg', url='sportdna.com.br/run', cta_k='19 perguntas · 212 tênis · 13 marcas',
    hook='Seu tênis combina\ncom *você?*', hook_tap=4.3, hook_f=(.25, .48),
    i2='O teste pergunta\nonde *dói.*', i2_tap=9.45, i2_f=(.5, .48),
    motor='Aí o motor\n*cruza tudo.*', ana=26.03, ana_rate=.7, n_main=(212, 'int', 'tênis cruzados com você'),
    kick='Por trás do motor', wall_hd='Não é *chute.*', wall=[(1755, 'mil', 'reviews lidas'), (41, 'int', 'estudos científicos'), (5000, 'mil', 'perfis de corredor simulados')],
    top_hd='Os *3* que mais\ncombinam.', top=31.0, rows=(.34, .46, .59), btn=.68, pcts=(96, 94, 91),
    why_hd='E o *porquê*\nde cada um.', card=41.0, card_f=(.5, .42), chip_k='Seu perfil de corredor', chip='Corredor de Prova'))
