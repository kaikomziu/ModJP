# cp_lib(Croparium)の種・作物・耕地などを生成し、残りは手訳と合わせて tsv/v18_cp.tsv に書く
import json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
M = {'Amethyst': 'アメジスト', 'Amythest': 'アメジスト', 'Blaze Rod': 'ブレイズロッド', 'Dragon Breath': 'ドラゴンブレス', 'Breeze Rod': 'ブリーズロッド',
     'Clay': '粘土', 'Coal': '石炭', 'Copper': '銅', 'Diamond': 'ダイヤモンド', 'Dripstone': '鍾乳石', 'Emerald': 'エメラルド',
     'Ender Pearl': 'エンダーパール', 'Flint': '火打石', 'Ghast Tear': 'ガストの涙', 'Glowstone Dust': 'グロウストーンダスト',
     'Glowstone': 'グロウストーン', 'Gold': '金', 'Gunpowder': '火薬', 'Honey': 'ハチミツ', 'Honeycomb': 'ハニカム', 'Iron': '鉄',
     'Lapis': 'ラピスラズリ', 'Magma Cream': 'マグマクリーム', 'Nautilus Shell': 'オウムガイの殻', 'Phantom Membrane': 'ファントムの皮膜',
     'Prismarine Crystal': 'プリズマリンクリスタル', 'Prismarine Crystals': 'プリズマリンクリスタル', 'Prismarine Shard': 'プリズマリンの欠片',
     'Qa Rosegold': 'Qaローズゴールド', 'Qarium': 'カリウム', 'Quartz': 'クォーツ', 'Redstone': 'レッドストーン', 'Shulker Shell': 'シュルカーの殻',
     'Slimeball': 'スライムボール', 'Turtle Scute': 'カメのウロコ', 'Armadillo Scute': 'アルマジロのウロコ', 'Echo Shard': '残響の欠片',
     'Leather': '革', 'Ink Sac': 'イカスミ', 'Glow Ink Sac': '輝くイカスミ', 'Ancient Debris': '古代の残骸', 'Sponge': 'スポンジ',
     'Sea Heart': '海洋の心', 'Obsidian': '黒曜石', 'Crying Obsidian': '泣く黒曜石', 'Everrose': '常咲きのバラ'}
F = {'Deepslate': '深層岩', 'Cobblestone': '丸石', 'Granite': '花崗岩', 'Andesite': '安山岩', 'Diorite': '閃緑岩', 'Basalt': '玄武岩',
     'Blackstone': 'ブラックストーン', 'End Stone': 'エンドストーン', 'Honeycomb Block': 'ハニカムブロック', 'Obsidian': '黒曜石',
     'Crying Obsidian': '泣く黒曜石', 'Deadrock': 'デッドロック', 'Soul Sand': 'ソウルサンド', 'Crawling': '這いずり石', 'Soul Soil': 'ソウルソイル',
     'Holystone': '聖石', 'Prismarine': 'プリズマリン', 'Dark Prismarine': 'ダークプリズマリン', 'Dripstone': '鍾乳石', 'Tuff': '凝灰岩'}
