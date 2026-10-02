"""All the Compressed の「<ブロック名> Nx」を「<公式名>(N重圧縮)」で生成する。バニラはキーのIDから公式訳を引く。"""
import json, re
from pathlib import Path

van = json.loads(Path("vanilla/ja_jp.json").read_text(encoding="utf-8"))
MOD = {
    "ATM Star Block": "ATMスターブロック", "Allthemodium Block": "オールザモジウムブロック", "Aluminum Block": "アルミニウムブロック",
    "Ancient Log": "古代の原木", "Ancient Stone": "古代の石", "Blaze Mesh": "ブレイズメッシュ", "Block Of Blazing Crystal": "燃え盛る結晶ブロック",
    "Block Of Energized Steel": "エネルギー鋼ブロック", "Block Of Niotic Crystal": "ナイオティック結晶ブロック",
    "Block Of Nitro Crystal": "ニトロ結晶ブロック", "Block Of Spirited Crystal": "スピリテッド結晶ブロック", "Block Of Uraninite": "閃ウラン鉱ブロック",
    "Block of Flint": "火打石ブロック", "Bronze Block": "青銅ブロック", "Conductive Alloy Block": "導電合金ブロック",
    "Constantan Block": "コンスタンタンブロック", "Copper Alloy Block": "銅合金ブロック", "Dark Steel Block": "ダークスチールブロック",
    "Electrum Block": "エレクトラムブロック", "End Steel Block": "エンドスチールブロック", "Ender Pearl Block": "エンダーパールブロック",
    "Enderium Block": "エンダリウムブロック", "Energetic Alloy Block": "エナジェティック合金ブロック", "Invar Block": "インバーブロック",
    "Iridium Block": "イリジウムブロック", "Lead Block": "鉛ブロック", "Lumium Block": "ルミウムブロック", "Nether Star Block": "ネザースターブロック",
    "Nickel Block": "ニッケルブロック", "Osmium Block": "オスミウムブロック", "Peridot Block": "ペリドットブロック", "Platinum Block": "プラチナブロック",
    "Pulsating Alloy Block": "パルセイティング合金ブロック", "Redstone Alloy Block": "レッドストーン合金ブロック", "Ruby Block": "ルビーブロック",
    "Sapphire Block": "サファイアブロック", "Signalum Block": "シグナルムブロック", "Silver Block": "銀ブロック", "Soularium Block": "ソウラリウムブロック",
    "Steel Block": "鋼鉄ブロック", "Tin Block": "スズブロック", "Unobtainium - Allthemodium Alloy Block": "アンオブタニウム-オールザモジウム合金ブロック",
    "Unobtainium - Vibranium Alloy Block": "アンオブタニウム-ヴィブラニウム合金ブロック", "Unobtainium Block": "アンオブタニウムブロック",
    "Uranium Block": "ウランブロック", "Vibranium - Allthemodium Alloy Block": "ヴィブラニウム-オールザモジウム合金ブロック",
    "Vibranium Block": "ヴィブラニウムブロック", "Vibrant Alloy Block": "ヴァイブラント合金ブロック", "Wax Block": "蝋ブロック", "Zinc Block": "亜鉛ブロック",
}
miss = json.loads(Path("extracted/allthecompressed.json").read_text(encoding="utf-8"))["missing"]
out, left = {}, []
for k, v in miss.items():
    m = re.fullmatch(r"block\.allthecompressed\.(.+)_(\d)x", k)
    vm = re.fullmatch(r"(.+) (\d)x", v)
    if m and vm:
        base = van.get(f"block.minecraft.{m.group(1)}") or MOD.get(vm.group(1))
        if base:
            out[k] = f"{base}({m.group(2)}重圧縮)"
            continue
    left.append((k, v))
FIX = {"AllTheCompressed": "AllTheCompressed", "Total blocks: %s": "ブロックの総数: %s"}
for k, v in list(left):
    if v in FIX:
        out[k] = FIX[v]
        left.remove((k, v))
print(len(out), "/", len(miss), left[:20])
Path("tr/batch_11_atc_gen.json").write_text(json.dumps({"allthecompressed": out}, ensure_ascii=False, indent=1), encoding="utf-8")
