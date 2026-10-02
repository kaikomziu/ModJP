# Productive Trees(26.1.2)の樹種×部位の名前を生成する
import json
from pathlib import Path
SP = {"Alder":"ハンノキ","Allspice":"オールスパイス","Almond":"アーモンド","Apricot":"アンズ","Aquilaria":"ジンコウ","Asai Palm":"アサイーヤシ",
"Ash":"トネリコ","Aspen":"ヤマナラシ","Avocado":"アボカド","Balsa":"バルサ","Balsam Fir":"バルサムモミ","Banana":"バナナ",
"Bay Leaf":"ゲッケイジュ","Beech":"ブナ","Beliy Naliv Apple":"ベーリーナリーフリンゴ","Black Cherry":"ブラックチェリー",
"Black Ember":"ブラックエンバー","Black Locust":"ニセアカシア","Blackthorn":"スピノサスモモ","Blue Mahoe":"ブルーマホー",
"Blue Yonder":"ブルーヨンダー","Boxwood":"ツゲ","Brazil Nut":"ブラジルナッツ","Brazilwood":"ブラジルボク","Breadfruit":"パンノキ",
"Brown Amber":"ブラウンアンバー","Buddhas Hand":"ブッシュカン","Bull Pine":"ポンデローサマツ","Butternut":"バタグルミ","Cacao":"カカオ",
"Candlenut":"ククイノキ","Carob":"イナゴマメ","Cashew":"カシューナッツ","Cave Dweller":"洞窟の住人","Cedar":"スギ","Cempedak":"チェンペダック",
"Ceylon Ebony":"セイロンコクタン","Cherry Plum":"ミロバランスモモ","Cinnamon":"シナモン","Citron":"シトロン","Clove":"クローブ",
"Cocobolo":"ココボロ","Coconut":"ココヤシ","Coffea":"コーヒーノキ","Copoazu":"クプアス","Copper Beech":"ムラサキブナ","Cork Oak":"コルクガシ",
"Cultivated Pear":"セイヨウナシ","Date Palm":"ナツメヤシ","Dogwood":"ハナミズキ","Douglas Fir":"ダグラスモミ","Elderberry":"ニワトコ",
"Elm":"ニレ","European Larch":"ヨーロッパカラマツ","Finger Lime":"フィンガーライム","Firecracker":"ファイアクラッカー",
"Flickering Sun":"ゆらめく太陽","Flowering Crabapple":"花咲くヒメリンゴ","Foggy Blast":"フォギーブラスト","Ginkgo":"イチョウ",
"Golden Delicious Apple":"ゴールデンデリシャスリンゴ","Grandidiers Baobab":"グランディディエリバオバブ",
"Granny Smith Apple":"グラニースミスリンゴ","Grapefruit":"グレープフルーツ","Great Sallow":"サルヤナギ","Greenheart":"グリーンハート",
"Hawthorn":"サンザシ","Hazel":"ハシバミ","Holly":"セイヨウヒイラギ","Hornbeam":"シデ","Ipe":"イペ","Iroko":"イロコ","Jackfruit":"ジャックフルーツ",
"Juniper":"ネズ","Kapok":"カポック","Key Lime":"キーライム","Kumquat":"キンカン","Lawson Cypress":"ローソンヒノキ","Lemon":"レモン",
"Lime":"ライム","Loblolly Pine":"テーダマツ","Logwood":"ログウッド","Mahogany":"マホガニー","Mandarin":"マンダリン","Mango":"マンゴー",
"Monkey Puzzle":"チリマツ","Moonlight Magic Crepe Myrtle":"ムーンライトマジック・サルスベリ","Myrtle Ebony":"マートルエボニー",
"Nectarine":"ネクタリン","Night Fuchsia":"ナイトフクシア","Nutmeg":"ナツメグ","Old Fustic":"オールドファスティック","Olive":"オリーブ",
"Orange":"オレンジ","Osage Orange":"オセージオレンジ","Padauk":"パドック","Pandanus":"タコノキ","Papaya":"パパイヤ","Peach":"モモ",
"Pecan":"ペカン","Persimmon":"カキ","Pink Ipe":"ピンクイペ","Pink Ivory":"ピンクアイボリー","Pistachio":"ピスタチオ","Plantain":"料理用バナナ",
"Plum":"スモモ","Pomegranate":"ザクロ","Pomelo":"ブンタン","Prairie Crabapple":"プレーリーヒメリンゴ","Purple Blackthorn":"紫のスピノサスモモ",
"Purple Crepe Myrtle":"紫のサルスベリ","Purple Ipe":"紫のイペ","Purple Spiral":"パープルスパイラル","Purpleheart":"パープルハート",
"Rainbow Gum":"レインボーユーカリ","Red Banana":"赤いバナナ","Red Crepe Myrtle":"赤いサルスベリ","Red Delicious Apple":"レッドデリシャスリンゴ",
"Red Maple":"アメリカハナノキ","Rippling Willow":"さざ波ヤナギ","Rose Gum":"ローズガム","Rosewood":"ローズウッド","Rowan":"ナナカマド",
"Rubber Tree":"パラゴムノキ","Salak":"サラク","Sand Pear":"ニホンナシ","Sandalwood":"ビャクダン","Satsuma":"温州みかん","Sequoia":"セコイア",
"Silver Fir":"ヨーロッパモミ","Silver Lime":"ギンヨウボダイジュ","Slimy Delight":"ぬるぬるの喜び","Socotra Dragon":"ソコトラリュウケツジュ",
"Soul Tree":"魂の木","Sour Cherry":"サワーチェリー","Soursop":"トゲバンレイシ","Sparkle Cherry":"きらめくサクランボ","Star Anise":"トウシキミ",
"Star Fruit":"スターフルーツ","Sugar Apple":"バンレイシ","Sugar Maple":"サトウカエデ","Swamp Gum":"スワンプガム","Sweet Chestnut":"ヨーロッパグリ",
"Sweet Crabapple":"スイートヒメリンゴ","Sweetgum":"モミジバフウ","Sycamore Fig":"エジプトイチジク","Tangerine":"タンジェリン","Teak":"チーク",
"Thunder Bolt":"サンダーボルト","Time Traveller":"時間旅行者","Tuscarora Crepe Myrtle":"タスカローラ・サルスベリ","Walnut":"クルミ",
"Water Wonder":"ウォーターワンダー","Wenge":"ウェンジ","Western Hemlock":"アメリカツガ","White Ipe":"白いイペ","White Poplar":"ギンドロ",
"White Willow":"セイヨウシロヤナギ","Whitebeam":"アズキナシ","Wild Cherry":"セイヨウミザクラ","Yellow Meranti":"イエローメランティ",
"Yew":"イチイ","Zebrano":"ゼブラノ"}
SUF = {"Bookshelf":"の本棚","Button":"のボタン","Door":"のドア","Fence":"のフェンス","Fence Gate":"のフェンスゲート",
"Hanging Sign":"の吊り看板","Leaves":"の葉","Log":"の原木","Planks":"の板材","Potted Sapling":"の苗木の鉢植え",
"Pressure Plate":"の感圧板","Sapling":"の苗木","Sign":"の看板","Slab":"のハーフブロック","Stairs":"の階段","Stripped Log":"の樹皮を剥いだ原木",
"Stripped Wood":"の樹皮を剥いだ木","Trapdoor":"のトラップドア","Wood":"の木","Logs":"の原木(全種)","Expansion Box":"の拡張箱",
"Fruiting Leaves":"の実のなる葉","Medium Leaves":"の中くらいの葉","Small Leaves":"の小さな葉","Sprout":"の新芽"}
NAMES = sorted(SP, key=len, reverse=True)
def tr(v):
    if v.startswith("Advanced ") and v.endswith(" Beehive"):
        s = v[9:-8]
        return f"{SP[s]}の高度な養蜂箱" if s in SP else None
    if v.endswith(" Beehive"):
        s = v[:-8]
        return f"{SP[s]}の養蜂箱" if s in SP else None
    for s in NAMES:
        if v.startswith(s + " ") and v[len(s)+1:] in SUF:
            return SP[s] + SUF[v[len(s)+1:]]
    return None
