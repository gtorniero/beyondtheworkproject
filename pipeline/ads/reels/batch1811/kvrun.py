"""18/11 (Gui): 4 ADs do TÊNIS DNA (RUN DNA), que agora é 100% grátis e leva ao Mercado Livre (link afiliado no resultado).
Foco: grátis; como o motor funciona; tênis é caro, teste antes; compre sem se arrepender. Campanha de corredores. Números só do site (sportdna.com.br/run, 18/11)."""
import sys, asyncio
import kvx
K = kvx.K; PH = K.PH
K.SP['run'] = dict(c='#FF8A3D', logo='rundna-logo-fundo-escuro.svg', cta='Descobrir meu tênis grátis', url='sportdna.com.br/run', fine='100% grátis · 3 minutos · sem cadastro.')
kvx.THEME['run'] = ('#0A0A0A', '#0E4D64')
SPEC = {
 'ADC-RN-06-v1': dict(sp='run', title='Qual tênis de corrida é *o seu?* Grátis.', kick='100% grátis', ph=PH('run2_land.jpg'),
                      nums=[('100%', 'grátis: teste e relatório completo, sem cadastro e sem cartão'), ('19', 'perguntas sobre o seu corpo, a sua corrida e o seu objetivo')],
                      post='Em 3 minutos você sai com o seu pódio de tênis.'),
 'ADC-RN-07-v1': dict(sp='run', title='Tênis de quase R$&nbsp;1.000? *Teste antes.*', kick='Antes de comprar', ph=PH('run2_res.jpg'),
                      nums=[('212', 'tênis de 13 marcas cruzados com o seu corpo e o seu treino'), ('Grátis', 'o relatório completo, com o preço de cada finalista')],
                      post='Você sabe quanto vai gastar antes de abrir a loja.'),
 'ADC-RN-08-v1': dict(sp='run', title='Compre o tênis certo. *Sem se arrepender.*', kick='Sem arrependimento', ph=PH('run2_meli.jpg'),
                      nums=[('3 min', 'e você sai com o pódio dos tênis que combinam com você'), ('1 toque', 'do resultado até a loja, com o link pronto pra comprar')],
                      post='Grátis, sem cadastro, sem cartão.'),
 'ADC-RN-09-v1': dict(sp='run', title='Como o motor *escolhe o seu tênis.*', kick='O motor', ph=PH('run2_km.jpg'),
                      nums=[('1.755', 'reviews lidas, de quem testa tênis e de clientes'), ('41', 'estudos científicos por trás das regras')],
                      chips=('Peso', 'Espuma', 'Drop', 'Durabilidade', 'Preço'), post='Nenhuma marca paga para aparecer. 100% grátis.'),
}
kvx.SPEC.update(SPEC); K.HERO.update({v: None for v in SPEC})
if __name__ == '__main__':
    mode = sys.argv[1]; ids = sys.argv[2:] or list(SPEC); out = kvx.HERE / 'out'
    async def go():
        async with K.async_playwright() as p:
            b = await p.chromium.launch(); pg = await b.new_page()
            if mode == 'hero':
                for v in ids:
                    d = out / v; d.mkdir(parents=True, exist_ok=True)
                    for f in ('sq', 'story'):
                        W, H = K.FMT[f]; await K.shot(pg, kvx.page(v, f), d / f'{v}-{f}.png', W, H)
            else:
                for v in ids: (out / v).mkdir(parents=True, exist_ok=True)
                await asyncio.gather(*[K.motion(b, v, 'story', out / v) for v in ids])
            await b.close()
    asyncio.run(go())
