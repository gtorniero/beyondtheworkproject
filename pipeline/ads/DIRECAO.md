# Direção dos ADs · modelo novo (Gui, 10/11/2026: "elevar a barra")

Objetivo: anúncio best in class, com cara de 2026, feito para parar o dedo e ser mandado no grupo. Sempre com o **produto real** (captura de verdade) como protagonista. Ferramenta: `pipeline/ads/estudio.py`.

## REFERÊNCIA OFICIAL: ADC-RZ-08-v1 (Gui, 10/11: "É isso! Essa é a referência para TODOS os nossos ADs")
Código: `pipeline/ads/reels/rz08.py`. Todo AD de todas as marcas segue essa técnica e esse look and feel:
- **Celular grande e central** (cerca de 70% da largura no 9:16), com a tela real do app, em perspectiva leve, que a câmera aproxima a cada toque (helpers `cam`, `rot`, `shot` do rz08.py).
- **Fundo vivo na cor da marca:** cor escura/base chapada + 2 manchas de luz desfocadas (blobs) nas cores de apoio, andando devagar.
- **Título enorme no topo**, 2 linhas, fonte de título da marca, com 1 palavra em destaque na cor de acento; troca a cada cena.
- **Big numbers:** números reais do app/site em corpo gigante, rodando com `count()` (SPORT DNA: o motor e a recomendação: modelos cruzados, % de combinação, confiança; Retrozap: mensagens; Quiddo: pontos, posição, jogadores).
- **Assets do site:** ícones, troféus, bichos, logos e ilustrações oficiais (dos repos dos sites e de `pipeline/assets`) entram como elementos de cena (flutuando, no CTA), nunca desenho novo.
- Wipes de cor da marca entre blocos, flash na revelação, CTA com assinatura oficial + frase + pílula da URL.
- Motions 4:5 e 1:1 recompostos pelo mesmo script (tabela `LAY`).

## Estrutura (reel 9:16, 16 a 24 s)
1. **Gancho, 0 a 1,5 s.** Uma pergunta ou provocação de até 6 palavras, em tipografia cinética grande, já com o produto na tela e em movimento. Nada de logo ou cartela parada na abertura. O quadro 0 já precisa funcionar como capa.
2. **Interação, 1,5 a 6 s.** O momento mais interativo do app, com o dedo agindo: palpite, raspadinha, resposta no celular, slider do teste. A câmera entra na tela (zoom para o ponto do toque), `ring()` no toque.
3. **Recompensa, 6 a 14 s.** A revelação: pódio, resultado, DNA. Corte seco ou `wipe()` na batida, `flash()` no instante da revelação, número rodando com `count()` quando houver número real da tela.
4. **Prova, 2 a 4 s.** 2 ou 3 cortes rápidos de outras telas reais (cada um ≥ 1,2 s, com zoom no que importa), para mostrar que tem mais.
5. **CTA, últimos 2,5 a 3 s.** Frase de ação + URL + logo oficial. O último quadro fica parado ≥ 1,2 s. O fundo final deve casar com o quadro 0 para o loop.

## Execução
- **Câmera:** a tela real nunca fica chapada e parada. Use celular com `phone()` em perspectiva (rotateX/rotateY leves), aproximações de 1,4× a 2,2× no ponto de interesse e reenquadramento a cada corte. Movimento sempre com `SNAP` ou `EASE`, nunca linear. Leitura: UI em close precisa ficar ≥ 1,6 s na tela; texto ≈ 0,35 s por palavra.
- **Ritmo:** cortes em grade de 0,5 s (qualquer áudio em alta encaixa). Um evento visual novo a cada 1 a 2 s. Vídeo sem faixa de áudio.
- **Tipografia:** fonte de título da marca, enorme (96 a 150 px no 9:16), no máximo 2 linhas, uma palavra em destaque (`*palavra*`). Texto e produto nunca se sobrepõem de forma ilegível: reserve a faixa do texto.
- **Cor e marca:** paleta, fontes e SVGs oficiais de `pipeline/assets` e `pipeline/fonts`. Cada marca com a sua cara: Quiddo = contorno grosso, sombra dura, creme/tinta e cores das respostas; Retrozap = Noite com Manga e cores de apoio; SPORT DNA = preto, off-white e a cor do esporte, grade técnica.
- **Zonas seguras 9:16:** nada importante nos 270 px de cima e 370 px de baixo. CTA e texto dentro da zona.

## Regras fixas do Gui (não negociáveis)
- Captura 100% real do produto; nada de tela recriada. Nada cortado de forma que quebre a leitura (zoom é permitido, desde que o elemento em foco apareça inteiro).
- **Nunca** etiqueta "exemplo", "simulação", "demonstração", "nomes fictícios", "ilustrativo".
- Sem música embutida, sem narração, sem IA generativa de imagem/vídeo/voz.
- Sem preço na arte do Retrozap; Quiddo: CTA "Faça o seu. Teste grátis.", nunca "até 10 pessoas"; privacidade não é tema de AD; sem logo ou cor de app de terceiros; sem pessoas, marcas ou personagens reais; sem ilustração de equipamento na SPORT DNA.
- Números só os que a tela real mostra (hoje o RACKET diz 183 raquetes).
- Nada vai para a conta de anúncios sem ordem do Gui.

## Entregas por AD
- `ADC-<ID>-v<n>.mp4` (reel 9:16) + `-capa.jpg`.
- Motion para feed: `-motion-feed45.mp4` (4:5) e `-motion-sq.mp4` (1:1), 8 a 14 s, recompostos para o formato (não é crop do reel): gancho, 1 interação, recompensa, CTA.
- Patch da entrada na Mesa (`pipeline/ads/patch-<ID>.json`) com version, v, media, cover, duration, formato, mudou, copy, titulo, cta, url (UTM com a versão), ferramentas, direitos, notes, arquivos (links dos motions).
- Antes de entregar: `preview()` a cada ~0,5 s, olhar a folha, corrigir sobreposição, texto cortado e contraste.
