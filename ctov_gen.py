B = {"beach":"砂浜","christmas":"クリスマス","dark_forest":"暗い森","desert":"砂漠","desert_fortified":"砂漠の要塞化された",
"jungle":"ジャングル","jungle_tree":"ジャングルの樹上","mesa":"荒野","mesa_fortified":"荒野の要塞化された","mountain":"和風",
"mountain_alpine":"高山","mushroom":"キノコ","plains":"平原","plains_fortified":"平原の要塞化された","savanna":"サバンナ",
"savanna_na":"サバンナの先住民","snowy":"雪原","swamp":"沼地","swamp_fortified":"沼地の要塞化された","taiga":"タイガ",
"taiga_fortified":"タイガの要塞化された","badlands":"荒野"}
S = {"large":"大","medium":"中","small":"小"}
out = ["## ctov"]
for line in open("cur_ctov.txt", encoding="utf-8"):
    k = line.split("\t")[0]
    p = k.split(".")
    if len(p) == 4:
        b = p[3][len("village_"):]
        j = B[b]
        out.append(f"{k}\t{j}{'' if j.endswith('た') else 'の'}村({S[p[2]]})")
    else:
        b = p[2][len("pillager_outpost_"):]
        out.append(f"{k}\t{'山岳' if b == 'mountain' else B[b]}のピリジャーの前哨基地")
open("tsv/v11_ctov_gen.tsv", "w", encoding="utf-8").write("\n".join(out) + "\n")
print(len(out) - 1)
