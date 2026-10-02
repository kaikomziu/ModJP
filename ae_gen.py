# aether_ii のブロック/アイテム名を素材×接尾辞で生成する
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

COLORS = {'White':'白色','Light Gray':'薄灰色','Gray':'灰色','Black':'黒色','Brown':'茶色','Red':'赤色','Orange':'橙色',
'Yellow':'黄色','Lime':'黄緑色','Green':'緑色','Cyan':'青緑色','Light Blue':'空色','Blue':'青色','Purple':'紫色',
'Magenta':'赤紫色','Pink':'桃色'}

# 素材(長いもの優先で照合)
MAT = {
 'Faded Holystone':'色あせた聖石','Irradiated Holystone':'照射された聖石','Mossy Holystone':'苔むした聖石',
 'Unstable Holystone':'不安定な聖石','Pointed Holystone':'尖った聖石','Holystone':'聖石',
 'Agiosite':'アギオサイト','Icestone':'氷石','Marbled Ichorite':'大理石模様のイコライト','Smooth Ichorite':'なめらかなイコライト',
 'Pointed Ichorite':'尖ったイコライト','Ichorite':'イコライト','Marbled':'大理石模様','Sentry':'哨兵石',
 'Unstable Undershale':'不安定なアンダーシェール','Undershale':'アンダーシェール',
 'Mossy Wisproot':'苔むしたウィスプルート','Skyroot':'スカイルート','Amberoot':'アンバールート','Greatroot':'グレートルート',
 'Wisproot':'ウィスプルート','Guardian':'ガーディアン','Infected':'感染した木',
 'Irradiated Greatboa':'照射されたグレートボア','Irradiated Greatoak':'照射されたグレートオーク','Irradiated Greatroot':'照射されたグレートルート',
 'Irradiated Skybirch':'照射されたスカイバーチ','Irradiated Skypine':'照射されたスカイパイン','Irradiated Skyplane':'照射されたスカイプレーン',
 'Irradiated Skyroot':'照射されたスカイルート','Irradiated Wisproot':'照射されたウィスプルート','Irradiated Wisptop':'照射されたウィスプトップ',
 'Greatboa':'グレートボア','Greatoak':'グレートオーク','Skybirch':'スカイバーチ','Skypine':'スカイパイン','Skyplane':'スカイプレーン',
 'Wisptop':'ウィスプトップ','Undergrowth':'下草','Rotshroom':'腐れキノコ','Shelf Rotshroom':'棚状の腐れキノコ',
 'Magnetic Shroom':'磁気キノコ','Spotted Magnetic Shroom':'斑点のある磁気キノコ',
 'Arkenium':'アーケニウム','Rustic Arkenium':'素朴なアーケニウム','Inert Arkenium':'不活性のアーケニウム','Inert Gravitite':'不活性のグラビタイト',
 'Gravitite':'グラビタイト','Zanite':'ザナイト','Ambrosium':'アンブロシア','Glint':'グリント','Corrobonite':'コロボナイト',
 'Golden Amber':'黄金の琥珀','Beast Pelt':'獣皮','Burrukai Plate':'ブルカイの甲殻','Neptune':'ネプチューン',
 'Quicksoil Glass':'流土のガラス','Gridded Quicksoil Glass':'格子の流土のガラス','Tiled Quicksoil Glass':'タイル張りの流土のガラス',
 'Crude Scatterglass':'粗い散光ガラス','Scatterglass':'散光ガラス','Ambrelinn Moss':'アンブレリン苔','Bryalinn Moss':'ブリャリン苔',
 'Shayelinn Moss':'シェイエリン苔','Cloudwool':'雲羊毛','Arctic Snow':'極地の雪','Arctic Ice':'極地の氷','Arctic Packed Ice':'極地の氷塊',
}
# 接尾辞 -> テンプレート({m}=素材)
SUF = [
 ('Brick Pressure Plate','{m}レンガの感圧板'),('Brick Button','{m}レンガのボタン'),
 ('Brick Slab','{m}レンガのハーフブロック'),('Brick Stairs','{m}レンガの階段'),('Brick Wall','{m}レンガの壁'),
 ('Base Bricks','{m}の土台レンガ'),('Base Pillar','{m}の土台の柱'),('Capstone Bricks','{m}の笠石レンガ'),('Capstone Pillar','{m}の笠石の柱'),
 ('Base Beam','{m}の土台の梁'),('Base Planks','{m}の土台の板材'),('Top Beam','{m}の上部の梁'),('Top Planks','{m}の上部の板材'),
 ('Small Shingles','{m}の小さな屋根板'),('Shingles','{m}の屋根板'),('Floorboards','{m}の床板'),('Highlight','{m}の縁取り板材'),
 ('Fence Gate','{m}のフェンスゲート'),('Hanging Sign','{m}の吊り看板'),('Pressure Plate','{m}の感圧板'),('Leaf Pile','{m}の落ち葉'),
 ('Log Slab','{m}の原木のハーフブロック'),('Wood Slab','{m}の木のハーフブロック'),('Log Base','{m}の原木の根元'),
 ('Crafting Table','{m}の作業台'),('Bricks','{m}レンガ'),('Flagstones','{m}の敷石'),('Keystone','{m}の要石'),('Pillar','{m}の柱'),
 ('Slab','{m}のハーフブロック'),('Stairs','{m}の階段'),('Wall','{m}の壁'),('Headstone','{m}の墓石'),('Runestone','{m}のルーン石'),
 ('Tile','{m}のタイル'),('Lightstone','{m}の光石'),('Button','{m}のボタン'),('Bookshelf','{m}の本棚'),('Furnace','{m}のかまど'),
 ('Smoker','{m}の燻製器'),('Lever','{m}のレバー'),('Vase','{m}の花瓶'),('Rock','{m}の小石'),('Quartz Ore','{m}の石英鉱石'),
 ('Beam','{m}の梁'),('Door','{m}のドア'),('Fence','{m}のフェンス'),('Leaves','{m}の葉'),('Log','{m}の原木'),('Planks','{m}の板材'),
 ('Sapling','{m}の苗木'),('Shelf','{m}の棚'),('Sign','{m}の看板'),('Trapdoor','{m}のトラップドア'),('Trunk','{m}の幹'),('Wood','{m}の木'),
 ('Roots','{m}の根'),('Deposit','{m}の琥珀鉱床'),('Barrel','{m}の樽'),('Chest','{m}のチェスト'),('Ladder','{m}のはしご'),
 ('Twig','{m}の小枝'),('Bed','{m}のベッド'),('Pane','{m}板'),('Ore','{m}鉱石'),('Bars','{m}の鉄格子'),('Chain','{m}の鎖'),
 ('Lantern','{m}のランタン'),('Carpet','{m}のカーペット'),('Vines','{m}のつる'),('Flowers','{m}の花'),('Block','{m}ブロック'),
 ('Stem','{m}の柄'),('Cluster','{m}の群生'),('Toadstool','{m}の傘'),
 # 道具・防具
 ('Axe','{m}の斧'),('Pickaxe','{m}のツルハシ'),('Shovel','{m}のシャベル'),('Hammer','{m}のハンマー'),('Pike','{m}のパイク'),
 ('Shortsword','{m}の短剣'),('Trowel','{m}の移植ごて'),('Crossbow','{m}のクロスボウ'),('Shield','{m}の盾'),('Helmet','{m}のヘルメット'),
 ('Chestplate','{m}のチェストプレート'),('Leggings','{m}のレギンス'),('Boots','{m}のブーツ'),('Gauntlets','{m}のガントレット'),
 ('Tunic','{m}のチュニック'),('Gloves','{m}の手袋'),('Cap','{m}の帽子'),('Pants','{m}のズボン'),('Shears','{m}のハサミ'),
 ('Pendant','{m}のペンダント'),('Core','{m}のコア'),('Plate','{m}の板'),('Gemstone','{m}の宝石'),('Chip','{m}のかけら'),
 ('Canister','{m}の容器'),('Alkahest Canister','アルカヘスト入りの{m}の容器'),('Hestveil Canister','ヘストヴェイル入りの{m}の容器'),
 ('Taluton Spawn Egg','{m}のタルトンのスポーンエッグ'),('Framed Crude Scatterglass Pane','{m}枠の粗い散光ガラス板'),
 ('Framed Crude Scatterglass','{m}枠の粗い散光ガラス'),('Framed Scatterglass Pane','{m}枠の散光ガラス板'),('Framed Scatterglass','{m}枠の散光ガラス'),
 ('Curved Arkenium Bars','曲がった{m}の鉄格子'),
]
SUF.sort(key=lambda x:-len(x[0]))
ORE_HOST = {'Undershale':'アンダーシェールの'}

