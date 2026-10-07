"""extracted_prev と extracted を比べ、訳済みキーで英語の原文が変わったものを列挙する"""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path(__file__).parent))
from build import load_translations
tr = load_translations()
n = 0
for f in sorted(Path('extracted').glob('*.json')):
    o = Path('extracted_prev') / f.name
    if not o.exists():
        continue
    new = json.loads(f.read_text(encoding='utf-8')); old = json.loads(o.read_text(encoding='utf-8'))
    ns = new['namespace']
    for k, v in new['missing'].items():
        if k in tr.get(ns, {}) and k in old['en_us'] and old['en_us'][k] != v:
            print(f"{ns}\t{k}\t{json.dumps(old['en_us'][k], ensure_ascii=False)}\t=>\t{json.dumps(v, ensure_ascii=False)}\t||\t{json.dumps(tr[ns][k], ensure_ascii=False)}")
            n += 1
print('changed', n)
