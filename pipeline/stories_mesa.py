"""Injeta os stories avulsos (stories_extra.py) na Mesa publicada, sem tocar nas peças do pack, nos votos nem nos ADs.
O dia vira um número relativo ao dia 1 do pack em common.DATAS (ex.: 16/11 = -6 no S03) e ganha um rótulo "Extra · <dia>".
Também troca os laços fixos de dia 1..7 do template pelos dias do manifesto (DK).
Uso: python3 stories_mesa.py <index.html publicado, sem o esqueleto> <pasta dos renders> <saida.html> [IDs]"""
import datetime as dt, hashlib, json, re, sys
from pathlib import Path
import common as C
from stories_extra import STORIES

live, rd, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]); ids = set(sys.argv[4:]) or set(STORIES)
DIAS_SEM = ['seg', 'ter', 'qua', 'qui', 'sex', 'sáb', 'dom']
d1 = dt.datetime.strptime(C.DATAS[1][:10], '%d/%m/%Y').date()
s = live.read_text()
# template: dias do manifesto em vez de 1..7
if 'const DK=' not in s:
    a = "const DAYS = M.days ||"
    assert a in s
    i = s.index(a); j = s.index(';', s.index('}', i)) + 1
    s = s[:j] + "\n  const DK=Object.keys(M.days||DAYS).map(Number).sort((a,b)=>a-b);" + s[j:]
    s = s.replace('[1,2,3,4,5,6,7].map(d=>[String(d)', 'DK.map(d=>[String(d)').replace('const days = [1,2,3,4,5,6,7].filter', 'const days = DK.filter')
    s = s.replace('[1,2,3,4,5,6,7].forEach(d=>{', 'DK.forEach(d=>{')
    assert '[1,2,3,4,5,6,7]' not in s
m = re.search(r'(<script id="manifest" type="application/json">)(.*?)(</script>)', s, re.S)
M = json.loads(m.group(2).replace('<\\/', '</'))
have = {p['id'] for p in M['pieces']}
for sid in sorted(ids):
    st = STORIES[sid]; data = dt.datetime.strptime(st['data'][:10], '%d/%m/%Y').date()
    day = (data - d1).days + 1; dia = f"{DIAS_SEM[data.weekday()]} {data:%d/%m}"
    if 1 <= day <= 7: raise SystemExit(f'{sid}: {dia} cai dentro do pack; use o pack')
    M['days'][str(day)] = f'Extra · {dia}'
    png = rd / f'{sid}.png'
    p = dict(id=sid, brand=st['brand'], fmt='story', day=day, dia=dia, slot='', title=st['title'], kind='story', caption='(story, sem legenda)',
             notes=st['notes'], version=f'X-{sid}-v1', v=1, hash=hashlib.md5(png.read_bytes()).hexdigest()[:10], media=[f'{sid}.png'],
             editable=f'editaveis/{sid}.html', duration=None, sticker='', previews=[f'{sid}.jpg'])
    assert sid not in have, f'{sid} já está na Mesa'
    M['pieces'].append(p)
js = json.dumps(M, ensure_ascii=False).replace('</', '<\\/')
out.write_text(s[:m.start(2)] + js + s[m.end(2):])
print('ok', len(M['pieces']), 'peças;', sorted(M['days'], key=int))
