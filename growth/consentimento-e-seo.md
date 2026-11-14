# Aviso de cookies, privacidade e SEO: padrão BTW

Vale para Retrozap, Quiddo e SportDNA. Escrito em 14/11/2026.

## 1. Aviso de cookies (barra curta)

**Objetivo:** mais aceites com um aviso leve, sem enganar e sem quebrar a LGPD nem o Guia de Cookies da ANPD.

- **Uma frase só, no tom de cada marca**, mais um link para a seção de medição da política de privacidade. Exemplos de estrutura (adapte as palavras, não copie de concorrentes):
  - Retrozap: "Usamos cookies de medição do Google e do Meta. Sua conversa continua no celular. [O que é medido]"
  - Quiddo: "Usamos cookies para medir visitas e anúncios. O Quiddo funciona igual sem eles. [O que é medido]"
  - SportDNA: "Usamos cookies para medir visitas e anúncios. Os testes funcionam igual sem eles. [O que é medido]"
- **O link** leva direto à seção de medição da política (ex.: `/privacidade#medicao`).
- **Componente igual nos 3 sites** (decisão do dono, 14/11):
  - **"Aceitar" é o botão principal**: preenchido, na cor de destaque da marca, à direita e com o foco inicial.
  - **"Recusar" é o botão secundário**: só contornado ou fantasma, em cor neutra, na mesma barra e no mesmo nível, com o mesmo tamanho e altura (mínimo de 44 px) e texto legível com contraste AA. Ele pode ser visualmente discreto, mas nunca pode virar link pequeno, ficar escondido numa segunda camada ou sumir.
  - **Texto curto e leve**, sem detalhe técnico. Quem quiser mais clica em "Saiba mais", que leva à seção de medição da política.
- **Barra discreta no rodapé da tela.** Não bloqueia o site, e o site funciona igual com recusa.
- **Antes do aceite nada de terceiros carrega**, a não ser os pings sem cookie do Consent Mode v2 onde já existem.
- **Sem respostas presumidas.** Fechar a barra ou não responder conta como recusa.
- **Mudar de ideia:** link no rodapé com o estado atual ("Medição ligada" / "Medição desligada"), que reabre o aviso. Revogar tem que ser tão fácil quanto aceitar.
- **Não mexer no que já funciona:**
  - chaves de consentimento, captura de consentimento da Conversions API e revogação (`/api/meta/revoke`);
  - nomes de eventos usados por anúncios, públicos e conversões: CreateRoom, QuizStarted, QuizCompleted, OfferViewed, InitiateCheckout, CheckoutOpened, Purchase, RetrospectivaIniciada, RetrospectivaConcluida, OfertaVista, CheckoutAberto, PixGerado, TentativaCheckout.

## 2. Política de privacidade: seção "O que medimos"

Escreva com as palavras e a estrutura de cada site, **descrevendo só o que o código faz de verdade**. Antes de escrever, confira no código. Nunca prometa o que não é verdade.

Estrutura sugerida, em linguagem simples:

1. **Quem é o responsável e como pedir algo:** Beyond the Work, CNPJ 69.746.447/0001-00, e o e-mail de contato do site.
2. **O que guardamos e por quê:** o mínimo de cada produto.
3. **O que não guardamos:**
   - Retrozap: conversas, nomes e telefones nunca saem do celular.
   - Quiddo: perguntas e respostas, quando for verdade.
4. **Medição com aceite:**
   - O que Google e Meta recebem: visitas, etapas e a compra confirmada, com o e-mail protegido por hash quando for o caso.
   - Que eles podem ligar a visita à conta da pessoa no Google, no Facebook ou no Instagram, conforme as regras deles.
   - Que sem aceite nada disso carrega.
5. **Parâmetros de campanha (UTM)** guardados quando a pessoa chega por anúncio: são dados do anúncio, não da pessoa.
6. **Lista curta de cookies:** necessários (nossos) e de medição (terceiros, só com aceite).
7. **Como mudar de ideia:** link no rodapé.
8. **Com quem compartilhamos:**
   - pagamento: Stripe e Mercado Pago, ou Efí onde houver;
   - e-mail, se houver;
   - Google e Meta, só com aceite.

   Não vendemos dados.
9. **Por quanto tempo guardamos, direitos da LGPD e mudanças nesta política.**

## 3. SEO: checklist de boas práticas

- **Páginas indexáveis:**
  - um `<title>` único (até cerca de 60 caracteres), com a busca principal antes da marca;
  - uma meta description única (até cerca de 155);
  - um `<h1>`;
  - `lang="pt-BR"` e canonical absoluto.
- **Compartilhamento:** Open Graph e Twitter Card com imagem 1200×630.
- **Indexação:**
  - `sitemap.xml` completo (todas as páginas e artigos, com `lastmod`) e citado no `robots.txt`;
  - `robots.txt` sem bloquear o que deve ranquear;
  - conteúdo importante não pode depender só de `#hash` (o Google não indexa rotas por hash): artigos precisam de URL própria em HTML estático.
- **Dados estruturados (JSON-LD):**
  - `Organization` e `WebSite`;
  - `SoftwareApplication` ou `Product` com `Offer` (preço em BRL) nas páginas de produto;
  - `FAQPage` onde houver perguntas e respostas visíveis;
  - `Article` nos posts e guias;
  - `BreadcrumbList`.
- **Conteúdo:**
  - links internos entre guias, artigos e a página do teste ou produto;
  - textos-âncora descritivos;
  - páginas de intenção de busca, como "qual raquete comprar", "quiz para confraternização" e "retrospectiva do grupo do WhatsApp".
- **Imagens:** `alt` descritivo, `width`/`height`, formatos modernos e `loading="lazy"` abaixo da dobra.
- **Velocidade:** fontes com `font-display: swap` e preload da principal; nada bloqueando a renderização sem necessidade. Meta de Core Web Vitals: LCP < 2,5 s, CLS < 0,1, INP < 200 ms.
- **Páginas que não devem aparecer na busca** (`noindex`): `/medicao`, páginas de teste e páginas de checkout ou conta.
- **Sem conteúdo duplicado:** escolher entre www e sem www e redirecionar a outra; canonical consistente.
