"""EMF のイージング関数説明(定型文)を生成する。"""
import json, re
from pathlib import Path
miss = json.loads(Path("extracted/entity_model_features.json").read_text(encoding="utf-8"))["missing"]
out = {}
for k, v in miss.items():
    m = re.fullmatch(r"(\w+\(k, x, y\))\nInterpolates between x and y using the (.+?) function\n\nexamples here: (https://easings\.net/)", v)
    if m:
        sig, fn, url = m.groups()
        fn = fn.replace("ease in and ease out", "ease in-out")
        out[k] = f"{sig}\n{fn} 関数で x と y の間を補間します\n\n例はこちら: {url}"
Path("tr/batch_05_emf_ease_gen.json").write_text(json.dumps({"entity_model_features": out}, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(out))
