"""家具MOD(cfm / nfm / refurbished_furniture)の「<素材> <家具>」形式のブロック名を語辞書から生成する。"""
import json
from pathlib import Path
from furn_common import NAME_RE, MAT

NOUN = {
    "Table": "テーブル", "Chair": "椅子", "Coffee Table": "コーヒーテーブル", "Cabinet": "キャビネット",
    "Bedside Cabinet": "ベッドサイドキャビネット", "Desk": "机", "Desk Cabinet": "デスクキャビネット", "Sofa": "ソファ",
    "Blinds": "ブラインド", "Upgraded Fence": "改良フェンス", "Upgraded Gate": "改良フェンスゲート",
    "Picket Fence": "ピケットフェンス", "Picket Gate": "ピケットゲート", "Crate": "木箱", "Park Bench": "公園のベンチ",
    "Mail Box": "郵便受け", "Mailbox": "郵便受け", "Hedge": "生け垣", "Trampoline": "トランポリン", "Cooler": "クーラーボックス",
    "Grill": "グリル", "Kitchen Counter": "キッチンカウンター", "Kitchen Drawer": "キッチン引き出し",
    "Kitchen Sink": "キッチンシンク", "Modern Table": "モダンテーブル", "Modern Chair": "モダンチェア",
    "Modern Coffee Table": "モダンコーヒーテーブル", "Modern Cabinet": "モダンキャビネット",
    "Modern Bedside Cabinet": "モダンベッドサイドキャビネット", "Modern Bed": "モダンベッド", "Curtain": "カーテン",
    "Modern Desk": "モダンデスク", "Modern Desk Cabinet": "モダンデスクキャビネット", "Wall Cabinet": "壁掛けキャビネット",
    "Modern Sofa": "モダンソファ", "Television Stand": "テレビ台", "Lamp": "ランプ",
    "Modern Kitchen Counter": "モダンキッチンカウンター", "Modern Kitchen Drawer": "モダンキッチン引き出し",
    "Modern Kitchen Sink": "モダンキッチンシンク", "Bar Stool": "バースツール", "Chopping Board": "まな板",
    "Door Bell": "ドアベル", "Inflatable Castle": "エアー遊具の城", "Cup": "カップ", "Water Tank": "貯水タンク",
    "Bird Bath": "バードバス", "Tap": "蛇口", "Digital Clock": "デジタル時計", "Drawer": "引き出し",
    "Kitchen Cabinetry": "キッチン収納棚", "Fridge": "冷蔵庫", "Toaster": "トースター", "Microwave": "電子レンジ",
    "Stove": "コンロ", "Cutting Board": "まな板", "Lightswitch": "照明スイッチ", "Ceiling Light": "シーリングライト",
    "Electricity Generator": "発電機", "Storage Jar": "保存瓶", "Light Ceiling Fan": "シーリングファン(ライト)",
    "Dark Ceiling Fan": "シーリングファン(ダーク)", "Storage Cabinet": "収納キャビネット",
    "Kitchen Storage Cabinet": "キッチン収納キャビネット", "Range Hood": "レンジフード", "Stool": "スツール",
    "Stepping Stones": "飛び石", "Toilet": "トイレ", "Basin": "洗面台", "Bath": "浴槽",
    "Lattice Fence": "格子フェンス", "Lattice Fence Gate": "格子フェンスゲート",
}
TONE = {"Light": "ライト", "Dark": "ダーク"}
out = {}
for ns in ["cfm", "nfm", "refurbished_furniture"]:
    miss = json.loads(Path(f"extracted/{ns}.json").read_text(encoding="utf-8"))["missing"]
    r = {}
    for k, v in miss.items():
        m = NAME_RE.match(v) if k.startswith("block.") else None
        if not m or m.group(2) not in NOUN:
            continue
        mat, noun, tone = m.groups()
        if mat in TONE:
            s = f"{NOUN[noun]}({TONE[mat]})"
        else:
            s = f"{MAT[mat]}の{NOUN[noun]}"
            if tone:
                s += f"({TONE[tone]})"
        r[k] = s
    out[ns] = r
    print(ns, len(r), "/", len(miss))
Path("tr/batch_01_furniture_gen.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
