"""Entradas da Mesa (aba ADs) para os 8 KVs SPORT DNA (kv_dna.py). Gera pipeline/ads/patch-dna-kv.json e, se receber o HTML
publicado mais recente da Mesa, injeta as entradas no manifesto (sem tocar em peças, votos ou outros ADs).
Uso: python3 kv_dna_mesa.py <pasta final dos KVs> [<index.html publicado> <saida.html>]"""
import hashlib, json, re, sys
from pathlib import Path
FIN = Path(sys.argv[1]); HERE = Path(__file__).resolve().parent
UTM = 'utm_source=meta&utm_medium=paid_social'
RK = dict(publico='Tenistas amadores 25–55 anos que vão trocar de raquete (interesses: tênis, torneios amadores, lojas de tênis).',
          objetivo='Tráfego para o teste RACKET DNA (diagnóstico grátis antes de pagar; relatório completo R$ 19,99, pagamento único).',
          path='https://sportdna.com.br/racket/', cta_art='Descobrir minha raquete →')
SF = dict(publico='Surfistas iniciantes e intermediários, 20–45 anos, cidades litorâneas (interesses: surf, escolas de surf, shapers, pranchas).',
          objetivo='Tráfego para o teste SURF DNA (prévia grátis; relatório completo R$ 19,99, pagamento único).',
          path='https://sportdna.com.br/surf/', cta_art='Descobrir minha prancha →')
COMUM_RK = ['Números do motor conferidos no site rodando a partir do código atual (gtorniero/sportdna, main 42f9455, 10/11/2026): 183 raquetes com specs medidas, 670 avaliações, 46 variáveis por raquete, 21 estudos, 379 casos de especialistas em 3 idiomas, 3.000 perfis simulados, 8.418 comparações e 279.990 combinações por teste.',
            'O site diz "Nenhuma raquete previne ou trata lesão": nenhum KV promete evitar lesão.']
COMUM_SF = ['Números do motor conferidos no site rodando a partir do código atual (gtorniero/sportdna, main 42f9455, 10/11/2026): 13 tipos, 416 tamanhos de 35 modelos, 422 casos reais, 17 medidas, 1.000+ fontes em 400+ sites, mais de 200 trilhões de pranchas possíveis; "Errar a prancha custa caro: uma nova sai por R$ 1.500 a R$ 4.000. Acertar custa R$ 19,99."']
TODOS = ['Tela no celular: captura real do teste (dna_capture.py, mesmo jogador/surfista coerente dos reels RK-01 v4 e SF-03 v1) ou da página do produto (kv_dna_stills.py). Na prévia, os nomes das 3 recomendadas aparecem borrados porque o próprio site esconde antes do pagamento.',
         'Logos oficiais (racketdna/surfdna-logo-fundo-escuro.svg), Archivo 800, Syne 800, DM Sans e JetBrains Mono; preto, grade técnica e a cor do esporte, como na referência ADC-RZ-08. Sem ilustração de equipamento, sem marca de terceiros, sem pessoas reais, sem etiqueta de exemplo. Sem IA generativa.']
