"""Cenas do WhatsApp (guia ilustrado do próprio site, V2_PASSOS) e da escolha do arquivo, por aparelho. Textos iguais aos do site em 11/11."""
ZOOM = [(0, .5, .64, 1.5), (None, .5, .66, 1.58)]


def _cam(d, z=ZOOM):
    return [(0, *z[0][1:]), (d, *z[1][1:])]


def wa(m, modo, how):
    obj = 'o grupo' if modo == 'grupo' else 'a conversa'
    Z = 'PASSO 2 · NO WHATSAPP · ' + ('ANDROID' if how == 'android' else 'IPHONE')
    outro = ('Tem iPhone? Toque na aba <b>iPhone</b>' if how == 'android' else 'Tem Android? Toque na aba <b>Android</b>') + ': o site mostra os passos do seu celular.'
    nao = 'Não mande o arquivo para ninguém: é só salvar.'
    if how == 'android':
        cenas = [
            dict(src=m['passo1'] + .4, dur=6.2, txt=f'Abra {obj} e toque em *⋮* › *Mais* › *Exportar conversa*.', notas=[(1.4, 0, outro)]),
            dict(src=m['passo2'] + .4, dur=6.2, txt='Escolha *Sem mídia* e salve em *Arquivos* (Downloads) ou no *Drive*.', notas=[(1.6, 0, nao)]),
        ]
        ultimo = 'passo3'
        nota_arq = 'Procure em <b>Downloads</b> ou <b>Recentes</b>: “Conversa do WhatsApp com…”.'
    else:
        p1 = 'Abra o grupo e toque no *nome do grupo*, lá em cima.' if modo == 'grupo' else 'Abra a conversa e toque no *nome da pessoa*, lá em cima.'
        cenas = [
            dict(src=m['passo1'] + .4, dur=4.8, rate=1.1, txt=p1, notas=[(1.4, 0, outro)], z=[(0, .5, .62, 1.45), (0, .5, .62, 1.55)]),
            dict(src=m['passo2'] + .4, dur=5.0, rate=1.1, txt='Role até o fim, toque em *Exportar conversa* e escolha *Sem mídia*.'),
            dict(src=m['passo3'] + .4, dur=5.0, rate=1.1, txt='Toque em *Salvar em Arquivos*, escolha *Downloads* e *Salvar*.', notas=[(1.6, 0, nao)]),
        ]
        ultimo = 'passo4'
        nota_arq = 'Em <b>Recentes</b>, o primeiro da lista: “WhatsApp Chat - ….zip”.'
    out = []
    for c in cenas:
        z = c.pop('z', ZOOM)
        out.append(dict(c, passo=Z, cam=_cam(c['dur'], z), nota_y=36))
    da, ra, dv, rv = (5.0, 1.45, 4.9, 1.2) if how == 'android' else (4.2, 1.7, 4.2, 1.4)
    out.append(dict(src=m[ultimo] + .3, dur=da, rate=ra, passo=Z, txt='Toque em *Abrir o WhatsApp*, faça os passos e *volte para o site*.', cam=[(0, .5, .3, 1.4)]))
    out.append(dict(src=m['voltou'] + .1, dur=dv, rate=rv, passo='PASSO 3 · DE VOLTA AO SITE', txt='Toque para escolher o arquivo que você salvou.',
                    cam=[(0, .5, .35, 1.35)], notas=[(1.0, 0, nota_arq)]))
    return out
