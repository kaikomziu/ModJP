# Twilight Forest(ja_jpが壊れている)の名前系を英文から自前で訳す。公式ja_jpは参照しない。
import json, re
COL = {"Black":"黒色","Blue":"青色","Brown":"茶色","Cyan":"水色","Gray":"灰色","Green":"緑色","Light Blue":"空色",
"Light Gray":"薄灰色","Lime":"黄緑色","Magenta":"赤紫色","Orange":"橙色","Pink":"桃色","Purple":"紫色","Red":"赤色",
"White":"白色","Yellow":"黄色"}
# 生き物・ボス名
E = {"Naga":"ナーガ","Lich":"リッチ","Minoshroom":"ミノシュルーム","Hydra":"ヒドラ","Knight Phantom":"ファントムナイト",
"Ur-Ghast":"ウル・ガスト","Alpha Yeti":"アルファイエティ","Snow Queen":"雪の女王","Quest Ram":"クエストラム","Final Boss":"最終ボス",
"Adherent":"信奉者","Armored Giant":"鎧の巨人","Bighorn Sheep":"ビッグホーン","Block and Chain Goblin":"鉄球ゴブリン",
"Boar":"イノシシ","Carminite Broodling":"カーミナイトの幼生","Carminite Ghastguard":"カーミナイトのガスト衛兵",
"Carminite Ghastling":"カーミナイトの子ガスト","Carminite Golem":"カーミナイトゴーレム","Death Tome":"死の書","Deer":"シカ",
"Dwarf Rabbit":"コビトウサギ","Fire Beetle":"ファイアビートル","Giant Miner":"巨人の鉱夫","Harbinger Cube":"前触れのキューブ",
"Hedge Spider":"生垣グモ","Helmet Crab":"ヘルメットガニ","Hostile Wolf":"凶暴なオオカミ","Ice Crystal":"氷の結晶",
"King Spider":"キンググモ","Kobold":"コボルト","Goblin Knight":"ゴブリンナイト","Lower Goblin Knight":"ゴブリンナイト(下)",
"Upper Goblin Knight":"ゴブリンナイト(上)","Maze Slime":"迷宮スライム","Minotaur":"ミノタウロス","Mist Wolf":"霧のオオカミ",
"Mosquito Swarm":"蚊の群れ","Penguin":"ペンギン","Pinch Beetle":"ハサミムシ甲虫","Raven":"ワタリガラス","Redcap":"レッドキャップ",
"Redcap Sapper":"レッドキャップの工兵","Skeleton Druid":"スケルトンドルイド","Slime Beetle":"スライムビートル",
"Snow Guardian":"雪の守護者","Squirrel":"リス","Stable Ice Core":"安定した氷のコア","Unstable Ice Core":"不安定な氷のコア",
"Swarm Spider":"群れグモ","Tiny Bird":"小鳥","Towerwood Borer":"タワーウッドの食い虫","Troll":"トロル","Winter Wolf":"冬のオオカミ",
"Wraith":"レイス","Yeti":"イエティ","Death Tome ":"死の書"}
# 木材名
W = {"Canopy Tree":"キャノピーツリー","Canopy":"キャノピー","Darkwood":"ダークウッド","Mangrove":"マングローブ",
"Minewood":"マインウッド","Sortingwood":"ソーティングウッド","Timewood":"タイムウッド","Transwood":"トランスウッド",
"Twilight Oak":"トワイライトオーク","Acacia":"アカシア","Birch":"シラカバ","Cherry":"サクラ","Dark Oak":"ダークオーク",
"Jungle":"ジャングル","Oak":"オーク","Spruce":"トウヒ","Bamboo":"竹","Crimson":"真紅","Warped":"歪んだ"}
SUF = [("Wall Hanging Sign","の壁掛け吊り看板"),("Hanging Sign","の吊り看板"),("Wall Sign","の壁の看板"),("Sign","の看板"),
("Fence Gate","のフェンスゲート"),("Pressure Plate","の感圧板"),("Chest Boat","のチェスト付きボート"),("Boat","のボート"),
("Button","のボタン"),("Chest","のチェスト"),("Door","のドア"),("Fence","のフェンス"),("Planks","の板材"),("Slab","のハーフブロック"),
("Stairs","の階段"),("Trapdoor","のトラップドア"),("Log","の原木"),("Wood","の木"),("Leaves","の葉"),("Banister","の手すり"),
("Bookshelf","の本棚"),("Sapling","の苗木")]
BANNER = {"Alpha Yeti Face":"アルファイエティの顔","Hydra Flame":"ヒドラの炎","Knight Helmet":"騎士の兜","Lich Crown":"リッチの冠",
"Minoshroom Axes":"ミノシュルームの斧","Naga Scales":"ナーガの鱗","Quest Ram Swirls":"クエストラムの渦巻き",
"Snow Queen Crown":"雪の女王の冠","Carminite Border":"カーミナイトの縁取り"}
SKULL = {"Creeper":"クリーパーの頭","Player":"プレイヤーの頭","Skeleton":"スケルトンの頭蓋骨","Wither Skeleton":"ウィザースケルトンの頭蓋骨",
"Zombie":"ゾンビの頭"}
PLANT = {"Canopy Tree Sapling":"キャノピーツリーの苗木","Darkwood Sapling":"ダークウッドの苗木","Burnt Thorn":"焦げたイバラ",
"Green Thorn":"緑のイバラ","Thorn":"イバラ","Robust Twilight Oak Sapling":"丈夫なトワイライトオークの苗木","Mayapple":"メイアップル",
"Miner's Tree Sapling":"鉱夫の木の苗木","Mushgloom":"マッシュグルーム","Rainbow Oak Sapling":"虹色のオークの苗木",
"Sorting Tree Sapling":"仕分けの木の苗木","Tree of Time Sapling":"時の木の苗木","Tree of Transformation Sapling":"変化の木の苗木",
"Sickly Twilight Oak Sapling":"病弱なトワイライトオークの苗木"}

