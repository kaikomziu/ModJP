T = {"elite":"エリート","ultra":"ウルトラ","mega":"メガ"}
P = {"exporter":"エクスポーター","importer":"インポーター","constructor":"コンストラクター","destructor":"デストラクター",
"disk_manipulator":"ディスクマニピュレーター","interface":"インターフェース","requester":"リクエスター"}
D = {("elite","exporter"):"より速い搬出！",("elite","importer"):"より速い搬入！",("elite","constructor"):"より速い設置/ドロップ！",
("elite","destructor"):"より速い破壊/回収！",("elite","disk_manipulator"):"より速い操作！",("elite","interface"):"アイテムの搬出入がより速い！",
("elite","requester"):"より速い要求！",("ultra","constructor"):"より速く、スタックアップグレード内蔵！",
("ultra","interface"):"スロット増加、スタックアップグレード内蔵！",("ultra","requester"):"スロット増加、スタックアップグレード内蔵！",
("mega","exporter"):"さらに速い搬出！",("mega","importer"):"さらに速い搬入！",("mega","constructor"):"さらに速い設置/ドロップ！",
("mega","destructor"):"さらに速い破壊/回収！",("mega","disk_manipulator"):"さらに速い操作！",
("mega","interface"):"アイテムの搬出入を同時にさらに速く！",("mega","requester"):"さらに速い要求！"}
out = ["## cabletiers", "itemGroup.cabletiers\tCable Tiers"]
for t, tj in T.items():
    for p, pj in P.items():
        out.append(f"block.cabletiers.{t}_{p}\t{tj}{pj}")
        out.append(f"advancements.cabletiers.{t}_{p}\t{tj}{pj}")
        out.append(f"advancements.cabletiers.{t}_{p}.description\t{D.get((t, p), 'フィルタースロット増加、スタックアップグレード内蔵！')}")
    out.append(f"gui.cabletiers.{t}_interface.import\t{tj}インターフェースの搬入")
    out.append(f"gui.cabletiers.{t}_interface.export\t{tj}インターフェースの搬出")
open("tsv/v11_ct_gen.tsv", "w", encoding="utf-8").write("\n".join(out) + "\n")
