T = {"improved":("改良",20,80),"sturdy":("頑丈",40,60),"reinforced":("強化",60,40),"everlasting":("永久",80,20)}
K = {"input":"搬入","duration":"時間","mesh":"メッシュ","output":"出力","everything":"万能"}
out = ["## strainers"]
for t, (j, p, d) in T.items():
    for k, kj in K.items():
        out.append(f"item.strainers.{t}_{k}_upgrade\t{j}の{kj}アップグレード")
    out.append(f"tooltips.strainers.{t}_input_upgrade.shift\t§a{p}%の確率で搬入アイテムが消費されない。")
    out.append(f"tooltips.strainers.{t}_mesh_upgrade.shift\t§a{p}%の確率で使用時にメッシュが傷まない。")
    out.append(f"tooltips.strainers.{t}_duration_upgrade.shift\t§aレシピの所要時間が全体の{d}%になる。")
    out.append(f"tooltips.strainers.{t}_output_upgrade.shift\t§aレシピの出力に{p}%の確率で追加抽選が行われる。")
    out.append(f"tooltips.strainers.{t}_everything_upgrade.shift\t§aすべてのアップグレードの効果を併せ持つ！")
for i in range(1, 7):
    out.append(f"tooltips.strainers.tier_{i}_mesh\tティア{i}のメッシュ")
out += r"""item.strainers.amethyst_mesh	アメジストのメッシュ
item.strainers.bamboo_mesh	竹のメッシュ
item.strainers.copper_mesh	銅のメッシュ
item.strainers.echo_mesh	残響のメッシュ
item.strainers.emerald_mesh	エメラルドのメッシュ
item.strainers.gold_mesh	金のメッシュ
item.strainers.leafy_mesh	葉のメッシュ
item.strainers.netherite_mesh	ネザライトのメッシュ
item.strainers.quartz_mesh	クォーツのメッシュ
item.strainers.eroding_water_bucket	浸食水入りバケツ
item.strainers.purified_water_bucket	浄水入りバケツ
item.strainers.stone_pebble	石の小石
item.strainers.deepslate_pebble	深層岩の小石
item.strainers.purifying_salt_mulch	浄化の塩マルチ
item.strainers.eroding_salt_mulch	浸食の塩マルチ
fluid_type.strainers.eroding_water_fluid	浸食水
fluid_type.strainers.purified_water_fluid	浄水
block.strainers.wooden_strainer	木のこし器
block.strainers.eroding_water_block	浸食水
block.strainers.purified_water_block	浄水
block.strainers.mulch	マルチ
block.strainers.summoning_block	召喚ブロック
block.strainers.strainer_tank	こし器タンク
item.strainers.specialized_input_upgrade	特化型搬入アップグレード
item.strainers.specialized_mesh_upgrade	特化型メッシュアップグレード
item.strainers.specialized_output_upgrade	特化型出力アップグレード
item.strainers.specialized_speed_upgrade	特化型時間アップグレード
tooltips.strainers.upgrade	§eSHIFT§rを押すと詳細を表示！
tooltips.strainers.specialized_output_upgrade.shift	§a出力が5倍に増加！§r、§c所要時間が3倍に増加！
tooltips.strainers.specialized_speed_upgrade.shift	§a所要時間が20tickに短縮！§r、§cメッシュの損耗が5倍に増加！
tooltips.strainers.specialized_mesh_upgrade.shift	§aメッシュが一切傷まない！§r、§c所要時間が1.5倍に増加！
tooltips.strainers.specialized_input_upgrade.shift	§a搬入アイテムが一切消費されない！§r、§cメッシュの損耗が10倍に増加！所要時間が4倍に増加！
tooltips.strainers.mesh.shift	メッシュの情報！
tooltips.strainers.mesh	メッシュの情報！
jei.strainers.purified_water	マルチブロックを浄化の塩マルチで右クリックすると、浄水の水源ブロックができる。
jei.strainers.eroding_water	マルチブロックを浸食の塩マルチで右クリックすると、浸食水の水源ブロックができる。
jei.strainers.mulch_block	クワで右クリックすると水の水源ブロックができる。\n\nマルチブロックを浸食の塩マルチで右クリックすると、浸食水の水源ブロックができる。\n\nマルチブロックを浸食の塩マルチで右クリックすると、浸食水の水源ブロックができる。
jei.strainer.place_block	上にブロックを置く
jei.strainer.place_fluid	上に液体を置く
jei.strainer.duration	所要時間
itemGroup.strainers	BBL Strainers""".split("\n")
open("tsv/v11_str_gen.tsv", "w", encoding="utf-8").write("\n".join(out) + "\n")
