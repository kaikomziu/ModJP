# Chisel(26.1.2)の名前と模様説明を生成する。名前はバニラ公式名を優先、模様説明は単語辞書と言い回し規則で組み立てる。
import json, re
from pathlib import Path

van_en = json.loads(Path("vanilla/en_us.json").read_text(encoding="utf-8"))
van_ja = json.loads(Path("vanilla/ja_jp.json").read_text(encoding="utf-8"))
VAN = {}
for k, v in van_en.items():
    if k.startswith(("block.minecraft.", "item.minecraft.")) and k.count(".") == 2 and k in van_ja:
        VAN.setdefault(v, van_ja[k])

NAMES = {"Lead":"鉛","Acacia Bookshelf":"アカシアの本棚","Aluminum":"アルミニウム","Ancient Stone":"古代の石","Antiblock":"アンチブロック",
"Arcane":"秘術ブロック","Auto Chisel":"自動のみ","Bamboo Bookshelf":"竹の本棚","Birch Bookshelf":"シラカバの本棚","Blank Rune":"無地のルーン",
"Bronze":"青銅","Builders Guide":"建築ガイド","Certus Quartz":"ケルタスクォーツ","Cherry Bookshelf":"サクラの本棚","Cloud":"雲",
"Coal Coke":"コークス","Cobalt":"コバルト","Concrete":"コンクリート","Crimson Bookshelf":"真紅の本棚","Dark Oak Bookshelf":"ダークオークの本棚",
"Electrum":"エレクトラム","Energized Voidstone":"活性化した虚空石","Factory Block":"工場ブロック","Futura Block":"フューチュラブロック",
"Grimstone":"グリムストーン","Hex Plating":"六角装甲板","Holystone":"聖石","Invar":"インバー","Jungle Bookshelf":"ジャングルの本棚",
"Laboratory Block":"研究所ブロック","Lavastone":"溶岩石","Leaf Block":"葉のブロック","Light blue Stained Glass":"空色の色付きガラス",
"Light blue Stained Glass Pane":"空色の色付きガラス板","Light gray Stained Glass":"薄灰色の色付きガラス",
"Light gray Stained Glass Pane":"薄灰色の色付きガラス板","Light_blue Concrete":"空色のコンクリート","Light_blue Wool":"空色の羊毛",
"Light_gray Concrete":"薄灰色のコンクリート","Light_gray Wool":"薄灰色の羊毛","Limestone":"石灰岩","Magma":"マグマ",
"Mangrove Bookshelf":"マングローブの本棚","Marble":"大理石","Military":"軍用ブロック","Mossy Blackstone":"苔むしたブラックストーン",
"Mossy Temple Block":"苔むした神殿ブロック","Nickel":"ニッケル","Oak Bookshelf":"オークの本棚","Pale Oak Bookshelf":"ペールオークの本棚",
"Pale Oak Planks":"ペールオークの板材","Paperwall":"紙壁","Platinum":"プラチナ","Purpur":"プルプァ","Road Lines":"道路の白線",
"Shingles":"こけら板","Silver":"銀","Sky Stone":"スカイストーン","Spruce Bookshelf":"トウヒの本棚","Steel":"鋼鉄","Tallow":"獣脂",
"Technical Block":"技術ブロック","Temple Block":"神殿ブロック","Thaumium":"タウミウム","Tin":"スズ","Tyrian":"ティリアン",
"Uranium":"ウラン","Valentine's Block":"バレンタインブロック","Voidstone":"虚空石","Warning Sign":"警告標識","Warped Bookshelf":"歪んだ本棚",
"Waterstone":"水石","Woolen Clay":"羊毛粘土"}

