"""TSV(キー<TAB>訳)を tr/batch_*.json に変換する。長文の多いMOD向け。

usage: python tsv2tr.py <namespace> <出力名> <tsv...>
- 行頭の "@" は "gui.xaero_" に展開する(Xaero系のキー省略用)
- 訳の中の "\\n" は改行に変換する
"""
import json, sys
from pathlib import Path

WORK = Path(__file__).parent
ns, name, files = sys.argv[1], sys.argv[2], sys.argv[3:]
miss = json.loads((WORK / f"extracted/{ns}.json").read_text(encoding="utf-8"))["missing"]
out = {}
for f in files:
    for n, line in enumerate(Path(f).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        k, v = line.split("\t", 1)
        if k.startswith("@"):
            k = "gui.xaero_" + k[1:]
        if k not in miss:
            sys.exit(f"{f}:{n}: 未翻訳リストに無いキー {k}")
        out[k] = v.replace("\\n", "\n")
(WORK / "tr" / f"batch_{name}.json").write_text(json.dumps({ns: out}, ensure_ascii=False, indent=1), encoding="utf-8")
print(ns, len(out), "/", len(miss))
