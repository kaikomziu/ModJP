# ModJP 開発メモ

CurseForgeインスタンス(Forge 1.20.1 / 402 MOD)の未翻訳キーを訳した配布用リソースパック。
jarは改変せず、jar同梱の公式ja_jpにないキーだけを追加する(他MOD・バニラに公式訳があるキーも入れない)。

## 手順

```
python extract.py      # mods/*.jar から en_us / ja_jp を抽出 → extracted/
python *_gen.py        # 定型名の機械生成(家具・石材・金属・缶詰・ポーション等) → tr/batch_0*_gen.json
python tsvin.py        # tsv/*.tsv(手訳) → tr/batch_tsv_*.json
python keep_gen.py     # 英語のまま残すキーを理由付きで tr/_keep_english.json に
python build.py        # 書式コード検査して pack/ を生成、translation_status.md を更新
python validate.py     # JSON厳密パース・公式訳の上書きがないか確認
python package.py      # dist/ModJP_1.20.1_v*.zip を作り、インスタンスの resourcepacks にもコピー
```

- TSV書式: `## 名前空間` 見出しの下に `キー<TAB>訳`。訳中の `\n` は改行。
  `=英文<TAB>訳` はその名前空間で英文が完全一致する未訳キーすべてに適用。
- 書式コード(`%s` `%1$s` `§a` 改行 `{0}` `$(...)`)の種類と個数が原文と一致しないとbuildがエラーにする。
- 流用元: ModpackJP(____ (1))・tatanai_ja_patch・client_mods_ja_patch の訳を prev_tm.json 経由で batch_00_reuse.json に。
- jar同梱のja_jpが壊れているMOD(ja_broken: Twilight Forest 4.3.2508 等)も公式訳は同梱しない。build.py の BUNDLE_BROKEN_OFFICIAL で切り替え可。

## MOD更新時

extract.py → build.py で「残り」を確認し、差分だけTSVに足す → keep_gen.py → build.py → validate.py → package.py。
バージョンを上げるときは build.py / validate.py の DESC と package.py の VERSION を変える。
