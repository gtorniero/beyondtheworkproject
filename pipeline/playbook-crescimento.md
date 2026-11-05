# Playbook de crescimento · Quiddo, Retrozap e SPORT DNA

Regras que valem para todo pack semanal a partir do Pack 02. Revisar a cada 4 semanas com os Insights dos perfis.

## 1. O que faz um post espalhar

- **Envio é o sinal que mais pesa.** O Instagram diz que "envios por alcance" (gente mandando o post por DM) é um dos sinais mais fortes para mostrar o conteúdo a quem ainda não segue. Para nós, "viralizar no WhatsApp" é isso: a pessoa vê e manda no grupo.
- **Toda peça precisa de um motivo para ser enviada:**
  - **Identidade:** "todo grupo tem um…", "a tia do quiz", "o amigo que manda áudio".
  - **Marcação:** a peça aponta alguém ("marca quem…", "manda pro…").
  - **Desafio:** "aposto que ninguém acerta", "0 de 9 acertaram".
  - **Utilidade:** salvar para usar depois, como lista, regra ou conta.
- **CTA de envio explícito na legenda:** "manda no grupo da família", "manda pro seu parceiro de beach", "marca o fantasma".

## 2. Volume por marca, por semana

Decisão do Gui (03/11): feed todos os dias, alternando reel e carrossel.

| Formato | Ritmo | Por semana |
|---|---|---|
| Reels | 1 a cada 2 dias | 3 ou 4 |
| Carrosséis | 1 a cada 2 dias, nos dias sem reel | 3 ou 4 |
| Feed total | 1 post por dia | 7 |
| Stories | 1 a 3 por dia, com um interativo por dia (enquete, quiz, caixa ou slider) | 7 a 21 |

- **Sequência contínua:** reel, carrossel, reel, carrossel… A semana seguinte começa pelo formato oposto ao do último dia, para nunca repetir o formato em dois dias seguidos.
- **Reels misturam meme e trend** com as peças próprias da marca.
- **Quiddo:** no mínimo 2 memes por semana.
- **Referência:** contas que postam de 6 a 9 vezes por semana crescem perto do dobro das que postam de 3 a 5 (estudo Buffer, 2 milhões de posts).
- **Stories:** quase não chegam a quem não segue; servem para conversar com quem já segue.

Para as 3 marcas: 21 posts de feed e de 21 a 63 stories por semana.

## 3. Horários (Brasília)

Começamos assim. Depois de 3 semanas, ajustamos pelos Insights de cada perfil, porque o estudo é global e não tem recorte do Brasil.

| Formato | Horário | Por quê |
|---|---|---|
| Reels | 19h45, todos os dias | o pico de engajamento é às 20h; domingo é o melhor dia para reels |
| Carrossel | 12h30 em dia útil | almoço (11h–13h) é forte; domingo 19h–21h também funciona |
| Stories | 12h | janela de 11h a 14h |
| Evitar | 2h às 5h | menor atividade do dia |

Teste a fazer: reels da SPORT DNA às 7h em uma semana e às 19h45 na outra, para comparar o público de corrida e de surf.

## 4. Trends e memes toda semana

**Rotina:**
1. **Domingo:** o DOT abre o Instagram no navegador e traz:
   - os 5 áudios em alta, do painel profissional ou da seta ↗ na biblioteca de áudio;
   - 3 formatos de meme que estão rodando no Brasil, com print;
   - 1 assunto da semana que conversa com cada marca, como feriado, jogo, final de reality ou Black Friday.
2. **O Gui cola isso no chat do Claude.**
3. **Eu adapto 2 peças por marca** e o pack chega na Mesa com a etiqueta "meme" ou "trend" nessas peças.

