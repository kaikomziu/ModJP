# 英文にリテラルの「\n」(バックスラッシュ+n、改行ではない)がある訳文を tr/batch_19_literal.json に直接書く
# (TSV経由だと \n が改行に変換されてしまうため)
import json
B = chr(92) + "n"
D = {
    "evilcraft": {
        "item.evilcraft.blood_extractor.info": "モブを倒すときにインベントリに入れておく。" + B + "Shift + 右クリックで抽出または自動供給。",
        "item.evilcraft.kineticator.info": "Shift + 右クリックで引き寄せを切り替え。" + B + "右クリックで範囲を変更。",
        "item.evilcraft.kineticator_repelling.info": "Shift + 右クリックで反発を切り替え。" + B + "右クリックで範囲を変更。",
        "item.evilcraft.vengeance_ring.info": "復讐の亡霊を引き寄せたり召喚したりすることがある。" + B + "Shift + 右クリックでブーストを切り替え。",
    },
    "alchemistry": {
        "alchemistry.jei.elements.description": "すべての元素(水素を除く)は核融合チャンバーのマルチブロックで作れる。" + B + "このマルチブロックは2つの元素を入力として受け取り、それらを融合して原子番号の和に等しい新しい元素を作る。\"",
    },
    "darkmodeeverywhere": {
        "config.darkemodeeverywhere.method_shader_blacklist": "ダークシェーダーを適用しないclass:method形式の文字列(描画メソッド)のリスト。" + B + "各文字列はダークシェーダーを止めるクラスとメソッド(または任意の部分文字列)からなる。" + B + "例えば 'renderHunger' だけで 'net.minecraftforge.client.gui.overlay.ForgeGui:renderFood' を止められる(どちらでもよい)",
        "config.darkemodeeverywhere.method_shader_dump": "この設定を有効にすると、ダークシェーダーを適用したGUIの描画に使われたメソッドを5秒ごとに出力する" + B + "出力はclass:method形式の文字列のリスト。例: 'net.minecraftforge.client.gui.overlay.ForgeGui:renderFood'" + B + "ブラックリストに入れたいGUIの描画メソッド文字列を探すのに使おう。",
    },
    "extremesoundmuffler": {
        "log.error.loadAnchorList": "ESM: アンカーリストの読み込みエラー:" + B + " %s",
        "log.error.saveAnchorList": "ESM: アンカーリストの保存エラー" + B + " %s",
        "log.error.loadMuffledList": "ESM: 消音リストの読み込みエラー:" + B + " %s",
        "log.error.saveMuffledList": "ESM: 消音リストの保存エラー:" + B + " %s",
    },
}
json.dump(D, open('tr/batch_19_literal.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(sum(map(len, D.values())))
