"""Gera um export de grupo (formato Android do WhatsApp) da Turma do Churras, 2025-2026, para passar pelo fluxo real de importação do Retrozap."""
import random, datetime as dt, sys
random.seed(26)
P = [
 dict(n='Pedrão', w=30, h=(9, 23), m=['áudio omitido', 'imagem ocultada', 'figurinha omitida'], t=['bora churras sábado?', 'quem leva a carne?', 'porra que jogo ontem', 'kkkkkk', 'bora bora', 'fechou então', 'tô dentro', 'chego 13h', 'alguém tem caixa térmica?', 'bom dia família ☀️', 'vamos marcar logo isso', 'cês viram isso?', 'pqp kkkkk', 'eu levo o carvão']),
 dict(n='Lu', w=22, h=(8, 23), m=['áudio omitido', 'figurinha omitida', 'imagem ocultada', 'Esta mensagem foi apagada'], t=['kkkkkkkkkk', 'hahahaha morri', 'kkkk socorro', 'amo vcs 💖', 'chegou bem?', 'kkkkk não acredito', 'gente kkkkkk', 'eu vou!!', 'que saudade de vcs', 'rindo até agora kkkk', 'MORTA kkkkk']),
 dict(n='Caio', w=16, h=(10, 21), m=['figurinha omitida'] * 4 + ['imagem ocultada'], t=['blz', 'ok', '👍', 'pode deixar', 'fechou', 'tô chegando', 'manda o pix', 'quanto deu?']),
 dict(n='Bia', w=12, h=(7, 21), m=['áudio omitido'] * 5 + ['imagem ocultada', 'vídeo omitido'], t=['gente, deixa eu contar o que aconteceu hoje no trabalho porque vocês não vão acreditar, foi do começo ao fim uma novela', 'bom dia ☀️', 'cuidado na estrada hein', 'parabéns!!! 🎂🎉', 'olha isso que eu achei']),
 dict(n='Juninho', w=10, h=(0, 4), t=['alguém acordado?', 'não consigo dormir', 'kkkk', 'que fome 🍕', 'Esta mensagem foi apagada', 'Esta mensagem foi apagada', 'vamos marcar o futebol?', 'acordado ainda kkk']),
 dict(n='Tati', w=6, h=(11, 20), t=['foi mal, não vou conseguir', 'fica pra próxima', 'não vai dar hoje 😩', 'amo vcs', 'semana que vem eu vou', 'gente, surgiu um compromisso']),
 dict(n='Rafa', w=4, h=(12, 22), t=['e aí galera', 'bora!', 'kkkk', 'valeu pessoal', 'quem vai?']),
]
tw = sum(p['w'] for p in P)
def pick():
    r = random.random() * tw
    for p in P:
        r -= p['w']
        if r < 0: return p
    return P[0]
out = []
ini = dt.datetime(2025, 1, 4); fim = dt.datetime(2026, 11, 1)
d = ini
while d < fim:
    n = random.randint(4, 14) + (14 if d.year == 2026 else 0) + (80 if d.date() in (dt.date(2026, 2, 14), dt.date(2026, 7, 11), dt.date(2026, 9, 7)) else 0)
    for _ in range(n):
        p = pick(); h0, h1 = p['h']
        span = (h1 - h0) % 24 or 24
        hh = (h0 + random.randint(0, span)) % 24
        t = d.replace(hour=hh, minute=random.randint(0, 59))
        pm = {'Pedrão': .12, 'Lu': .12}.get(p['n'], .45)
        body = random.choice(p['m']) if p.get('m') and random.random() < pm else random.choice(p['t'])
        out.append((t, f"{t:%d/%m/%Y %H:%M} - {p['n']}: {body}"))
    d += dt.timedelta(days=1)
for i in range(1, 6):  # aniversários no grupo
    t = dt.datetime(2026, 5, 20, 8 + i, 5); out.append((t, f"{t:%d/%m/%Y %H:%M} - {P[i]['n']}: parabéns, Pedrão!!! 🎂🎉"))
out.sort()
hdr = '04/01/2025 10:00 - As mensagens e as ligações são protegidas com a criptografia de ponta a ponta.\n04/01/2025 10:01 - Pedrão criou o grupo "Turma do Churras"\n'
open(sys.argv[1], 'w').write(hdr + '\n'.join(l for _, l in out) + '\n')
print(len(out))
