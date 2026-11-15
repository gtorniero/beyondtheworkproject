# Beyond the Work

Site institucional da Beyond the Work Ideas. Página estática única (`index.html`), publicada na Cloudflare Pages.

- `index.html`: o site completo (HTML, CSS e JS num arquivo só)
- `favicon.svg`: a Série

Para publicar: conectar este repositório a um projeto da Cloudflare Pages (sem build, diretório de saída `/`) e apontar o domínio.

## Rodada (versão de teste) · `/rodada`

- `rodada/`: os jogos (página inicial, 1%, Mais ou Menos, Cidade Dorme, Piscadinha, Infiltrado e Quem Sou Eu?). Fora do Google (`noindex`).
- `rodada/sala.js`: liga os jogos ao vivo ao servidor de salas (`wss://salas.beyondthework.com.br`). Para testar com um servidor local, abra a página com `?salas=ws://127.0.0.1:8787`.
- `servidores/rodada-salas/`: o servidor das salas (Cloudflare Worker + Durable Object, publicado à parte em `salas.beyondthework.com.br`). Para publicar uma mudança: `npx wrangler deploy` nesta pasta.
- O 1% e o Mais ou Menos rodam com perguntas de exemplo e o resultado fica só no aparelho; o ranking online ainda não existe fora do protótipo.
