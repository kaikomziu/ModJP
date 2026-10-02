W = {"acacia":"アカシア","birch":"シラカバ","cherry":"サクラ","crimson":"真紅","dark_oak":"ダークオーク","jungle":"ジャングル",
"mangrove":"マングローブ","oak":"オーク","spruce":"トウヒ","warped":"歪んだ木","fluid":"液体","framed":"額縁"}
Z = {"1":"1x1","2":"1x2","4":"2x2"}
out = ["## functionalstorage"]
for w, j in W.items():
    for n, z in Z.items():
        out.append(f"block.functionalstorage.{w}_{n}\t{j}の引き出し({z})")
out += r"""block.functionalstorage.armory_cabinet	武器庫キャビネット
block.functionalstorage.compacting_drawer	圧縮引き出し
block.functionalstorage.compacting_framed_drawer	額縁の圧縮引き出し
block.functionalstorage.controller_extension	コントローラーアクセスポイント
block.functionalstorage.ender_drawer	エンダー引き出し
block.functionalstorage.framed_controller_extension	額縁のコントローラーアクセスポイント
block.functionalstorage.framed_simple_compacting_drawer	額縁の簡易圧縮引き出し
block.functionalstorage.framed_storage_controller	額縁のストレージコントローラー
block.functionalstorage.simple_compacting_drawer	簡易圧縮引き出し
configurationtool.configmode	設定モード:
configurationtool.configmode.indicator	インジケーター表示の切り替え
configurationtool.configmode.indicator.mode_0	非表示
configurationtool.configmode.indicator.mode_1	進行バーを表示
configurationtool.configmode.indicator.mode_2	満杯のときだけ進行バーを表示
configurationtool.configmode.indicator.mode_3	満杯のときだけ背景なしで進行バーを表示
configurationtool.configmode.locking	ロック
configurationtool.configmode.toggle_numbers	数量の表示/非表示
configurationtool.configmode.toggle_render	アイテム描画の表示/非表示
configurationtool.configmode.toggle_upgrades	アップグレード描画の表示/非表示
configurationtool.use	スニーク+空中を右クリックでモード切り替え。引き出しを右クリックでオプションを切り替える。
drawer.block.contents	内容:
frameddrawer.use	テクスチャの変え方: \n作業台の1番目のスロットに引き出しの外側に使いたいブロック、2番目のスロットに額縁の引き出しの内側に使うブロック、3番目のスロットに額縁の引き出しを置く。4番目のスロットにブロックを入れると引き出しの仕切りのテクスチャも変えられる\n
gui.functionalstorage.amount	数量:
gui.functionalstorage.fluid	液体:
gui.functionalstorage.item	アイテム:
gui.functionalstorage.open_gui	しゃがんで右クリックでGUIを開く
gui.functionalstorage.slot	スロット:
gui.functionalstorage.storage	ストレージ
gui.functionalstorage.storage_range	範囲
gui.functionalstorage.utility	ユーティリティ
item.functionalstorage.collector_upgrade	回収アップグレード
item.functionalstorage.configuration_tool	設定ツール
item.functionalstorage.copper_upgrade	銅のアップグレード
item.functionalstorage.creative_vending_upgrade	クリエイティブ自販アップグレード
item.functionalstorage.diamond_upgrade	ダイヤモンドのアップグレード
item.functionalstorage.gold_upgrade	金のアップグレード
item.functionalstorage.iron_downgrade	鉄のダウングレード
item.functionalstorage.linking_tool	リンクツール
item.functionalstorage.puller_upgrade	搬入アップグレード
item.functionalstorage.pusher_upgrade	搬出アップグレード
item.functionalstorage.redstone_upgrade	レッドストーンアップグレード
item.utility.direction.desc	GUI内で右クリックすると方向を変更する
item.utility.downgrade	スロットの上限を64個にする
item.utility.slot.desc	GUI内で右クリックするとスロットを変更する
itemGroup.functionalstorage	Functional Storage
key.categories.storage	ストレージ
key.categories.utility	ユーティリティ
linkingtool.controller	コントローラー:
linkingtool.ender.clear	スニーク+空中を右クリックで周波数を消去。
linkingtool.ender.frequency	周波数:
linkingtool.linkingaction	リンク動作:
linkingtool.linkingaction.add	追加
linkingtool.linkingaction.remove	削除
linkingtool.linkingmode	リンクモード:
linkingtool.linkingmode.multiple	複数
linkingtool.linkingmode.multiple.desc	2点間の複数の引き出しをリンクする
linkingtool.linkingmode.single	単体
linkingtool.linkingmode.single.desc	引き出しをコントローラーにリンクする
linkingtool.use	* スニーク+空中を右クリックでモード切り替えまたは周波数を消去。\n* エンダー引き出しを左クリックでその周波数を記憶。\n* 空中を右クリックで動作を切り替え。\n\nコントローラーを右クリックしてツールを設定し、近くの引き出しに使ってリンクする。\n\nツールを持っている間は、選択したコントローラーに接続された引き出しが表示される。
storageupgrade.desc.fluid	ブロックの液体容量を次の倍率にする:
storageupgrade.desc.item	ブロックのアイテム容量を次の倍率にする:
storageupgrade.desc.range	コントローラーの半径を%sブロック広げる
upgrade.type	種類:
upgrade.type.storage	ストレージ
upgrade.type.utility	ユーティリティ""".split("\n")
open("tsv/v11_fs_gen.tsv", "w", encoding="utf-8").write("\n".join(out) + "\n")
