# 配布済みzipと現在のpack/を比べ、消えたキーを表示する: python diff_pack.py dist/xxx.zip
import zipfile, json, sys
from pathlib import Path
z = zipfile.ZipFile(sys.argv[1])
old = {n.split("/")[1]: json.loads(z.read(n).decode("utf-8")) for n in z.namelist() if n.endswith("lang/ja_jp.json")}
new = {p.parts[-3]: json.loads(p.read_text(encoding="utf-8")) for p in Path("pack/assets").glob("*/lang/ja_jp.json")}
for ns, d in old.items():
    gone = set(d) - set(new.get(ns, {}))
    if gone:
        print(ns, len(gone), sorted(gone)[:5])
