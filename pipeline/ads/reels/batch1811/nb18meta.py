"""Metadados do lote de ADs de 18/11: Retrozap com pôsteres reais (RZ-19 a RZ-26) e RACKET/SURF DNA (RK-15 a RK-19, SF-13 a SF-16)."""
from nbmeta import RK_D, SF_D, U
DIR = ("Lote 18/11, foco em ADs (pedido do Gui). Visual do RK-05: título direto, número grande, botão. "
       "Motion 9:16 de 12 s com música de banco (Mixkit) e estático 1:1. Você aprova esses dois; as outras dimensões saem depois.")
RZP = ["Pôsteres REAIS do app do Retrozap (os mesmos que o usuário baixa), gerados no site local com conversa fictícia: Dani & Cris (casal) e Turma do Churras (grupo). Nomes e números inventados, sem rosto nem voz de pessoa real.",
       "Ranking Top Brasil: o pôster é o do app; as posições mostradas são da conversa fictícia. A copy não promete posição: convida a ver em que o casal/grupo fica no Top.",
       "Oferta conferida no site: 1º grupo grátis; casal pago, R$ 13,99 até 30/11 (dezembro: versão R$ 8,99).",
       "Música Mixkit (licença livre, uso comercial). Sem voz: não precisa do rótulo de IA."]
RC = dict(brand='Retrozap', direitos=RZP, publico='Casais de 20 a 40 anos (interesses: relacionamento, presentes criativos, aniversário de namoro, Natal).',
          objetivo='Vender a retrospectiva de casal (R$ 13,99 até 30/11).', cta='Na arte: "Fazer a de vocês". Botão do anúncio: Saiba mais.',
          notes='Preço R$ 13,99 na arte: rodar até 30/11. Em dezembro sai a versão R$ 8,99.')
RG = dict(brand='Retrozap', direitos=RZP, publico='Adultos de 18 a 45 anos com grupos ativos no WhatsApp (amigos, família, trabalho; interesses: amigos, memes, festas de fim de ano).',
          objetivo='Gerar retrospectivas de grupo (1º grupo grátis) e levar ao Premium.', cta='Na arte: "Fazer a do meu grupo". Botão do anúncio: Saiba mais.', notes='')
def rz(i, base, utm, **k):
    d = dict(base); d.update(k); d['id'] = f'ADC-RZ-{i}'; d['url'] = f'https://retrozap.com.br/?{"m=casal&" if base is RC else ""}{U}&utm_campaign={utm}&utm_content=ADC-RZ-{i}-v1'; return d
RKB = dict(brand='SPORT DNA', direitos=RK_D, publico='Tenistas amadores de 25 a 55 anos (interesses: tênis, raquetes, artigos esportivos).',
           objetivo='Levar ao teste RACKET DNA (avaliação grátis) e vender o relatório completo (R$ 19,99).', cta='Na arte: botão do teste. Botão do anúncio: Saiba mais.', notes='')
SFB = dict(brand='SPORT DNA', direitos=SF_D, publico='Surfistas iniciantes e intermediários de 20 a 50 anos (interesses: surf, pranchas, shapers).',
           objetivo='Levar ao teste SURF DNA (prévia grátis) e vender o relatório completo (R$ 19,99).', cta='Na arte: "Fazer o teste". Botão do anúncio: Saiba mais.', notes='')
def dn(pref, i, base, utm, **k):
    d = dict(base); d.update(k); d['id'] = f'ADC-{pref}-{i}'; sl = 'racket' if pref == 'RK' else 'surf'
    d['url'] = f'https://sportdna.com.br/{sl}/?{U}&utm_campaign={utm}&utm_content=ADC-{pref}-{i}-v1'; return d
