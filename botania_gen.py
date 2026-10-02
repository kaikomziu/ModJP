# botania の植木鉢(potted_*)を公式訳の花の名前から生成して tsv/v11_botania_gen.tsv に出す
import json, os
d = json.load(open('extracted/botania.json', encoding='utf-8'))
en, ja = d['en_us'], dict(d['ja_jp'] or {})
p = 'pack/assets/botania/lang/ja_jp.json'
if os.path.exists(p):
    for k, v in json.load(open(p, encoding='utf-8')).items():
        ja.setdefault(k, v)
out = {}
miss = []
for k in en:
    if k.startswith('block.botania.potted_') and k not in d['ja_jp']:
        base = 'block.botania.' + k[len('block.botania.potted_'):]
        if base in ja:
            out[k] = '鉢植えの' + ja[base]
        else:
            miss.append(k)
lines = ["## botania"] + [k + "\t" + v for k, v in out.items()]
open('tsv/v11_botania_gen.tsv', 'w', encoding='utf-8').write("\n".join(lines) + "\n")
print(len(out), 'miss', miss)
