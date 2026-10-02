"""PneumaticCraft の色違いブロック(プラスチックブロック・壁ランプ)を生成 → tr/batch_13_pnc_gen.json"""
import json
from pathlib import Path

WORK = Path(__file__).parent
van = json.loads((WORK / "vanilla/ja_jp.json").read_text(encoding="utf-8"))
miss = json.loads((WORK / "extracted/pneumaticcraft.json").read_text(encoding="utf-8"))["missing"]
COLORS = ["black", "blue", "brown", "cyan", "gray", "green", "light_blue", "light_gray", "lime",
          "magenta", "orange", "pink", "purple", "red", "white", "yellow"]
out = {}
for c in COLORS:
    col = van["color.minecraft." + c]
    out[f"block.pneumaticcraft.plastic_brick_{c}"] = f"{col}のプラスチック建築ブロック™"
    out[f"block.pneumaticcraft.smooth_plastic_brick_{c}"] = f"滑らかな{col}のプラスチック建築ブロック™"
    out[f"block.pneumaticcraft.wall_lamp_{c}"] = f"{col}の壁ランプ"
    out[f"block.pneumaticcraft.wall_lamp_inverted_{c}"] = f"{col}の壁ランプ(反転)"
out = {k: v for k, v in out.items() if k in miss}
(WORK / "tr/batch_13_pnc_gen.json").write_text(json.dumps({"pneumaticcraft": out}, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(out))
