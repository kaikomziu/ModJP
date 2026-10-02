N = {"monastery":"修道院","illager_campsite":"イリジャーの野営地","illager_castle":"イリジャーの城","illager_hall":"イリジャーの館",
"illager_fort":"イリジャーの砦","abandoned_temple":"放棄された神殿","lighthouse":"灯台","mushroom_mines":"キノコの鉱山",
"mushroom_village":"キノコの村","coliseum":"闘技場","fishing_hut":"釣り小屋","small_prairie_house":"草原の小さな家",
"wishing_well":"願いの井戸","merchant_campsite":"商人の野営地","infested_temple":"虫食いの神殿","heavenly_rider":"天空の騎兵",
"mining_system":"採掘施設","heavenly_conqueror":"天空の征服者","scorched_mines":"焦げた鉱山","undead_pirate_ship":"アンデッドの海賊船",
"foundry":"鋳造所","small_blimp":"小型飛行船","bandit_village":"山賊の村","typhon":"テュポーン","ceryneian_hind":"ケリュネイアの鹿",
"heavenly_challenger":"天空の挑戦者","illager_corsair":"イリジャーの私掠船","illager_galley":"イリジャーのガレー船",
"mushroom_house":"キノコの家","aviary":"鳥小屋","bandit_towers":"山賊の塔","giant_mushroom":"巨大キノコ",
"illager_windmill":"イリジャーの風車","plague_asylum":"疫病の療養所","shiraz_palace":"シーラーズ宮殿",
"thornborn_towers":"ソーンボーンの塔","keep_kayra":"カイラ城","greenwood_pub":"グリーンウッドの酒場","bathhouse":"浴場",
"mechanical_nest":"機械の巣"}
TITLE = {"wda_root":"When Dungeons Arise","find_abandoned_temple":"言葉を失って","find_aviary":"3羽の小鳥",
"find_bandit_towers":"ラスベガスで起きたことは…","find_bandit_village":"錆びた根","find_ceryneian_hind":"誰がこいつを殺した？",
"find_coliseum":"何世紀も覚えていて","find_fishing_hut":"暗闇で釣りを","find_foundry":"鉄の処女","find_giant_mushroom":"神秘",
"find_heavenly_challenger":"帝国のマーチ","find_heavenly_conqueror":"空の幽霊騎兵","find_heavenly_rider":"ワルキューレの騎行",
"find_illager_campsite":"まぼろしの世界","find_illager_corsair_or_illager_galley":"君は海賊だ","find_illager_fort":"荒くれ話",
"find_illager_windmill":"見張り塔からずっと","find_infested_temple":"スーパークリープス","find_infested_temple_map":"路上",
"find_lighthouse":"ライトハウス","find_merchant_campsite":"レッツ・グルーヴ","find_mining_system":"ストーン・フリー",
"find_monasteries":"クワイエット・プレイス","find_mushroom_house":"庭の壁を越えて","find_mushroom_mines":"みんなで持ち上げよう",
"find_mushroom_village":"スウィート・ドリームス","find_plague_asylum":"恋愛サーキュレーション","find_scorched_mines":"冥府下り",
"find_shiraz_palace":"エンター・サンドマン","find_small_blimp":"スカイ・ハイ","find_small_prairie_house":"グッド・プレイス",
"find_thornborn_towers":"ガンズ・アンド・ローゼズ","find_typhon":"ジョーズ","find_undead_pirate_ship":"スモーク・オン・ザ・ウォーター",
"find_wishing_well":"ジャンプ","find_keep_kayra":"遠い夢想家","find_greenwood_pub":"サージェント・ペパーズ・ロンリー・ハーツ・クラブ",
"find_bathhouse":"呪い","find_mechanical_nest":"ようこそマシーンへ"}
out = ["## dungeons_arise", "advancement.dungeons_arise.wda_root.desc\t勇敢なる新世界にダンジョンが立ち上がる",
"advancement.dungeons_arise.find_infested_temple_map.desc\t虫食いの神殿の探検家の地図を見つける",
"advancement.dungeons_arise.find_lighthouse.desc\t灯台にたどり着く",
"advancement.dungeons_arise.find_illager_corsair_or_illager_galley.desc\tイリジャーの私掠船かイリジャーのガレー船を見つける",
"advancement.dungeons_arise.find_thornborn_towers.desc\tソーンボーンの塔を訪れる",
"advancement.dungeons_arise.find_monasteries.desc\t修道院を見つける",
"advancement.dungeons_arise.find_mushroom_mines.desc\tキノコの鉱山を見つける"]
done = {l.split("\t")[0] for l in out[1:]}
miss = []
for line in open("cur_dungeons_arise.txt", encoding="utf-8"):
    k = line.split("\t")[0]
    if k in done: continue
    if k.startswith("filled_map.dungeons_arise:"):
        n = k.split(":")[1]
        out.append(f"{k}\t{N[n]}の探検家の地図"); continue
    if k.startswith("advancement.dungeons_arise."):
        a, _, f = k[len("advancement.dungeons_arise."):].rpartition(".")
        if f == "title" and a in TITLE:
            out.append(f"{k}\t{TITLE[a]}"); continue
        if f == "desc" and a.startswith("find_") and a[5:] in N:
            out.append(f"{k}\t{N[a[5:]]}を見つける"); continue
    miss.append(line.rstrip())
open("tsv/v11_da_gen.tsv", "w", encoding="utf-8").write("\n".join(out) + "\n")
print(len(out) - 1, miss)
