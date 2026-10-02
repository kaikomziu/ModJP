# naturalist の midnightconfig(動物ごとの定型設定)を生成して tsv/v11_nat_gen.tsv に出す
import json
en = json.load(open('extracted/naturalist.json', encoding='utf-8'))['en_us']
A = {"alligator": "ワニ", "bass": "バス", "bear": "クマ", "bluejay": "アオカケス", "bird": "鳥", "boar": "イノシシ",
     "butterfly": "チョウ", "canary": "カナリア", "cardinal": "ショウジョウコウカンチョウ", "catfish": "ナマズ",
     "coralSnake": "サンゴヘビ", "deer": "シカ", "dragonfly": "トンボ", "duck": "アヒル", "elephant": "ゾウ",
     "finch": "フィンチ", "firefly": "ホタル", "forestFox": "森のキツネ", "forestRabbit": "森のウサギ",
     "giraffe": "キリン", "hippo": "カバ", "lion": "ライオン", "lizard": "トカゲ", "rattlesnake": "ガラガラヘビ",
     "rhino": "サイ", "robin": "コマドリ", "snail": "カタツムリ", "snake": "ヘビ", "sparrow": "スズメ",
     "tortoise": "リクガメ", "vulture": "ハゲワシ", "zebra": "シマウマ"}
P = "naturalist.midnightconfig."
out = {}
for a, j in A.items():
    out[P + a + "Removed"] = "§7%sを削除" % j
    out[P + a + "Removed.tooltip"] = "§8§o[?]§7§o 「Yes」にすると、%sはスポーンしなくなり、既存の%sも削除される。" % (j, j)
    out[P + a + "SpawnWeight"] = "§9%sのスポーンの重み" % j
    out[P + a + "SpawnWeight.tooltip"] = "§8§o[?]§7§o ワールドに%sがスポーンする確率。" % j
    out[P + a + "SpawnMinGroupSize"] = "§7§o%sの最小群れサイズ" % j
    out[P + a + "SpawnMinGroupSize.tooltip"] = "§8§o[?]§7§o 群れでスポーンできる%sの最小数。" % j
    out[P + a + "SpawnMaxGroupSize"] = "§7§o%sの最大群れサイズ" % j
    out[P + a + "SpawnMaxGroupSize.tooltip"] = "§8§o[?]§7§o 群れでスポーンできる%sの最大数。" % j
lines = ["## naturalist"] + [k + "\t" + v for k, v in out.items() if k in en]
open('tsv/v11_nat_gen.tsv', 'w', encoding='utf-8').write("\n".join(lines) + "\n")
print(len(lines) - 1)
