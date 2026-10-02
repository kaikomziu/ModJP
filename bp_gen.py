C = {"black":"黒色","blue":"青色","brown":"茶色","cyan":"水色","gray":"灰色","green":"緑色","light_blue":"空色",
"light_gray":"薄灰色","lime":"黄緑色","magenta":"赤紫色","orange":"橙色","pink":"桃色","purple":"紫色","red":"赤色",
"white":"白色","yellow":"黄色"}
out = ["## botanypots",
"block.botanypots.terracotta_botany_pot\t栽培ポット",
"block.botanypots.terracotta_hopper_botany_pot\tホッパー付き栽培ポット"]
for c, j in C.items():
    for m, mj in (("terracotta", ""), ("concrete", "コンクリートの"), ("glazed_terracotta", "彩釉の")):
        out.append(f"block.botanypots.{c}_{m}_botany_pot\t{j}の{mj}栽培ポット")
        out.append(f"block.botanypots.{c}_{m}_hopper_botany_pot\t{j}の{mj}ホッパー付き栽培ポット")
out += """itemGroup.botanypots.creative_tab	Botany Pots
tooltip.botanypots.invalid_soil	このアイテムは土として使えない。
tooltip.botanypots.invalid_seed	このアイテムは種として使えない。
tooltip.botanypots.incorrect_soil	この土では今の種を育てられない。
tooltip.botanypots.incorrect_seed	この種は今の土では育たない。
tooltip.botanypots.missing_soil	種を育てるには土が必要。
tooltip.botanypots.missing_seed	種を置くと栽培が始まる。
tooltip.botanypots.soil_modifier	種が%s倍の速さで育つ。
tooltip.botanypots.seed_item	種アイテム
tooltip.botanypots.soil_item	土アイテム
tooltip.botanypots.soil_id	土ID: %s
tooltip.botanypots.crop_id	作物ID: %s
tooltip.botanypots.soil	土: %s
tooltip.botanypots.seed	種: %s
tooltip.botanypots.progress	進行度:
tooltip.botanypots.chance	確率: %s
tooltip.botanypots.rolls	抽選回数: %s
tooltip.botanypots.rollrange	抽選回数: %s - %s
tooltip.botanypots.grow_time	成長時間: %s
tooltip.botanypots.modifier	速度: %s倍
advancements.botany_pots.get_pot.title	育て、育て
advancements.botany_pots.get_pot.description	栽培ポットを手に入れる
advancements.botany_pots.get_hopper_pot.title	ホッパーで栽培しよう
advancements.botany_pots.get_hopper_pot.description	ホッパー付き栽培ポットを手に入れる
commands.botanypots.mod_message	[§aBotany Pots§r] %s
commands.botanypots.dump.no_results	結果が見つからなかった。
commands.botanypots.dump.missing_crops	不足している可能性のある作物が%d件見つかった。この一覧は網羅的ではなく、誤検出や見落としを含む場合がある。このメッセージをクリックすると一覧をクリップボードにコピーする。
gui.jei.category.botanypots.crop	作物""".split("\n")
open("tsv/v11_bp_gen.tsv", "w", encoding="utf-8").write("\n".join(out) + "\n")
