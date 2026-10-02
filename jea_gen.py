# jearchaeology のブラシ対象構造物名を生成
import re, sys
sys.stdout.reconfigure(encoding='utf-8')
N = {'lush_den':'緑豊かな巣穴','sandy_den':'砂の巣穴','sunscorched_den':'日に焼けた巣穴','enhydro_agate':'水入り瑪瑙','eroded_pillar':'侵食された柱',
 'frozen_spike':'凍ったとげ','powdered_deposit':'粉の堆積','preserved_skeleton':'保存された骨格','submerged_impact':'水没した衝突跡',
 'submerged_spike':'水没したとげ','sunscorched_remains':'日に焼けた遺骸','suspicious_mound':'怪しい塚','underwater_fissure':'水中の裂け目',
 'mud_pit':'泥の穴','rooted_pit':'根の張った穴','dripstone_oasis':'鍾乳石のオアシス','frozen_pond':'凍った池','mossy_pond':'苔むした池',
 'birch_tree':'シラカバの木','oak_tree':'オークの木','spruce_tree':'トウヒの木','hydrothermal_vents':'熱水噴出孔','vibrant_hydrothermal_vents':'色鮮やかな熱水噴出孔',
 'deserted_tower_ruins':'砂漠の塔の遺跡','deserted_gimmi_tower':'砂漠のギミの塔','lush_gimmi_tower':'緑豊かなギミの塔','rooted_gimmi_tower':'根の張ったギミの塔',
 'sunscorched_gimmi_tower':'日に焼けたギミの塔','temperate_gimmi_tower':'温帯のギミの塔','frozen_gimmi_tower':'凍ったギミの塔',
 'stonjourner_henge_ruins':'ストーンジョーナーの環状列石の遺跡','sol_henge_ruins':'太陽の環状列石の遺跡','luna_henge_ruins':'月の環状列石の遺跡',
 'crumbling_arch_ruins':'崩れかけたアーチの遺跡','rooted_arch_ruins':'根の張ったアーチの遺跡','decaying_crypt_ruins':'朽ちた地下墓所の遺跡',
 'deserted_house_ruins':'砂漠の家の遺跡','deserted_town_center_ruins':'砂漠の町の中心の遺跡','fallen_statue_ruins':'倒れた像の遺跡',
 'hidden_bunker_ruins':'隠れた掩蔽壕の遺跡','mossy_oubliette_ruins':'苔むした地下牢の遺跡','toppled_pillars_ruins':'倒れた柱の遺跡',
 'unstable_cave_ruins':'不安定な洞窟の遺跡','archaeological_site':'発掘現場','wishing_weald':'願いの森','observatory':'天文台'}
R = {'common':' [C]','uncommon':' [UC]','rare':' [R]'}
out = ['## jearchaeology']
for line in open('cur_jearchaeology.txt', encoding='utf-8'):
    k, v = line.rstrip('\n').split('\t', 1)
    m = re.fullmatch(r'jearchaeology\.brush\.structure\.(prehistoric_)?(\w+?)(?:_(common|uncommon|rare)(?:_\w+)?)?', k)
    if m and m.group(2) in N:
        out.append(k + '\t' + ('先史時代の' if m.group(1) else '') + N[m.group(2)] + (R[m.group(3)] if m.group(3) else ''))
    else:
        print('miss', k)
open('tsv/v14_jea_gen.tsv', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(len(out) - 1)
