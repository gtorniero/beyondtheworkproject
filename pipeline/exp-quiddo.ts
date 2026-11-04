import { avatarSvg, comMoldura } from '../sites/quiddo/src/lib/avatar-art';
import { miniVisual, cortinaVisual } from '../sites/quiddo/src/lib/visuais-arte';
import { simbolo, OLHO } from '../sites/quiddo/src/lib/simbolos';
const out: any = { av: {}, mini: {}, cortina: {}, sim: [], olho: OLHO };
const bichos = ['tucano','capivara','onca','preguica','arara','mico','tamandua','tatu','boto','jacare','loboguara','quati','sapo','coruja','jabuti','papagaio','bemtevi','caramelo','gato','peixeboi'];
const cab = ['-','bone','palha','coroa','laranja','flor','fone','festa','gorro','faixa','cartola'];
const ros = ['-','escuros','redondos','coracao','bigode','estrela'];
for (const b of bichos) for (const h of cab) for (const f of ros) for (let c=0;c<10;c++) {
  const k = `${b}.${h}.${f}.${c}`; out.av[k] = avatarSvg(k, 120);
}
for (const v of ['floresta','escritorio','entretenimento','sala','album','espaco','amor'] as const) out.mini[v] = miniVisual(v);
for (const v of ['escritorio','entretenimento','sala','album','espaco','amor'] as const) out.cortina[v] = cortinaVisual(v);
for (let i=0;i<4;i++) out.sim.push(simbolo(i));
out.lider = (s:string)=>0;
console.log(JSON.stringify(out));