**Regras do meme:**
- **Usar o formato, nunca a imagem de outra pessoa.** Formatos bons: POV, "ninguém: / eu:", expectativa × realidade, tier list, "manda pro amigo que…", "me diga X sem dizer X", antes × depois.
- **Sem personagem, série, celebridade ou pessoa real.** Também não usamos marca de terceiros. Quem atua no meme são os nossos personagens: os bichos do Quiddo, os ícones do Retrozap e os desenhos técnicos da SPORT DNA.
- **O áudio em alta entra no app** na hora de agendar ou postar. Os vídeos saem mudos e com tempo de corte flexível.
- **Trend vence rápido.** Peça de trend sai na mesma semana em que foi feita; se perder a janela, cai.
- **Quiddo é a marca mais "meme"**, com família, firma, escola e amigo secreto. A SPORT DNA faz meme com dado e ironia ("perguntei pra IA…"). O Retrozap faz meme com comportamento de grupo.

## 4b. Design tangível (feedback do Gui, S02 rodada 1)

- **Variar o design de verdade:** simular um celular (moldura genérica, sem marca de aparelho), bloco de notas, conversa de grupo (sem marca de app, com etiqueta de simulação), tela do produto.
- **Mostrar o produto em uso:** como se usa, exemplo de relatório da SPORT DNA, exemplo de uma partida no Quiddo, exemplo de uma retrospectiva do Retrozap. Sempre com etiqueta "dados de exemplo".
- **Menos peça só de texto:** frase solta e glossário puro foram reprovados por serem básicos. Cada peça precisa de um objeto concreto na tela.
- **Peça de conteúdo não é site** (Gui, S02 rodada 2): nada de "1º grupo grátis", preço ou etiqueta "dados de exemplo"/"simulação" em story de conteúdo. Nomes e dados fictícios continuam fictícios (Turma do Churras, modelos sem marca), só sem etiqueta.
- **Produto complexo vira reel** (Gui, S02 rodada 2): relatório da SPORT DNA, partida do Quiddo e retrospectiva do Retrozap se mostram em reel com a tela rolando e completa. Story estático com tela de produto faz o produto parecer simples.
- **Mostrar o produto como gravação de tela** (Gui, S02 rodada 3): reel em tela cheia com o indicador vermelho de gravação, a barra de endereço do site, toques visíveis e o fluxo real (perguntas, análise, relatório; ou subir a conversa e os 3 atos). Legenda curta por cima. Helpers `C.rec_bar()`, `C.tap()`, `C.legenda()`.
- O ideal é gravar o app de verdade: daqui a rede bloqueia os sites das marcas e os repositórios dos apps não estão na sessão; por ora as telas são recriadas no estilo do app (decisão do Gui, 05/11).
- Helpers: `C.phone()` e `C.bubble()` em `pipeline/common.py`.

## 5. Backlog e harmonia

- **Backlog:** quando o Gui termina de aprovar um pack, o Claude já produz o próximo. Fica sempre um pack aprovado à frente, no máximo 2.
- **Sem repetição:** nada de repetir tema, gancho ou piada da mesma marca nas últimas 4 semanas. O Claude confere os packs anteriores e o Registro de publicações.
- **Grade harmônica:** antes de ir para a Mesa, o Claude monta a grade das 9 últimas peças de cada marca com as novas e ajusta cor e composição.

## 6. Fluxo da semana

| Dia | O quê | Quem |
|---|---|---|
| Domingo | pesquisa de trends e áudios | DOT, Gui cola no chat |
| Segunda e terça | produção do pack da semana seguinte e Mesa no ar | Claude |
| Quarta | revisão e "Finalizar rodada" (o resumo é copiado e o Gui cola no chat) | Gui |
| Quinta | ajustes até tudo aprovado; zips para "05. Social Content" no Drive | Claude e Gui |
| Sexta | agendamento no Meta Business Suite e lembretes dos stories com adesivo | DOT |

## Fontes

- Envios como sinal de alcance: Search Engine Journal, "Instagram algorithm shift: why sends matter more than ever".
- Frequência: Buffer, "How often should you post on Instagram in 2026" (2 milhões de posts).
- Horários: Metricool, "Melhor horário para postar no Instagram em 2026" (24 milhões de posts, global).
