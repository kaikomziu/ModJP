"""Rechiseled の装飾ブロック名を「<バニラ公式名>(<模様>)[の階段/のハーフブロック]」で生成する。
キーが <バニラのブロックID>_<模様>[_slab|_stairs][_connecting] の形なので、英語名ではなくキーから組み立てる。"""
import json, re
from pathlib import Path

van_en = json.loads(Path("vanilla/en_us.json").read_text(encoding="utf-8"))
van = json.loads(Path("vanilla/ja_jp.json").read_text(encoding="utf-8"))
BASE = {k.split(".")[2]: v for k, v in van.items() if k.startswith("block.minecraft.") and k.count(".") == 2}
BASE["purpur"] = BASE["purpur_block"]
IDS = sorted(BASE, key=len, reverse=True)

PAT = {
    "bars": "格子", "beams": "梁", "big_tiles": "大タイル", "blobs": "斑点", "bordered": "縁取り", "bordered_crosses": "縁取り十字",
    "bordered_diagonal_tiles": "縁取り斜めタイル", "bordered_plating": "縁取り装甲板", "bordered_polished": "縁取り研磨",
    "brick_bordered": "レンガ縁", "brick_pattern": "レンガ模様", "brick_paving": "レンガ舗装", "bricks": "レンガ", "bundled": "束ね",
    "carved": "彫刻", "chiseled": "模様入り", "chiseled_border": "模様入り縁", "chiseled_bricks": "模様入りレンガ",
    "chiseled_circles": "模様入り円", "chiseled_clovers": "模様入りクローバー", "chiseled_creeper": "クリーパー彫刻",
    "chiseled_cubes": "模様入りキューブ", "chiseled_piglin": "ピグリン彫刻", "chiseled_pillar": "模様入り柱",
    "chiseled_skeleton": "スケルトン彫刻", "chiseled_squares": "模様入り四角", "chunks": "塊", "circles": "円", "clovers": "クローバー",
    "clumps": "かたまり", "cobbled": "丸石風", "compacted": "圧縮", "compressed": "高圧縮", "cone": "円錐", "connecting": "連結",
    "cracked": "ひび割れ", "crate": "木箱", "crosses": "十字", "crushed": "砕石", "crystal": "結晶", "cut": "カット", "dark": "暗色",
    "decorated": "装飾", "decorated_bordered": "装飾縁取り", "dented": "くぼみ", "diagonal_bricks": "斜めレンガ",
    "diagonal_stripes": "斜めストライプ", "diagonal_tiles": "斜めタイル", "dotted": "ドット", "edged": "縁付き", "fabric": "布目",
    "flooring": "床張り", "framed": "フレーム", "gears": "歯車", "glossy": "光沢", "grid": "格子模様", "grooves": "溝",
    "indented": "へこみ", "inverted_dented": "逆くぼみ", "inverted_tiles": "逆タイル", "jewel": "宝石", "jewel_block": "宝石ブロック",
    "large_bricks": "大レンガ", "large_squares": "大四角", "large_tiles": "大タイル", "lines": "線", "mesh": "網目",
    "meteoric": "隕石", "mosaic": "モザイク", "muddy": "泥", "ovals": "楕円", "path": "小道", "pattern": "模様", "patterned": "柄",
    "patterned_squares": "柄四角", "paving": "舗装", "pillar": "柱", "pillars": "列柱", "pipes": "パイプ", "plated": "メッキ",
    "plating": "装甲板", "polished": "研磨", "processed": "加工", "pulverized": "粉砕", "reinforced": "補強", "rhombuses": "ひし形",
    "rib": "リブ", "rocky": "岩肌", "rotated_bricks": "回転レンガ", "rows": "列", "scales": "うろこ", "shafts": "シャフト",
    "sheared": "刈り込み", "sheets": "シート", "shiny": "輝き", "shiny_bordered": "輝き縁取り", "skull": "ドクロ",
    "slanted_tiles": "傾斜タイル", "slated": "スレート", "small_bricks": "小レンガ", "small_tiles": "小タイル", "smooth": "なめらか",
    "smooth_brick_paving": "なめらかレンガ舗装", "smooth_clumps": "なめらかかたまり", "smooth_large_tiles": "なめらか大タイル",
    "smooth_rotated_bricks": "なめらか回転レンガ", "smooth_tiles": "なめらかタイル", "soil": "土壌", "spiral_pattern": "渦巻き模様",
    "spots": "斑点模様", "squares": "四角", "striped": "縞", "stripes": "ストライプ", "swirling": "渦", "tiles": "タイル",
    "tilled": "耕し", "waves": "波", "wavy": "波線", "waxed": "蝋引き", "worn_stripes": "擦れたストライプ", "woven": "編み込み",
    "organic_pattern": "有機模様", "jagged_pattern": "ギザギザ模様",
}
FIXED = {
    "rechiseled.item_group": "Rechiseled", "rechiseled.tooltip.connecting": "連結テクスチャ",
    "rechiseled.chiseling.preview.mode_0": "1×1でプレビュー", "rechiseled.chiseling.preview.mode_1": "3×1でプレビュー",
    "rechiseled.chiseling.preview.mode_2": "3×3でプレビュー", "rechiseled.chiseling.connecting": "連結テクスチャ: %s",
    "rechiseled.chiseling.connecting.on": "オン", "rechiseled.chiseling.connecting.off": "オフ",
    "rechiseled.chiseling.chisel_all": "すべて彫る", "rechiseled.chiseling.chisel_all.shift": "%sですべての形状",
    "rechiseled.chiseling.chisel_all.items": "%s個のアイテム", "rechiseled.chiseling.select_block": "%sを選択",
    "rechiseled.chiseling.preview": "ブロックのプレビュー", "rechiseled.chiseling.select_shape": "形状: %s",
    "rechiseled.chiseling.filter": "絞り込み", "rechiseled.chiseling.filter.clear": "右クリックで解除",
    "rechiseled.chiseling.filter.show_blocks": "ブロックを表示", "rechiseled.chiseling.filter.show_stairs": "階段を表示",
    "rechiseled.chiseling.filter.show_slabs": "ハーフブロックを表示", "rechiseled.chiseling.filter.show_non_connecting": "連結しないものを表示",
    "rechiseled.chiseling.scrollbar": "スクロールバー", "rechiseled.chiseling.entry.recipe": "レシピ: %s",
    "rechiseled.chiseling.entry.owner": "プラグイン: %s", "rechiseled.recipe_category.title": "彫刻",
    "rechiseled.recipe_category.conversion_value": "変換値: %s", "rechiseled.item.chisel": "のみ",
    "rechiseled.chiseling.shape.block": "ブロック", "rechiseled.chiseling.shape.stairs": "階段", "rechiseled.chiseling.shape.slab": "ハーフブロック",
}

miss = json.loads(Path("extracted/rechiseled.json").read_text(encoding="utf-8"))["missing"]
out, left = {}, []
for k, v in miss.items():
    if k in FIXED:
        out[k] = FIXED[k]
        continue
    m = re.match(r"(?:block\.rechiseled|rechiseled\.block)\.(.+)", k)
    s = re.sub(r"_connecting$", "", m.group(1)) if m else ""
    shape = re.search(r"_(slab|stairs)$", s)
    s = re.sub(r"_(slab|stairs)$", "", s)
    b = next((b for b in IDS if s.startswith(b + "_")), None)
    p = s[len(b) + 1:] if b else None
    if not b or p not in PAT:
        left.append((k, v))
        continue
    name = f"{BASE[b]}({PAT[p]})"
    if shape:
        name += {"slab": "のハーフブロック", "stairs": "の階段"}[shape.group(1)]
    out[k] = name
print(len(out), "/", len(miss), left[:10])
Path("tr/batch_10_rechiseled_gen.json").write_text(json.dumps({"rechiseled": out}, ensure_ascii=False, indent=1), encoding="utf-8")
