import re
M = {"acacia_planks":"アカシア","birch_planks":"シラカバ","oak_planks":"オーク","dark_oak_planks":"ダークオーク",
"jungle_planks":"ジャングル","spruce_planks":"トウヒ","crimson_planks":"真紅","warped_planks":"歪んだ",
"cobblestone":"丸石","mossy_cobblestone":"苔むした丸石","glass":"ガラス","iron_block":"鉄","gold_block":"金",
"diamond_block":"ダイヤモンド","packed_ice":"氷","pink_wool":"桃色の羊毛","magenta_wool":"赤紫色の羊毛",
"nether_bricks":"ネザーレンガ","red_nether_bricks":"赤いネザーレンガ","sandstone":"砂岩","cut_sandstone":"研がれた砂岩",
"stone":"石","end_stone":"エンドストーン","end_stone_bricks":"エンドストーンレンガ","stone_bricks":"石レンガ",
"mossy_stone_bricks":"苔むした石レンガ","smooth_stone":"滑らかな石","blackstone":"ブラックストーン",
"polished_andesite":"磨かれた安山岩","polished_diorite":"磨かれた閃緑岩","polished_granite":"磨かれた花崗岩",
"polished_blackstone":"磨かれたブラックストーン"}
P = [("al_lamp_","のランプ"),("al_torch_","のALたいまつ"),("fire_pit_s_","の焚き火台"),("fire_pit_l_","の焚き火台(大)"),
     ("standing_torch_s_","のスタンドたいまつ"),("standing_torch_l_","のスタンドたいまつ(大)")]
out = ["## additional_lights"]
for line in open("cur_additional_lights.txt", encoding="utf-8"):
    k = line.split("\t")[0]
    if not k.startswith("block.additional_lights."): continue
    n = k[len("block.additional_lights."):]
    for p, s in P:
        if n.startswith(p) and n[len(p):] in M:
            out.append(f"{k}\t{M[n[len(p):]]}{s}"); break
open("tsv/v11_al_gen.tsv", "w", encoding="utf-8").write("\n".join(out) + "\n")
print(len(out) - 1)
