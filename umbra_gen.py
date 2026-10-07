# umbra_poor_ores の「Small/Tiny/Poor ○○」を生成し、残りは手訳を足して tsv/v18_umbra.tsv に書く
import json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
M = {'Aluminium': 'アルミニウム', 'Andesite': '安山岩', 'Apatite': '燐灰石', 'Blackstone': 'ブラックストーン', 'Cinnabar': '辰砂', 'Clay': '粘土',
     'Coal': '石炭', 'Copper': '銅', 'Diamond': 'ダイヤモンド', 'Dirt': '土', 'Emerald': 'エメラルド', 'Fluorite': '蛍石', 'Gold': '金',
     'Gravel': '砂利', 'Iron': '鉄', 'Lapis Lazuli': 'ラピスラズリ', 'Lava': '溶岩', 'Lead': '鉛', 'Nether Quartz': 'ネザークォーツ',
     'Netherite': 'ネザライト', 'Netherrack': 'ネザーラック', 'Nickel': 'ニッケル', 'Niter': '硝石', 'Oil': '石油', 'Oil Sand': 'オイルサンド',
     'Osmium': 'オスミウム', 'Poorium': 'プアリウム', 'Quartz': 'クォーツ', 'Red Sand': '赤い砂', 'Redstone': 'レッドストーン', 'Ruby': 'ルビー',
     'Salt': '塩', 'Sand': '砂', 'Sapphire': 'サファイア', 'Silver': '銀', 'Soul Sand': 'ソウルサンド', 'Stone': '石', 'Sulfur': '硫黄',
     'Tin': 'スズ', 'Uranium': 'ウラン', 'Water': '水', 'Zinc': '亜鉛', 'Phytorium': 'フィトリウム'}
GEN = {'Ore': '鉱石', 'Nether Ore': 'ネザー鉱石', 'Soil': '土壌', 'Stone': '石'}
MANUAL = {
    'advancements.ore_tier_2.descr': 'もっと役に立つが、まだ遅い', 'advancements.ore_tier_1.title': '鉱石 ティア1',
    'advancements.first_steps.title': '最初の一歩', 'advancements.wait.descr': 'ちょっと待って、あれは何？いったい何を作ったの？',
    'advancements.stone_tier_2.descr': 'たぶんそれほど役に立たない',
    'advancements.nether_tier_1.descr': 'ネザーの生成機を手に入れた。もうネザーに行く必要すらない。 ',
    'advancements.hidden_in_the_generator.title': '生成機に隠されたもの', 'advancements.ore_tier_3.title': '鉱石 ティア3',
    'advancements.soil_tier_2.title': '土壌 ティア2', 'advancements.wait.title': '待って…', 'advancements.soil_tier_2.descr': '採掘者のアップグレード',
    'block.umbra_poor_ores.poor_nether_ore_generator_tier_1.description_0': '生成: 乏しいネザーラック、ソウルサンド、ブラックストーン、クォーツ、金',
    'block.umbra_poor_ores.poor_ore_generator_tier_1.description_0': '生成: 乏しい石炭、乏しい銅、乏しい鉄',
    'block.umbra_poor_ores.poor_nether_ore_generator_tier_2.description_0': '生成: 乏しいネザーラック、ソウルサンド、ブラックストーン、クォーツ、金',
    'advancements.soil_tier_1.title': '土壌 ティア1', 'advancements.ore_tier_2.title': '鉱石 ティア2', 'advancements.ore_tier_3.descr': 'これぞ本物',
    'advancements.stone_tier_2.title': '石 ティア2',
    'block.umbra_poor_ores.poor_ore_generator_tier_3.description_0': '生成: 乏しい石炭、銅、鉄、金、レッドストーン、ラピスラズリ、ダイヤモンド、エメラルド。',
    'advancements.first_steps.descr': 'ここから乏しい鉱石の旅が始まる。この苦しい時代に生成機を手に入れよう',
    'item.umbra_poor_ores.flint_chip': '火打石のかけら', 'advancements.soil_tier_1.descr': 'やっとまともな食べ物', 'advancements.ore_tier_1.descr': '遅いガラクタ',
    'advancements.nether_tier_2.title': 'ネザー ティア2', 'item.umbra_poor_ores.big_poorium': '大きなプアリウム',
    'block.umbra_poor_ores.poor_soil_generator_tier_2.description_0': '生成: 乏しい土', 'advancements.going_up.descr': '小さなプアリウムを手に入れた',
    'advancements.going_up.title': '上へ', 'block.umbra_poor_ores.poor_soil_generator_tier_2.description_5': '赤い砂と溶岩',
    'advancements.nether_tier_2.descr': 'ネザーの生成機 ティア2を手に入れた。今度はイトも出る', 'advancements.truly_poor.title': '本当に乏しい',
    'advancements.truly_poor.descr': 'プアリウムを1つ手に入れた。本当に乏しいね', 'advancements.hidden_in_the_generator.descr': 'ネザーのイト',
    'advancements.nether_tier_1.title': 'ネザー ティア1', 'item.umbra_poor_ores.phytorium': 'フィトリウム',
    'itemGroup.tabpoor_ores': 'Poor Ores', 'item_group.umbra_poor_ores.poor_ores': 'Poor Ores',
    'block.umbra_poor_ores.poor_soil_generator_tier_2.description_1': '砂利', 'block.umbra_poor_ores.poor_soil_generator_tier_2.description_2': '砂',
    'block.umbra_poor_ores.poor_soil_generator_tier_2.description_3': '粘土', 'block.umbra_poor_ores.poor_soil_generator_tier_2.description_4': '水'}
d = json.loads(Path('extracted/umbra_poor_ores.json').read_text(encoding='utf-8'))
out, miss = ['## umbra_poor_ores'], []
MR = '|'.join(sorted(map(re.escape, M), key=len, reverse=True))
for k, v in d['missing'].items():
    t = MANUAL.get(k)
    if not t:
        m = re.fullmatch(rf'(Small|Tiny|Poor) ({MR})( Ore)?', v)
        g = re.fullmatch(r'Poor (Ore|Nether Ore|Soil|Stone) Generator(?: Tier (\d))?', v)
        if m:
            t = {'Small': '小さな', 'Tiny': 'ちっぽけな', 'Poor': '乏しい'}[m.group(1)] + M[m.group(2)] + ('鉱石' if m.group(3) else '')
        elif g:
            t = f'乏しい{GEN[g.group(1)]}の生成機' + (f' ティア{g.group(2)}' if g.group(2) else '')
        elif re.fullmatch(r'Poor .+ Generator Tier \d', v):
            pass
    (out.append(f'{k}\t{t}') if t else miss.append(f'{k}\t{v}'))
Path('tsv/v18_umbra.tsv').write_text('\n'.join(out) + '\n', encoding='utf-8')
print(len(out) - 1, 'miss', miss)
