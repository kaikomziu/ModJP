# v1.8: Mekanism系アドオンの定型名(素材×武器など)を生成
from pathlib import Path
W = {'longsword': '太刀', 'twinblade': '双刃', 'rapier': 'レイピア', 'katana': '刀', 'sai': '釵', 'spear': '槍', 'glaive': '薙刀',
     'warglaive': 'ウォーグレイブ', 'cutlass': 'カトラス', 'claymore': '大剣', 'greataxe': '大斧', 'greathammer': '大鎚',
     'chakram': 'チャクラム', 'scythe': '大鎌', 'halberd': 'ハルバード'}
M = {'lapis_lazuli': 'ラピスラズリ', 'refined_glowstone': '精製グロウストーン', 'refined_obsidian': '精製黒曜石'}
out = ['## mek_integrated_simply_swords']
for m, mj in M.items():
    for w, wj in W.items():
        out.append(f'item.mek_integrated_simply_swords.{m}_{w}\t{mj}の{wj}')
out.append('item.mek_integrated_simply_swords.bronze_scythe\t青銅の大鎌')
out.append('item.mek_integrated_simply_swords.steel_scythe\t鋼の大鎌')
out.append('mod.mek_integrated_simply_swords.description\tMekanism Toolsの素材でSimply Swordsの武器を追加する。')
# autcraftmekanism: 精製素材×道具/防具
AM = {'real_dark': '真の闇', 'eternal_blood': '永遠の血', 'wave_breaker': '波砕き', 'sigia': 'シギア', 'eclipse': 'エクリプス', 'iridium': 'イリジウム'}
AT = {'sword': '剣', 'pickaxe': 'ツルハシ', 'axe': '斧', 'shovel': 'シャベル', 'hoe': 'クワ', 'armor_helmet': 'ヘルメット',
      'armor_chestplate': 'チェストプレート', 'armor_leggings': 'レギンス', 'armor_boots': 'ブーツ'}
out.append('## autcraftmekanism')
for m, mj in AM.items():
    for t, tj in AT.items():
        out.append(f'item.autcraftmekanism.refined_{m}_{t}\t精製{mj}の{tj}')
    out.append(f'item.autcraftmekanism.refined_{m}_ingot\t精製{mj}')
    out.append(f'block.autcraftmekanism.refined_{m}_block\t精製{mj}のブロック')
for k, v in {'real_dark_dust': '真の闇の粉', 'eternal_bood_dust': '永遠の血の粉', 'wave_breaker_dust': '波砕きの粉', 'sigia_dust': 'シギアの粉',
             'eclipse_dust': 'エクリプスの粉', 'enriched_plutonium': '濃縮プルトニウム', 'enriched_sulfur': '濃縮硫黄'}.items():
    out.append(f'item.autcraftmekanism.{k}\t{v}')
out.append('item_group.autcraftmekanism.aucraft_mekanism\tAucraft: Mekanism Compatibility')
# tfcorewashing: TFCの鉱物×洗鉱の段階(用語はTFCの公式訳)
OR = {'cassiterite': '錫石', 'galena': '方鉛鉱', 'tetrahedrite': '四面銅鉱', 'bauxite': 'ボーキサイト', 'gold': '自然金', 'chromite': 'クロム鉄鉱',
      'sphalerite': '閃亜鉛鉱', 'graphite': '黒鉛', 'bismuthinite': '輝蒼鉛鉱', 'uraninite': '閃ウラン鉱', 'magnetite': '磁鉄鉱',
      'cinnabar': '辰砂', 'garnierite': '珪ニッケル鉱', 'malachite': '孔雀石', 'sulfur': '硫黄', 'silver': '自然銀', 'limonite': '褐鉄鉱',
      'hematite': '赤鉄鉱', 'cryolite': '氷晶石', 'copper': '自然銅', 'chromium': 'クロム'}
ST = {'dirty_pile': '汚れた{}の山', 'briquet': '{}のブリケット', 'pellet': '{}のペレット', 'rocky_chunks': '岩混じりの{}の塊',
      'dirty_dust': '汚れた{}の粉', 'chunks': '{}の塊'}
SAND = {'black': '黒い', 'red': '赤い', 'white': '白い', 'brown': '茶色い', 'pink': '桃色の', 'yellow': '黄色い', 'green': '緑の'}
out.append('## tfcorewashing')
for s, t in ST.items():
    for o, oj in OR.items():
        out.append(f'item.tfcorewashing.{s}_{o}\t' + t.format(oj))
