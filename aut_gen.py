"""autcraft_adventure の名前を規則で訳して tsv/v18_aut_gen.tsv に書く(未訳キーのみ)。残りを表示。"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from build import official_keys, effective_missing

NS = "autcraft_adventure"
d = json.loads(Path(f"extracted/{NS}.json").read_text(encoding="utf-8"))
SELF = Path("tr/batch_tsv_v18_aut_gen.json")
done = {}
for f in Path("tr").glob("*.json"):
    if f == SELF or f.name.startswith("_"):
        continue
    done.update(json.loads(f.read_text(encoding="utf-8")).get(NS, {}))
missing = {k: v for k, v in effective_missing(d, official_keys()).items() if k not in done}

MAT = {
    "darkmoon": "ダークムーン", "aesinfernum": "アエス・インフェルヌム", "aesnfernum": "アエス・インフェルヌム",
    "aesinferium": "アエス・インフェルヌム", "aesinferiumtool": "アエス・インフェルヌム", "eternal": "エターナル",
    "magicalvoid": "マジカルヴォイド", "sunborn": "サンボーン", "eclipse": "エクリプス", "necrite": "ネクライト",
    "necritetool": "ネクライト", "last": "ラスト", "voidtool": "ヴォイド", "espectrum": "エスペクトラム",
    "realdark": "リアルダーク", "lacrima": "ラクリマ", "lácrima": "ラクリマ", "iridium": "イリジウム",
    "witherium": "ウィザリウム", "newmoon": "ニュームーン", "lunar": "ルナ", "darksun": "ダークサン",
    "voidmetal": "ヴォイドメタル", "lastbreath": "ラストブレス", "wave": "ウェーブ", "wavebraker": "ウェーブブレイカー",
    "wavebreaker": "ウェーブブレイカー", "corruptedblood": "汚れた血", "hefestite": "ヘフェスタイト", "zenit": "ゼニト",
    "solar": "ソーラー", "heavygold": "ヘビーゴールド", "sigia": "シギア", "eternalblood": "永遠の血",
    "magicalsunborn": "マジカルサンボーン", "barium": "バリウム", "plutonium": "プルトニウム", "tungsten": "タングステン",
    "bismuth": "ビスマス", "bismuthcrystal": "ビスマスクリスタル", "voiderite": "ヴォイデライト", "voidnetherite": "ヴォイドネザライト",
    "bloodnetherite": "ブラッドネザライト", "darknetherite": "ダークネザライト", "solarite": "ソラライト",
    "adventures": "アドベンチャー", "hefestitedust": "ヘフェスタイト",
}
TOOL = {"Sword": "の剣", "Pickaxe": "のツルハシ", "Axe": "の斧", "Shovel": "のシャベル", "Hoe": "のクワ",
        "Helmet": "のヘルメット", "Chestplate": "のチェストプレート", "Leggings": "のレギンス", "Boots": "のブーツ",
        "Ingot": "インゴット", "Ore": "鉱石", "Block": "ブロック", "Dust": "の粉", "Shield": "の盾", "Gem": "の宝石"}
WOOD = {"BloodTree": "血の木", "PurpleTree": "紫の木", "Wolframic": "ウォルフラム"}
WOODP = {"Log": "の原木", "Wood": "の木", "Planks": "の板材", "Stairs": "の階段", "Slab": "のハーフブロック",
         "Fence": "のフェンス", "Fence Gate": "のフェンスゲート", "Button": "のボタン", "Pressure Plate": "の感圧板",
         "Leaves": "の葉"}
PLACE = {"Small Island": "小島", "Ice Peak": "氷の峰", "Cherry": "桜", "Desert": "砂漠", "Soul Sand": "ソウルサンド",
         "Ocean": "海", "Void": "虚空", "Badlands": "荒野", "Plain": "平原", "Taiga": "タイガ", "Warped Forest": "歪んだ森",
         "Deep Dark": "ディープダーク", "Jungle": "ジャングル", "Basalt Delta": "玄武岩デルタ", "Mountain": "山",
         "Swamp": "沼", "Crimson Forest": "真紅の森", "Cave": "洞窟", "Forest": "森", "Mushroom Fields": "キノコ島",
         "Savanna": "サバンナ", "Nether Waste": "ネザーの荒地"}
EFF = {"Miner": "採掘者", "Hefestite": "ヘフェスタイト", "Barium": "バリウム", "Disgusting": "嫌悪", "Animal Power": "獣の力",
       "Adventure": "冒険", "Cinabrio": "シナブリオ", "Radiation": "放射線", "Autcrafter Substrate": "オートクラフターの培地",
       "Heavy Gold": "ヘビーゴールド", "Lunar Freeze Potion": "月の凍結", "Wolframic": "ウォルフラム", "Electrocuted": "感電",
       "Return": "帰還"}
# ボス・固有名(entity名と卵で共用)
MOB = {
    "Seraphim": "セラフィム", "Crimson Man": "真紅の男", "Forest Ogre": "森のオーガ", "Lythos, the Primordial Rock": "原初の岩リトス",
    "Wardrock, the First Exiled": "最初の追放者ウォードロック", "Pet Robot": "ペットロボット", "Osirik, the Desert Apostle": "砂漠の使徒オシリク",
    "Greyoak, the Swamp King": "沼の王グレイオーク", "Ice Wraith": "氷のレイス", "Urgasha, the Magician Sister": "魔術師の姉妹ウルガシャ",
    "Hefesto, the Blacksmith": "鍛冶師ヘフェスト", "Calisto, the first dragon": "最初の竜カリスト", "Jungle Folk": "ジャングルの民",
    "Grafted Guardian": "接ぎ木の守護者", "Desert Ogre": "砂漠のオーガ", "Blood Priest": "血の司祭", "Cosmic Anomaly": "宇宙の異常体",
    "Cultist Piglin": "教団員ピグリン", "Capybara": "カピバラ", "Cirtus Kyrie, the Void Emperor": "虚空の皇帝シルトゥス・キリエ",
    "Grukhar, the Warrior Brother": "戦士の兄弟グルカー", "Basalt Blaze": "玄武岩のブレイズ", "Shogunate Captain": "幕府の隊長",
    "Circe, the Elder Witch": "老魔女キルケー", "Gelatto, The Wrong Toe": "間違ったつま先ジェラット", "Nether Ogre": "ネザーのオーガ",
    "Dense Zombie": "高密度ゾンビ", "Cultist Drowned": "教団員ドラウンド", "Siderius, the Starborn": "星生まれのシデリウス",
    "Exilium, the End Wither": "エンドのウィザー、エグジリウム", "Logan, The Butcher": "肉屋のローガン", "Enslaved Soul": "囚われた魂",
    "End Wraith": "エンドのレイス", "Walkinger, the Relentless": "容赦なきウォーキンガー", "Kagemura, the Eternal General": "永遠の将軍カゲムラ",
    "Shogunate Soldier": "幕府の兵士", "Warped Man": "歪んだ男", "Albert, the Disgusting": "気持ち悪いアルバート",
    "Crazy Machine": "狂った機械", "Men Eater": "人食い", "Land Dragon": "陸竜", "Daklijisħet, the  Executor of Souls": "魂の処刑人ダクリジシェット",
    "Allsee": "オールシー", "Giant Jellyfish": "巨大クラゲ", "Nangarekoha, the Jungle Protector": "ジャングルの守護者ナンガレコハ",
    "Ice Ogre": "氷のオーガ", "Black Minotaur": "黒いミノタウロス", "Brodcaver": "ブロドケイバー", "Orphaim": "オルファイム",
    "Pet Robot": "ペットロボット", "Drijighost": "ドリジゴースト", "Giant Mushroom": "巨大キノコ", "Guinea Pig": "モルモット",
    "Triobite": "トリオバイト", "Tapir": "バク", "Robot Friend 0 1": "ロボットの友達01", "Abbadon, the Creator": "創造主アバドン",
    "Niútóu, the King of the Coliseum": "闘技場の王ニウトウ", "Gallahan, the Blackblade": "黒剣のギャラハン",
    "Arachmuth, The Crystal Eater": "結晶を食らうアラクムス", "Gallahan": "ギャラハン",
}

DEF = {"Siderius": "シデリウス", "Grafted Guardian": "接ぎ木の守護者", "Nangarekoha": "ナンガレコハ", "Arachmuth": "アラクムス",
       "Osirik": "オシリク", "Circe": "キルケー", "Kagemura": "カゲムラ", "Giant Mushroom": "巨大キノコ", "Albert": "アルバート",
       "Greyoak": "グレイオーク", "Nióutóu": "ニウトウ", "Logan": "ローガン", "Gelatto": "ジェラット", "Wardrock": "ウォードロック"}


def name(en):
    if en in MOB:
        return MOB[en]
    m = re.fullmatch(r"(.+) Spawn Egg", en)
    if m and name(m.group(1)):
        return name(m.group(1)) + "のスポーンエッグ"
    m = re.fullmatch(r"Relic Of The (.+)", en)
    if m and m.group(1) in PLACE:
        return PLACE[m.group(1)] + "の遺物"
    m = re.fullmatch(r"(.+) Altar", en)
    if m and m.group(1) in PLACE:
        return PLACE[m.group(1)] + "の祭壇"
    for w, wj in WOOD.items():
        for p, pj in WOODP.items():
            if en == f"{w} {p}":
                return wj + pj
    m = re.fullmatch(r"(.+?)(?:Tool)? (Sword|Pickaxe|Axe|Shovel|Hoe|Helmet|Chestplate|Leggings|Boots|Ingot|Ore|Block|Dust|Shield|Gem)", en)
    if m:
        k = m.group(1).replace(" ", "").lower()
        if k in MAT:
            return MAT[k] + TOOL[m.group(2)]
    for pre, ja in [("Potion of ", "{}のポーション"), ("Splash Potion of ", "{}のスプラッシュポーション"),
                    ("Lingering Potion of ", "{}の残留ポーション"), ("Arrow of ", "{}の矢")]:
        if en.startswith(pre) and en[len(pre):] in EFF:
            return ja.format(EFF[en[len(pre):]])
    return None


out = {}
for k, v in missing.items():
    if k.startswith(("item.", "block.", "entity.")):
        r = name(v)
        if r:
            out[k] = r
    m = re.fullmatch(r"advancements\.(.+)\.descr", k)
    if m:
        m2 = re.fullmatch(r"Defeat (.+)", v)
        if m2:
            out[k] = f"{DEF.get(m2.group(1), m2.group(1))}を倒す"

lines = [f"## {NS}"] + [f"{k}\t{v}" for k, v in out.items()]
Path("tsv/v18_aut_gen.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("gen", len(out))
for k, v in missing.items():
    if k not in out and not k.endswith(".author"):
        print(f"{k}\t{v}")
