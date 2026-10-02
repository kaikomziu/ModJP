"""定型パターンの名前を生成する(Alex's Mobs の旗の模様、Astra Shastra の防具、Obscure API の攻撃速度アイコン)。"""
import json, re
from pathlib import Path
from furn_common import COLOR

COLOR = {**COLOR, "Silver": "薄灰色"}
out = {}


def load(ns):
    return json.loads(Path(f"extracted/{ns}.json").read_text(encoding="utf-8"))["missing"]


# Alex's Mobs の旗の模様(バニラの「白色の縁取り」と同じ語形)
PAT = {"Bear": "クマ", "Star Cross": "星の十字", "Union Jack Ensign": "ユニオンジャックの旗", "Sun Symbol": "太陽の紋章",
       "Caption Band": "標語の帯"}
CR = "|".join(map(re.escape, sorted(COLOR, key=len, reverse=True)))
r = {}
for k, v in load("alexsmobs").items():
    m = re.fullmatch(rf"({CR}) (.+)", v)
    if k.startswith("block.minecraft.banner.") and m and m.group(2) in PAT:
        r[k] = f"{COLOR[m.group(1)]}の{PAT[m.group(2)]}"
out["alexsmobs"] = r

# Astra Shastra
NAME = {"Agni-Kavacha": "アグニ・カヴァチャ", "Divine Kavacha": "神聖なカヴァチャ", "Gada-Kavacha": "ガダ・カヴァチャ",
        "Iron Kavacha": "鉄のカヴァチャ", "Kavacha-Kundala": "カヴァチャ・クンダラ", "Kirita-Mukuta": "キリータ・ムクタ",
        "Mahishasura-Mardini": "マヒシャースラ・マルディニー", "Surya-Kavacha": "スーリヤ・カヴァチャ",
        "Vaijayanti-Kavacha": "ヴァイジャヤンティー・カヴァチャ", "Vajra-Kavacha": "ヴァジュラ・カヴァチャ",
        "Varuna-Kavacha": "ヴァルナ・カヴァチャ", "Vayu-Kavacha": "ヴァーユ・カヴァチャ", "Wooden Kavacha": "木のカヴァチャ",
        "Yamadharma-Kavacha": "ヤマダルマ・カヴァチャ"}
PIECE = {"Boots": "の具足", "Cuirass": "の胸甲", "Helm": "の兜", "Greaves": "のすね当て"}
FIXED = {"Astra Shastra": "Astra Shastra", "Daitya": "ダイティヤ", "Mahishasura": "マヒシャースラ", "Rakshasa": "ラークシャサ",
         "Brahmastra": "ブラフマーストラ", "Daitya Spawn Egg": "ダイティヤのスポーンエッグ", "Gandiva": "ガーンディーヴァ",
         "Iron Chakra": "鉄のチャクラム", "Iron Gandiva": "鉄のガーンディーヴァ", "Iron Kaumodaki": "鉄のカウモーダキー",
         "Kaumodaki": "カウモーダキー", "Mahishasura Spawn Egg": "マヒシャースラのスポーンエッグ",
         "Rakshasa Spawn Egg": "ラークシャサのスポーンエッグ", "Sudarshana Chakra": "スダルシャナ・チャクラ", "Vajra": "ヴァジュラ",
         "Wooden Chakra": "木のチャクラム", "Wooden Gandiva": "木のガーンディーヴァ", "Wooden Kaumodaki": "木のカウモーダキー"}
NR = "|".join(map(re.escape, sorted(NAME, key=len, reverse=True)))
r = {}
for k, v in load("astrashastra").items():
    m = re.fullmatch(rf"({NR}) (Boots|Cuirass|Helm|Greaves)", v)
    if m:
        r[k] = NAME[m.group(1)] + PIECE[m.group(2)]
    elif v in FIXED:
        r[k] = FIXED[v]
out["astrashastra"] = r

# Obscure API の攻撃速度アイコン(先頭のアイコン文字はそのまま残す)
SPD = {"Very Fast": "とても速い", "Very Slow": "とても遅い", "Fast": "速い", "Medium": "普通", "Slow": "遅い"}
r = {}
for k, v in load("obscure_api").items():
    if k.startswith("icon.attack_speed."):
        for a, b in SPD.items():
            if v.endswith(a):
                r[k] = v[: -len(a)] + b
                break
out["obscure_api"] = r

for ns, d in out.items():
    print(ns, len(d))
Path("tr/batch_08_misc_gen.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