E = {'Overworld': 'オーバーワールド', 'Nether': 'ネザー', 'End': 'エンド', 'Sweet': '甘味', 'Tough': '強靭', 'Biomass': 'バイオマス', 'Aether': 'エーテル', 'Marine': '海洋'}
MAN = {
    'item_group.cp_lib.croparium': 'Croparium', 'itemGroup.cp_lib.croparium': 'Croparium', 'item.cp_lib.croparium_logo': 'Cropariumのロゴ',
    'block.cp_lib.tile_stonecutter': 'アルファ石切台', 'item.cp_lib.tile_stonecutter': 'アルファ石切台',
    'block.cp_lib.reactor_core': 'リアクターコア', 'item.cp_lib.reactor_core': 'リアクターコア',
    'block.cp_lib.reinforced_reactor_core': '強化リアクターコア', 'item.cp_lib.reinforced_reactor_core': '強化リアクターコア',
    'fluid_type.cp_lib.excessively_sweet_water': '甘すぎる水', 'block.cp_lib.excessively_sweet_water': '甘すぎる水',
    'fluid.cp_lib.excessively_sweet_water': '甘すぎる水', 'item.cp_lib.excessively_sweet_water_bucket': '甘すぎる水入りバケツ',
    'item.cp_lib.honey_cream': 'ハチミツクリーム', 'block.cp_lib.rotten_flesh_block': '腐った肉のブロック', 'item.cp_lib.rotten_flesh_block': '腐った肉のブロック',
    'item.cp_lib.condensed_dragon_breath': '凝縮したドラゴンブレス', 'block.cp_lib.fermented_biomass_block': '発酵したバイオマスのブロック',
    'item.cp_lib.fermented_biomass_block': '発酵したバイオマスのブロック',
    'advancements.not_enough_minerals.descr': 'クラシック石切台で原材料を累計50個取り出す。', 'advancements.not_enough_minerals.title': 'ミネラル不足',
    'advancements.early_alpha.title': '初期のポケット', 'advancements.early_alpha.descr': 'クラシック石切台とリアクターコアを手に入れる。',
    'advancements.reactor_core_engineer.title': 'リアクターコア技師', 'advancements.reactor_core_engineer.descr': 'リアクターコアの土台をレベル4に上げる。',
    'item.cp_lib.blank_reactor_module': '空のリアクターモジュール', 'item.cp_lib.autosmelting_reactor_module': '自動精錬リアクターモジュール',
    'item.cp_lib.xp_reactor_module': '経験値リアクターモジュール', 'item.cp_lib.autogather_reactor_module': '自動回収リアクターモジュール',
    'item.cp_lib.fortune_reactor_module': '幸運リアクターモジュール', 'item.cp_lib.agriculture_reactor_module': '農業リアクターモジュール',
    'advancements.no_need_dig.descr': '鉱石は自然に育つ。', 'advancements.no_need_dig.title': '千回掘る必要はない',
    'advancements.master_of_shard_extraction.descr': 'バニラのマインクラフトで手に入る胚の欠片をすべて手に入れる。',
    'advancements.master_of_shard_extraction.title': '欠片抽出の達人',
    'advancements.ore_seed_collector.descr': 'バニラのマインクラフトの鉱石の鉱物の種をすべて集める。', 'advancements.ore_seed_collector.title': '鉱物の種コレクター',
    'advancements.control_core.descr': '空のリアクターモジュールを手に入れる。', 'advancements.control_core.title': '制御コア',
    'advancements.no_more_hunger.descr': '農業リアクターモジュールを手に入れる。苗は木陰を作り、黄金の穂は穀倉を満たす——かつては生きるための絶え間ない営みだったそれは、生涯土を耕し続けた誠実さを宿している。',
    'advancements.no_more_hunger.title': 'もう飢えない', 'gui.cp_lib.stonecutter_gui.button_extract': '取り出す',
    'item.cp_lib.sponge_chunk': 'スポンジの塊', 'item.cp_lib.wet_sponge_chunk': '濡れたスポンジの塊', 'item.cp_lib.dragon_breath_bucket': 'ドラゴンブレス入りバケツ',
    'info.cp_lib.merge_successful': '変更に成功した', 'info.cp_lib.merge_failed': '変更に失敗した',
    'item.cp_lib.obsidian_shards': '黒曜石の欠片', 'item.cp_lib.crying_obsidian_shards': '泣く黒曜石の欠片',
    'info.cp_lib.growth_condition_biomass': 'バイオマス資源の耕地に植える', 'info.cp_lib.growth_condition_overworld': 'オーバーワールド鉱物の耕地に植える',
    'info.cp_lib.growth_condition_nether': 'ネザー鉱物の耕地に植える', 'info.cp_lib.growth_condition_marine': '海洋資源の耕地に植える',
    'info.cp_lib.growth_condition_sweet': '甘味資源の耕地に植える', 'info.cp_lib.growth_condition_tough': '強靭資源の耕地に植える',
    'info.cp_lib.growth_condition_end': 'エンダー資源の耕地に植える',
    'cp_lib.configuration.reactorcoreconsumemoduledurability': 'リアクターコアがモジュールの耐久値を消費する',
    'cp_lib.configuration.reactorcoreverticalrangemultiplier': 'リアクターコアの縦の範囲の倍率', 'cp_lib.configuration.farmland_settings': '耕地の設定',
    'cp_lib.configuration.shardextractsuccessrate': '欠片の抽出成功率', 'cp_lib.configuration.enablerightclickharvestcrops': '右クリックでの作物の収穫を有効にする',
    'cp_lib.configuration.customagriculturalcrop': '独自の農作物', 'cp_lib.configuration.cropgrowthspeedfactor': '作物の成長速度の係数',
    'cp_lib.configuration.shardripencrops': '欠片で作物を熟させる', 'cp_lib.configuration.fireaspectharvestsmeltdrop': '火属性で収穫するとドロップを精錬',
    'cp_lib.configuration.reactorcoreruntimecycle': 'リアクターコアの動作周期', 'cp_lib.configuration.alphastonecutterusinginterface': 'アルファ石切台で画面を使う',
    'cp_lib.configuration.reactor_core_settings': 'リアクターコアの設定', 'cp_lib.configuration.entityhurtonlavafarmland': '溶岩の耕地でエンティティがダメージを受ける',
    'cp_lib.configuration.entityburntimeonlavafarmland': '溶岩の耕地でエンティティが燃える時間', 'cp_lib.configuration.enablereactorcore': 'リアクターコアを有効にする',
    'cp_lib.configuration.misc_settings': 'その他の設定', 'cp_lib.configuration.crop_settings': '作物の設定',
    'cp_lib.configuration.rightclickharvestbasedropcount': '右クリック収穫の基本ドロップ数',
    'cp_lib.configuration.reactorcorehorizontalrangemultiplier': 'リアクターコアの横の範囲の倍率',
    'cp_lib.configuration.resetmappingtableonworldjoin': 'ワールド参加時に対応表をリセット',
    'cp_lib.configuration.breakmaturecropbasedropcount': '育った作物を壊したときの基本ドロップ数',
    'fluid.cp_lib.dragon_breath': 'ドラゴンブレス', 'fluid_type.cp_lib.dragon_breath': 'ドラゴンブレス', 'block.cp_lib.dragon_breath': 'ドラゴンブレス'}
