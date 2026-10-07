"""chaosmod の名前・進捗を規則で訳して tsv/v18_chaos_gen.tsv に書く(未訳キーのみ)。"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from build import load_translations, official_keys, effective_missing

NS = "chaosmod"
d = json.loads(Path(f"extracted/{NS}.json").read_text(encoding="utf-8"))
tr = load_translations()
tr.get(NS, {}).clear() if False else None
SELF = Path("tr/batch_tsv_v18_chaos_gen.json")
done = {}
for f in Path("tr").glob("*.json"):
    if f == SELF or f.name.startswith("_"):
        continue
    j = json.loads(f.read_text(encoding="utf-8"))
    done.update(j.get(NS, {}))
missing = {k: v for k, v in effective_missing(d, official_keys()).items() if k not in done}

TIER = {"Stable": "安定", "Unstable": "不安定", "Duality": "デュアリティ", "Void": "ヴォイド", "Basic": "基本",
        "Chaos": "カオス", "Chaotic": "カオス", "Stellar": "ステラー", "Darklight": "ダークライト",
        "Nova": "ノヴァ", "Zenith": "ゼニス", "Reality": "現実", "Center": "中央"}
NOUN = {
    "Particle": "粒子", "Bar": "インゴット", "Dust": "の粉", "Orb": "オーブ", "Sword": "の剣", "Pickaxe": "のツルハシ",
    "Axe": "の斧", "Helmet": "のヘルメット", "Chestplate": "のチェストプレート", "Leggings": "のレギンス",
    "Boots": "のブーツ", "Cable": "ケーブル", "Transporter Cable": "搬送ケーブル", "Extractor": "抽出機",
    "Refiner": "精製機", "Battery": "バッテリー", "Coal Generator": "石炭発電機", "Generator": "発電機",
    "Core": "コア", "Fragment": "の欠片", "Capacitor": "コンデンサー", "Circuit": "回路", "Wire": "ワイヤー",
    "Rod": "ロッド", "Shard": "の欠片", "Zombie": "ゾンビ", "Skeleton": "スケルトン", "Creeper": "クリーパー",
    "Spider": "クモ", "Stability Module": "安定化モジュール", "Speed Module": "速度モジュール",
    "Energy Module": "効率化モジュール", "Strata Stone": "の層状石", "Weathered Stone": "の風化石",
    "Banded Stone": "の縞状石", "Crystal Matrix": "の結晶基質", "Gleaming Stone": "の輝石",
    "Reality Loam": "の現実ローム", "Mineral Sand": "の鉱物砂", "Mineral Gravel": "の鉱物砂利",
    "Slate": "の粘板岩", "Porous Stone": "の多孔石", "Marbled Stone": "のマーブル石", "Cracked Stone": "のひび割れた石",
    "Crystal Schist": "の結晶片岩", "Dense Stone": "の高密度石", "Mineral Clay": "の鉱物粘土", "Silt": "のシルト",
    "Pebbled Soil": "の小石混じりの土", "Crystal Sand": "の結晶砂", "Particle Ore": "粒子鉱石", "Block": "ブロック",
    "Crystal Block": "クリスタルブロック", "Accelerator": "加速器", "Accelerator Curve": "加速器(曲線)",
    "Accelerator Input": "加速器入力", "Accelerator Rod": "加速ロッド", "Reactor Core": "リアクターコア",
    "Reactor Item Port": "リアクターアイテムポート", "Reactor Energy Port": "リアクターエネルギーポート",
    "Reactor Controller": "リアクター制御装置", "Matter": "物質", "Crystal": "クリスタル", "Pearl": "パール",
    "Geode": "ジオード", "Heart": "ハート", "Prism": "プリズム", "Essence": "エッセンス", "Flower": "フラワー",
    "Catalyst": "触媒", "Station": "ステーション", "Anvil": "金床", "Cube": "キューブ", "Converter": "変換機",
}
WHOLE = {
    "Nadir": "ナディア", "Zenith": "ゼニス", "Exotic Dust": "エキゾチックダスト", "Blackhole": "ブラックホール",
    "Orbital Deflector": "軌道偏向機", "Silica-Rich Sand": "シリカを多く含む砂", "Silicon Boule": "シリコンブール",
    "Doped Wafer": "ドープウエハー", "Potted Stellar Flower": "ステラーフラワーの植木鉢", "Antimatter Block": "反物質ブロック",
    "Darklight Ore": "ダークライト鉱石", "Gateway Terminal": "ゲートウェイ端末", "Gateway Frame": "ゲートウェイフレーム",
    "Reality Condensate": "現実凝縮物", "Energy Cable": "エネルギーケーブル", "Shadow Infused Coal": "影を宿した石炭",
    "Flux Crystal": "フラックスクリスタル", "Solarite": "ソラライト", "Machine Controller": "機械制御装置",
    "Dimensional Anchor": "次元アンカー", "Meteor": "隕石", "Reality Rift": "現実の裂け目", "Reality Wisp": "現実のウィスプ",
    "Rift Walker": "リフトウォーカー", "Reality Parasite": "現実寄生体", "Rift Residue": "裂け目の残滓",
    "Rift Core": "裂け目のコア", "Reality Anchor": "現実アンカー", "Black Hole": "ブラックホール",
    "Antimatter": "反物質", "Silicon Wafer": "シリコンウエハー", "Machine Casing": "機械筐体",
    "Silicon Dust": "シリコンの粉", "Silicon Rich Sand": "シリカを多く含む砂", "Unstable Particle": "不安定粒子",
    "Stable Particle": "安定粒子", "Reality Extractor": "現実抽出機", "Reality Core": "現実コア",
    "Basic Circuit": "基本回路", "Basic Capacitor": "基本コンデンサー", "Basic Battery": "基本バッテリー",
}


def name(en):
    if en in WHOLE:
        return WHOLE[en]
    m = re.fullmatch(r"(.+) Deposit", en)
    if m and name(m.group(1)):
        return name(m.group(1)) + "の鉱床"
    w = en.split(" ", 1)
    if len(w) == 2 and w[0] in TIER and w[1] in NOUN:
        t, n = TIER[w[0]], NOUN[w[1]]
        if n.startswith("の") and t in ("安定", "不安定"):
            return t + ("した" if t == "安定" else "な") + n[1:]
        return t + n
    return None


out = {}
for k, v in missing.items():
    if k.startswith(("item.", "block.", "entity.")):
        r = name(v)
        if r:
            out[k] = r

SUF = {"Storage": "蓄電", "Conduit": "導線", "Logistics": "物流", "Refinement": "精製", "Extraction": "抽出",
       "Excavation": "掘削", "Cleaver": "の斧", "Armor": "の防具", "Logic": "論理", "Power": "の力",
       "Matter": "物質", "Edge": "の刃", "Grade": "級", "Material": "素材", "Tier": "級", "Blade": "の刃",
       "Vein": "の鉱脈"}
TITLE = {
    "Chaos Logistics": "カオス物流", "Matter from Collision": "衝突から生まれた物質", "Vessel for Realities": "現実の器",
    "The Beginning": "はじまり", "Silicon Dust": "シリコンの粉", "Stellar Flower": "ステラーフラワー",
    "Stellar Essence": "ステラーエッセンス", "Stellar Bar": "ステラーインゴット", "The Eletronic Age": "電子の時代",
    "Doped and Ready": "ドープ完了", "Basic Logic": "基本の論理", "Stored Potential": "蓄えられた力",
    "Machine Foundation": "機械の土台", "First Charge": "はじめての充電", "Primitive Power": "原始的な電力",
    "Fueling the Void": "虚空への燃料", "Solar Ambition": "太陽の野望", "A dust from void?": "虚空からの粉？",
    "Into the Void": "虚空へ", "Void Station": "ヴォイドステーション", "Dual Nature": "二つの性質",
    "Chaotic Catalyst": "カオス触媒", "Perfect Refinement": "完璧な精製", "Synthetic Mining": "合成採掘",
    "Matter From Nothing": "無から物質を", "Extract the reality": "現実を抽出せよ", "Energy Line": "エネルギーライン",
    "Item Routing": "アイテム搬送", "Unstable Discovery": "不安定な発見", "Stabilized Matter": "安定した物質",
    "Antimatter Containment": "反物質の封じ込め", "What is inside?": "中には何が？", "Fallen Star Matter": "落ちた星の物質",
    "Unbalanced Blade": "不均衡な刃", "Balanced Blade": "均衡の刃", "Dual Blade": "二元の刃", "Dual Pickaxe": "二元のツルハシ",
    "Dual Axe": "二元の斧", "Blade of Darklight": "ダークライトの刃", "Darklight Fragment": "ダークライトの欠片",
    "Slayer": "殺戮者", "Destroyer": "破壊者", "Chaos Incarnate": "混沌の化身", "Anvil of Chaos": "混沌の金床",
    "The ultimate energy generator": "究極の発電機", "Orbital Deflection": "軌道偏向", "Nova Reactor": "ノヴァリアクター",
    "Reactor Core": "リアクターコア", "Energy Port": "エネルギーポート", "Item Port": "アイテムポート",
    "Zenith Accelerator": "ゼニス加速器", "Accelerator Input": "加速器入力", "Particle Alignment": "粒子の整列",
    "Chaos Tier": "カオス級", "Darklight Power": "ダークライトの力", "Void Logic": "ヴォイドの論理",
    "Basic Refinement": "基本の精製", "Duality Armor": "デュアリティの防具", "Chaos Armor": "カオスの防具",
}
NAMEMAP = {}
for k, v in d["missing"].items():
    if k.startswith(("item.", "block.", "entity.")):
        r = out.get(k) or done.get(k) or name(v)
        if r:
            NAMEMAP[v] = r
NAMEMAP.update({"Black Hole": "ブラックホール", "Silicon Rich Sand": "シリカを多く含む砂", "Silicon Dust": "シリコンの粉",
                "Silicon Wafer": "シリコンウエハー", "Machine Casing": "機械筐体", "Basic Circuit": "基本回路",
                "Basic Capacitor": "基本コンデンサー", "Basic Battery": "基本バッテリー", "Antimatter": "反物質",
                "Unstable Particle": "不安定粒子", "Stable Particle": "安定粒子"})


def desc(en):
    for pat, ja in [(r"Craft (?:a|an|your first|the) (.+?)\.?", "{}をクラフトする。"),
                    (r"Upgrade (?:into|to) a (.+)\.", "{}にアップグレードする。"),
                    (r"Obtain (?:a|an) (.+?)\.?", "{}を手に入れる。"), (r"Create a (.+)\.", "{}を作る。"),
                    (r"Find (?:a )?(.+)\.", "{}を見つける。"), (r"Get (.+)\.", "{}を手に入れる。"),
                    (r"Harness energy with a (.+)\.", "{}でエネルギーを得る。")]:
        m = re.fullmatch(pat, en)
        if m and m.group(1) in NAMEMAP:
            return ja.format(NAMEMAP[m.group(1)])
    return None


for k, v in missing.items():
    if not k.startswith("advancements.") or k in out:
        continue
    if k.endswith(".title"):
        r = TITLE.get(v)
        if not r:
            w = v.split(" ", 1)
            if len(w) == 2 and w[0] in TIER and w[1] in SUF:
                r = TIER[w[0]] + SUF[w[1]]
            elif v in NAMEMAP:
                r = NAMEMAP[v]
    else:
        r = desc(v)
    if r:
        out[k] = r

lines = [f"## {NS}"] + [f"{k}\t{v}" for k, v in out.items()]
Path("tsv/v18_chaos_gen.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("gen", len(out))
for k, v in missing.items():
    if k not in out:
        print(f"{k}\t{v}")
