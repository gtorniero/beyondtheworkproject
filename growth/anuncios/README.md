# Fila de anúncios (Meta)

`fila.csv` é a lista de anúncios que podem subir. Quem opera os anúncios (o ChatGPT do Gui) lê só as linhas com status **PRONTO** ou **PRONTO (com data)**.

- **PRONTO**: aprovado pelo Gui na Mesa, com todos os formatos. Os arquivos já estão na biblioteca de mídia da conta act_1471479281571654 com o mesmo nome.
- **PRONTO (com data)**: só dentro da data indicada na observação.
- **AGUARDANDO APROVAÇÃO**: não subir.
- **NÃO USAR**: reprovado ou substituído.

O Claude atualiza este arquivo toda manhã a partir de `ads/aprovados/INDEX.md` (branch `social`).

Ver como tabela: https://github.com/gtorniero/beyondtheworkproject/blob/claude/sweet-hypatia-43ca1s/growth/anuncios/fila.csv
CSV direto: https://raw.githubusercontent.com/gtorniero/beyondtheworkproject/claude/sweet-hypatia-43ca1s/growth/anuncios/fila.csv
