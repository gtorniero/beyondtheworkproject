# Pack Semanal de Instagram · Quiddo, Retrozap e SPORT DNA

## Estado atual
- **Limites da Mesa (10/11):** 512 arquivos e 256 MB por versão, 64 MB por publish. Os vídeos de AD na Mesa são versões mais leves (CRF 27) dos originais em `ads/mesa` e `ads/aprovados` no GitHub; o hash do AD continua o do original (não reabre aprovação). Os editáveis saíram de `final/` (ficam em `editaveis/`).
- **Quiddo Empresas (10/11):** KV principal ADC-QD-10-v1 ("Sua apresentação vira participação", 4:5, captura real do modo Corporativo) e a linha em vídeo ADC-QD-07 (reunião geral), 08 (onboarding) e 09 (treinamento). Adaptações do KV (1:1, 9:16, 1,91:1, 16:9 e vídeo de até 15 s) só depois da aprovação. /criar abre o editor e o modo Corporativo se escolhe lá dentro (não há parâmetro de URL).
- **S03 fechado em 10/11: 42 de 42 aprovadas e liberadas (rodada 2).**
- **ADs · modelo novo (10/11):** kit `pipeline/ads/estudio.py` + direção `pipeline/ads/DIRECAO.md` (câmera, tipografia cinética, cortes, captura real como clipe). Na Mesa para revisão: ADC-RZ-08-v1, ADC-RN-03-v1, ADC-QD-03-v3, ADC-QD-04-v3 (reel 20 s + motion 4:5 e 1:1), além dos reels refeitos RZ-01-v3, RZ-02-v2, RK-01-v3, QD-01-v3. Scripts em `pipeline/ads/reels/`; mídia em `ads/mesa/`. Captura: repos gtorniero/quiddo, retrozap e sportdna rodando local (os sites públicos são bloqueados pelo proxy; fontes do Google servidas local).
- **Pack Semanal 03 · na Mesa desde 10/11, rodada 1** (semana 23–29/11/2026). 42 peças: por marca 4 reels (seg, qua, sex, dom) + 3 carrosséis (ter, qui, sáb) + 7 stories sem adesivo. Memes/trends: Quiddo Q-R7 (trend ligar/desligar), Q-R8 e Q-R9 (memes), Q-R10 (trend minivlog); Retrozap R-R8 e R-R10 (trends), R-R9 e R-R11 (memes); SPORT DNA D-R8 e D-R11 (memes), D-R9 e D-R10 (trends). Sem peça de produto em gravação de tela (aguarda o Gui dizer qual artefato é o app atual). Grade em packs/S03/grade-S03.jpg. Código do S02 em `pipeline/arquivo/S02/`, estado em `pipeline/state/S02/`.
- **ADs:** os 19 ADs do S02 continuam na Mesa com o banco `ads/S02_<id>` (campo `adsPack` no manifesto; dados em `pipeline/ads/S02.json`, mídia só na Mesa). O `tool_template.html` agora é o da Mesa no ar (com ADs).
- **Pack Semanal 02 · fechado com 40 peças, todas aprovadas** (semana 16–22/11/2026). R-R7 e D-R7 cancelados pelo Gui na rodada 3 (voltam quando der para gravar o app real ou os artefatos que simulam). Histórico: rodada 3: 40 de 42 aprovadas; R-S6 virou o reel R-R7 (gravação de tela da retrospectiva) e o D-R7 virou gravação de tela do teste e relatório do SURF DNA; os dois na segunda 19h45. Antes: Rodada 2: 39 de 42 aprovadas; R-S6 e R-S10 em v3 sem etiquetas; story D-S6 trocado pelo reel D-R7 (relatório do RUN DNA rolando no celular, seg 19h45, 2º post de feed da SPORT DNA no dia). Mesa: painéis Em aprovação e Aprovados, header preto, visão Calendário, feedback geral limpo a cada rodada. Rodada 1: 35 aprovadas, 4 stories reprovados (R-S6, R-S10, D-S6, D-S8) refeitos em v2 com celular, conversa, relatório e bloco de notas; Q-C4, Q-S8 e R-C4 sem decisão. A Mesa ganhou a aba "Assets da semana" (o que vai entrar, por dia, e contagem de aprovados por formato e marca). 42 peças: 21 feed (por marca 3 reels + 4 carrosséis, 1 por dia, começando por carrossel na segunda) e 21 stories (1 por dia por marca, sem adesivo).
  - Memes: Q-R5, Q-C4, Q-R4 (veio do S01 sem decisão, mesma arte), R-R4, D-R5. Trends: Q-R6, R-R5, D-R6 (Black Friday 27/11).
  - Produto: Q-C6, R-R6, D-C6.
  - Stories sem adesivo: Quiddo "Pergunta do dia" (resposta de cabeça pra baixo), Retrozap "frase pro grupo" (print), SPORT DNA "Dicionário DNA".
  - Grade conferida com `grade.py` (packs/S02/grade-S02.jpg).