if __name__ == "__main__":
    out, rest = ["## productivetrees"], []
    for l in open("cur_pt.txt", encoding="utf-8"):
        k, v = l.rstrip("\n").split("\t", 1)
        j = tr(v) if k.startswith(("block.", "item.")) else None
        if j: out.append(f"{k}\t{j}")
        else: rest.append(l.rstrip("\n"))
    Path("tsv/v14_pt_gen.tsv").write_text("\n".join(out) + "\n", encoding="utf-8")
    Path("cur_pt_rest.txt").write_text("\n".join(rest) + "\n", encoding="utf-8")
    print(len(out) - 1, len(rest))

FR = {"Allspice":"オールスパイス","Almond":"アーモンド","Apricot":"アンズ","Asai Berry":"アサイーベリー","Avocado":"アボカド","Banana":"バナナ",
"Baobab Fruit":"バオバブの実","Bay Leaf":"ローリエ","Beechnut":"ブナの実","Beliy Naliv Apple":"ベーリーナリーフリンゴ","Black Cherry":"ブラックチェリー",
"Brazil Nut":"ブラジルナッツ","Breadfruit":"パンの実","Buddhas Hand":"ブッシュカン","Butternut":"バタグルミの実","Candlenut":"ククイの実",
"Carob":"イナゴマメ","Cashew":"カシューナッツ","Cempedak":"チェンペダック","Cherry Plum":"ミロバラン","Chestnut":"栗","Cinnamon":"シナモン",
"Citron":"シトロン","Clove":"クローブ","Coconut":"ココナッツ","Coffee Bean":"コーヒー豆","Copoazu":"クプアス","Date":"ナツメヤシの実",
"Elderberry":"エルダーベリー","Fig":"イチジク","Finger Lime":"フィンガーライム","Flowering Crabapple":"花咲くヒメリンゴの実",
"Ginkgo Nut":"ギンナン","Golden Delicious Apple":"ゴールデンデリシャスリンゴ","Granny Smith Apple":"グラニースミスリンゴ",
"Grapefruit":"グレープフルーツ","Hala Fruit":"タコノキの実","Haw":"サンザシの実","Hazelnut":"ヘーゼルナッツ","Jackfruit":"ジャックフルーツ",
"Juniper Berry":"ジュニパーベリー","Key Lime":"キーライム","Kumquat":"キンカン","Lemon":"レモン","Lime":"ライム","Mandarin":"マンダリン",
"Mango":"マンゴー","Nectarine":"ネクタリン","Nutmeg":"ナツメグ","Olive":"オリーブ","Orange":"オレンジ","Osage Orange":"オセージオレンジの実",
"Papaya":"パパイヤ","Peach":"モモ","Pear":"ナシ","Pecan":"ペカンナッツ","Persimmon":"カキ","Pistachio":"ピスタチオ","Planet Peach":"惑星モモ",
"Plantain":"料理用バナナ","Plum":"スモモ","Pomegranate":"ザクロ","Pomelo":"ブンタン","Prairie Crabapple":"プレーリーヒメリンゴの実",
"Red Banana":"赤いバナナ","Rowan":"ナナカマドの実","Sand Pear":"ニホンナシ","Satsuma":"温州みかん","Sloe":"スピノサスモモの実",
"Snake Fruit":"スネークフルーツ","Sour Cherry":"サワーチェリー","Soursop":"トゲバンレイシ","Sparkling Cherry":"きらめくサクランボ",
"Star Anise":"八角","Star Fruit":"スターフルーツ","Sweet Crabapple":"スイートヒメリンゴの実","Sweetsop":"バンレイシ","Tangerine":"タンジェリン",
"Walnut":"クルミ","Wild Cherry":"セイヨウミザクラの実","Firework Rocket":"ロケット花火","Air":"空気"}
PL = {}
for s in FR:
    for p in (s + "s", s + "es", s[:-1] + "ies" if s.endswith("y") else None, s.replace("Hand", "Hands"), s.replace("Bean", "Beans")):
        if p: PL[p] = s
