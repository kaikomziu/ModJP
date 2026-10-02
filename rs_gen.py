V = {"end":"エンド","nether":"ネザー","ocean":"海洋","underground":"地下","overworld":"オーバーワールド","jungle":"ジャングル",
"grassy":"草地","mangrove":"マングローブ","mushroom":"キノコ","stone":"石","birch":"シラカバ","desert":"砂漠","oak":"オーク",
"savanna":"サバンナ","snowy":"雪原","taiga":"タイガ","crimson":"真紅","dark_forest":"暗い森","icy":"氷雪","swamp":"沼地",
"warped":"歪んだ","badlands":"荒野","giant_tree_taiga":"巨木のタイガ","nether_brick":"ネザーレンガ","flower_forest":"花の森",
"cold":"寒冷","hot":"熱帯","warm":"温暖","nether_bricks":"ネザーレンガ","nether_basalt":"玄武岩","nether_crimson":"真紅",
"nether_soul":"ソウル","nether_warped":"歪んだ","nether_wasteland":"ネザーの荒地","bamboo":"竹","cherry":"サクラ",
"giant_taiga":"巨大タイガ","mountains":"山岳"}
T = {"ancient_city":"古代都市","bastion":"砦の遺跡","city":"都市","fortress":"要塞","igloo":"イグルー","mansion":"森の洋館",
"mineshaft":"廃坑","monument":"海底神殿","outpost":"前哨基地","pyramid":"ピラミッド","ruined_portal":"荒廃したポータル",
"ruins_land":"陸の遺跡","ruins":"遺跡","shipwreck":"難破船","stronghold":"要塞","temple":"神殿","village":"村","witch_hut":"ウィッチの小屋"}
out = ["## repurposed_structures", "=Locating... (Do not buy this map until finished)\t探索中…(完了するまでこの地図を買わないこと)"]
miss = []
for line in open("cur_repurposed_structures.txt", encoding="utf-8"):
    k = line.split("\t")[0]
    if not k.startswith("structure."): continue
    n = k[len("structure.repurposed_structures."):]
    for t in sorted(T, key=len, reverse=True):
        if n.startswith(t + "_") and n[len(t) + 1:] in V:
            nm = T[t]
            if t == "fortress": nm = "ネザー要塞"
            out.append(f"{k}\t{V[n[len(t)+1:]]}の{nm}"); break
    else:
        miss.append(n)
open("tsv/v11_rs_gen.tsv", "w", encoding="utf-8").write("\n".join(out) + "\n")
print(len(out) - 1, miss)