# 単体名
NAME = {
 'Abandoned Bag':'捨てられたかばん','Aechor Cutting':'エーコル草の挿し穂','Aether Bush':'エーテルの茂み','Aether Dirt':'エーテルの土',
 'Aether Dirt Path':'エーテルの土の道','Aether Farmland':'エーテルの耕地','Aether Fern':'エーテルのシダ','Aether Grass Block':'エーテルの草ブロック',
 'Aether Portal':'エーテルポータル','Alkahest':'アルカヘスト','Alkahest Purifier':'アルカヘスト浄化器','Altar':'祭壇','Amber Hourglass':'琥珀の砂時計',
 'Block of Ambrosium':'アンブロシアのブロック','Ambrosium Campfire':'アンブロシアの焚き火','Ambrosium Torch':'アンブロシアの松明','Animal Stash':'動物の隠し場所',
 'Arilum':'アリラム','Blooming Arilum':'咲いたアリラム','Block of Arkenium':'アーケニウムのブロック','Arkenium Forge':'アーケニウムの鍛造炉',
 "Artisan's Bench":'職人の作業台','Blade Poa':'ブレードポア','Blue Aercloud':'青い天空雲','Blueberry Bush':'ブルーベリーの茂み','Blueberry Bush Stem':'ブルーベリーの茂みの茎',
 'Boss Doorway Block':'ボス部屋の入口ブロック','Brettl Flower':'ブレトルの花','Brettl Grass Bundle':'ブレトル草の束','Brettl Plant':'ブレトル草','Brettl Plant Tip':'ブレトル草の先端',
 'Brexallen Vase':'ブレクサレンの花瓶','Carrion Cutting':'キャリオン芽の挿し穂','Cloudwool':'雲羊毛','Cloudwool Bedroll':'雲羊毛の寝袋','Cloudwool Carpet':'雲羊毛のカーペット',
 'Cloudwool Roofing':'雲羊毛の屋根','Coarse Aether Dirt':'粗いエーテルの土','Cold Aercloud':'冷たい天空雲','Block of Corrobonite':'コロボナイトのブロック',
 'Enchanted Aether Grass Block':'エンチャントされたエーテルの草ブロック','Ferrosite':'フェロサイト','Ferrosite Mud':'フェロサイトの泥','Ferrosite Sand':'フェロサイトの砂',
 'Rusted Ferrosite':'錆びたフェロサイト','Floral Arkenium Bars':'花模様のアーケニウムの鉄格子','Patterned Arkenium Bars':'模様入りのアーケニウムの鉄格子',
 'Curved Arkenium Bars':'曲がったアーケニウムの鉄格子','Rustic Curved Arkenium Bars':'素朴な曲がったアーケニウムの鉄格子','Rustic Floral Arkenium Bars':'素朴な花模様のアーケニウムの鉄格子',
 'Rustic Patterned Arkenium Bars':'素朴な模様入りのアーケニウムの鉄格子','Fragile Arctic Ice':'もろい極地の氷','Frosted Arctic Ice':'霜の降りた極地の氷',
 'Frosted Ice':'氷霜','Fungal Cache':'菌類の隠し場所','Gel Block':'ジェルブロック','Block of Glint':'グリントのブロック','Golden Aercloud':'金色の天空雲',
 'Block of Golden Amber':'黄金の琥珀のブロック','Block of Gravitite':'グラビタイトのブロック','Green Aercloud':'緑の天空雲','Guardian Donation Box':'ガーディアンの献金箱',
 'Guardian Lamp':'ガーディアンのランプ','Guardian Pew':'ガーディアンの長椅子','Lucent Guardian Roots':'光るガーディアンの根','Unstable Guardian Roots':'不安定なガーディアンの根',
 'Hanging Undergrowth':'垂れ下がる下草','Hanging Undergrowth Plant':'垂れ下がる下草の株','Hesperose':'ヘスペローズ','Hestveil':'ヘストヴェイル','Holpupea':'ホルプピア',
 'Block of Inert Arkenium':'不活性のアーケニウムのブロック','Block of Inert Gravitite':'不活性のグラビタイトのブロック','Irradiated Dust Block':'照射された塵のブロック',
 'Large Arctic Ice Crystal':'大きな極地の氷晶','Medium Arctic Ice Crystal':'中くらいの極地の氷晶','Small Arctic Ice Crystal':'小さな極地の氷晶',
 'Lilichime':'リリチャイム','Locked Block':'鍵のかかったブロック','Magnetic Shroom':'磁気キノコ','Medium Aether Grass':'中くらいのエーテルの草',
 'Short Aether Grass':'背の低いエーテルの草','Tall Aether Grass':'背の高いエーテルの草','Moa Egg':'モアの卵','Mural':'壁画','Mycelial Aether Dirt':'菌糸のエーテルの土',
 'Orange Tree':'オレンジの木','Outpost Campfire':'前哨地の焚き火','Pluracian':'プルラシアン','Poasprout':'ポアの芽','Prayer Candle':'祈りのろうそく',
 'Purple Aercloud':'紫の天空雲','Quicksoil':'流土','Rotgrowth Vines':'腐れ茂みのつる','Rotshroom':'腐れキノコ','Sage Chest':'賢者のチェスト',
 'Satival Shoot':'サティヴァルの芽','Sentry Crate':'哨兵の木箱','Sentry Spawner':'哨兵のスポナー','Sentry Trap':'哨兵の罠','Shield Fern':'シールドシダ',
 'Shimmering Silt':'きらめく沈泥','Sky Roots':'天空の根','Storm Aercloud':'嵐の天空雲','Tangled Branches':'絡まった枝','Tarabloom':'タラブルーム',
 'Tarahesp Flowers':'タラヘスプの花','Treasure Doorway Block':'宝物部屋の入口ブロック','Undergrowth Leaves':'下草の葉','Undergrowth Vines':'下草のつる',
 'Valkyrie Sprout':'ワルキューレの芽','Veradexian Vase':'ヴェラデクシアンの花瓶','Woven Skyroot Sticks':'編んだスカイルートの棒','Holystone Quartz Ore':'聖石の石英鉱石',
 'Irradiated Holystone':'照射された聖石','Unstable Obsidian':'不安定な黒曜石','Block of Zanite':'ザナイトのブロック','Icestone':'氷石','Holystone':'聖石',
 'Agiosite':'アギオサイト','Ichorite':'イコライト','Undershale':'アンダーシェール','Corrobonite Cluster':'コロボナイトの結晶群',
 # アイテム
 'Aechor Petal':'エーコル花弁','Aerbunny Bell':'ソラウサギの鈴','Aether Portal Frame':'エーテルポータルのフレーム','Aether Quartz':'エーテルの石英',
 'Ambrosium Shard':'アンブロシアの欠片','Antitoxin Vial':'解毒剤の小瓶','Antivenom Vial':'抗毒素の小瓶','Arctic Snowball':'極地の雪玉','Arilum Bulbs':'アリラムの球根',
 'Arkenium Canister':'アーケニウムの容器','Arkenium Alkahest Canister':'アルカヘスト入りのアーケニウムの容器','Arkenium Hestveil Canister':'ヘストヴェイル入りのアーケニウムの容器',
 'Bandage':'包帯','Beast Pelt':'獣皮','Beast Pelt Bundle':'獣皮の包み','Blue Aercloud Glider':'青い天空雲のグライダー','Blueberry':'ブルーベリー',
 'Blueberry Moa Feed':'ブルーベリーのモアの餌','Brettl Cane':'ブレトルの茎','Brettl Grass':'ブレトル草','Brettl Rope':'ブレトルのロープ','Brettl Lasso':'ブレトルの投げ縄',
 'Broken Item':'壊れたアイテム','Broken %s':'壊れた%s','Burrukai Plate':'ブルカイの甲殻','Burrukai Plate Shield':'ブルカイの甲殻の盾','Burrukai Rib Cut':'ブルカイのあばら肉の切り身',
 'Burrukai Ribs':'ブルカイのあばら肉','Charge Catalyst':'チャージの触媒','Cloud Skiff':'雲の小舟','Cloudtwine':'雲より糸','Cockatrice Feather':'コカトリスの羽根',
 'Cold Aercloud Glider':'冷たい天空雲のグライダー','Corrobonite Crystal':'コロボナイトの結晶','Dart Shooter':'吹き筒','Enchanted Blueberry':'エンチャントされたブルーベリー',
 'Enchanted Moa Feed':'エンチャントされたモアの餌','Enchanted Orange':'エンチャントされたオレンジ','Enchanted Swet Jelly':'エンチャントされたスェットゼリー',
 'Enchanted Wyndberry':'エンチャントされたウィンドベリー','Engraved Disc':'刻まれたディスク','Eye of the Mimic':'ミミックの目','Fossilized Corrobonite':'化石化したコロボナイト',
 'Fossilized Glint':'化石化したグリント','Fossilized Zanite':'化石化したザナイト','Fried Prismallard Egg':'プリズマラードの目玉焼き','Glint Coin':'グリント硬貨',
 'Glint Gemstone':'グリントの宝石','Golden Aercloud Glider':'金色の天空雲のグライダー','Golden Amber':'黄金の琥珀','Golden Wyndberry':'黄金のウィンドベリー',
 'Guidebook Page':'手引書のページ','Hammer of Demolition':'破壊のハンマー','Healing Stone':'治癒の石','Icestone Pendant':'氷石のペンダント','Inert Arkenium':'不活性のアーケニウム',
 'Inert Gravitite':'不活性のグラビタイト','Irradiated Armor':'照射された防具','Random Armor':'ランダムな防具','Irradiated Chunk':'照射された塊','Random Item':'ランダムなアイテム',
 'Irradiated Dust':'照射された塵','Irradiated Tool':'照射された道具','Random Tool':'ランダムな道具','Irradiated Weapon':'照射された武器','Random Weapon':'ランダムな武器',
 'Kinetic Thrusters':'運動推進器','Kirrid Cutlet':'キリッドのカツレツ','Kirrid Loin':'キリッドのロース','Kirrid Plate':'キリッドの板','Large Moa Saddlebag':'大きなモアの鞍袋',
 'Moa Feather':'モアの羽根','Moa Feed':'モアの餌','Moa Saddle':'モアの鞍','Moa Saddlebag':'モアの鞍袋','Music Player':'音楽プレーヤー','Neptune Scale':'ネプチューンの鱗',
 'Orange':'オレンジ','Prismallard Egg':'プリズマラードの卵','Prismallard Feather':'プリズマラードの羽根','Prismallard Leg':'プリズマラードのもも肉',
 'Prismallard Roast':'プリズマラードのロースト','Purple Aercloud Glider':'紫の天空雲のグライダー','Raw Taegore Meat':'生のタエゴアの肉','Resonant Stone':'共鳴する石',
 'Roasted Skyroot Lizard on a Stick':'スカイルートトカゲの串焼き','Skyroot Lizard on a Stick':'スカイルートトカゲの串刺し','Satival Bulb':'サティヴァルの球根',
 'Scatterglass Bolt':'散光ガラスの矢','Scatterglass Shard':'散光ガラスの破片','Scatterglass Vial':'散光ガラスの小瓶','Sentry Boots':'哨兵のブーツ','Sentry Servo':'哨兵のサーボ',
 'Shifting Glass':'移ろいのガラス','Skyroot Bucket':'スカイルートのバケツ','Skyroot Bucket of Axolotl':'ウーパールーパー入りスカイルートのバケツ',
 'Skyroot Bucket of Cod':'タラ入りスカイルートのバケツ','Skyroot Bucket of Pufferfish':'フグ入りスカイルートのバケツ','Skyroot Bucket of Salmon':'サケ入りスカイルートのバケツ',
 'Skyroot Bucket of Tadpole':'オタマジャクシ入りスカイルートのバケツ','Skyroot Bucket of Tropical Fish':'熱帯魚入りスカイルートのバケツ','Skyroot Milk Bucket':'牛乳入りスカイルートのバケツ',
 'Skyroot Powder Snow Bucket':'粉雪入りスカイルートのバケツ','Skyroot Water Bucket':'水入りスカイルートのバケツ','Skyroot Pinecone':'スカイルートの松ぼっくり','Skyroot Stick':'スカイルートの棒',
 'Splint':'添え木','Swet Gel':'スェットのジェル','Swet Jelly':'スェットゼリー','Swet Sugar':'スェットの砂糖','Taegore Steak':'タエゴアのステーキ','Valkyrie Tea':'ワルキューレの茶',
 'Valkyrie Wings':'ワルキューレの翼','Water Vial':'水の小瓶','Wyndberry':'ウィンドベリー','Zanite Gemstone':'ザナイトの宝石','Zephyr Husk':'ゼファーの抜け殻',
 'Arkenium Plate':'アーケニウムの板','Gravitite Plate':'グラビタイトの板',
}
DARTS = {'Amber':'琥珀','Ambrosium Poisoning':'アンブロシア中毒','Charged':'帯電','Crystallized':'結晶化','Fracture':'骨折','Frostbite':'凍傷','Fungal Rot':'菌腐れ',
 'Immolation':'焼身','Stun':'気絶','Toxin':'毒素','Venom':'猛毒','Webbed':'クモの巣','Wound':'負傷'}
