# evolvedmekanism の溶融金属・道具・盾・鉱石・ソーラー発電機などを生成する
# 素材名は 全公式訳+自前訳 から作った英→日辞書と EXTRA で引く
import json, re, sys, glob, collections
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
SELF = 'batch_tsv_v18_evo_gen.json'
tr = collections.defaultdict(dict)
for p in sorted(Path('tr').glob('*.json')):
    if p.name.startswith('_') or p.name == SELF:
        continue
    data = json.loads(p.read_text(encoding='utf-8'))
    if p.name.startswith('batch_'):
        for ns, d in data.items():
            tr[ns].update(d)
    else:
        tr[p.stem].update(data)
votes = collections.defaultdict(collections.Counter)
ven = json.loads(Path('vanilla/en_us.json').read_text(encoding='utf-8')); vja = json.loads(Path('vanilla/ja_jp.json').read_text(encoding='utf-8'))
for k, v in ven.items():
    if k in vja: votes[v][vja[k]] += 3
for f in glob.glob('extracted/*.json'):
    d = json.loads(Path(f).read_text(encoding='utf-8'))
    for k, v in d['en_us'].items():
        ja = d['ja_jp'].get(k) or tr.get(d['namespace'], {}).get(k)
        if ja and isinstance(v, str): votes[v.strip()][ja.strip()] += 2 if k in d['ja_jp'] else 1
dic = {en: c.most_common(1)[0][0] for en, c in votes.items()}
EXTRA = {'Soul': '魂', 'Queens Slime': 'クイーンスライム', 'Refined Redstone': '精製レッドストーン', 'Flux-Infused': 'フラックス注入',
         'The Ultimate': 'アルティメット', 'Debris': '残骸', 'Blaze': 'ブレイズ', 'Pink Slime': 'ピンクスライム', 'Better Gold': 'より良い金',
         'Electrolyte': '電解質', 'Hellforged': '地獄鍛造', 'Awakened Supremium': '覚醒したスプレミウム', 'Prosperity': 'プロスペリティ',
         'Copper Alloy': '銅合金', 'Infused Iron': '注入された鉄', 'Tainted Gold': '汚れた金',
         'Energetic Alloy': 'エナジェティック合金', 'Vibrant Alloy': 'ヴァイブラント合金', 'Redstone Alloy': 'レッドストーン合金',
         'Conductive Alloy': '導電性合金', 'Pulsating Alloy': 'パルセイティング合金', 'Dark Steel': 'ダークスチール', 'Soularium': 'ソウラリウム',
         'End Steel': 'エンドスチール', 'Cyanite': 'シアナイト',
         'Silicon Bronze': 'シリコンブロンズ', 'Gravitite': 'グラビタイト', 'Juperium': 'ジュペリウム', 'Saturlyte': 'サターライト',
         'Gaiasteel': 'ガイアスチール', 'Ornium': 'オルニウム', 'Lightium': 'ライティウム', 'Tornium': 'トルニウム', 'Ouranium': 'ウラニウム',
         'Oratchalcum': 'オラトカルクム', 'Prismalium': 'プリズマリウム', 'Melodium': 'メロディウム', 'Stellarium': 'ステラリウム',
         'Black Iron': '黒鉄', 'Redstone Ingot': 'レッドストーンインゴット', 'Enhanced Redstone Ingot': '強化レッドストーンインゴット',
         'Ender Ingot': 'エンダーインゴット', 'Enhanced Ender Ingot': '強化エンダーインゴット', 'Crystaltine': 'クリスタルタイン',
         'Chorium': 'コーリウム', 'Sentrite': 'セントライト', 'Skyjade': 'スカイジェード', 'Ambrosium': 'アンブロシウム', 'Zanite': 'ザナイト',
         'Plaslitherite': 'プラスリザライト'}
