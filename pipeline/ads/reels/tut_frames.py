"""Quadros grandes de conferência do tutorial. Uso: python3 tut_frames.py <modo> <captura> <saida.jpg> t1 t2 ..."""
import json, sys, importlib.util
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import tut_edit as E
modo, CAP, OUT = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]); ts = [float(x) for x in sys.argv[4:]]
spec = importlib.util.spec_from_file_location('r', Path(__file__).with_name(f'tut_roteiro_{modo}.py')); r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
c = E.build(modo, CAP, r.roteiro(json.load(open(CAP / 'capture.json'))['marks']))
print(E.preview(c, OUT, ts, cols=min(4, len(ts)), scale=.42))