CHARM = {'Agility':'敏捷','Damage':'ダメージ','Defense':'防御','Dexterity':'器用さ','Efficiency':'効率','Health':'体力','Knockback':'ノックバック','Reach':'リーチ',
 'Resistance':'耐性','Toughness':'強靭さ'}
MOBS = {'Aechor Plant':'エーコル草','Aerbunny':'ソラウサギ','Aerwhale':'天界鯨','Burrukai':'ブルカイ','Kirrid':'キリッド','Taegore':'タエゴア','Blue Swet':'青スェット',
 'Carrion Sprout':'キャリオン芽','Cockatrice':'コカトリス','Detonation Sentry':'爆発セントリー','Flying Cow':'空飛ぶウシ','Glitterwing':'グリッターウィング',
 'Golden Swet':'金のスェット','Moa':'モア','Phyg':'トブタ','Prismallard':'プリズマラード','Sentry Crate Mimic':'哨兵の木箱ミミック','Sentry Golem':'セントリーゴーレム',
 'Sheepuff':'ワターメェ','Shroudwing':'シュラウドウィング','Skephid':'スケフィッド','Skyroot Lizard':'スカイルートトカゲ','Slider':'スライダー','Tempest':'テンペスト',
 'Zephyr':'ゼファー','Arkenium Taluton':'アーケニウムのタルトン','Gravitite Taluton':'グラビタイトのタルトン'}
