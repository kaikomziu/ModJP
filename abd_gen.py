C = {"black":"黒色","blue":"青色","brown":"茶色","cyan":"水色","gray":"灰色","green":"緑色","light_blue":"空色",
"light_gray":"薄灰色","lime":"黄緑色","magenta":"赤紫色","orange":"橙色","pink":"桃色","purple":"紫色","red":"赤色",
"white":"白色","yellow":"黄色"}
M = {"raw_copper":"銅の原石","raw_gold":"金の原石","raw_iron":"鉄の原石","basalt":"玄武岩","sandstone":"砂岩",
"red_sandstone":"赤い砂岩","blackstone":"ブラックストーン","stone":"石","cobblestone":"丸石","diamond":"ダイヤモンド",
"lapis":"ラピスラズリ","emerald":"エメラルド","amethyst":"アメジスト","quartz_bricks":"クォーツレンガ","obsidian":"黒曜石",
"crying_obsidian":"泣く黒曜石","iron":"鉄","netherite":"ネザライト","bone":"骨","honeycomb":"ハニカム",
"packed_ice":"氷塊","blue_ice":"青氷","soul_soil":"ソウルソイル","soul_sand":"ソウルサンド","moss":"苔",
"gilded_blackstone":"きらめくブラックストーン","shroomlight":"シュルームライト",
"cracked_polished_blackstone_bricks":"ひび割れたポリッシュドブラックストーンレンガ","deepslate":"深層岩",
"rooted_dirt":"根付いた土","muddy_mangrove_roots":"泥だらけのマングローブの根","snow":"雪","netherrack":"ネザーラック",
"coarse_dirt":"粗い土","gold":"金"}
for c, j in C.items():
    M["concrete_" + c] = j + "のコンクリート"
    M["terracotta_" + c] = j + "のテラコッタ"
    M["wool_" + c] = j + "の羊毛"
S = {"slab":"のハーフブロック","stairs":"の階段","wall":"の塀","gate":"のフェンスゲート","trapdoor":"のトラップドア"}
out = ["## absentbydesign"]
miss = []
for line in open("cur_absentbydesign.txt", encoding="utf-8"):
    k = line.split("\t")[0]
    if not k.startswith("block.absentbydesign."):
        miss.append(line.rstrip()); continue
    n = k[len("block.absentbydesign."):]
    t, _, m = n.partition("_")
    if t in S and m in M:
        out.append(f"{k}\t{M[m]}{S[t]}")
    else:
        miss.append(line.rstrip())
open("tsv/v11_abd_gen.tsv", "w", encoding="utf-8").write("\n".join(out) + "\n")
print(len(out) - 1)
print("\n".join(miss))
