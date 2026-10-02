C = {"black":"黒色","blue":"青色","brown":"茶色","cyan":"水色","gray":"灰色","green":"緑色","light_blue":"空色",
"light_gray":"薄灰色","lime":"黄緑色","magenta":"赤紫色","orange":"橙色","pink":"桃色","purple":"紫色","red":"赤色",
"white":"白色","yellow":"黄色"}
out = ["## simplylight",
"=Simple light block,\tシンプルな照明ブロック。",
"=Activates by %s.\t%sで点灯する。",
"=Deactivates by %s.\t%sで消灯する。",
"block.simplylight.illuminant_block\t発光ブロック",
"block.simplylight.illuminant_block_on\t発光ブロック(反転)"]
for c, j in C.items():
    out.append(f"block.simplylight.illuminant_{c}_block\t{j}の発光ブロック")
    out.append(f"block.simplylight.illuminant_{c}_block_on\t{j}の発光ブロック(反転)")
out += """block.simplylight.edge_light	ダイナミックエッジライト(下)
block.simplylight.edge_light_top	ダイナミックエッジライト(上)
=Follows walls around itself,	周囲の壁に沿って形を変える。
=perfect for hallways.	廊下に最適。
=Will morph depending on the blocks present around itself on placement.\\nShape will persist afterward, letting you make shapes using temporary blocks.	設置時に周囲にあるブロックに応じて形が変わる。\\nその後も形は保たれるので、仮置きのブロックを使って形を作れる。
block.simplylight.illuminant_panel	発光パネル
block.simplylight.illuminant_panel.info	シンプルなLEDパネル照明。
=Place in any direction.	どの向きにも設置できる。
block.simplylight.illuminant_slab	発光ハーフブロック
block.simplylight.illuminant_slab.info	シンプルなハーフブロックの照明。
block.simplylight.lamp_post	発光柱
block.simplylight.lamp_post.info	高さ3ブロックの街灯。
block.simplylight.lamp_post.info2	一番上のブロックが光る。
block.simplylight.lightbulb	シンプルな電球
block.simplylight.lightbulb.info	ただのシンプルな電球。
block.simplylight.lightbulb.info2	どの向きにも設置できる。
block.simplylight.rodlamp	発光ロッド
block.simplylight.rodlamp.info	シンプルな光の棒。
block.simplylight.rodlamp.info2	どの向きにも設置できる。
block.simplylight.wall_lamp	発光器具
block.simplylight.wall_lamp.info	壁から吊るしたり、天井や床に付けたりできる。
itemGroup.simplylight	Simply Light
simplylight.key.shift	Shift
simplylight.redstone	レッドストーン
simplylight.shift	<%s>で詳細を表示""".split("\n")
open("tsv/v11_sl_gen.tsv", "w", encoding="utf-8").write("\n".join(out) + "\n")
