"""Gera um export de conversa de casal (formato Android do WhatsApp) de Dani & Cris, 2025-2026, para o fluxo real de casal do Retrozap."""
import random, datetime as dt, sys
random.seed(14)
P = [
 dict(n='Dani', w=55, m=['áudio omitido', 'figurinha omitida', 'imagem ocultada'], pm=.18,
      t=['bom dia, amor ☀️', 'te amo ❤️', 'saudade de você 🥺', 'já chegou?', 'o que vamos jantar?', 'pizza hoje? 🍕', 'kkkkkk', 'amor, viu isso?', 'tô saindo agora', 'chegou bem?', 'meu amor 😍', 'desculpa, tava em reunião', 'bora no cinema sábado?', 'que fome', 'te amo muito 💕', 'manda foto', 'ai que saudade', 'boa noite, vida 😘', 'hahaha', 'vou passar no mercado, quer algo?']),
 dict(n='Cris', w=45, m=['áudio omitido', 'imagem ocultada', 'vídeo omitido'], pm=.22,
      t=['bom dia, vida', 'te amo mais ❤️', 'já tô indo', 'pode ser pizza', 'kkkk', 'onde você tá?', 'que saudade, bb', 'chegando em 10', 'amor 🥰', 'foi mal, sem bateria', 'bora!', 'comprei aquele doce', 'hahahaha', 'boa noite, amor', 'olha essa foto', 'quer jantar fora?', 'tô com saudade', 'perdão, esqueci', 'te espero aqui', 'neném 😍']),
]
out = []; d = dt.datetime(2025, 2, 14); fim = dt.datetime(2026, 11, 1)
while d < fim:
    n = random.randint(14, 30) + (12 if d.year == 2026 else 0) + (60 if d.date() in (dt.date(2025, 6, 12), dt.date(2026, 6, 12), dt.date(2026, 2, 14)) else 0)
    first = True
    for _ in range(n):
        p = P[0] if (first and random.random() < .62) else random.choices(P, weights=[p['w'] for p in P])[0]
        hh = 7 if first else random.choice(list(range(8, 24)) + [0, 1])
        t = d.replace(hour=hh, minute=random.randint(0, 59)); first = False
        body = random.choice(p['m']) if random.random() < p['pm'] else random.choice(p['t'])
        out.append((t, f"{t:%d/%m/%Y %H:%M} - {p['n']}: {body}"))
    d += dt.timedelta(days=1)
out.sort()
hdr = '14/02/2025 09:00 - As mensagens e as ligações são protegidas com a criptografia de ponta a ponta.\n'
open(sys.argv[1], 'w').write(hdr + '\n'.join(l for _, l in out) + '\n'); print(len(out))
