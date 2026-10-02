"""ChemLib の元素・化合物名(＋粉/インゴット/板/塊/ブロック/ガス/ランプ/バケツ)を化学名の辞書から生成する。"""
import json, re
from pathlib import Path

EL = dict(x.split(":") for x in """Hydrogen:水素 Helium:ヘリウム Lithium:リチウム Beryllium:ベリリウム Boron:ホウ素 Carbon:炭素 Nitrogen:窒素 Oxygen:酸素
Fluorine:フッ素 Neon:ネオン Sodium:ナトリウム Magnesium:マグネシウム Aluminum:アルミニウム Silicon:ケイ素 Phosphorus:リン Sulfur:硫黄
Chlorine:塩素 Argon:アルゴン Potassium:カリウム Calcium:カルシウム Scandium:スカンジウム Titanium:チタン Vanadium:バナジウム Chromium:クロム
Manganese:マンガン Iron:鉄 Cobalt:コバルト Nickel:ニッケル Copper:銅 Zinc:亜鉛 Gallium:ガリウム Germanium:ゲルマニウム Arsenic:ヒ素
Selenium:セレン Bromine:臭素 Krypton:クリプトン Rubidium:ルビジウム Strontium:ストロンチウム Yttrium:イットリウム Zirconium:ジルコニウム
Niobium:ニオブ Molybdenum:モリブデン Technetium:テクネチウム Ruthenium:ルテニウム Rhodium:ロジウム Palladium:パラジウム Silver:銀
Cadmium:カドミウム Indium:インジウム Tin:スズ Antimony:アンチモン Tellurium:テルル Iodine:ヨウ素 Xenon:キセノン Cesium:セシウム
Barium:バリウム Lanthanum:ランタン Cerium:セリウム Praseodymium:プラセオジム Neodymium:ネオジム Promethium:プロメチウム Samarium:サマリウム
Europium:ユウロピウム Gadolinium:ガドリニウム Terbium:テルビウム Dysprosium:ジスプロシウム Holmium:ホルミウム Erbium:エルビウム
Thulium:ツリウム Ytterbium:イッテルビウム Lutetium:ルテチウム Hafnium:ハフニウム Tantalum:タンタル Tungsten:タングステン Rhenium:レニウム
Osmium:オスミウム Iridium:イリジウム Platinum:白金 Gold:金 Mercury:水銀 Thallium:タリウム Lead:鉛 Bismuth:ビスマス Polonium:ポロニウム
Astatine:アスタチン Radon:ラドン Francium:フランシウム Radium:ラジウム Actinium:アクチニウム Thorium:トリウム Protactinium:プロトアクチニウム
Uranium:ウラン Neptunium:ネプツニウム Plutonium:プルトニウム Americium:アメリシウム Curium:キュリウム Berkelium:バークリウム
Californium:カリホルニウム Einsteinium:アインスタイニウム Fermium:フェルミウム Mendelevium:メンデレビウム Nobelium:ノーベリウム
Lawrencium:ローレンシウム Rutherfordium:ラザホージウム Dubnium:ドブニウム Seaborgium:シーボーギウム Bohrium:ボーリウム Hassium:ハッシウム
Meitnerium:マイトネリウム Darmstadtium:ダームスタチウム Roentgenium:レントゲニウム Copernicium:コペルニシウム Nihonium:ニホニウム
Flerovium:フレロビウム Moscovium:モスコビウム Livermorium:リバモリウム Tennessine:テネシン Oganesson:オガネソン""".split())
ANION = {"Carbonate": "炭酸", "Chloride": "塩化", "Hydroxide": "水酸化", "Nitrate": "硝酸", "Oxide": "酸化", "Sulfate": "硫酸",
         "Sulfide": "硫化", "Iodide": "ヨウ化", "Disulfide": "二硫化", "Aluminate": "アルミン酸", "Trioxide": "三酸化", "Trisulfide": "三硫化"}