PL.update({"Mangos":"Mango","Peaches":"Peach","Cempedak":"Cempedak","Copoazu":"Copoazu","Haw":"Haw","Sloe":"Sloe","Coffee Beans":"Coffee Bean"})
def fruit(x):
    s = PL.get(x, x)
    return FR.get(s)
def tr2(k, v):
    if k.endswith(".latin"): return None
    if k.startswith("tag.item.") and k.endswith("_logs") and v.endswith(" Logs") and v[:-5] in SP:
        return f"{SP[v[:-5]]}の原木類"
    if k.startswith("tag.item.c.storage_blocks."):
        f = fruit(v); return f and f"{f}の貯蔵ブロック"
    if v.startswith("Crate of "):
        x = v[9:]; r = x.startswith("Roasted ")
        f = fruit(x[8:] if r else x); return f and f"{'ローストした' if r else ''}{f}の木箱"
    if k.startswith("item.productivetrees."):
        r = v.startswith("Roasted ")
        f = fruit(v[8:] if r else v); return f and f"{'ローストした' if r else ''}{f}"
    return None
if __name__ == "__main__":
    out2, rest2 = [], []
    for l in open("cur_pt_rest.txt", encoding="utf-8"):
        if not l.strip(): continue
        k, v = l.rstrip("\n").split("\t", 1)
        j = tr2(k, v)
        if j: out2.append(f"{k}\t{j}")
        elif not k.endswith(".latin"): rest2.append(l.rstrip("\n"))
    with open("tsv/v14_pt_gen.tsv", "a", encoding="utf-8") as f:
        f.write("\n".join(out2) + "\n")
    Path("cur_pt_rest2.txt").write_text("\n".join(rest2) + "\n", encoding="utf-8")
    print(len(out2), len(rest2))