W = {"Pillar":"柱","Bricks":"レンガ","Brick":"レンガ","Encased":"枠付き","Small":"小さな","Panel":"パネル","Tiles":"タイル","Tile":"タイル",
"Connected":"連結","Large":"大きな","Wood":"材","Meander":"雷文","Gem":"宝石","Glass":"ガラス","Ionic":"イオニア式","Chisel":"のみ",
"Basic":"基本","Dent":"くぼみ","Vertical":"縦","Block":"ブロック","Blocks":"ブロック","Triple":"三連","Chaotic":"乱雑な","Bookshelf":"本棚",
"Planks":"板材","Plank":"板材","French":"フレンチ","Pane":"板","Braid":"編み込み","Plain":"無地","Scaffold":"足場","Spiral":"らせん",
"Round":"丸い","Facet":"多面","Layers":"層","Layer":"層","Stripes":"ストライプ","Cracked":"ひび割れた","Ornate":"装飾","Crate":"木箱",
"Borderless":"枠なし","Plate":"板","Plates":"板","Anti":"アンチ","Fancy":"豪華な","Classic":"クラシック","Shiny":"光沢","Skull":"ドクロ",
"Oak":"オーク","Indent":"へこみ","Horizontal":"横","Checker":"市松","Square":"四角","Medium":"中くらいの","Road":"道路","Polished":"磨かれた",
"Parquet":"寄木","Medallion":"メダリオン","Lodestone":"ロードストーン","Line":"線","Lines":"線","Inlayed":"象嵌","Herringbone":"ヘリンボーン",
"Dots":"ドット","Mosaic":"モザイク","Twisted":"ねじれた","Slanted":"斜め","Plating":"装甲板","Jellybean":"ジェリービーンズ",
"Circular":"円形","Array":"配列","Zag":"ジグザグ","Weaver":"織り","Cuts":"切り込み","Solid":"無垢","Soft":"柔らかい","Red":"赤い",
"Raw":"原石","Light":"明るい","Smooth":"なめらかな","Prismatic":"プリズム","Sandstone":"砂岩","Log":"原木","Bubble":"泡","Temple":"神殿",
"Scribbles":"落書き","Frame":"枠","Dull":"くすんだ","Creeper":"クリーパー","Mossy":"苔むした","Star":"星","Heart":"ハート","White":"白い",
"Caution":"注意","Border":"縁","Blue":"青い","Iron":"鉄","Dark":"暗い","Cobblestone":"丸石","Waves":"波","Slab":"ハーフブロック",
"Skeleton":"スケルトン","Cobble":"丸石","Purple":"紫の","Old":"古い","Marble":"大理石","Books":"本","Black":"黒い","Shipping":"出荷用",
"Relic":"遺物","Bolted":"ボルト留め","Yellow":"黄色い","Thermal":"熱","Pink":"桃色の","Obsidian":"黒曜石","Cabin":"小屋","Stone":"石",
"Machine":"機械","Gray":"灰色の","Grey":"灰色の","Warped":"歪んだ","Spruce":"トウヒ","Pale":"ペール","Mangrove":"マングローブ",
"Jungle":"ジャングル","Crimson":"真紅","Cherry":"サクラ","Birch":"シラカバ","Acacia":"アカシア","Woolen":"羊毛","Voidstone":"虚空石",
"Quad":"四分割","Orange":"橙色の","Nether":"ネザー","Llama":"ラマ","Legacy":"旧式","Grimstone":"グリムストーン","Green":"緑の",
"Cyan":"青緑色の","Clay":"粘土","Brown":"茶色の","Bordered":"縁取り","Redstone":"レッドストーン","Magenta":"赤紫色の","Lime":"黄緑色の",
"Holystone":"聖石","Rainbow":"虹色の","Netherrack":"ネザーラック","Modern":"モダン","Masonry":"石積み","Tomes":"大型本","Stacked":"積み重ね",
"Pastel":"パステル","Papers":"書類","Necromancer’s":"死霊術師の","Necromancer's":"死霊術師の","Hoarder's":"収集家の",
"Historian's":"歴史家の","Dirt":"土","Cans":"缶","Apprentice":"見習いの","Abandoned":"放棄された","Greek":"ギリシャ風",
"Bamboo":"竹","(North-South)":"(南北)","(East-West)":"(東西)","Limestone":"石灰岩","Emerald":"エメラルド","Diamond":"ダイヤモンド",
"Capstone":"笠石","Prism":"プリズム","Paperwall":"紙壁","Golden":"金の","Rune":"ルーン","Metal":"金属","Lapis":"ラピスラズリ",
"Diagonal":"斜め","Coal":"石炭","Rusty":"錆びた","Meat":"肉","Fan":"ファン","Energized":"活性化した","125":"125","Wall":"壁","Steel":"鋼鉄",
"Stand":"台","Lamp":"ランプ","Gold":"金","Double":"二重","Bars":"格子","Weathered":"風化した","Tape":"テープ","Platform":"足場",
"Panels":"パネル","Moon":"月","Lava":"溶岩","Inverted":"反転","Guts":"内臓","Engineering":"工学","Enamelled":"琺瑯","Damaged":"傷んだ",
"Concrete":"コンクリート","Cloud":"雲","Circuit":"回路","Bismuth":"ビスマス","Zelda":"ゼルダ風","Worn":"すり減った","Wide":"幅広",
"Waterstone":"水石","Vents":"通気口","Terracotta":"テラコッタ","Stack":"積み","Squares":"四角","Smiling":"笑顔の","Screen":"画面",
"Runes":"ルーン","Rough":"粗い","Right":"右","Purpur":"プルプァ","Prismarine":"プリズマリン","Neutral":"無表情の","Neon":"ネオン",
"Magma":"マグマ","Lavastone":"溶岩石","Japanese":"和風","Ingots":"インゴット","Grid":"格子","Granite":"花崗岩","Felsic":"珪長質",
"End":"エンド","Egregiously":"ひどく","Disordered":"乱れた","Diorite":"閃緑岩","Deepslate":"深層岩","Coke":"コークス","Coin":"硬貨",
"Chiseled":"模様入り","Chinese":"中華風","Charcoal":"木炭","Carved":"彫られた","Camouflaged":"迷彩","Basalt":"玄武岩","Andesite":"安山岩",
"Wireframe":"ワイヤーフレーム","Water":"水","Transparent":"透明","Striked":"打ち抜き","Simple":"シンプルな","Mixed":"混合",
"Matrix":"マトリクス","Glowing":"光る","Dotted":"点描","Detailed":"精緻な","Dented":"くぼんだ","Decoration":"装飾","Construction":"工事",
"Console":"コンソール","Column":"円柱","Clear":"透き通った","Chunks":"塊","Chunk":"塊","Blood":"血","Big":"大きな","Wax":"蝋",
"Under-Pipe":"配管下","Tiny":"ごく小さな","Thin":"細い","Thick":"太い","Teamed":"チーム","Tall":"高い","Symbol":"記号","Streak":"筋",
"Spattered":"飛び散った","Smirking":"にやりとした","Sleeping":"眠った","Shale":"頁岩","Scary":"怖い","Sad":"悲しい","Runic":"ルーンの",
"Rose":"バラ","Rivets":"リベット","Reinforced":"補強された","Quartz":"クォーツ","Pensive":"物思いの","Ornamental":"装飾用",
"Organic-Looking":"有機的な","Mysterious":"謎の","Metallic":"金属の","Metal-Bordered":"金属縁の","Menacing":"威圧的な","Marker":"標識",
"Map":"地図","Mafic":"苦鉄質","Leaves":"葉","Layered":"層状の","Laughing":"笑う","Labyrinthic":"迷宮風","Huge":"巨大な",
"Heads-up":"上向き","Heads-down":"下向き","Hazard":"危険","Grate":"格子蓋","Gold-Plated":"金めっき","Glow":"光","Gears":"歯車",
"Floor":"床","Flat":"平らな","Fence":"柵","Falling":"落下","Faded":"色あせた","Eye":"目","Exited":"興奮した","Evil":"邪悪な",
"Embroidered":"刺繍","Emboss":"浮き彫り","Edge":"縁","Disappointed":"がっかりした","Direction":"方向","Diamonds":"ダイヤモンド",
"Curious":"好奇心の","Convex":"凸面","Cobble-Dirt":"丸石と土","Closed":"閉じた","Christmas":"クリスマス","Cheeky":"生意気な",
"Candle":"ロウソク","Bulb":"電球","Bored":"退屈した","Borders":"縁","Blank":"無地","Beveled":"面取り","Astonished":"驚いた",
"Arranged":"並べた","Applied":"応用","(Secluded)":"(隔離)","Yellow-Black":"黄黒","Wires":"配線","Warning":"警告","Voltage":"電圧",
"Very":"とても","Vertically":"縦に","Ventilation":"換気","Varied":"さまざまな","Valentines":"バレンタイン","Under":"下","Unboxed":"箱なし",
"Totem":"トーテム","Tinted":"色付き","Surprised":"びっくりした","Suprised":"びっくりした","Supaplex":"スーパープレックス","Sunken":"沈んだ",
"Sturdy":"頑丈な","Stuff":"もの","Spinning":"回転","Spikes":"トゲ","Smaller":"より小さな","Slow":"遅い","Skulls":"ドクロ","Six":"6",
"Simplistic":"簡素な","Shaped":"形の","Shade":"日よけ","Server":"サーバー","Sectioned":"区切られた","Seams":"継ぎ目","Sandcobble":"砂丸石",
"Rusted":"錆びた","Rust":"錆","Roundel":"円形紋","Required":"必須","Region":"区域","Radiation":"放射線","Radial":"放射状",
"Prototype":"試作","Poptart":"ポップタルト","Poison":"毒","Plain-Plain":"無地-無地","Plain-Greek":"無地-ギリシャ風","Piping":"配管",
"Pipes)":"パイプ)","Pipe)":"パイプ)","Petals":"花びら","Pattern":"模様","Pareidolia":"顔に見える","Pads":"パッド","Oxygen":"酸素",
"Original":"オリジナル","Orange-White":"橙白","Openings":"開口部","Opening":"開口部","Old-Timey":"昔風","Objects":"物体","Normal":"通常",
"No":"なし","Nethergravel":"ネザー砂利","Mortarless":"モルタルなし","Middle":"中央","Megacell":"メガセル","Massive":"巨大",
"Malfunctioning":"故障した","Makeshift":"間に合わせの","Loud":"大きな音","Little":"少しの","Lights":"照明","Lattice":"格子細工",
"Laboratory":"研究所","Insulation":"断熱材","Information":"情報","Imitating":"真似た","Illuminati":"イルミナティ","Ice":"氷",
"Horizontally":"横に","High":"高","Hex":"六角","Happy":"幸せな","Growth":"成長","Grinder":"粉砕機","Gridded":"格子状の",
"Greek-Plain":"ギリシャ風-無地","Greek-Greek":"ギリシャ風-ギリシャ風","Glyphs":"象形文字","Generic":"汎用","Fuzzy":"ぼやけた",
"Freezing":"凍結","Flywheels":"はずみ車","Flowing":"流れる","Floral":"花柄","Flaky":"剥がれかけの","Fire":"炎","Fast":"速い",
"Farmland":"耕地","Explosion":"爆発","Exhaust":"排気","Ere":"昔の","Entry":"入口","Engraved":"刻まれた","Embossed":"浮き彫りの",
"Elaborate":"凝った","Dungeon":"ダンジョン","Door":"扉","Design":"デザイン","Decor":"装飾","Death":"死","Dead":"枯れた",
"Darker":"より暗い","Dangerous":"危険な","Danger":"危険","Crystal":"結晶","Cryogenic":"極低温","Crushes":"砕く","Crushed":"砕いた",
"Crumbling":"崩れかけの","Crossed":"交差した","Conduit":"コンジット","Circle":"円","Chunky":"ごつごつした","Chrono":"クロノ",
"Chemicals":"化学薬品","Checkerboard":"チェッカーボード","Cells":"セル","Cell":"セル","Cart":"トロッコ","Cage":"檻","Cables":"ケーブル",
"Bright":"明るい","Brain":"脳","Boxed":"箱入り","Box":"箱","Bleak":"寒々とした","Blackstone":"ブラックストーン","Biohazard":"バイオハザード",
"Bevel":"面取り","Base":"土台","Balls":"玉","Asphalt":"アスファルト","Arrangement":"配置","Aged":"古びた","Advanced":"高度な",
"Adorned":"飾られた","Long":"長い","disarray":"乱雑","A":"","(Small":"(小さな","(Large":"(大きな","(Right)":"(右)","(Off)":"(オフ)","(Malfunctioning)":"(故障)",
"(Left)":"(左)","(Fast)":"(高速)","&":"と","1":"1","2":"2","3":"3","4":"4","5":"5","6":"6","gray":"灰色の","blue":"青い","emerald":"エメラルド",
"stone":"石","Wood Tiles":"材タイル"}
LOWER = {"light blue":"空色の","light gray":"薄灰色の"}
def words(s):
    s2 = s
    for a, b in (("Light blue ", "空色の "), ("Light gray ", "薄灰色の ")):
        s2 = s2.replace(a, b)
    out = []
    for w in s2.split():
        if w in ("空色の", "薄灰色の"): out.append(w); continue
        if w not in W: return None
        out.append(W[w])
    return "".join(out)