COL = {'White': '白色', 'Orange': '橙色', 'Magenta': '赤紫色', 'Light Blue': '空色', 'Yellow': '黄色', 'Lime': '黄緑色', 'Pink': '桃色', 'Gray': '灰色',
       'Light Gray': '薄灰色', 'Cyan': '青緑色', 'Purple': '紫色', 'Blue': '青色', 'Brown': '茶色', 'Green': '緑色', 'Red': '赤色', 'Black': '黒色'}
TOOL = {'Axe': '斧', 'Boots': 'ブーツ', 'Chestplate': 'チェストプレート', 'Helmet': 'ヘルメット', 'Hoe': 'クワ', 'Leggings': 'レギンス',
        'Paxel': 'パクセル', 'Pickaxe': 'ツルハシ', 'Shield': '盾', 'Shovel': 'シャベル', 'Sword': '剣'}
STONE = {'Depthrock': 'デプスロック', 'End Stone': 'エンドストーン', 'Holystone': '聖石', 'Netherrack': 'ネザーラック', 'Shiverstone': 'シバーストーン'}
ORE = {'Fluorite': '蛍石', 'Lead': '鉛', 'Osmium': 'オスミウム', 'Tin': 'スズ', 'Uranium': 'ウラン'}
TIER = {'Advanced': '発展', 'Elite': '精鋭', 'Ultimate': '究極', 'Overclocked': '超速', 'Quantum': '量子', 'Dense': '高密', 'Multiversal': '多元',
        'Creative': 'クリエイティブ'}
MOLD = {'Coin': 'コイン', 'Dust': '粉', 'Gear': '歯車', 'Gem': '宝石', 'Nugget': '塊', 'Plate': '板', 'Rod': '棒', 'Block': 'ブロック', 'Wire': 'ワイヤー'}
OTHER = {
    'block.evolvedmekanism.supercharging_element_mk2': '過充電素子 MK2',
    'container.mekanism_extras.absolute_alloying_factory': '絶対合金ファクトリー', 'container.mekanism_extras.supreme_alloying_factory': '至高合金ファクトリー',
    'container.mekanism_extras.cosmic_alloying_factory': '宇宙合金ファクトリー', 'container.mekanism_extras.infinite_alloying_factory': '無限合金ファクトリー',
    'block.evolvedmekanism.thermalizer': '溶解機', 'container.evolvedmekanism.thermalizer': '溶解機',
    'block.evolvedmekanism.solidification_chamber': '固化室', 'container.evolvedmekanism.solidification_chamber': '固化室',
    'item.evolvedmekanism.max_tier_installer': '最大ティアインストーラー', 'item.evolvedmekanism.upgrade_solar': 'ソーラーアップグレード',
    'description.mekanism.thermalizer': 'アイテムを溶かして液体にする機械。', 'description.mekanism.solidification_chamber': '液体を固めてアイテムにする機械。',
    'module.evolvedmekanism.air_affinity_unit': '空中採掘ユニット', 'description.evolvedmekanism.air_affinity_unit': '飛んでいるときの採掘速度の低下をなくす。',
    'module.evolvedmekanism.aoe_unit': '範囲効果ユニット', 'description.evolvedmekanism.aoe_unit': '道具の効果範囲を広げる。',
    'module.evolvedmekanism.aqua_affinity_unit': '水中採掘ユニット', 'description.evolvedmekanism.aqua_affinity_unit': '水中での採掘速度の低下をなくす。',
    'module.evolvedmekanism.bee_shielding_unit': 'ハチ防護ユニット',
    'description.evolvedmekanism.bee_shielding_unit': 'MekaSuitの防具に、ハチを通さない分厚い金属装甲を付ける。',
    'module.evolvedmekanism.capturing_unit': '捕獲ユニット', 'description.evolvedmekanism.capturing_unit': 'モブを倒したとき、確率でスポーンエッグを手に入れられる。',
    'module.evolvedmekanism.luck_unit': '幸運ユニット', 'description.evolvedmekanism.luck_unit': 'より良い戦利品が出る確率を上げる。',
    'module.evolvedmekanism.thermal_shielding_unit': '熱防護ユニット',
    'description.evolvedmekanism.thermal_shielding_unit': 'MekaSuitの防具に、熱を通さない分厚い金属装甲を付ける。',
    'description.evolvedmekanism.max_tier_installer': '対応する機械を%sティアまで直接アップグレードする。',
    'upgrade.mekanism.radioactive': '放射性', 'upgrade.mekanism.radioactive.description': '放射性ガスを入れられるようにする。',
    'upgrade.mekanism.solar': 'ソーラー', 'upgrade.mekanism.solar.description': '発電機の太陽光発電量を増やす。',
    'tooltip.evolvedmekanism.not_consumed': '消費されない'}


