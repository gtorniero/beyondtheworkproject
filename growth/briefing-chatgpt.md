# Briefing para os agentes do ChatGPT

**De:** Growth Manager BTW (Claude)
**Regras:** nada é ativado, nenhum orçamento muda e nada é gasto sem ok explícito do Guilherme. Nenhum dado de cliente sai de lugar nenhum. Ao terminar cada tarefa, responda com um print ou o link e a palavra FEITO.

Cole a parte do agente certo no chat dele.

---

## Agente de Ads (navegador)

### Agora (hoje)

1. **Aceitar os termos de público personalizado da conta de anúncios.**
   Abra https://www.facebook.com/customaudiences/app/tos/?act=1471479281571654 e aceite. Isso destrava os 12 públicos do pixel que o Claude cria pela API.
2. **Ligar a correspondência automática avançada nos 3 pixels.**
   Gerenciador de Eventos → cada pixel (Retrozap — Web, Quiddo — Web, SPORT DNA — Web) → Configurações → "Correspondência avançada automática" → Ligar, com e-mail e telefone marcados. Os sites só ativam o pixel depois do aceite de cookies, então isso fica dentro da LGPD.
3. **Iniciar a verificação do Business** "Beyond the Work" (ID 303359410698910): Configurações do negócio → Central de segurança → Verificação, com o CNPJ 69.746.447/0001-00.
4. **Não mexer** nas 3 campanhas ativas. Mudanças nelas são feitas pelo Claude via API, depois do ok.

### Semana 2: Google

5. **GA4 (as 3 propriedades):** marcar como eventos-chave a compra (`purchase`), a sala criada (Quiddo) e o teste concluído (SportDNA). Vincular cada GA4 ao Google Ads e ao Search Console.
6. **Planejador de palavras-chave** (Google Ads → Ferramentas): exportar em CSV o volume mensal no Brasil destas listas:
   - RACKET: qual raquete comprar, raquete de tênis para iniciante, melhor raquete de tênis, raquete para tennis elbow, raquete babolat ou wilson
   - RUN: qual tênis de corrida comprar, tênis de corrida para iniciante, melhor tênis para correr
   - Quiddo: quiz ao vivo, quiz online para grupo, quiz para empresa, dinâmica para treinamento, quiz para sala de aula, alternativa kahoot
   - Retrozap: retrospectiva whatsapp, retrospectiva do grupo, wrapped whatsapp
7. **Montar no Google Ads, PAUSADAS:**
   - **RACKET DNA:** campanha de Search com 1 grupo de palavras exatas e de frase da lista acima. Anúncio levando a sportdna.com.br/racket/ com UTM `utm_source=google&utm_medium=cpc&utm_campaign=rk_search`. Orçamento sugerido: R$ 20/dia, que **só entra com ok**.
   - **Quiddo empresas/escola:** mesma estrutura, levando a quiddo.com.br/criar com `utm_campaign=qd_search_b2b`.

### Toda segunda-feira, até 10h

8. **Exportar para o Google Drive**, na pasta `BTW Growth/exports/AAAA-MM-DD/`:
   - GA4 de cada site: usuários, sessões e eventos-chave por origem/mídia, últimos 7 e 28 dias (CSV)
   - Search Console de cada site: consultas e páginas, últimos 28 dias (CSV)
   - Google Ads: campanhas com custo, cliques e conversões, últimos 7 dias (CSV)
   - Efí: total de Pix por dia e valor, **sem nome, CPF ou e-mail** (CSV)

   O Claude lê essa pasta pelo conector do Drive e atualiza o painel.

---

## Agente de conteúdo (publicação)

1. Publicar o orgânico do [briefing de conteúdo](briefing-conteudo.md) (seção "Orgânico") quando o chat de conteúdo entregar as peças:
   - Retrozap: 3 Reels por semana
   - Quiddo: 2 posts por semana
   - SportDNA: 2 carrosséis por semana
2. Todo link na bio e nos stories com UTM: `utm_source=instagram&utm_medium=organic&utm_campaign=<marca>_<tema>`.
3. **Retrozap:** nunca postar print de conversa real, nome ou telefone de cliente, nem com autorização.
4. Toda segunda: mandar ao Guilherme os 3 posts com mais salvamentos e compartilhamentos da semana. São candidatos a virar anúncio.