def name(v):
    if v in E: return E[v]
    for c, cj in COL.items():
        for b, bj in BANNER.items():
            if v == f"{c} {b}": return f"{cj}の{bj}"
    m = re.fullmatch(r"(.+) Boss Spawner", v)
    if m and m.group(1) in E: return f"{E[m.group(1)]}のボススポナー"
    m = re.fullmatch(r"(.+) Trophy", v)
    if m and m.group(1) in E: return f"{E[m.group(1)]}のトロフィー"
    m = re.fullmatch(r"(.+) Spawn Egg", v)
    if m and m.group(1) in E: return f"{E[m.group(1)]}のスポーンエッグ"
    m = re.fullmatch(r"(.+?)( Wall)? Skull Candle", v)
    if m and m.group(1) in SKULL: return f"{'壁付きの' if m.group(2) else ''}ロウソク付き{SKULL[m.group(1)]}"
    m = re.fullmatch(r"Potted (.+)", v)
    if m and m.group(1) in PLANT: return f"鉢植えの{PLANT[m.group(1)]}"
    m = re.fullmatch(r"Hollow (.+) (Log|Stem)", v)
    if m and m.group(1) in W: return f"空洞の{W[m.group(1)]}の{'原木' if m.group(2)=='Log' else '幹'}"
    m = re.fullmatch(r"Stripped (.+) (Log|Wood)", v)
    if m and m.group(1) in W: return f"樹皮を剥いだ{W[m.group(1)]}の{'原木' if m.group(2)=='Log' else '木'}"
    for s, sj in SUF:
        if v.endswith(" " + s):
            w = v[:-len(s)-1]
            if w in W: return W[w] + sj
    return None

d = json.load(open("extracted/twilightforest.json", encoding="utf-8"))
keys = [l.split("\t")[0] for l in open("cur_tf.txt", encoding="utf-8")]
out, miss = ["## twilightforest"], []
for k in keys:
    v = d["en_us"][k]
    j = name(v) if (k.startswith(("block.", "item.", "entity.")) and ".desc" not in k) else None
    if j: out.append(f"{k}\t{j}")
    else: miss.append(f"{k}\t{json.dumps(v, ensure_ascii=False)[1:-1]}")
open("tsv/v12_tf_gen.tsv", "w", encoding="utf-8").write("\n".join(out) + "\n")
open("cur_tf_rest.txt", "w", encoding="utf-8").write("\n".join(miss) + "\n")
print(len(out) - 1, len(miss))
