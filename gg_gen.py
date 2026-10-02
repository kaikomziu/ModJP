# generatorgalore の発電機名・アップグレード名を生成
T = {'copper':'銅','culinary':'料理','diamond':'ダイヤモンド','emerald':'エメラルド','enchantment':'エンチャント','ender':'エンダー','gold':'金',
     'halitosis':'口臭','honey':'ハチミツ','iron':'鉄','magmatic':'マグマ','netherite':'ネザライト','netherstar':'ネザースター','obsidian':'黒曜石',
     'potion':'ポーション'}
UP = ['copper_to_iron','culinary_to_honey','culinary_to_potion','diamond_to_emerald','diamond_to_netherite','diamond_to_obsidian','ender_to_halitosis',
      'gold_to_culinary','gold_to_diamond','iron_to_gold','netherite_to_netherstar','obsidian_to_enchantment','obsidian_to_ender','obsidian_to_magmatic']
out = ['## generatorgalore']
for k, j in T.items():
    out.append(f'block.generatorgalore.{k}_generator\t{j}発電機')
    out.append(f'block.generatorgalore.{k}_generator_8x\t8倍{j}発電機')
    out.append(f'block.generatorgalore.{k}_generator_64x\t64倍{j}発電機')
for u in UP:
    a, b = u.split('_to_')
    out.append(f'item.generatorgalore.{u}_upgrade\t{T[a]}から{T[b]}へのアップグレード')
out += ['generatorgalore.recipe.burn_rate\t燃焼速度: %smB/t', 'generatorgalore.recipe.burn_time\t燃焼時間: %s',
        'generatorgalore.recipe.fluid_fuel\t液体燃料', 'generatorgalore.recipe.rate\t発電量: %sFE/t', 'generatorgalore.recipe.solid_fuel\t固体燃料',
        'generatorgalore.recipe.total\t合計: %sFE', 'generatorgalore.recipe.total_bucket\t合計: %sFE/B', 'generatorgalore.screen.empty\t空',
        'generatorgalore.screen.energy_level\tエネルギー: %s', 'generatorgalore.screen.fuel_time\t燃料の残り時間: %s',
        'generatorgalore.screen.fuel_type\t燃料の種類: %s', 'generatorgalore.screen.generation_rate\t発電量: %sFE/t',
        'generatorgalore.screen.max_energy\t最大エネルギー: %sFE', 'generatorgalore.screen.transfer_rate\t送電量: %sFE/t',
        'itemGroup.generatorgalore\tGenerator Galore']
open('tsv/v14_gg_gen.tsv', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
