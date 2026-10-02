"""ModJP_Pack の全JSONを厳密にパースし、公式訳の上書きがないかを確認する。"""
import json, glob
from pathlib import Path

PACK = Path(__file__).parent / "pack"
DESC = "§6MOD日本語化パック §7v1.2 (1.20.1)"


def strict_load(p):
    raw = p.read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf"), f"BOM付き: {p}"
    def no_dup(pairs):
        keys = [k for k, _ in pairs]
        dup = {k for k in keys if keys.count(k) > 1}
        assert not dup, f"重複キー {dup} in {p}"
        return dict(pairs)
    return json.loads(raw.decode("utf-8"), object_pairs_hook=no_dup)


files = sorted(PACK.rglob("*.json")) + [PACK / "pack.mcmeta"]
total = 0
for p in files:
    d = strict_load(p)
    if p.name == "pack.mcmeta":
        assert d == {"pack": {"pack_format": 15, "description": DESC}}, d
        continue
    assert all(isinstance(v, str) for v in d.values()), p
    ns = p.parts[-3]
    ex = json.loads(Path(f"extracted/{ns}.json").read_text(encoding="utf-8"))
    over = [k for k in d if k in ex["ja_jp"] and d[k] != ex["ja_jp"][k]]
    assert not over, f"公式訳を上書き: {ns} {over[:3]}"
    restored = sum(1 for k in d if k in ex["ja_jp"])
    assert not restored, f"{ns}: 公式訳のキーを{restored}件含んでいる(他人の訳の同梱は禁止)"
    total += len(d)
    print(f"OK {ns:24} {len(d):6} keys" + (f" (うち公式訳の復旧 {restored})" if restored else ""))
for f in glob.glob("tr/*.json"):
    strict_load(Path(f))
print(f"全 {len(files)} ファイル パース成功 / 合計 {total} キー / 公式訳の上書き 0")
