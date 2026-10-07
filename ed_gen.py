"""electrodynamics の色付きケーブル名を訳して tsv/v18_ed_gen.tsv に書く。"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from build import official_keys, effective_missing

NS = "electrodynamics"
d = json.loads(Path(f"extracted/{NS}.json").read_text(encoding="utf-8"))
missing = effective_missing(d, official_keys())
METAL = {"Copper": "銅", "Gold": "金", "Iron": "鉄", "Silver": "銀", "Superconductive": "超電導", "Tin": "スズ"}
KIND = {"Ceramic": "セラミックケーブル", "Thick": "高圧ケーブル", "Insulated": "絶縁ケーブル", "Logistical": "センサーケーブル"}
COL = {"Black": "黒", "Blue": "青", "Brown": "茶", "Cyan": "青緑", "Gray": "灰", "Green": "緑", "Light Blue": "空色",
       "Light Gray": "薄灰", "Lime": "黄緑", "Magenta": "赤紫", "Orange": "橙", "Pink": "桃", "Purple": "紫", "Red": "赤",
       "White": "白", "Yellow": "黄"}
out = {}
for k, v in missing.items():
    m = re.fullmatch(r"(Ceramic|Thick|Insulated|Logistical) (\w+) Wire \((.+)\)", v)
    if m and k.startswith("block."):
        out[k] = f"{METAL[m.group(2)]}{KIND[m.group(1)]}({COL[m.group(3)]})"
Path("tsv/v18_ed_gen.tsv").write_text("\n".join([f"## {NS}"] + [f"{k}\t{v}" for k, v in out.items()]) + "\n", encoding="utf-8")
print("gen", len(out))
