"""未訳キーを表示: python todo.py [ns] [start] [count]  (ns省略で一覧)"""
import json, sys, glob
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from build import load_translations, official_keys, effective_missing
tr = load_translations()
rem = {}
official = official_keys()
keep = json.loads(Path("tr/_keep_english.json").read_text(encoding="utf-8"))
for f in glob.glob("extracted/*.json"):
    d = json.loads(Path(f).read_text(encoding="utf-8"))
    r = {k: v for k, v in effective_missing(d, official).items() if k not in tr.get(d["namespace"], {}) and k not in keep.get(d["namespace"], {})}
    if r: rem[d["namespace"]] = r
if len(sys.argv) < 2:
    for ns, r in sorted(rem.items(), key=lambda x: -len(x[1])): print(ns, len(r))
    print("TOTAL", sum(map(len, rem.values())))
else:
    ns = sys.argv[1]; s = int(sys.argv[2]) if len(sys.argv) > 2 else 0; n = int(sys.argv[3]) if len(sys.argv) > 3 else 100000
    for k, v in list(rem[ns].items())[s:s+n]:
        print(f"{k}\t{json.dumps(v, ensure_ascii=False)[1:-1]}")
