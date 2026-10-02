# MOD日本語化パック (ModJP)

**英語のまま表示されているMODの文字を、日本語にするリソースパックです。**
Minecraft 1.20.1 / Forge 向け。**402 MOD・約7万項目**に日本語訳を追加します。

![ロゴ](ここにロゴ画像)

---

## 特徴

- **MOD本体は一切いじりません**
  リソースパックなので、MODを更新しても壊れません。外せばすぐ元に戻ります。
- **公式の日本語訳は上書きしません**
  MODにもともと入っている日本語訳はそのまま使い、足りない部分だけを補います。
- **入っていないMODの分は自動で無視されます**
  402 MOD全部を入れていなくても、入っているMODの分だけ日本語になります。
- **表示崩れのチェック済み**
  `%s` や色コード(§)、改行の数など、ゲーム内の表示に関わる記号はすべて原文と一致するよう検査しています。

## 使い方

1. ダウンロードした zip を **解凍せずに**、インスタンスの `resourcepacks` フォルダに入れる
   (CurseForgeアプリならインスタンスを右クリック →「フォルダを開く」→ `resourcepacks`)
2. ゲームの **設定 → 言語** を「日本語」にする
3. **設定 → リソースパック** で「MOD日本語化パック」を右側(有効)に移す
   ※ 他のリソースパックより **上** に置いてください

## 主な対応MOD

訳を追加した項目が多い順に一部を載せています。全402 MODの一覧は zip 同梱の `説明書.txt` を見てください。

| MOD | 追加した訳 |
|---|---|
| Chipped | 7,258 |
| Rechiseled | 3,656 |
| Tetra | 2,613 |
| Theurgy | 2,376 |
| PneumaticCraft: Repressurized | 2,029 |
| Integrated Dynamics | 1,753 |
| Simply Swords | 1,630 |
| Steam 'n' Rails | 1,614 |
| Item Descriptions | 1,545 |
| Twilight Forest | 1,488 |
| Corail Tombstone | 1,188 |
| Vampirism | 1,061 |
| Hexerei | 1,048 |
| Productive Bees | 1,036 |
| ChemLib | 1,022 |
| All The Compressed | 983 |
| Croptopia | 646 |
| FTB Quests | 584 |
| Tinkers' Construct | 548 |
| Oh The Biomes You'll Go | 494 |
| Xaero's Minimap | 459 |

このほか AE2 アドオン、Mekanism アドオン、RFTools、Botania アドオン、Ars Nouveau アドオン、Hex Casting アドオンなど、ATM8 系の MOD を多数カバーしています。

## よくある質問

**Q. 日本語にならない文字があります**
A. そのMODが対応していない(バージョン違いを含む)か、意図的に英語のまま残している項目です。MOD内蔵の開発用テキストや、記号・型番だけの項目などは訳していません。

**Q. 他の日本語化パックと一緒に使えますか？**
A. 使えます。同じ項目を訳しているパックがある場合は、リソースパック画面で上にある方が優先されます。

**Q. 1.20.1 以外のバージョンで使えますか？**
A. 1.20.1 用に作っています。他のバージョンでも一部は表示されますが、動作は保証しません。

## 誤訳・要望

「MOD名」「表示されている文字(英語/日本語)」「どう直すべきか」を、コメント欄か GitHub の Issues に書いてください。
GitHub: https://github.com/kaikomziu/ModJP

---

### English

A Japanese translation resource pack for **402 mods** on Minecraft 1.20.1 (Forge), adding about 70,000 Japanese strings.
It never modifies mod jars and never overrides official Japanese translations bundled with mods; it only fills in missing entries.
Put the zip (do not extract) into `resourcepacks`, set the language to 日本語, and enable the pack.
