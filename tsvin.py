"""tsv/*.tsv(「## namespace」見出し + キー<TAB>訳)を tr/batch_tsv_<名前>.json に変換する。
訳の中の \n は改行に変換。未翻訳リストに無いキーはエラー。"""
import json, sys
from pathlib import Path
WORK = Path(__file__).parent
bad = 0
for f in sorted((WORK / "tsv").glob("*.tsv")):
    out, ns, miss, pre = {}, None, {}, ""
    for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        if line.startswith("## "):
            ns = line[3:].strip()
            miss = json.loads((WORK / f"extracted/{ns}.json").read_text(encoding="utf-8"))["missing"]
            out.setdefault(ns, {})
            continue
        if line.startswith("@ "):  # @ 接頭辞 : 以降「.」で始まるキーは接頭辞+残り(長いキーの省略用)
            pre = line[2:].strip()
            continue
        if "\t" not in line:
            print(f"{f.name}:{n}: タブ無し: {line[:60]}"); bad += 1; continue
        k, v = line.split("\t", 1)
        if k.startswith(".") and pre:
            k = pre + k[1:]
        if k.startswith("="):  # =英文<TAB>訳 : この名前空間で英文が完全一致する未訳キーすべてに適用
            src = k[1:].replace("\\n", "\n")
            hit = [mk for mk, mv in miss.items() if mv == src]
            if not hit:
                print(f"{f.name}:{n}: 一致する英文なし {ns}:{src[:40]}"); bad += 1
            for mk in hit:
                out[ns].setdefault(mk, v.replace("\\n", "\n"))
            continue
        if k not in miss:
            print(f"{f.name}:{n}: 未翻訳リストに無いキー {ns}:{k}"); bad += 1; continue
        out[ns][k] = v.replace("\\n", "\n").replace("\\r", "\r")
    (WORK / "tr" / f"batch_tsv_{f.stem}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
sys.exit(1 if bad else 0)