TIP = {
 'Enchants Nature':'自然をエンチャントする','Upgrades Further':'さらに強化できる','Calms Animals':'動物を落ち着かせる','Upwards Boost':'上昇ブースト','Stun Resistance':'気絶耐性',
 'Prevents Baby Animal Aging':'子どもの動物の成長を止める','Levitates Block':'ブロックを浮かせる','Double Jump':'二段ジャンプ','Straight Shot':'直進射撃','Increases Gravity':'重力を強める',
 'Shoots Explosive':'爆発物を撃つ','Sheds Ambrosium':'アンブロシアを落とす','Spread Shot':'拡散射撃','Freezes Liquids':'液体を凍らせる','Irradiates Nature':'自然を照射する',
 'Walk in Water':'水中歩行','Forwards Boost':'前進ブースト','Zephyr Protection':'ゼファーからの保護','Directional Dash':'方向ダッシュ','Increases Yield':'収穫量が増える',
 'Double Shot':'二連射','Grows Nature':'自然を育てる','Grows Stronger':'強くなっていく','Speed Boost':'速度上昇',
}
USE = {'Click-Use':'クリックで使用','Crouch-Interact':'しゃがんで使用','Crouch-Use':'しゃがんで使用'}

def name(v):
    if v in NAME: return NAME[v]
    m = re.fullmatch(r'(.+) Darts', v)
    if m and m.group(1) in DARTS: return DARTS[m.group(1)]+'のダーツ'
    m = re.fullmatch(r'Charm of (\w+) I', v)
    if m and m.group(1) in CHARM: return CHARM[m.group(1)]+'のお守り I'
    m = re.fullmatch(r'(.+) Spawn Egg', v)
    if m and m.group(1) in MOBS: return MOBS[m.group(1)]+'のスポーンエッグ'
    m = re.fullmatch(r'Potted (.+)', v)
    if m:
        r = name(m.group(1)); return '鉢植えの'+r if r else None
    m = re.fullmatch(r'Stripped (.+)', v)
    if m:
        r = name(m.group(1)); return '樹皮を剥いだ'+r if r else None
    m = re.fullmatch(r'Secret (\w+) (Door|Trapdoor)', v)
    if m and m.group(1) in MAT: return MAT[m.group(1)]+'の隠し'+('ドア' if m.group(2)=='Door' else 'トラップドア')
    for c in sorted(COLORS, key=len, reverse=True):
        if v.startswith(c+' '):
            rest = v[len(c)+1:]
            if rest in ('Cloudwool','Cloudwool Carpet','Arilum Lantern','Skyroot Bed'):
                return COLORS[c]+'の'+name(rest) if rest!='Arilum Lantern' else COLORS[c]+'のアリラムのランタン'
    if v == 'Arilum Lantern': return 'アリラムのランタン'
    for mat in sorted(MAT, key=len, reverse=True):
        if v.startswith(mat+' '):
            rest = v[len(mat)+1:]
            for s,t in SUF:
                if rest == s:
                    if s == 'Ore' and mat not in ('Undershale',):
                        return MAT[mat]+'鉱石'
                    return t.format(m=MAT[mat])
            # Undershale Zanite Ore
            if mat == 'Undershale' and rest.endswith(' Ore'):
                inner = rest[:-4]
                if inner in MAT: return 'アンダーシェールの'+MAT[inner]+'鉱石'
        if v == mat: return MAT[mat]
    return None

def tip(v):
    m = re.fullmatch(r'§9Ability:§r (.+)', v)
    if m and m.group(1) in TIP: return '§9能力:§r '+TIP[m.group(1)]
    m = re.fullmatch(r'§3Use:§r (.+)', v)
    if m and m.group(1) in USE: return '§3使い方:§r '+USE[m.group(1)]
    if v == '§9Set Pieces:§r %s': return '§9セット:§r %s'
    if v == '§4§oWork in Progress§r§r': return '§4§o開発中§r§r'
    return None

if __name__ == '__main__':
    out = ['## aether_ii']; miss = []
    for line in open('cur_ae.txt', encoding='utf-8'):
        k, v = line.rstrip('\n').split('\t', 1)
        if not (k.startswith('block.') or k.startswith('item.')): continue
        r = tip(v) or name(v)
        if r: out.append(k+'\t'+r)
        else: miss.append(k+'\t'+v)
    open('tsv/v14_ae_gen.tsv', 'w', encoding='utf-8').write('\n'.join(out)+'\n')
    open('ae_miss.txt', 'w', encoding='utf-8').write('\n'.join(miss)+'\n')
    print(len(out)-1, 'generated,', len(miss), 'missing')