def desc(s):
    m = re.fullmatch(r"(.+) in Disarray", s)
    if m:
        a = words(m.group(1)); return a and f"乱雑な{a}"
    m = re.fullmatch(r"(.+) with(?:out)? (.+)", s)
    if m:
        a, b = words(m.group(1)), words(m.group(2))
        if a and b: return f"{b}{'なし' if ' without ' in s else '付き'}の{a}"
        return None
    m = re.fullmatch(r"(.+) made of (.+)", s)
    if m:
        a, b = words(m.group(1)), words(m.group(2)); return a and b and f"{b}でできた{a}"
    m = re.fullmatch(r"(.+) in (.+)", s)
    if m:
        a, b = words(m.group(1)), words(m.group(2)); return a and b and f"{b}にはめた{a}"
    m = re.fullmatch(r"(.+) of (.+)", s)
    if m:
        a, b = words(m.group(1)), words(m.group(2)); return a and b and f"{b}の{a}"
    return words(s)

def name(s):
    return NAMES.get(s) or VAN.get(s)

if __name__ == "__main__":
    out, miss = ["## chisel"], []
    seen = set()
    for l in open("cur_chisel.txt", encoding="utf-8"):
        k, v = l.rstrip("\n").split("\t", 1)
        if not k.startswith("block."): continue
        j = desc(v) if k.endswith(".desc") else name(v)
        if j:
            out.append(f"{k}\t{j}")
        elif v not in seen:
            seen.add(v); miss.append(v)
    Path("tsv/v14_chisel_gen.tsv").write_text("\n".join(out) + "\n", encoding="utf-8")
    Path("cur_chisel_miss.txt").write_text("\n".join(miss) + "\n", encoding="utf-8")
    print(len(out) - 1, len(miss))
