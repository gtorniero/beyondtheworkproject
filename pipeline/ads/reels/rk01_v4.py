"""ADC-RK-01 v4 · RACKET DNA na referência (dna_ref.py). Captura: dna_capture.py racket → quadros 30 fps."""
from dna_ref import main
main(dict(v='ADC-RK-01-v4', color='#DDF247', logo='racketdna-logo-fundo-escuro.svg', icon='racketdna-icone-sem-fundo-cor.svg', url='sportdna.com.br/racket', cta_k='183 raquetes · 46 variáveis por raquete',
    hook='Qual raquete\né a *sua?*', hook_tap=5.35, hook_f=(.66, .43),
    i2='Até se o braço\njá *doeu.*', i2_tap=11.35, i2_f=(.5, .48),
    motor='Aí o motor\n*cruza tudo.*', ana=34.57, ana_rate=.36, n_main=(183, 'int', 'raquetes cruzadas com o seu jogo'),
    kick='Por trás do motor', wall_hd='Não é *chute.*', wall=[(670, 'int', 'avaliações de testadores lidas'), (46, 'int', 'variáveis por raquete'), (3000, 'mil', 'perfis simulados por teste')],
    top_hd='As *3* que mais\ncombinam.', top=38.2, rows=(.40, .53, .67), btn=.76, pcts=(96, 96, 94),
    why_hd='E o *porquê*\nde cada uma.', card=47.4, card_f=(.5, .40), chip_k='Seu DNA de jogo', chip='Atacante de fundo<br>de topspin moderado'))