for c, cj in SAND.items():
    out.append(f'item.tfcorewashing.pile_{c}_sand\t{cj}砂の山')
out.append('item.tfcorewashing.rock_powder\t岩の粉')
out.append('item.tfcorewashing.chromium_powder\tクロムの粉')
# shippy_ships: 木材×船の種類
WD = {'oak': 'オーク', 'birch': 'シラカバ', 'spruce': 'トウヒ', 'jungle': 'ジャングル', 'dark_oak': 'ダークオーク', 'pale_oak': 'ペールオーク',
      'acacia': 'アカシア', 'cherry': 'サクラ', 'mangrove': 'マングローブ', 'bamboo': '竹'}
SH = {'sailboat': '帆船', 'cog': 'コグ船', 'caravel': 'キャラベル船'}
out.append('## shippy_ships')
for w, wj in WD.items():
    out.append(f'info.shippy_ships.wood.{w}\t{wj}')
    for s, sj in SH.items():
        out.append(f'entity.shippy_ships.{w}_{s}\t{wj}の{sj}')
SP = {'base': '基本', 'brick': 'レンガ', 'checker': '市松', 'circle': '円', 'creeper': 'クリーパー', 'cross': '斜め十字', 'straight_cross': '十字',
      'flow': 'フロー', 'flower': '花', 'globe': '地球', 'guster': 'ガスター', 'large_checker': '大きな市松', 'large_stripes': '太い縞',
      'mojang': 'Mojang', 'piglin': 'ピグリン', 'rhombus': 'ひし形', 'skull': 'ドクロ', 'stripes': '縞', 'vanilla_stripes': 'バニラの縞'}
for p, pj in SP.items():
    out.append(f'item.shippy_ships.{p}_sail_pattern\t{pj}の帆の模様')
for b, bj in {'ship': '帆船', 'cog': 'コグ船', 'caravel': 'キャラベル船'}.items():
    n = 'sailboat' if b == 'ship' else b
    out += [f'info.shippy_ships.{b}_builder.add_logs\t原木を加える。 ', f'info.shippy_ships.{b}_builder.add_planks\t板材を加える。 ',
            f'info.shippy_ships.{b}_builder.add_iron_nuggets\t鉄塊を加える。 ', f'info.shippy_ships.{b}_builder.add_wool\t羊毛を加える。 ',
            f'info.shippy_ships.{b}_builder.add_wax\t蝋か樹脂を塗る。 ', f'info.shippy_ships.{b}_builder.choose_log\t原木を選んで建造を始めよう！',
            f'info.shippy_ships.{b}_builder.building\t%1$sの{bj}を建造中！ %2$s 進行: %3$d',
            f'info.shippy_ships.{b}_builder.wood_set\t木材: %1$s', f'info.shippy_ships.{b}_builder.wrong_wood\t%1$sの素材を使ってください',
            f'info.shippy_ships.{b}_builder.progress\t進行: %1$d / %2$d', f'info.shippy_ships.{b}_builder.step_complete\t工程完了！次: %1$s',
            f'info.shippy_ships.{b}_builder.ship_ready\t船が完成した！', f'info.shippy_ships.{b}_builder.destroyed\t{bj}が壊れた！最初からやり直し。',
            f'info.shippy_ships.{b}_builder.error\tアイテムか工程が違う！ %1$s']
out += ['block.shippy_ships.ship_builder\t帆船の建造台', 'block.shippy_ships.cog_builder\tコグ船の建造台', 'block.shippy_ships.caravel_builder\tキャラベル船の建造台',
        'block.shippy_ships.ship_builder_deco\t飾りの船の建造台', 'key.categories.shippyships\tShippy Ships', 'key.shippy_ships.zoom_in\t船のズームイン',
        'key.shippy_ships.zoom_out\t船のズームアウト', 'key.shippy_ships.eject_passengers\t乗客を全員降ろす', 'key.shippy_ships.isPressingCtrl\tすばやく建造(スタックを使う)',
        'info.shippy_ships.no_free_mount\t装備スロットに空きがない']
# 実際に未訳のキーだけ残す(生成した組み合わせの一部は存在しない)
import json
ns, keep = None, []
for line in out:
    if line.startswith('## '):
        ns = line[3:]
        miss = json.loads(Path(f'extracted/{ns}.json').read_text(encoding='utf-8'))['missing']
        keep.append(line)
    elif line.split('\t', 1)[0] in miss:
        keep.append(line)
out = keep
Path('tsv/v18_gen.tsv').write_text('\n'.join(out) + '\n', encoding='utf-8')
print(len(out) - 1)