COMP = {
    "Acetic Acid": "酢酸", "Acetylene": "アセチレン", "Acetylsalicylic Acid": "アセチルサリチル酸", "Amide": "アミド", "Ammonia": "アンモニア",
    "Ammonium": "アンモニウム", "Ammonium Chloride": "塩化アンモニウム", "Beryl": "緑柱石", "Beta Carotene": "βカロテン", "Butane": "ブタン",
    "Caffeine": "カフェイン", "Carbon Dioxide": "二酸化炭素", "Carbon Disulfide": "二硫化炭素", "Carbon Monoxide": "一酸化炭素",
    "Carbonate": "炭酸塩", "Cellulose": "セルロース", "Chitin": "キチン", "Cucurbitacin": "ククルビタシン", "Diammonium Phosphate": "リン酸二アンモニウム",
    "Epinephrine": "エピネフリン", "Ethane": "エタン", "Ethanol": "エタノール", "Ethylene": "エチレン", "Graphite": "黒鉛", "Han Purple": "漢紫",
    "Hexane": "ヘキサン", "Hydrochloric Acid": "塩酸", "Hydrogen Sulfide": "硫化水素", "Hydroxide": "水酸化物", "Hydroxylapatite": "ヒドロキシアパタイト",
    "Kaolinite": "カオリナイト", "Keratin": "ケラチン", "Methane": "メタン", "Mullite": "ムライト", "Nitrate": "硝酸塩", "Nitric Acid": "硝酸",
    "Nitric Oxide": "一酸化窒素", "Nitrogen Dioxide": "二酸化窒素", "Pentane": "ペンタン", "Phosphate": "リン酸塩", "Phosphoric Acid": "リン酸",
    "Polyvinyl Chloride": "ポリ塩化ビニル", "Potassium Cyanide": "シアン化カリウム", "Potassium Dichromate": "二クロム酸カリウム",
    "Potassium Ethyl Xanthate": "エチルキサントゲン酸カリウム", "Potassium Permanganate": "過マンガン酸カリウム", "Propane": "プロパン",
    "Protein": "タンパク質", "Silicon Dioxide": "二酸化ケイ素", "Sodium Bisulfate": "硫酸水素ナトリウム", "Starch": "デンプン", "Sucrose": "スクロース",
    "Sulfur Dioxide": "二酸化硫黄", "Sulfur Trioxide": "三酸化硫黄", "Sulfuric Acid": "硫酸", "Triglyceride": "トリグリセリド", "Urea": "尿素", "Water": "水",
}
FORM = {"Dust": "の粉", "Ingot": "インゴット", "Plate": "板", "Nugget": "の塊", "Block": "ブロック", "Metal Block": "ブロック", "Gas": "ガス",
        "Lamp": "ランプ", "Bucket": "入りバケツ", "Gas Bucket": "ガス入りバケツ"}
FIXED = {"Effects on Hit": "命中時の効果", "Compounds": "化合物", "Elements": "元素", "Metals": "金属", "Misc Items": "その他のアイテム",
         "Periodic Table of the Elements": "元素周期表", "Use this to see a full periodic table.": "使うと周期表全体を見られます。",
         "Use the Periodic Table of the Elements to learn more about this element.": "元素周期表でこの元素について詳しく調べられます。"}


def name(b):
    if b in COMP:
        return COMP[b]
    if b in EL:
        return EL[b]
    m = re.fullmatch(r"(\w+?)(?: (I|Ii|Iii))? (\w+)", b)
    if m and m.group(1) in EL and m.group(3) in ANION:
        roman = {"I": "(I)", "Ii": "(II)", "Iii": "(III)", None: ""}[m.group(2)]
        return ANION[m.group(3)] + EL[m.group(1)] + roman
    return None


miss = json.loads(Path("extracted/chemlib.json").read_text(encoding="utf-8"))["missing"]
out, left = {}, []
for k, v in miss.items():
    if v in FIXED:
        out[k] = FIXED[v]
        continue
    if ".jei.compound." in k:
        continue
    m = re.fullmatch(r"(?:Liquid )?(.*?)(?: (Dust|Ingot|Plate|Nugget|Metal Block|Block|Gas Bucket|Gas|Lamp|Bucket))?", v)
    n = name(m.group(1))
    if n is None:
        left.append(v)
        continue
    f = m.group(2)
    out[k] = n + (FORM[f] if f else "")
print(len(out), "/", len(miss), "手訳待ち:", left)
Path("tr/batch_12_chemlib_gen.json").write_text(json.dumps({"chemlib": out}, ensure_ascii=False, indent=1), encoding="utf-8")