ADS = [
 rz(19, RC, 'rz_casal_posteres', track=('1005', 4.0), title='Casal · O mapa astral do WhatsApp de vocês',
    hipotese='O pôster é o produto que a pessoa posta. Mapa astral é o mais "compartilhável" do casal e curioso sem precisar explicar.',
    copy='O mapa astral do WhatsApp de vocês. ✨\nSol em Tagarela, Lua em Áudio, ascendente na frase que vocês mais falam: tudo tirado da conversa do casal. Vem junto com o recibo do amor, o boletim e o placar de vocês dois.\nPagamento único, sem assinatura. Nada sai do seu celular.', titulo='O mapa astral do casal'),
 rz(20, RC, 'rz_casal_posteres', track=('859', 6.0), title='Casal · Quem paga o jantar? O recibo do amor',
    hipotese='Provocação de casal ("quem paga o jantar?") + recibo item por item: gera marcação do parceiro nos comentários.',
    copy='Quem paga o jantar? O recibo do amor responde. 🧾💌\nQuem mandou mais "te amo", quem puxou o papo, quem mandou mais boa noite: item por item, tirado da conversa de vocês.\nPagamento único, sem assinatura. Nada sai do seu celular.', titulo='Quem paga o jantar?'),
 rz(21, RC, 'rz_casal_posteres', track=('1063', 3.0), title='Casal · Boletim do casal: aprovados pra 2027?',
    hipotese='Formato escolar (nota de cada um) é rápido de ler e dá vontade de comparar.',
    copy='Boletim do casal: vocês passam de ano? 📒\nRomantismo, pontualidade, comunicação, iniciativa: nota de cada um, tirada da conversa de vocês. Mais o mapa astral, o recibo do amor e o placar.\nPagamento único, sem assinatura. Nada sai do seu celular.', titulo='Boletim do casal'),
 rz(22, RC, 'rz_casal_ranking', track=('801', 2.0), title='Casal · Vocês contra os casais do Brasil (ranking)',
    hipotese='Competição: comparar o casal com o Brasil (Top %) é o gancho que o Gui pediu.',
    copy='Vocês contra os casais do Brasil. 🇧🇷💘\nMensagens, risadas, declarações de amor, áudios: veja em que vocês ficam no Top do Brasil entre os casais do Retrozap. Só os números saem do celular, sem nomes nem textos.\nPagamento único, sem assinatura.', titulo='Vocês contra o Brasil'),
 rz(23, RG, 'rz_grupo_ranking', track=('1076', 0.0), title='Grupo · Seu grupo contra o Brasil inteiro (ranking)',
    hipotese='Pedido do Gui: "descubra o seu grupo contra todos os rankings do Brasil". Competição entre grupos + 1º grátis.',
    copy='Seu grupo contra o Brasil inteiro. 🇧🇷\nRisada, madrugada, figurinhas, mensagens: veja em que o seu grupo fica no Top do Brasil entre os grupos do Retrozap. Só os números saem do celular, sem nomes nem textos.\nO 1º grupo é grátis.', titulo='Seu grupo contra o Brasil'),
 rz(24, RG, 'rz_grupo_posteres', track=('830', 4.0), title='Grupo · Procura-se: o fantasma do grupo',
    hipotese='Todo grupo tem um que some. Pôster de "procura-se" é meme pronto para marcar a pessoa.',
    copy='Procura-se: o fantasma do seu grupo. 👻\nTodo grupo tem um que visualiza e não responde. A retrospectiva acha, e ele ganha o próprio pôster. Mais troféus, ranking e o Plantão do Zap.\nO 1º grupo é grátis. Nada sai do seu celular.', titulo='Procura-se no seu grupo'),
 rz(25, RG, 'rz_grupo_posteres', track=('5', 2.0), title='Grupo · URGENTE: seu grupo virou notícia (Plantão do Zap)',
    hipotese='Formato manchete chama atenção no feed e o grupo vira assunto.',
    copy='URGENTE: seu grupo virou notícia. 🚨\nO Plantão do Zap conta 2026 do grupo em manchete: quem falou mais, o dia do caos, quem sumiu. Mais troféus, o fantasma e as mais tocadas.\nO 1º grupo é grátis. Nada sai do seu celular.', titulo='Seu grupo virou notícia'),
 rz(26, RG, 'rz_grupo_posteres', track=('1057', 5.0), title='Grupo · As mais tocadas do grupo (Rádio Turma FM)',
    hipotese='A gíria oficial do grupo é o tipo de detalhe que faz o grupo inteiro rir e compartilhar.',
    copy='As mais tocadas do seu grupo. 📻\nA gíria oficial, quem mais falou, o assunto do ano: a Rádio Turma FM toca o 2026 do grupo. Mais troféus, ranking e pôsteres.\nO 1º grupo é grátis. Nada sai do seu celular.', titulo='As mais tocadas do grupo'),
 dn('RK', 15, RKB, 'rk_gratis_avaliacao', track=('644', 20.0), sp='rkfree', title='RACKET grátis · Você joga com a raquete errada?',
    hipotese='Mudança do produto: o grátis já avalia a raquete atual. Pergunta direta + tela "Sua atual × a nova".',
    copy='Você joga com a raquete errada? 🎾\nAvalie a sua raquete de graça: o RACKET DNA compara peso e balanço da sua com o ideal para o seu jogo e o seu braço. Se quiser trocar, o relatório completo mostra as 3 que mais combinam.', titulo='Avalie sua raquete grátis'),
 dn('RK', 16, RKB, 'rk_gratis_avaliacao', track=('780', 10.0), sp='rkfree', title='RACKET grátis · A sua ficha ideal, nota por nota',
    hipotese='Ficha ideal (peso, cabeça, swingweight, balanço) é útil mesmo sem comprar: leva a pessoa para a loja com o teste na mão.',
    copy='A sua raquete ideal, nota por nota. 🎾\nDe graça, o RACKET DNA monta a sua ficha ideal: peso, tamanho de cabeça, swingweight e balanço. Leve para a loja ou compare com a sua.', titulo='Sua ficha ideal, grátis'),
 dn('RK', 17, RKB, 'rk_natal', track=('1005', 12.0), title='RACKET Natal · Raquete de presente? Acerte',
    hipotese='Dezembro: presente de tenista é comum e arriscado. O teste vira "seguro" do presente.',
    copy='Vai dar raquete de presente? Acerte. 🎄🎾\nFaça o teste junto com quem vai ganhar: o RACKET DNA mostra as 3 raquetes que mais combinam com o jogo dele. Prévia grátis; relatório completo por R$ 19,99.', titulo='Raquete de presente? Acerte'),
 dn('RK', 18, RKB, 'rk_setup', track=('859', 14.0), title='RACKET · Raquete certa, setup errado?',
    hipotese='Público mais avançado: corda e tensão importam tanto quanto a raquete. 279.990 combinações reforça o motor.',
    copy='Raquete certa, setup errado? 🎾\nRaquete, grip, corda, espessura e tensão: são 279.990 combinações. O RACKET DNA acha a sua. Prévia grátis; relatório completo por R$ 19,99.', titulo='O setup completo'),
 dn('RK', 19, RKB, 'rk_perfil', track=('1063', 20.0), title='RACKET · Seu perfil de jogo em um hexágono',
    hipotese='Visual de "perfil de jogador" (radar) é curioso e compartilhável, como um card de videogame.',
    copy='O seu perfil de jogo em um hexágono. 🎾\nPotência, controle, spin, conforto, manobra e estabilidade: veja o seu perfil e compare a sua raquete atual com a recomendada. Prévia grátis.', titulo='Seu perfil de jogo'),
 dn('SF', 13, SFB, 'sf_litragem', track=('644', 40.0), title='SURF · Sua prancha tem os litros certos?',
    hipotese='Litragem é a dúvida nº 1 de quem compra prancha. Número concreto (34,2 L para 70 kg) e "e para você?".',
    copy='Sua prancha tem os litros certos? 🏄\nLitragem decide se você rema e entra na onda. Em 3 minutos, o SURF DNA calcula a sua pelo seu peso, nível e mar. Prévia grátis, sem cadastro.', titulo='Os seus litros certos'),
 dn('SF', 14, SFB, 'sf_natal', track=('801', 12.0), title='SURF Natal · Prancha de presente? Acerte as medidas',
    hipotese='Presente de surfista é caro e fácil de errar; o teste dá as medidas.',
    copy='Vai dar prancha de presente? Acerte as medidas. 🎄🏄\nFaça o teste junto com quem vai ganhar: o SURF DNA entrega 17 medidas prontas para a loja ou o shaper. Prévia grátis; relatório completo por R$ 19,99.', titulo='Prancha de presente? Acerte'),
 dn('SF', 15, SFB, 'sf_shaper', track=('830', 14.0), title='SURF · Vai encomendar no shaper? Leve a ficha',
    hipotese='Quem encomenda prancha sob medida precisa das medidas; ficha técnica pronta é utilidade direta.',
    copy='Vai encomendar prancha no shaper? Leve a ficha pronta. 🏄\nComprimento, largura, espessura, litros e mais: 17 medidas do SURF DNA, calculadas para o seu surf. Prévia grátis · 3 minutos · sem cadastro.', titulo='A ficha para o shaper'),
 dn('SF', 16, SFB, 'sf_usada', track=('5', 10.0), title='SURF · Prancha usada? Confira antes de pagar',
    hipotese='Mercado de usadas é grande; conferir antes de pagar é uma dor concreta.',
    copy='Vai comprar prancha usada? Confira antes de pagar. 🏄\nO SURF DNA compara 416 tamanhos de 35 modelos com o seu surf e mostra o que combina com você. Relatório completo por R$ 19,99, contra R$ 1.500 a R$ 4.000 de uma prancha. Prévia grátis.', titulo='Prancha usada? Confira'),
]