def mat(x):
    if x in EXTRA: return EXTRA[x]
    for cand in (x, x + ' Ingot', 'Ingot of ' + x):
        if cand in dic:
            j = re.sub(r'(インゴット|の延べ棒)$', '', dic[cand]).rstrip('の')
            return None if re.search(r'[A-Za-z]', j) else j
    return None


SUN = re.compile(r"An? (advanced|elite|ultimate|overclocked|quantum|dense|multiversal|creative) generator that directly absorbs "
                 r"the sun's rays with little loss to produce energy\.")
d = json.loads(Path('extracted/evolvedmekanism.json').read_text(encoding='utf-8'))
out, miss = ['## evolvedmekanism'], []
for k, v in d['missing'].items():
    if k in tr.get('evolvedmekanism', {}):
        continue
    t = OTHER.get(k)
    m = re.fullmatch(r'Molten (.+?)( Bucket)?', v)
    if not t and m and (j := mat(m.group(1))):
        t = f'溶融した{j}' + ('入りバケツ' if m.group(2) else '')
    m = re.fullmatch(r'(?:(.+) )?(Better Gold|Plaslitherite|Refined Redstone) (Axe|Boots|Chestplate|Helmet|Hoe|Leggings|Paxel|Pickaxe|Shield|Shovel|Sword)', v)
    if not t and m and (m.group(1) is None or m.group(1) in COL):
        t = (COL[m.group(1)] + 'の' if m.group(1) else '') + mat(m.group(2)) + 'の' + TOOL[m.group(3)]
    m = re.fullmatch(r'(Depthrock|End Stone|Holystone|Netherrack|Shiverstone) (Fluorite|Lead|Osmium|Tin|Uranium) Ore', v)
    if not t and m:
        t = STONE[m.group(1)] + 'の' + ORE[m.group(2)] + '鉱石'
    m = re.fullmatch(r'(Advanced|Elite|Ultimate|Overclocked|Quantum|Dense|Multiversal|Creative) Solar (Generator|Panel)', v)
    if not t and m:
        t = TIER[m.group(1)] + ('太陽光発電機' if m.group(2) == 'Generator' else 'ソーラーパネル')
    m = SUN.fullmatch(v)
    if not t and m:
        t = '太陽の光を少ない損失で直接吸収してエネルギーを作る、' + TIER[m.group(1).capitalize()] + 'の発電機。'
    m = re.fullmatch(r'(Coin|Dust|Gear|Gem|Nugget|Plate|Rod|Block|Wire) Mold', v)
    if not t and m:
        t = MOLD[m.group(1)] + 'の型'
    (out.append(f'{k}\t{t}') if t else miss.append(f'{k}\t{v}'))
Path('tsv/v18_evo_gen.tsv').write_text('\n'.join(out) + '\n', encoding='utf-8')
print(len(out) - 1)
Path(r'C:\Users\4yoma\AppData\Local\Temp\claude\C--Users-4yoma-curseforge-minecraft-Instances-------2-\41914c65-dffe-46d4-93ae-d955dbb413b6\scratchpad\evo_miss.txt').write_text('\n'.join(miss), encoding='utf-8')
print('miss', len(miss))
