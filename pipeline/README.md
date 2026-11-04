# Pack Semanal de Instagram · Quiddo, Retrozap e SPORT DNA

## Estado atual
- **Pack Semanal 01 · rodada 3 (Q-S3 v3 e Q-R4 meme novo; resto aprovado)** (semana 09–15/11/2026). Rodada 1 revisada pelo Gui em 03/11; 11 peças foram para v2. 30 peças: 15 feed (3 reels + 2 carrosséis por marca, dias 1, 2, 4, 5 e 7) e 15 stories.
- Peças de produto (2): R-C2 (Retrozap, o que vem na retrospectiva) e D-C2 (SPORT DNA, como o motor escolhe). O resto é engajamento.
- Ferramenta de aprovação: **Mesa de Aprovação**, https://claude.ai/artifact/KAwUuKVHZgYknpdquaTkwd
  - Botão "Finalizar rodada N e enviar ao Claude" grava `rodadas/R<N>` (foto das decisões) e `pack/S01.ultimaRodada`. Quando o Gui disser "finalizei a rodada", ler `rodadas/R<N>` e `pack/S01`.
  - Aba Publicação: monta os 3 zips no navegador (arquivos em `final/<marca>/`) e mostra o guia do DOT. Guia também no Drive: pasta "Instagram · Pack Semanal 01" (1eeyUwJgospoBN7ZdCzJ9nBvtS3i3TJuL).
  - Banco do artefato: `reviews/<id da peça>` = {status: aprovado|reprovado|null, comment, hash, version, at, history[]}; `pack/S01` = {geral, at}.
  - Status "revisar de novo" = o hash da mídia mudou desde a última decisão. O comentário anterior fica visível.
  - O feedback geral nunca aprova nem reprova peças.
- Pack anterior (lançamento, v2): Drive `quiddo-insta-pack-v2`, Retrozap "Pack completo + guias", `SPORT-DNA-instagram.zip`.

## Para aplicar feedbacks
1. Ler `reviews` e `pack/S01` com ArtifactData (url acima).
2. Ajustar o código da peça (quiddo.py, retrozap.py, sportdna.py), renderizar (render.py, partes em paralelo), montar com make_tool.py e republicar a Mesa no mesmo URL. A versão sobe sozinha quando a mídia muda.

## Decisões em vigor
- Tudo de social vai para o Drive em "05. Social Content" (1y4dovKtUNSnNvcflf5d3cLItGrH8ajOm), uma subpasta por pack. Eu subo os docs; os zips (binários) o Gui arrasta, porque o conector do Drive não sobe binário com segurança.
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
