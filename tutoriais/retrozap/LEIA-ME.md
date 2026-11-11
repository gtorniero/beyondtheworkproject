# Retrozap · tutoriais para WhatsApp (11/11/2026)

Dois vídeos didáticos e independentes: como fazer a retrospectiva do **grupo** e a retrospectiva de **casal**.
Briefing do Gui pelo CEO/GPT em 11/11. Gui aprova o hero de cada um na Mesa (aba "Tutoriais · WhatsApp"). Nada foi publicado, agendado nem enviado a grupos.

| Pasta | O quê | Aparelho demonstrado | Na Mesa |
|---|---|---|---|
| `TUT-RZ-GRUPO-v1/` | hero do tutorial de grupo | Android | sim (versão WhatsApp) |
| `TUT-RZ-CASAL-v1/` | hero do tutorial de casal | iPhone | sim (versão WhatsApp) |
| `complementos/` | o mesmo tutorial no outro aparelho (grupo no iPhone, casal no Android) | iPhone / Android | não: depois da aprovação do hero, sai junto, sem nova aprovação |

Cada pasta de vídeo tem:
- `*-master.mp4`: 1080×1920, 30 fps, H.264 de alta qualidade, sem áudio.
- `*-whatsapp.mp4`: 720×1280, mais leve para mandar no WhatsApp, com o texto ainda legível depois da compressão do app.
- `*-capa.jpg`: a capa, que é o primeiro quadro do vídeo. O WhatsApp usa esse quadro como miniatura.
- `*.srt`: as legendas, com o mesmo texto que aparece na tela.
- `MENSAGEM-WHATSAPP.txt`: a mensagem curta sugerida para mandar junto com o vídeo, com a URL.

## Como foi feito (e o que foi conferido)
- **Gravação real** do site publicado (repo `gtorniero/retrozap`, commit `fabe1c7`, onboarding v2), rodando local, em tela de celular (390×693). O site e o fluxo não foram alterados.
- **Conversas fictícias** exportadas no formato real de cada aparelho:
  - grupo "Turma do Churras", no formato Android (`.txt`);
  - casal "Dani & Cris", no formato iPhone (`.zip` com `_chat.txt`).
  - Os resultados que aparecem são os que o próprio site calcula com essas conversas. Etiqueta fixa no topo: "Demonstração com conversa fictícia".
- **Passos do WhatsApp:** aparecem pelo guia ilustrado do próprio site (`/exportar`, abas iPhone/Android), com o texto do site em cada passo. O vídeo diz qual aparelho está sendo mostrado e que a outra aba mostra os passos do outro celular.
- **Telas do sistema que não foram gravadas:** o app do WhatsApp, o seletor de arquivos e a folha de compartilhar do celular. Elas não foram imitadas. Nesses pontos, uma nota escrita diz o que fazer.
- **Oferta conferida no código em 11/11:**
  - 1º grupo grátis.
  - Casal é sempre pago: R$ 8,99, pagamento único, no Pix ou no cartão. O aviso de pagamento aparece depois do Ato I e foi gravado assim. O pagamento em si não foi gravado.
  - O vídeo do grupo é Premium. Por isso o tutorial de grupo compartilha uma imagem (Diário da Turma) e o de casal compartilha o Recibo do amor.
- Sem narração e sem música (deliberado). Todo o texto está na tela e no `.srt`.

## Como refazer
`pipeline/ads/reels/`:
1. `tut_cap.py`: grava o site.
2. `tut_roteiro_grupo.py` e `tut_roteiro_casal.py`: o roteiro de cada vídeo.
3. `tut_wa.py`: as cenas do WhatsApp por aparelho.
4. `tut_edit.py`: a montagem.
5. `tut_mesa.py`: põe os vídeos na Mesa.

A captura bruta e as conversas fictícias de cada versão ficam em `fonte/`.
