"""Productive Bees のハチ名(entity.productivebees.*_bee)を生成 → tr/batch_16_bees_gen.json

「<素材> Bee」は「<素材>のハチ」にする。元素名は chemlib_gen の辞書を流用。
"""
import json, re
from pathlib import Path
import importlib.util

WORK = Path(__file__).parent
spec = importlib.util.spec_from_file_location("chem", WORK / "chemlib_gen.py")
src = (WORK / "chemlib_gen.py").read_text(encoding="utf-8")
EL = dict(x.split(":") for x in re.search(r'EL = dict\(x\.split\(":"\) for x in """(.*?)"""', src, re.S).group(1).split())

MAT = {
    "Agate": "瑪瑙", "Alexandrite": "アレキサンドライト", "Alfsteel": "エルフ鋼", "Allthemodium": "オールザモジウム",
    "Aluminium": "アルミニウム", "Amber": "琥珀", "Amethyst": "アメジスト", "Amethyst Bronze": "アメジスト青銅",
    "Ametrine": "アメトリン", "Ammolite": "アンモライト", "Apatite": "燐灰石", "Aquamarine": "アクアマリン",
    "Arcane": "秘術", "Ashy Mining": "灰色の採掘", "Awakened": "覚醒", "Awakened Supremium": "覚醒スプレミウム",
    "Benitoite": "ベニトアイト", "Bismuth": "ビスマス", "Black Diamond": "黒ダイヤモンド", "Black Opal": "ブラックオパール",
    "Blazing": "ブレイズ", "Blazing Crystal": "ブレイズクリスタル", "Bloody": "血まみれ", "Blue Banded": "青帯",
    "Brass": "真鍮", "Bronze": "青銅", "Bumble": "マルハナ", "Calorite": "カロライト", "Carnelian": "カーネリアン",
    "Cats Eye": "キャッツアイ", "Chaos": "混沌", "Chocolate Mining": "チョコ色の採掘", "Chrysoprase": "クリソプレーズ",
    "Cinnabar": "辰砂", "Citrine": "シトリン", "Coal": "石炭", "Cobalt": "コバルト", "Collector": "収集",
    "Common Salvage": "一般回収", "Compressed Iron": "圧縮鉄", "Constantan": "コンスタンタン",
    "Conductive Alloy": "導電合金", "Copper Alloy": "銅合金", "Copper": "銅", "Coral": "サンゴ", "Cosmic": "宇宙",
    "Crystalline": "結晶", "Dark Gem": "闇の宝石", "Dark Steel": "ダークスチール", "Desh": "デッシュ",
    "Destabilized Redstone": "不安定化レッドストーン", "Diamond": "ダイヤモンド", "Digger": "穴掘り",
    "Draconic": "竜", "Draconium": "ドラコニウム", "Drenched Iron": "浸潤鉄", "Dye": "染料", "Electrum": "エレクトラム",
    "Elementium": "エレメンチウム", "Emerald": "エメラルド", "Emeraldite": "エメラルダイト", "End Gobber": "エンドゴバー",
    "End Steel": "エンドスチール", "Ender": "エンダー", "Ender Slimy": "エンダースライム", "Enderium": "エンダリウム",
    "Energetic Alloy": "エネルギー合金", "Energized Glowstone": "励起グロウストーン", "Energized Steel": "励起鋼",
    "Epic Salvage": "エピック回収", "Ether Gas": "エーテルガス", "Euclase": "ユークレース", "Experience": "経験値",
    "Farmer": "農家", "Fey": "妖精", "Fireite": "ファイアライト", "Fire Dragonsteel": "炎の竜鋼", "Fluix": "フルーix",
    "Fluorite": "蛍石", "Flux Dust": "フラックスダスト", "Frosty": "霜", "Gaiasteel": "ガイア鋼", "Garnet": "ガーネット",
    "Geode": "ジオード", "Ghostly": "幽霊", "Glowing": "発光", "Gobber": "ゴバー", "Gold": "金", "Grave's": "墓守",
    "Green Carpenter": "緑のクマバチ", "Green Sapphire": "グリーンサファイア", "Heliodor": "ヘリオドール",
    "Hematophagous": "吸血", "Hepatizon": "ヘパティゾン", "Hoarder": "貯め込み", "Ice Dragonsteel": "氷の竜鋼",
    "Ichor Slimy": "イコルスライム", "Imperium": "インペリウム", "Iesnium": "イエスニウム", "Inert Crystal": "不活性結晶",
    "Air Crystal": "風の結晶", "Earth Crystal": "大地の結晶", "Fire Crystal": "炎の結晶", "Water Crystal": "水の結晶",
    "Inferium": "インフェリウム", "Insanium": "インサニウム", "Invar": "インバー", "Iolite": "アイオライト",
    "Iridium": "イリジウム", "Iron": "鉄", "Jade": "翡翠", "Jasper": "ジャスパー", "Knightslime": "ナイトスライム",
    "Kunzite": "クンツァイト", "Kyanite": "カイヤナイト", "Lapis": "ラピスラズリ", "Lead": "鉛", "Leafcutter": "ハキリ",
    "Legendary Salvage": "伝説回収", "Lightning Dragonsteel": "雷の竜鋼", "Lumber": "木こり", "Lumium": "ルミウム",
    "Magmatic": "マグマ", "Malachite": "マラカイト", "Mana": "マナ", "Manasteel": "マナスチール", "Manyullyn": "マニュリン",
    "Mason": "石工", "Menril": "メンリル", "Moldavite": "モルダバイト", "Moonstone": "ムーンストーン",
    "Morganite": "モルガナイト", "Neon Cuckoo": "ネオンカッコウ", "Nether Gobber": "ネザーゴバー", "Nickel": "ニッケル",
    "Niotic Crystal": "ナイオティッククリスタル", "Niter": "硝石", "Nitro Crystal": "ニトロクリスタル", "Nomad": "遊牧",
    "Obsidian": "黒曜石", "Oily": "油まみれ", "Onyx": "オニキス", "Opal": "オパール", "Osmium": "オスミウム",
    "Ostrum": "オストラム", "Patrick": "パトリック", "Pearl": "真珠", "Pendorite": "ペンドライト", "Peridot": "ペリドット",
    "Phosphophyllite": "フォスフォフィライト", "Pig Iron": "銑鉄", "Pink Slimy": "桃色スライム", "Plastic": "プラスチック",
    "Platinum": "白金", "Prismarine": "プリズマリン", "Prudentium": "プルデンティウム", "Pulsating Alloy": "脈動合金",
    "Pure": "純粋", "Pure Crystal": "純粋な結晶", "Pyrope": "パイロープ", "Quarry": "採石", "Quartz Enriched Iron": "クォーツ強化鉄",
    "Queens Slime": "女王のスライム", "Radioactive": "放射性", "Rancher": "牧場", "Rare Salvage": "レア回収",
    "Redstone Alloy": "レッドストーン合金", "Redstone": "レッドストーン", "Reed": "アシ", "Refined Glowstone": "精製グロウストーン",
    "Refined Obsidian": "精製黒曜石", "Regenerative": "再生", "Resin": "樹脂", "Resonant Ender": "共鳴エンダー",
    "Rock Crystal": "水晶", "Rose Gold": "ローズゴールド", "Rose Quartz": "ローズクォーツ", "Sapphire": "サファイア",
    "Salty": "塩", "Sculk": "スカルク", "Signalum": "シグナルム", "Silicon": "シリコン", "Silky": "絹", "Silver": "銀",
    "Skeletal": "骸骨", "Sky Slimy": "空スライム", "Slimesteel": "スライムスチール", "Slimy": "スライム",
    "Sodalite": "ソーダライト", "Soularium": "ソウラリウム", "Soulium": "ソウリウム", "Soulsteel": "ソウルスチール",
    "Soul Lava": "魂の溶岩", "Spatial": "空間", "Spectrum": "スペクトラム", "Spinel": "スピネル", "Spirit": "霊",
    "Spirited Crystal": "霊の結晶", "Sponge": "スポンジ", "Springaline": "スプリンガライン", "Starmetal": "星鋼",
    "Starry": "星空", "GregStar": "グレッグスター", "Neutronium": "ニュートロニウム", "Steel": "鋼鉄",
    "Sticky Resin": "粘着樹脂", "Sussy": "あやしい", "Sugarbag": "シュガーバッグ", "Sulfur": "硫黄",
    "Sunstone": "サンストーン", "Supremium": "スプレミウム", "Sweat": "コハナ", "Swift Alloy": "迅速合金",
    "Tanzanite": "タンザナイト", "Tea": "茶", "Tektite": "テクタイト", "Terrasteel": "テラスチール", "Tertium": "テルティウム",
    "Tin": "スズ", "Titanium": "チタン", "Topaz": "トパーズ", "Tourmaline": "トルマリン", "Tungsten": "タングステン",
    "Turquoise": "ターコイズ", "Uncommon Salvage": "アンコモン回収", "Unobtainium": "アンオブタニウム",
    "Uraninite": "閃ウラン鉱", "Vibranium": "ヴィブラニウム", "Vibrant Alloy": "活力合金",
    "Wasted Radioactive": "廃放射性", "Withered": "ウィザー", "White Diamond": "白ダイヤモンド",
    "Yellow Carpenter": "黄色のクマバチ", "Zinc": "亜鉛", "Zircon": "ジルコン", "Water": "水", "Cyanite": "シアナイト",
    "Blutonium": "ブルトニウム", "Magentite": "マゼンタイト", "Ludicrite": "ルディクライト", "Ridiculite": "リディキュライト",
    "Inanite": "イナナイト", "Insanite": "インサナイト", "Deorum": "デオルム", "Rune": "ルーン", "Stellarite": "ステラライト",
    "Hyper Experience": "ハイパー経験値", "Soul Infused": "魂注入", "Shellite": "シェライト", "Twinite": "ツイナイト",
    "Dragonsteel": "竜鋼", "Arcane Debris": "秘術の残骸", "Arcane Essence": "秘術のエッセンス", "Infused Iron": "注入鉄",
    "Tainted Gold": "汚れた金", "Arcane Gold": "秘術の金", "Pewter": "ピューター", "HOP Graphite": "HOPグラファイト",
    "Hellfire": "地獄の炎", "Sky Steel": "スカイスチール", "Astral": "星界", "Etherium": "エセリウム", "Bauxite": "ボーキサイト",
    "Cobaltite": "輝コバルト鉱", "Chromite": "クロム鉄鉱", "Barite": "重晶石", "Electrotine": "エレクトロチン",
    "Ilmenite": "チタン鉄鉱", "Galena": "方鉛鉱", "Pyrochlore": "パイロクロア", "Lepidolite": "リチア雲母",
    "Graphite": "グラファイト", "Bastnasite": "バストネサイト", "Naquadah": "ナクアダ", "Oilsands": "オイルサンド",
    "Pyrolusite": "軟マンガン鉱", "Realgar": "鶏冠石", "Scheelite": "灰重石", "Sheldonite": "シェルドナイト",
    "Sphalerite": "閃亜鉛鉱", "Stibnite": "輝安鉱", "Tantalite": "タンタル石", "Tetrahedrite": "四面銅鉱",
    "Tricalcium Phosphate": "リン酸三カルシウム", "Tungstate": "タングステン酸塩", "Vanadium Magnetite": "バナジウム磁鉄鉱",
    "Miracle": "奇跡", "Mithril": "ミスリル", "Prismalium": "プリズマリウム", "Melodium": "メロディウム",
    "Stellarium": "ステラリウム", "Silicium": "ケイ素",
}
MAT["Fluix"] = "フルーイックス"
SPECIAL = {
    "BazBee": "バズビー", "BitzBee": "ビッツビー", "BizBee": "ビズビー", "Brown Shroombee": "茶色のキノコバチ",
    "CheezyB": "チーズビー", "Choco Bee": "チョコのハチ", "CreeBee": "クリービー", "Crimson Shroombee": "真紅のキノコバチ",
    "CuBee": "キュービー", "Bee of Infinity": "無限のハチ", "KamikazBee": "カミカゼビー", "Ancient Bee": "古代のハチ",
    "Pepto Beesmol": "ペプトビースモル", "ProsperiBee": "プロスペリビー", "Red Shroombee": "赤いキノコバチ", "RuBee": "ルビー",
    "WannaBee": "ワナビー", "Warped Shroombee": "歪んだキノコバチ", "ZomBee": "ゾンビー", "Full Metal Patrick Bee": "フルメタル・パトリックのハチ",
    "Arcanus Bee": "アルカヌスのハチ", "Bee of the Sky": "空のハチ", "Soul Bee": "魂のハチ", "Etherium Bee": "エセリウムのハチ",
    "Chaos Bee": "混沌のハチ", "%s": "%s",
}
m = json.loads((WORK / "extracted/productivebees.json").read_text(encoding="utf-8"))["missing"]
out, miss_names = {}, []


def bee(v):
    if v in SPECIAL:
        return SPECIAL[v]
    r = re.match(r"(.+) Bee$", v)
    if not r:
        return None
    n = r.group(1)
    if n in MAT:
        return f"{MAT[n]}のハチ"
    if n in EL:
        return f"{EL[n]}のハチ"
    return None


for k, v in m.items():
    if k.startswith("entity.productivebees."):
        j = bee(v)
        if j:
            out[k] = j
        else:
            miss_names.append(v)
    r = re.match(r"(.+) Spawn Egg$", v)
    if k.startswith("item.productivebees.spawn_egg_") and r:
        j = bee(r.group(1)) if r.group(1) != "%s" else "%s"
        if j:
            out[k] = f"{j}のスポーンエッグ"
(WORK / "tr/batch_16_bees_gen.json").write_text(json.dumps({"productivebees": out}, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(out), "未対応:", miss_names)