K = [
 ('ADC-RK-03', RK, 'racket_kv_braco', 'RACKET KV: raquete errada, o braço paga',
  'Quem já sentiu o cotovelo tem medo de errar de novo; falar do custo no corpo (e não do preço) provoca mais. 21 estudos e 46 variáveis mostram que não é palpite.',
  'Raquete errada, o braço paga. 🎾\nRigidez, peso, balanço e a articulação que dói: o RACKET DNA avalia tudo antes de você pagar. São 46 variáveis cruzadas para cada raquete e 21 estudos científicos sobre braço e equipamento por trás das regras.\nVocê vê o diagnóstico antes de pagar.',
  'Raquete errada, o braço paga', 'Conforto no braço: tela real da pergunta "Onde dói ou doía?" do teste.'),
 ('ADC-RK-04', RK, 'racket_kv_seis', 'RACKET KV: não é uma escolha, são seis',
  'Mostrar que a compra tem 6 decisões (279.990 combinações) desmonta o "é só escolher a raquete" e cria a necessidade do teste.',
  'Raquete não é uma escolha. São seis. 🎾\nModelo, cabeça, grip, corda, espessura e tensão: 279.990 combinações, e uma decisão errada anula as outras certas. O RACKET DNA faz 8.418 comparações entre você e o catálogo a cada teste.\nVocê vê o diagnóstico antes de pagar.',
  'Raquete não é uma escolha. São seis.', 'Tela real da seção "Por que é fácil errar" da página do RACKET DNA.'),
 ('ADC-RK-05', RK, 'racket_kv_183', 'RACKET KV: 183 raquetes, uma é a sua',
  'Big number do catálogo + o resultado com % de combinação dá a sensação de escolha sob medida; os nomes borrados da prévia geram curiosidade.',
  '183 raquetes. Uma é a sua. 🎾\nO RACKET DNA cruza as suas respostas com as specs medidas de 183 raquetes, uma a uma, lê 670 avaliações de testadores e simula 3.000 perfis em cada teste de segurança. No fim, as 3 que mais combinam com o seu jogo.\nVocê vê o diagnóstico antes de pagar.',
  '183 raquetes. Uma é a sua.', 'Tela real da prévia do resultado (96%, 96%, 94%).'),
 ('ADC-RK-06', RK, 'racket_kv_idolo', 'RACKET KV: raquete do ídolo, golpe atrasado',
  'Provoca o erro mais comum (comprar a raquete do profissional) com o argumento do próprio site; o card de DNA mostra o que a pessoa ganha no lugar.',
  'Raquete do ídolo, golpe atrasado. 🎾\nModelo de profissional tem mais peso e swingweight. Jogando duas vezes por semana, o golpe atrasa e o braço cansa. O RACKET DNA foi calibrado com 379 casos de especialistas e 670 avaliações de testadores para achar a raquete do seu jogo.\nVocê vê o diagnóstico antes de pagar.',
  'Raquete do ídolo, golpe atrasado', 'Tela real do card "Seu DNA de jogo" (Atacante de fundo de topspin moderado).'),
 ('ADC-SF-04', SF, 'surf_kv_custo', 'SURF KV: errar a prancha custa caro',
  'Contraste de preço (até R$ 4.000 de prancha × R$ 19,99 de relatório), com os números do próprio site, transforma o teste em seguro barato.',
  'Errar a prancha custa caro. 🏄\nUma prancha nova sai por R$ 1.500 a R$ 4.000. Acertar a escolha custa R$ 19,99: o SURF DNA cruza o seu corpo, o seu surf e o seu mar com 13 tipos de prancha e 416 tamanhos.\nPrévia grátis, 3 minutos, sem cadastro.',
  'Errar a prancha custa caro', 'Tela real da prévia do resultado (96%, 88%, 84%) com a frase do site sobre o preço.'),
 ('ADC-SF-05', SF, 'surf_kv_litros', 'SURF KV: duas 6\'0" com 10 litros de diferença',
  'Quem escolhe pelo tamanho em pés não sabe que o volume muda tanto; o dado surpreende e leva à litragem certa.',
  'Duas 6\'0" podem ter 10 litros de diferença. 🏄\nÉ a litragem que decide se você rema e entra na onda. O SURF DNA compara 416 tamanhos de 35 modelos, medida por medida, e mostra quanto a sua prancha deve boiar.\nPrévia grátis, 3 minutos, sem cadastro.',
  'Duas 6\'0" podem ter 10 litros de diferença', 'Tela real de "O que está por trás" (13 tipos, 39–43 L).'),
 ('ADC-SF-06', SF, 'surf_kv_200tri', 'SURF KV: 200 trilhões de pranchas, a sua sob medida',
  'O número absurdo (200 trilhões) vende a ideia de sob medida; o card de DNA de surf mostra o resultado pessoal.',
  'Mais de 200 trilhões de pranchas possíveis. A sua sai sob medida. 🏄\nO SURF DNA transforma suas respostas em nível, estilo e mar, compara com 13 tipos de prancha e calcula cada medida: 17 medidas na ficha técnica, prontas para levar a qualquer shaper.\nPrévia grátis, 3 minutos, sem cadastro.',
  'A sua prancha sob medida', 'Tela real do card "Seu DNA de surf" (Surfista de curvas de onda pequena, DNA Score 96%).'),
 ('ADC-SF-07', SF, 'surf_kv_amigo', 'SURF KV: a prancha do amigo foi feita pra outro surfista',
  'Comprar a prancha (ou a usada) do amigo é comum; dizer que ela foi feita para outro peso, nível e mar provoca e abre a dúvida.',
  'A prancha do amigo foi feita pra outro surfista. 🏄\nA litragem foi pensada para outro peso, outro nível e outro mar. O SURF DNA foi calibrado com 422 casos reais e mais de 1.000 fontes de surf para achar a sua.\nPrévia grátis, 3 minutos, sem cadastro.',
  'A prancha do amigo é de outro surfista', 'Tela real da pergunta "O que você já faz na onda?" do teste.'),
]


