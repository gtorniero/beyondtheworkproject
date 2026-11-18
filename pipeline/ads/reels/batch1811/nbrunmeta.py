"""4 ADs do TÊNIS DNA (RUN DNA), 18/11: 100% grátis; resultado com link afiliado do Mercado Livre. Campanha de corredores."""
from nbmeta import U
DIR = ("Lote 18/11 · TÊNIS DNA (RUN DNA), pedido do Gui: 4 ADs, foco em grátis, como o motor escolhe, tênis é caro (teste antes) e comprar sem se arrepender. "
       "Visual do RK-05 na cor do RUN (#FF8A3D). Motion 9:16 com música + estático 1:1.")
RN_D = ["Telas reais do RUN DNA (sportdna.com.br/run), capturadas em 18/11 com o relatório pronto do próprio site.",
        "Marcas e modelos de tênis borrados na tela, e também o nome da loja (sem marca de terceiros na arte). O link de compra no resultado é afiliado do Mercado Livre (como o site já mostra).",
        "Números do site: 100% grátis, sem cadastro, sem cartão; 19 perguntas; 3 minutos; 212 tênis de 13 marcas; 1.755 reviews; 41 estudos; nenhuma marca paga para aparecer.",
        "Sem promessa médica. Música Mixkit. Sem voz: não precisa do rótulo de IA."]
B = dict(brand='SPORT DNA', direitos=RN_D, publico='Corredores de 20 a 55 anos (interesses: corrida de rua, maratona, meia maratona, treino, apps de corrida, tênis de corrida), inclusive iniciantes.',
         objetivo='Campanha de corredores: levar ao teste grátis do RUN DNA; a venda acontece no clique para o Mercado Livre (afiliado).', cta='Na arte: "Descobrir meu tênis grátis". Botão do anúncio: Saiba mais.', notes='')
def rn(i, utm, **k):
    d = dict(B); d.update(k); d['id'] = f'ADC-RN-{i:02d}'; d['ver'] = 'v1'; d['mudou'] = 'Peça nova: TÊNIS DNA grátis (18/11).'
    d['url'] = f'https://sportdna.com.br/run/?{U}&utm_campaign=rn_corredores&utm_term={utm}&utm_content=ADC-RN-{i:02d}-v1'; return d
ADS = [
 rn(6, 'gratis', track=('1076', 40.0), title='TÊNIS DNA · Qual tênis de corrida é o seu? 100% grátis',
    hipotese='"Grátis" + "qual é o seu" é o gancho mais direto. O RUN agora é 100% grátis: tira a barreira do preço.',
    copy='Qual tênis de corrida é o seu? 🏃\nResponda 19 perguntas sobre seu corpo, sua corrida e seu objetivo e receba o relatório completo com o pódio dos tênis que combinam com você. 100% grátis, sem cadastro e sem cartão.', titulo='Descubra o seu tênis, grátis'),
 rn(7, 'caro', track=('644', 50.0), title='TÊNIS DNA · Tênis de quase R$ 1.000? Teste antes',
    hipotese='Tênis bom é caro: o teste grátis evita gastar errado. O resultado mostra o preço de cada finalista.',
    copy='Tênis de corrida de quase R$ 1.000? Teste antes de comprar. 🏃\nO RUN DNA cruza o seu corpo e o seu treino com 212 tênis de 13 marcas e mostra o preço de cada finalista. Você sabe quanto vai gastar antes de abrir a loja. 100% grátis.', titulo='Teste antes de comprar'),
 rn(8, 'arrependimento', track=('1005', 30.0), title='TÊNIS DNA · Compre o tênis certo, sem se arrepender',
    hipotese='Medo de errar a compra. Do resultado ao link de compra em um toque: reduz o atrito até o Mercado Livre.',
    copy='Compre o tênis de corrida certo. Sem se arrepender. 🏃\nEm 3 minutos você sai com o pódio dos tênis que combinam com você e o link pronto pra comprar. 100% grátis, sem cadastro.', titulo='Sem se arrepender'),
 rn(9, 'motor', track=('859', 40.0), title='TÊNIS DNA · Como o motor escolhe o seu tênis',
    hipotese='Prova de autoridade para o corredor que pesquisa: 1.755 reviews, 41 estudos, nenhuma marca paga.',
    copy='Como o RUN DNA escolhe o seu tênis de corrida. 🏃\n1.755 reviews lidas, 41 estudos científicos e 212 tênis cruzados com o seu corpo e o seu treino: peso, espuma, drop, durabilidade e preço. Nenhuma marca paga para aparecer. 100% grátis.', titulo='Como o motor escolhe'),
]
