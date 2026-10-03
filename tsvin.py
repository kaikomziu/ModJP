"""tsv/*.tsv(「## namespace」見出し + キー<TAB>訳)を tr/batch_tsv_<名前>.json に変換する。
訳の中の \n は改行に変換。未翻訳リストに無いキーはエラー。"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from build import BUNDLE_BROKEN_OFFICIAL
WORK = Path(__file__).parent
bad = 0
STRICT = "v15"  # 今回の版のTSVだけ厳密にチェック(古いTSVはMOD差し替えで消えたキー・名前空間を黙って飛ばす)
stale = 0
for f in sorted((WORK / "tsv").glob("*.tsv")):
    out, ns, miss, pre = {}, None, {}, ""
    for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        if line.startswith("## "):
            ns = line[3:].strip()
            if not (WORK / f"extracted/{ns}.json").exists():
                if f.stem.startswith(STRICT):
                    print(f"{f.name}:{n}: 名前空間なし {ns}"); bad += 1
                miss = None; continue
            _d = json.loads((WORK / f"extracted/{ns}.json").read_text(encoding="utf-8"))
            miss = _d["en_us"] if (_d.get("ja_broken") and not BUNDLE_BROKEN_OFFICIAL) else _d["missing"]
            out.setdefault(ns, {})
            continue
        if line.startswith("@ "):  # @ 接頭辞 : 以降「.」で始まるキーは接頭辞+残り(長いキーの省略用)
            pre = line[2:].strip()
            continue
        if miss is None:
            stale += 1; continue
        if "\t" not in line:
            print(f"{f.name}:{n}: タブ無し: {line[:60]}"); bad += 1; continue
        k, v = line.split("\t", 1)
        if k.startswith(".") and pre:
            k = pre + k[1:]
        if k.startswith("="):  # =英文<TAB>訳 : この名前空間で英文が完全一致する未訳キーすべてに適用
            src = k[1:].replace("\\n", "\n")
            hit = [mk for mk, mv in miss.items() if mv == src]
            if not hit and f.stem.startswith(STRICT):
                print(f"{f.name}:{n}: 一致する英文なし {ns}:{src[:40]}"); bad += 1
            for mk in hit:
                out[ns].setdefault(mk, v.replace("\\n", "\n"))
            continue
        if k not in miss and not f.stem.startswith(STRICT):
            stale += 1; continue
        if k not in miss:
            print(f"{f.name}:{n}: 未翻訳リストに無いキー {ns}:{k}"); bad += 1; continue
        out[ns][k] = v.replace("\\n", "\n").replace("\\r", "\r")
    (WORK / "tr" / f"batch_tsv_{f.stem}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("古いTSVで使われなくなった行:", stale)
sys.exit(1 if bad else 0)
