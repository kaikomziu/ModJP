"""色や名前の組み合わせで機械的に作れるキーを生成 → tr/batch_15_pattern_gen.json

- runelic: 旗の模様「<色> Rune x」
"""
import json, re
from pathlib import Path

WORK = Path(__file__).parent
van = json.loads((WORK / "vanilla/ja_jp.json").read_text(encoding="utf-8"))
COLOR_EN = {}
for c in ["black", "blue", "brown", "cyan", "gray", "green", "light_blue", "light_gray", "lime",
          "magenta", "orange", "pink", "purple", "red", "white", "yellow"]:
    COLOR_EN[c] = van["color.minecraft." + c]


def miss(ns):
    return json.loads((WORK / f"extracted/{ns}.json").read_text(encoding="utf-8"))["missing"]


out = {}

# runelic
m = miss("runelic")
o = {"itemGroup.runelic.creative_tab": "Runelic", "item.runelic.runelic_pattern.desc": "ルーン文字"}
for k, v in m.items():
    r = re.match(r"block\.minecraft\.banner\.runelic\.runelic_(\w+)\.(\w+)$", k)
    if r and r.group(2) in COLOR_EN:
        o[k] = f"{COLOR_EN[r.group(2)]}のルーン {r.group(1)}"
out["runelic"] = {k: v for k, v in o.items() if k in m}

# productivebees: 巣箱・拡張ボックス・石化したハチミツ
WOOD = {
    "Ebony": "黒檀", "Witch Hazel": "マンサク", "Skyris": "スカイリス", "Ether": "エーテル", "Pine": "マツ",
    "Zelkova": "ケヤキ", "Lament": "嘆きの木", "Palm": "ヤシ", "Sythian": "シシアン", "Jacaranda": "ジャカランダ",
    "Fir": "モミ", "Cika": "チカ", "Embur": "エンバー", "Green Enchanted": "緑の魔法の木", "Mahogany": "マホガニー",
    "Redwood": "セコイア", "Imparius": "インパリウス", "Aspen": "ポプラ", "Bulbis": "バルビス", "Nightshade": "ナイトシェード",
    "White Mangrove": "白いマングローブ", "Cypress": "イトスギ", "Willow": "ヤナギ", "Blue Enchanted": "青の魔法の木",
    "Baobab": "バオバブ", "Maple": "カエデ", "Holly": "ヒイラギ", "Wisteria": "フジ", "Rosewood": "ローズウッド",
    "Kousa": "ヤマボウシ", "Grimwood": "グリムウッド", "Yucca": "ユッカ", "Morado": "モラド", "River": "リバー",
    "Driftwood": "流木", "Socotra": "ソコトラ", "Eucalyptus": "ユーカリ", "Kapok": "カポック", "Cobalt": "コバルト",
    "Dead": "枯れ木", "Pink Bioshroom": "桃色のバイオシュルーム", "Magnolia": "モクレン",
    "Yellow Bioshroom": "黄色のバイオシュルーム", "Blue Bioshroom": "青色のバイオシュルーム", "Blackwood": "ブラックウッド",
    "Joshua": "ジョシュア", "Alpha Oak": "アルファオーク", "Green Bioshroom": "緑色のバイオシュルーム", "Larch": "カラマツ",
    "Mauve": "モーブ", "Poise": "ポイズ", "Magic": "魔法の木", "Umbran": "アンブラン", "Hellbark": "ヘルバーク",
    "Blossom": "花", "Azalea": "ツツジ", "Bamboo": "竹", "Cherry": "サクラ", "Crimson": "真紅", "Birch": "シラカバ",
    "Oak": "オーク", "Acacia": "アカシア", "Warped": "歪んだ", "Jungle": "ジャングル", "Dark Oak": "ダークオーク",
    "Mangrove": "マングローブ", "Snake Block": "ヘビブロック", "Spruce": "トウヒ", "Canvas": "キャンバス",
}
m = miss("productivebees")
o = {}
for k, v in m.items():
    if not k.startswith("block.productivebees."):
        continue
    r = re.match(r"Advanced (.+) Beehive$", v)
    if r and r.group(1) in WOOD:
        o[k] = f"高度な{WOOD[r.group(1)]}の養蜂箱"
        continue
    r = re.match(r"(.+) Expansion Box$", v)
    if r and r.group(1) in WOOD:
        o[k] = f"{WOOD[r.group(1)]}の拡張ボックス"
        continue
    r = re.match(r"block\.productivebees\.(\w+)_petrified_honey$", k)
    if r and r.group(1) in COLOR_EN:
        o[k] = f"{COLOR_EN[r.group(1)]}の石化したハチミツ"
out["productivebees"] = o

(WORK / "tr/batch_15_pattern_gen.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print({k: len(v) for k, v in out.items()})
