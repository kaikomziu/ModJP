"""tfmg の規則的な名前(色付きブロック・素材別部品・石材)を訳して tsv/v18_tfmg_gen.tsv に書く。残りを表示。"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from build import official_keys, effective_missing

NS = "tfmg"
d = json.loads(Path(f"extracted/{NS}.json").read_text(encoding="utf-8"))
SELF = Path("tr/batch_tsv_v18_tfmg_gen.json")
done = {}
for f in Path("tr").glob("*.json"):
    if f == SELF or f.name.startswith("_"):
        continue
    done.update(json.loads(f.read_text(encoding="utf-8")).get(NS, {}))
missing = {k: v for k, v in effective_missing(d, official_keys()).items() if k not in done}

COL = {"White": "白色", "Orange": "橙色", "Magenta": "赤紫色", "Light Blue": "空色", "Yellow": "黄色", "Lime": "黄緑色",
       "Pink": "桃色", "Gray": "灰色", "Light Gray": "薄灰色", "Cyan": "青緑色", "Purple": "紫色", "Blue": "青色",
       "Brown": "茶色", "Green": "緑色", "Red": "赤色", "Black": "黒色"}
MAT = {"Aluminum": "アルミニウム", "Brass": "真鍮", "Cast Iron": "鋳鉄", "Steel": "鋼鉄", "Copper": "銅",
       "Constantan": "コンスタンタン", "Lead": "鉛", "Nickel": "ニッケル", "Zinc": "亜鉛", "Plastic": "プラスチック",
       "Heavy": "重", "Steel Casing": "鋼鉄ケーシング"}
PART = {"Bars": "の格子", "Cable Hub": "のケーブルハブ", "Cogwheel": "の歯車", "Large {} Cogwheel": "", "Door": "のドア",
        "Fluid Tank": "の液体タンク", "Fluid Valve": "の液体バルブ", "Flywheel": "のフライホイール", "Frame": "のフレーム",
        "Ladder": "のハシゴ", "Lamp": "のランプ", "Mechanical Pump": "のメカニカルポンプ", "Pipe": "のパイプ",
        "Scaffolding": "の足場", "Smart Fluid Pipe": "のスマート液体パイプ", "Truss": "のトラス", "Chemical Vat": "の化学槽",
        "Gearbox": "のギアボックス", "Trapdoor": "のトラップドア", "Axe": "の斧", "Hoe": "のクワ", "Pickaxe": "のツルハシ",
        "Shovel": "のシャベル", "Sword": "の剣", "Spool": "のスプール", "Wire": "ワイヤー", "Encased Shaft": "で覆われたシャフト"}
SHAPE = {"": "", " Slab": "のハーフブロック", " Stairs": "の階段", " Wall": "の塀"}
STONE = {"Bauxite": "ボーキサイト", "Galena": "方鉛鉱"}


def cog(s):
    m = re.fullmatch(r"(Large )?(Aluminum|Steel) Cogwheel", s)
    if m:
        return ("大きな" if m.group(1) else "") + MAT[m.group(2)] + "の歯車"
    if s == "Shaft":
        return "シャフト"
    return None


def name(en):
    for c, cj in COL.items():
        for sh, shj in SHAPE.items():
            if en == f"{c} Rebar Concrete{sh}":
                return f"{cj}の鉄筋コンクリート{shj}"
        if en == f"{c} Caution Block":
            return f"{cj}の警告ブロック"
        if en == f"{c} Multimeter":
            return f"{cj}のマルチメーター"
    for s, sj in STONE.items():
        for sh, shj in SHAPE.items():
            for pat, ja in [(f"Cut {s}", f"切り出し{sj}"), (f"Cut {s} Brick", f"切り出し{sj}レンガ"),
                            (f"Polished Cut {s}", f"磨かれた切り出し{sj}"), (f"Small {s} Brick", f"小さな{sj}レンガ")]:
                if en == pat + sh:
                    return ja + shj
            if en == f"Cut {s} Bricks":
                return f"切り出し{sj}レンガ"
            if en == f"Small {s} Bricks":
                return f"小さな{sj}レンガ"
        if en == f"Layered {s}":
            return f"層状の{sj}"
        if en == f"{s} Pillar":
            return f"{sj}の柱"
    m = re.fullmatch(r"(Copper|Steel|Heavy Casing) Encased (.+)", en)
    if m:
        inner = cog(m.group(2)) or (MAT.get(m.group(2)[:-5]) + "のパイプ" if m.group(2).endswith(" Pipe") and m.group(2)[:-5] in MAT else None)
        if inner:
            return {"Copper": "銅", "Steel": "鋼鉄", "Heavy Casing": "重機ケーシング"}[m.group(1)] + "で覆われた" + inner
    m = re.fullmatch(r"Glass (.+) Pipe", en)
    if m and m.group(1) in MAT:
        return f"ガラス窓付き{MAT[m.group(1)]}のパイプ"
    if cog(en):
        return cog(en)
    for mt, mj in MAT.items():
        for p, pj in PART.items():
            if en == f"{mt} {p}" and pj:
                return mj + pj
    return None


out = {}
for k, v in missing.items():
    if k.startswith(("item.", "block.")) and ".tooltip" not in k:
        r = name(v)
        if r:
            out[k] = r
lines = [f"## {NS}"] + [f"{k}\t{v}" for k, v in out.items()]
Path("tsv/v18_tfmg_gen.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("gen", len(out))
seen = set()
for k, v in sorted(missing.items()):
    if k not in out and (v not in seen or not ".tooltip" in k):
        print(f"{k}\t{v}")
        seen.add(v)