d = json.loads(Path('extracted/cp_lib.json').read_text(encoding='utf-8'))
MR = '|'.join(sorted(map(re.escape, M), key=len, reverse=True))
FR = '|'.join(sorted(map(re.escape, F), key=len, reverse=True))
ER = '|'.join(map(re.escape, E))
out, miss = ['## cp_lib'], []
for k, v in d['missing'].items():
    t = MAN.get(k)
    if not t:
        for pat, fn in [(rf'({MR}) Seeds', lambda m: M[m.group(1)] + 'の種'), (rf'Seed of ({MR})', lambda m: M[m.group(1)] + 'の種'),
                        (rf'({MR}) Crop', lambda m: M[m.group(1)] + 'の作物'), (rf'({FR}) Farmland', lambda m: F[m.group(1)] + 'の耕地'),
                        (rf'({ER}) Embryo Shard', lambda m: E[m.group(1)] + 'の胚の欠片'), (rf'({ER}) Embryo Block', lambda m: E[m.group(1)] + 'の胚のブロック'),
                        (rf'({ER}) Essence Core', lambda m: E[m.group(1)] + 'の精髄コア')]:
            m = re.fullmatch(pat, v)
            if m:
                t = fn(m); break
    (out.append(f'{k}\t{t}') if t else miss.append(f'{k}\t{v}'))
Path('tsv/v18_cp.tsv').write_text('\n'.join(out) + '\n', encoding='utf-8')
print(len(out) - 1, 'miss', miss)
