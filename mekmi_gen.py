"""mekmi(Mekanism Industrialization)の「<ティア> [Compact] <機械名>」を生成 → tr/batch_17_mekmi_gen.json"""
import json, re
from pathlib import Path

WORK = Path(__file__).parent
MACH = {
    "Electric Blast Furnace": "電気溶鉱炉", "Wiremill": "伸線機", "Water Pump": "給水ポンプ", "Vacuum Freezer": "真空冷凍機",
    "Unpacker": "開梱機", "Universal Factory": "万能工場", "Replicator": "複製機", "Pressurizer": "加圧機",
    "Polarizer": "偏極器", "Plasma Turbine": "プラズマタービン", "Packer": "梱包機", "Oil Drilling Rig": "石油掘削リグ",
    "Nuclear Reactor": "原子炉", "Mixer": "ミキサー", "Macerator": "粉砕機",
    "High-Pressure Advanced Large Steam Boiler": "高圧高度大型蒸気ボイラー", "High-Pressure Large Steam Boiler": "高圧大型蒸気ボイラー",
    "Advanced Large Steam Boiler": "高度大型蒸気ボイラー", "Large Steam Turbine": "大型蒸気タービン",
    "Large Steam Boiler": "大型蒸気ボイラー", "Large Diesel Generator": "大型ディーゼル発電機",
    "Implosion Compressor": "爆縮圧縮機", "Heat Exchanger": "熱交換器", "Fusion Reactor": "核融合炉",
    "Forge Hammer": "鍛造ハンマー", "Electrolyzer": "電解槽", "Electric Quarry": "電気採石機", "Electric Furnace": "電気炉",
    "Distillery": "蒸留器", "Distillation Tower": "蒸留塔", "Diesel Generator": "ディーゼル発電機",
    "Cutting Machine": "切断機", "Crusher": "破砕機", "Compressor": "圧縮機", "Coke Oven": "コークス炉",
    "Chemical Reactor": "化学反応器", "Centrifuge": "遠心分離機", "Boiler": "ボイラー", "Assembler": "組立機",
    "Purifying Chamber": "精製室", "Pressurized Reaction Base": "加圧反応室", "Oxidation Chamber": "酸化室",
    "Enriching Machine": "濃縮機", "Chemical Output Hatch": "化学物質出力ハッチ", "Chemical Input Hatch": "化学物質入力ハッチ",
    "Chemical Injection Chamber": "化学物質注入室",
}
TIER = {"Basic": "基本", "Advanced": "高度", "Elite": "エリート", "Ultimate": "究極", "Absolute": "絶対",
        "Supreme": "至高", "Cosmic": "宇宙", "Infinite": "無限", "Paradox Infinite": "パラドックス無限"}
RE = re.compile(r"^(?:(Paradox Infinite|Basic|Advanced|Elite|Ultimate|Absolute|Supreme|Cosmic|Infinite) )?(Compact )?("
                + "|".join(sorted(map(re.escape, MACH), key=len, reverse=True)) + r")$")
m = json.loads((WORK / "extracted/mekmi.json").read_text(encoding="utf-8"))["missing"]
out = {}
for k, v in m.items():
    r = RE.match(v)
    if not r:
        continue
    s = ""
    if r.group(1):
        s += TIER[r.group(1)] + "の"
    if r.group(2):
        s += "コンパクト"
    out[k] = s + MACH[r.group(3)]
(WORK / "tr/batch_17_mekmi_gen.json").write_text(json.dumps({"mekmi": out}, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(out))