- **Pack Semanal 01** (09–15/11): 17 de 18 liberadas; Q-R4 foi para o S02. Código do S01 em `pipeline/arquivo/S01/`, estado em `pipeline/state/S01/`.
- Ferramenta de aprovação: **Mesa de Aprovação**, https://claude.ai/artifact/KAwUuKVHZgYknpdquaTkwd
  - Banco: `reviews/S02_<id>`, `pack/S02`, `rodadas/R<n>`. A Mesa mostra só o pack mais recente; as decisões do S01 continuam no banco.
  - Botão "Finalizar rodada N e enviar ao Claude" grava `rodadas/R<N>` e `pack/<SNN>.ultimaRodada`.
  - Aba Publicação: zips por marca e guia do DOT. Aba Grade: feed novo + feed do pack anterior (apagado).
  - Publicar a Mesa: no máximo 255 arquivos por publish e 511 por versão. Publique em lotes (mídia e editáveis; depois `null` nos arquivos do pack anterior; depois `final/`).

## Para aplicar feedbacks
1. Ler `reviews` e `pack/S01` com ArtifactData (url acima).
2. Ajustar o código da peça (quiddo.py, retrozap.py, sportdna.py), renderizar (render.py, partes em paralelo), montar com make_tool.py e republicar a Mesa no mesmo URL. A versão sobe sozinha quando a mídia muda.

## Decisões em vigor
- Tudo de social vai para o Drive em "05. Social Content" (1y4dovKtUNSnNvcflf5d3cLItGrH8ajOm), uma subpasta por pack. Eu subo os docs; os zips (binários) o Gui arrasta, porque o conector do Drive não sobe binário com segurança.
- Stories: só os que funcionam sem adesivo e sem pedir resposta no direct (Gui cancelou os de enquete/quiz/caixa/link no S01, rodada 4).
- Volume a partir do Pack 02: por marca, 1 post de feed por dia alternando reel e carrossel (1 reel a cada 2 dias, 1 carrossel a cada 2 dias), 1 a 3 stories por dia; reels misturam meme e trend; Quiddo com no mínimo 2 memes por semana.
- Playbook de crescimento (volume, horários, envios, trends e memes): claude/pack-semanal/playbook-crescimento.md e no Drive.
- Ao finalizar a rodada, a Mesa copia um resumo em texto; o Gui cola no chat. Ler também `rodadas/R<N>.resumo`.
- Quiddo: CTA sempre "Faça o seu. Teste grátis." e nunca citar "até 10 pessoas" (Gui, rodada 1).
- SPORT DNA: linha nova pedida pelo Gui: simulação de IA genérica (sem marca, com etiqueta de simulação), "Parece simples. Não é.", modelo calibrado com atletas e esportistas.
- Sem "um projeto Beyond the Work" nas artes e vídeos (feedback #1 do brief; o kit 00 ainda pede a assinatura, mas o brief é mais novo).
- Texto na tela ≈ 0,33 s por palavra; reels de 15–21 s; nada de texto nos 250 px de cima e 350 px de baixo; arte importante dentro do recorte 4:5 central.
- Simulações (notificações, conversas) levam a etiqueta "simulação · nomes de exemplo". Dados de exemplo sempre marcados.
- Quiddo: bichos só do avatarSvg do site; respostas A–D = folha/verde, sol/laranja, gota/azul, flor/vermelho. Grátis até 10 pessoas.
- Retrozap: dados de exemplo só Turma do Churras e Dani & Cris. Preço R$ 8,99 e 1º grupo grátis.
- SPORT DNA: números do site no ar (62 raquetes, 212 tênis, 13 tipos de prancha, 422 casos; R$ 9,99 RUN, R$ 19,99 SURF/RACKET). Logo só em algumas peças.
