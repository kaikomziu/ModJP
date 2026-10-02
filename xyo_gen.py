C = {"blue":"青い","dark":"暗い","green":"緑の","light":"明るい","red":"赤い"}
M = {"bricks":"レンガ","chiseled_deepslate":"模様入りの深層岩","chiseled_nether_bricks":"模様入りのネザーレンガ",
"chiseled_polished_blackstone":"模様入りのポリッシュドブラックストーン","chiseled_red_sandstone":"模様入りの赤い砂岩",
"chiseled_sandstone":"模様入りの砂岩","chiseled_stone_bricks":"模様入りの石レンガ","chiseled_wood_pillar":"模様入りの木の柱",
"crying_obsidian":"泣く黒曜石","deepslate_bricks":"深層岩レンガ","deepslate_tiles":"深層岩タイル",
"end_stone_bricks":"エンドストーンレンガ","gilded_blackstone":"きらめくブラックストーン","magma":"マグマブロック",
"mossy_stone_bricks":"苔むした石レンガ","mud_bricks":"泥レンガ","nether_bricks":"ネザーレンガ",
"polished_blackstone_bricks":"ポリッシュドブラックストーンレンガ","prismarine_bricks":"プリズマリンレンガ",
"purpur_block":"プルパーブロック","purpur_pillar":"プルパーの柱","quartz_bricks":"クォーツレンガ","stone_bricks":"石レンガ"}
out = ["## xycraft_override", "itemGroup.xycraft_override\tXyCraft Override"]
miss = []
for line in open("cur_xycraft_override.txt", encoding="utf-8"):
    k = line.split("\t")[0]
    n = k.replace("block.xycraft_override.", "")
    base, _, c = n.rpartition("_")
    if k.startswith("block.") and base in M and c in C:
        out.append(f"{k}\t{C[c]}{M[base]}")
    elif k != "itemGroup.xycraft_override":
        miss.append(line.rstrip())
open("tsv/v11_xyo_gen.tsv", "w", encoding="utf-8").write("\n".join(out) + "\n")
print(len(out), miss)
