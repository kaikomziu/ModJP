"""訳さずに英語(原文)のまま残すキーを理由付きで tr/_keep_english.json に書き出す。"""
import json, sys, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from build import load_translations

tr = load_translations()
keep = {}
for f in sorted(Path("extracted").glob("*.json")):
    d = json.loads(f.read_text(encoding="utf-8"))
    ns = d["namespace"]
    for k, v in d["missing"].items():
        if k in tr.get(ns, {}):
            continue
        if ns == "collective":
            why = "Collective内の未導入Serilum系MOD用の文言"
        elif ns == "vampirismguide":
            why = "GuideAPI-VP未導入のため表示されないガイド本文"
        elif ns == "enchdesc":
            why = "未導入MODのエンチャント説明"
        elif ns == "patchouli" and "landing" in k:
            why = "開発用テスト本の文言"
        elif ns == "modonomicon" and (k.startswith("book.modonomicon.demo.") or k.startswith("modonomicon.test.")
                                      or k in ("test.test.test", "advancement.minecraft.husbandry.ride_a_boat_with_a_goat.title")
                                      or k.startswith("patchouli.occultism.")):
            why = "Modonomicon内蔵の開発用デモ/テスト本の文言"
        elif ns == "darkutils" and k.startswith("font.") and k.endswith(".preview"):
            why = "特殊フォントの英字パングラム見本(英字グリフ専用)"
        elif ns in ("productivetrees", "productivefarming") and k.endswith(".latin"):
            why = "樹木の学名(ラテン語)"
        elif ns == "zeta" and k == "zeta.jei.hint_preamble":
            why = "MOD名の接頭辞のみ"
        elif k.startswith("jukebox_song.") or k.startswith("aether_ii.music.") or k.startswith("subtitle.apothic_enchanting.music_disc."):
            why = "楽曲名(作曲者 - 曲名)"
        elif ns == "aether_ii" and v.startswith("Lorem ipsum"):
            why = "未完成の図鑑項目のダミー文"
        elif re.fullmatch(r"(%\d+\$[sd])+", v):
            why = "書式指定子のみ"
        elif k.endswith(".tooltip") and re.fullmatch(r"item\.[A-Z_]+", v):
            why = "Createのツールチップ用内部識別子"
        elif v.startswith("NA | INVALID"):
            why = "無効化されたアイテムの仮名"
        elif not re.search(r"[A-Za-z]{2}", re.sub(r"§.", "", v)) or re.fullmatch(r"MKI+|V|eof|\d+(\.\d+)*", v):
            why = "記号・アイコン・型番のみ"
        else:
            why = None
        if why:
            keep.setdefault(ns, {})[k] = why
        else:
            print("未分類:", ns, k, repr(v))
Path("tr/_keep_english.json").write_text(json.dumps(keep, ensure_ascii=False, indent=1), encoding="utf-8")
print("keep", sum(map(len, keep.values())))
