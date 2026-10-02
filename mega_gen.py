S = ["1m", "4m", "16m", "64m", "256m"]
T = {"item":"アイテム","fluid":"液体","chemical":"化学物質","mana":"マナ","source":"ソース"}
out = ["## megacells"]
for s in S:
    u = s.upper()
    out.append(f"block.megacells.{s}_crafting_storage\t{u} MEGAクラフトストレージ")
    out.append(f"item.megacells.cell_component_{s}\t{u} MEGAストレージコンポーネント")
    for t, j in T.items():
        out.append(f"item.megacells.{t}_storage_cell_{s}\t{u} MEGA{j}ストレージセル")
        out.append(f"item.megacells.portable_{t}_cell_{s}\t{u} ポータブル{j}セル")
for t, j in T.items():
    out.append(f"item.megacells.mega_{t}_cell_housing\tMEGA{j}セル筐体")
out += """block.megacells.mega_crafting_accelerator	MEGA並列クラフトユニット
block.megacells.mega_crafting_monitor	MEGAクラフトモニター
block.megacells.mega_crafting_unit	MEGAクラフトユニット
block.megacells.mega_emc_interface	MEGA変換インターフェース
block.megacells.mega_energy_cell	超濃縮エナジーセル
block.megacells.mega_interface	MEGAインターフェース
block.megacells.mega_pattern_provider	MEGAパターンプロバイダー
block.megacells.sky_steel_block	スカイスチールブロック
gui.megacells.ModName	MEGA Cells
gui.tooltips.megacells.ALot	たくさん。
gui.tooltips.megacells.AcceleratorThreads	1ブロックごとに並列処理スレッドを4つ提供する。
gui.tooltips.megacells.Compression	圧縮: %s
gui.tooltips.megacells.Contains	内容: %s
gui.tooltips.megacells.Disabled	無効
gui.tooltips.megacells.Empty	空
gui.tooltips.megacells.Enabled	有効
gui.tooltips.megacells.FilterChemicalUnsupported	フィルターの化学物質に対応していない！
gui.tooltips.megacells.MismatchedFilter	フィルターが一致しない！
gui.tooltips.megacells.NotPartitioned	未分割
gui.tooltips.megacells.PartitionedFor	分割先: %s
gui.tooltips.megacells.ProcessingOnly	加工パターンのみ対応。
gui.tooltips.megacells.Quantity	数量: %s
item.megacells.accumulation_processor	蓄積プロセッサ
item.megacells.accumulation_processor_press	蓄積回路の金型
item.megacells.bulk_cell_component	MEGAバルクストレージコンポーネント
item.megacells.bulk_item_cell	MEGAバルクアイテムストレージセル
item.megacells.cable_mega_emc_interface	MEGA変換インターフェース
item.megacells.cable_mega_interface	MEGAインターフェース
item.megacells.cable_mega_pattern_provider	MEGAパターンプロバイダー
item.megacells.cell_dock	MEセルドック
item.megacells.compression_card	圧縮カード
item.megacells.decompression_module	MEGA展開モジュール
item.megacells.decompression_pattern	展開パターン
item.megacells.greater_energy_card	上位エナジーカード
item.megacells.printed_accumulation_processor	蓄積回路
item.megacells.radioactive_cell_component	MEGA放射性ストレージコンポーネント
item.megacells.radioactive_chemical_cell	MEGA放射性化学物質ストレージセル
item.megacells.sky_steel_ingot	スカイスチールインゴット
text.autoconfig.megacells.option.AllowSpentWaste	(AppMek) 使用済み核廃棄物を許可
text.autoconfig.megacells.option.AllowSpentWaste.@Tooltip	MEGA放射性セルに使用済み核廃棄物を保存できるかどうか。
text.autoconfig.megacells.option.CompressionChainLimit	バルク圧縮の連鎖上限
text.autoconfig.megacells.option.CompressionChainLimit.@Tooltip	圧縮を有効にしたバルクセルが保存中として報告できるバリエーションの最大数。
text.autoconfig.megacells.title	MEGA Cells""".split("\n")
open("tsv/v11_mega_gen.tsv", "w", encoding="utf-8").write("\n".join(out) + "\n")