def entry(i, B, camp, title, hip, copy, titulo, tela):
    ver = f'{i}-v1'; png = FIN / f'{ver}-feed45.png'
    return {
        'id': i, 'brand': 'SPORT DNA', 'fmt': 'estatico', 'lote': 'dna-kv',
        'formato': 'KV estático 4:5 (hero). Adaptações 1:1, 9:16, 1,91:1 e 16:9 e motion depois da aprovação.',
        'title': title, 'objetivo': B['objetivo'], 'publico': B['publico'], 'hipotese': hip, 'copy': copy, 'titulo': titulo,
        'cta': f'Na arte: "{B["cta_art"]}" + {B["path"].replace("https://", "").rstrip("/")}. Botão do anúncio: Saiba mais.',
        'url': f'{B["path"]}?{UTM}&utm_campaign={camp}&utm_content={ver}',
        'direitos': (COMUM_RK if B is RK else COMUM_SF) + [tela] + TODOS,
        'notes': 'Série de 4 KVs por esporte pedida pelo Gui em 10/11 ("foco em big numbers dos motores, chamativo, provocativo: errar equipamento custa caro"). Você aprova só o hero; as adaptações seguem o hero.',
        'version': ver, 'v': 1, 'mudou': 'Peça nova (série KV SPORT DNA de 10/11).',
        'media': [f'ads/{ver}/{ver}-feed45.png'], 'cover': f'{ver}-hero.jpg', 'producao': 'pronto para revisão',
        'ferramentas': 'Captura real do site (dna_capture.py e kv_dna_stills.py, Playwright); composição em HTML/CSS com SVGs e fontes oficiais (kv_dna.py). Sem IA generativa.',
        'arquivos': [{'label': 'KV 4:5 (hero)', 'path': f'media/ads/{ver}/{ver}-feed45.png'}],
        'hash': hashlib.md5(png.read_bytes()).hexdigest()[:10],
    }


E = [entry(*k) for k in K]
(HERE.parent / 'patch-dna-kv.json').write_text(json.dumps(E, ensure_ascii=False, indent=1))
LOTE = '10/11 · SPORT DNA, série de KVs: 4 RACKET (ADC-RK-03 a 06) e 4 SURF (ADC-SF-04 a 07), estáticos 4:5 com big numbers do motor, título provocativo e tela real do teste no celular. Adaptações e motion depois da aprovação.'
if len(sys.argv) > 3:
    s = Path(sys.argv[2]).read_text()
    m = re.search(r'(<script id="manifest" type="application/json">)(.*?)(</script>)', s, re.S)
    M = json.loads(m.group(2).replace('<\\/', '</'))
    ids = {e['id'] for e in E}
    assert not ids & {a['id'] for a in M['ads']}, 'ID já existe na Mesa'
    M['ads'] += E; M['adsLote'] = [LOTE] + [x for x in M.get('adsLote', []) if x != LOTE]
    js = json.dumps(M, ensure_ascii=False).replace('</', '<\\/')
    Path(sys.argv[3]).write_text(s[:m.start(2)] + js + s[m.end(2):])
    print('ok', len(M['ads']), 'ADs;', len(M['pieces']), 'peças intactas')
