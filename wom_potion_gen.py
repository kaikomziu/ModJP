"""Weapons of Miracles の強化/延長ポーション名をバニラ公式訳 + (強化)/(延長) で生成する。"""
import json, re
from pathlib import Path
ja = json.loads(Path("vanilla/ja_jp.json").read_text(encoding="utf-8"))
ALIAS = {"jump_boost": "leaping", "speed": "swiftness", "instant_health": "healing", "instant_damage": "harming"}
miss = json.loads(Path("extracted/wom.json").read_text(encoding="utf-8"))["missing"]
out = {}
for k in miss:
    m = re.fullmatch(r"item\.minecraft\.(potion|splash_potion|lingering_potion|tipped_arrow)\.effect\.(longer|stronger)_(\w+)", k)
    if m:
        kind, mod, eff = m.groups()
        base = ja[f"item.minecraft.{kind}.effect.{ALIAS.get(eff, eff)}"]
        out[k] = base + ("(延長)" if mod == "longer" else "(強化)")
Path("tr/batch_03_wom_potion_gen.json").write_text(json.dumps({"wom": out}, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(out))
