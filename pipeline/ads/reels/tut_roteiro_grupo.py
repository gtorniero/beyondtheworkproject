"""Roteiro do tutorial GRUPO (Android). Tempos de fonte pelas marcas da captura (tut_cap.py)."""
from tut_wa import wa
MODO = 'grupo'


def roteiro(m, how='android'):
    return dict(
        etiqueta='Demonstração com conversa fictícia',
        cenas=[
            # prévia: o resultado real, rápido
            dict(src=m['f0'] + 2.0, dur=2.2, txt='Como fazer a\n*retrospectiva\ndo seu grupo*', big=92, cam=[(0, .5, .32, 1.18), (2.2, .5, .32, 1.28)]),
            dict(src=m['t1_rvl'] + .5, dur=2.0, txt='Como fazer a\n*retrospectiva\ndo seu grupo*', big=92, cam=[(0, .5, .52, 1.12), (2.0, .5, .52, 1.2)]),
            dict(src=m['f6'] + 1.0, dur=1.9, txt='Como fazer a\n*retrospectiva\ndo seu grupo*', big=92, cam=[(0, .5, .45, 1.1), (1.9, .5, .45, 1.16)]),
            dict(src=m['fim'] + .8, dur=1.9, txt='É só seguir\n*6 passos:*', big=92, cam=[(0, .5, .5, 1.0)]),
            # 1 · site
            dict(src=m['inicio'] + .2, dur=3.7, passo='PASSO 1 · NO SITE', txt='Abra *retrozap.com.br*, escolha *Grupos* e toque em *Começar*.',
                 cam=[(0, .5, .45, 1.22)]),
            dict(src=m['caminho'] + .3, dur=4.0, passo='PASSO 1 · NO SITE', txt='Toque em *Preciso exportar*: o site mostra onde tocar.',
                 cam=[(0, .5, .3, 1.55)]),
            # 2 · WhatsApp (guia do próprio site) e 3 · arquivo
            *wa(m, MODO, how),
            dict(src=m['lembrete'] + .2, dur=3.4, rate=1.2, passo='PASSO 3 · DE VOLTA AO SITE', txt='Leia o lembrete e toque em *Entendi, bora!*',
                 cam=[(0, .5, .42, 1.3)]),
            # 4 · turma
            dict(src=m['turma'] + .2, dur=4.6, rate=1.6, passo='PASSO 4 · A TURMA', txt='Confira quem está no grupo e toque em *Começar*.',
                 cam=[(0, .5, .45, 1.15)]),
            # 5 · cerimônia
            dict(src=m['ato1'] + .4, dur=4.2, rate=2.1, passo='PASSO 5 · A CERIMÔNIA', txt='Primeiro, a história do grupo em números.',
                 cam=[(0, .5, .45, 1.12)]),
            dict(src=m['spoiler'] + .3, dur=3.0, passo='PASSO 5 · A CERIMÔNIA', txt='Quer suspense? *Mande o spoiler* e deixe a galera palpitar.',
                 cam=[(0, .5, .55, 1.15)]),
            dict(src=m['t1_podio'] + .6, dur=5.2, rate=1.45, passo='PASSO 5 · A CERIMÔNIA', txt='Depois, revele os troféus, *um por um.*',
                 cam=[(0, .5, .5, 1.1)]),
            dict(src=m['f0'] + .3, dur=2.6, passo='PASSO 5 · A CERIMÔNIA', txt='No fim, o ano do grupo *em números.*', cam=[(0, .5, .38, 1.2)]),
            dict(src=m['f6'] + .5, dur=2.4, passo='PASSO 5 · A CERIMÔNIA', txt='No fim, o ano do grupo *em números.*', cam=[(0, .5, .45, 1.12)]),
            # 6 · compartilhar
            dict(src=m['fim'] + .4, dur=2.6, passo='PASSO 6 · MANDE NO GRUPO', txt='Em *Mídias do grupo*, escolha uma imagem e toque em *Salvar ou compartilhar.*',
                 cam=[(0, .5, .4, 1.12)]),
            dict(src=m['carr_prox'] - .7, dur=5.6, rate=(m['compartilhar'] + 2.0 - m['carr_prox'] + .7) / 5.6, passo='PASSO 6 · MANDE NO GRUPO',
                 txt='Em *Mídias do grupo*, escolha uma imagem e toque em *Salvar ou compartilhar.*',
                 cam=[(0, .5, .42, 1.12), (3.0, .5, .5, 1.2)],
                 notas=[(2.4, 0, 'O celular abre as opções: escolha o <b>WhatsApp</b> e o grupo.')]),
        ],
        fim_dur=4.2,
        fim=dict(titulo='Agora é a vez\ndo *seu grupo.*', oferta='O 1º grupo é grátis. Sem cadastro.'),
    )
