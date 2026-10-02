out = ["## glassential"]
A = [("", ""), ("dark_", "色付き"), ("light_", "発光"), ("magma_", "マグマの")]
B = [("", "ガラス"), ("_ghostly", "幽霊ガラス"), ("_ethereal", "霊妙なガラス"), ("_ethereal_reverse", "逆霊妙なガラス")]
for ob, oj in (("", ""), ("obsidian_", "防爆")):
    for a, aj in A:
        for b, bj in B:
            k = "_".join(x for x in ["block.glassential.glass", ob.strip("_"), a.strip("_"), b.strip("_")] if x)
            out.append(f"{k}\t{oj}{aj}{bj}")
    out.append(f"block.glassential.glass_{ob}redstone\t{oj}レッドストーンガラス")
out += """tooltip.glassential.redstone	レッドストーン信号を出す
tooltip.glassential.ghostly	エンティティは通り抜けられる
tooltip.glassential.ethereal	プレイヤーは通り抜けられる
tooltip.glassential.ethereal_reverse	プレイヤーにとってだけ固体
tooltip.glassential.dark	光を遮る
tooltip.glassential.light	光を放つ
tooltip.glassential.magma	触れるとダメージを受ける
tooltip.glassential.obsidian	爆発に耐える
itemGroup.glassential.items	Glassential""".split("\n")
open("tsv/v11_gl_gen.tsv", "w", encoding="utf-8").write("\n".join(out) + "\n")
