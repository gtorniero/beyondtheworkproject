"""Roteiro do tutorial CASAL (iPhone). Tempos de fonte pelas marcas da captura (tut_cap.py)."""
from tut_wa import wa
MODO = 'casal'


def roteiro(m, how='iphone'):
    return dict(
        etiqueta='Demonstração com conversa fictícia',
        cenas=[
            # prévia
            dict(src=m['f0'] + 2.0, dur=2.2, txt='Como fazer a\n*retrospectiva\nde casal*', big=92, cam=[(0, .5, .32, 1.18), (2.2, .5, .32, 1.28)]),
            dict(src=m['t2_raspa'] + 3.2, dur=2.0, txt='Como fazer a\n*retrospectiva\nde casal*', big=92, cam=[(0, .5, .45, 1.12), (2.0, .5, .45, 1.2)]),
            dict(src=m['f3'] + .8, dur=1.9, txt='Como fazer a\n*retrospectiva\nde casal*', big=92, cam=[(0, .5, .35, 1.15)]),
            dict(src=m['fim'] + .8, dur=1.9, txt='É só seguir\n*6 passos:*', big=92, cam=[(0, .5, .5, 1.0)]),
            # 1 · site
            dict(src=m['inicio'] + .2, dur=3.8, rate=1.6, passo='PASSO 1 · NO SITE', txt='Abra *retrozap.com.br*, escolha *Casais* e toque em *Começar*.',
                 cam=[(0, .5, .42, 1.22)]),
            dict(src=m['caminho'] + .3, dur=3.4, rate=1.15, passo='PASSO 1 · NO SITE', txt='Toque em *Preciso exportar*: o site mostra onde tocar.',
                 cam=[(0, .5, .3, 1.55)]),
            # 2 · WhatsApp (guia do próprio site) e 3 · arquivo
            *wa(m, MODO, how),
            dict(src=m['lembrete'] + .2, dur=2.8, rate=1.45, passo='PASSO 3 · DE VOLTA AO SITE', txt='Leia o lembrete e toque em *Entendi, bora!*',
                 cam=[(0, .5, .42, 1.3)]),
            dict(src=m['quem_sao'] + .3, dur=3.0, rate=1.15, passo='PASSO 3 · DE VOLTA AO SITE', txt='Toque em *Somos um casal.*', cam=[(0, .5, .45, 1.35)]),
            # 4 · nomes
            dict(src=m['turma'] + .2, dur=3.6, rate=2.0, passo='PASSO 4 · VOCÊS DOIS', txt='Confira os nomes de vocês e toque em *Começar*.',
                 cam=[(0, .5, .45, 1.15)]),
            dict(src=m['ato1'] + .4, dur=3.4, rate=2.6, passo='PASSO 4 · VOCÊS DOIS', txt='Primeiro, a história de vocês em números.',
                 cam=[(0, .5, .45, 1.12)]),
            # 5 · acesso
            dict(src=m['paywall'] + .3, dur=4.4, passo='PASSO 5 · OS TROFÉUS', txt='Para ver os troféus: *R$ 8,99*, pagamento único, no Pix ou no cartão.',
                 cam=[(0, .5, .25, 1.25)],
                 notas=[(1.2, 0, 'A retrospectiva de casal é paga. Grátis é o 1º grupo.')]),
            dict(src=m['pos_pagamento'] + .3, dur=2.6, passo='PASSO 5 · OS TROFÉUS', txt='Mande o *spoiler* pro seu amor e apostem quem leva cada um.',
                 cam=[(0, .5, .55, 1.15)]),
            dict(src=m['t1_palpite'] + .4, dur=3.4, rate=2.1, passo='PASSO 5 · OS TROFÉUS', txt='Dê seu palpite e *raspe* pra revelar.',
                 cam=[(0, .5, .5, 1.1)]),
            dict(src=m['t2_raspa'] + .2, dur=3.4, rate=1.9, passo='PASSO 5 · OS TROFÉUS', txt='Dê seu palpite e *raspe* pra revelar.',
                 cam=[(0, .5, .5, 1.1)]),
            dict(src=m['f0'] + .3, dur=2.2, passo='PASSO 5 · OS TROFÉUS', txt='No fim, o ano de vocês *em números.*', cam=[(0, .5, .38, 1.2)]),
            # 6 · compartilhar
            dict(src=m['fim'] + .4, dur=2.6, passo='PASSO 6 · MANDE PRO SEU AMOR', txt='Em *Mídias de vocês*, escolha uma imagem e toque em *Salvar ou compartilhar.*',
                 cam=[(0, .5, .4, 1.12)]),
            dict(src=m['carr_prox'] - .7, dur=5.4, rate=(m['compartilhar'] + 2.0 - m['carr_prox'] + .7) / 5.4, passo='PASSO 6 · MANDE PRO SEU AMOR',
                 txt='Em *Mídias de vocês*, escolha uma imagem e toque em *Salvar ou compartilhar.*',
                 cam=[(0, .5, .42, 1.12), (3.0, .5, .5, 1.2)],
                 notas=[(2.4, 0, 'O celular abre as opções: escolha o <b>WhatsApp</b> e a conversa de vocês.')]),
        ],
        fim_dur=4.0,
        fim=dict(titulo='Agora é a vez\nde *vocês dois.*', oferta='Retrospectiva de casal: R$ 8,99,<br>pagamento único, no Pix ou no cartão.'),
    )
