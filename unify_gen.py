"""Create: Unify の金属アイテム/ブロック名をバニラの語形(鉄インゴット・鉄塊・深層岩鉄鉱石・鉄の原石ブロック)に合わせて生成する。"""
import json, re
from pathlib import Path

METAL = {"Aluminum": "アルミニウム", "Bauxite": "ボーキサイト", "Bronze": "青銅", "Cast Iron": "鋳鉄", "Constantan": "コンスタンタン",
         "Lead": "鉛", "Nickel": "ニッケル", "Platinum": "プラチナ", "Silver": "銀", "Tin": "スズ", "Tungsten": "タングステン",
         "Wolfram": "タングステン", "Uranium": "ウラン", "Electrum": "エレクトラム", "Invar": "インバー", "Steel": "鋼鉄",
         "Tarnished Gold": "くすんだ金", "Wrought Iron": "錬鉄", "Gay": "ゲイ"}
MR = "|".join(map(re.escape, sorted(METAL, key=len, reverse=True)))
SUF = {"Ingot": "インゴット", "Nugget": "塊", "Rod": "の棒", "Sheet": "板", "Wire": "ワイヤー", "Block": "ブロック", "Ore": "鉱石"}


def tr(v):
    m = re.fullmatch(rf"(Deepslate )?({MR}) (Ingot|Nugget|Rod|Sheet|Wire|Block|Ore)", v)
    if m:
        ds, metal, suf = m.groups()
        return ("深層岩" if ds else "") + METAL[metal] + SUF[suf]
    m = re.fullmatch(rf"Block of Raw ({MR})", v)
    if m:
        return METAL[m.group(1)] + "の原石ブロック"
    m = re.fullmatch(rf"(Crushed )?Raw ({MR})", v)
    if m:
        return ("砕いた" if m.group(1) else "") + METAL[m.group(2)] + "の原石"
    return {"Create: Unify": "Create: Unify"}.get(v)


miss = json.loads(Path("extracted/unify.json").read_text(encoding="utf-8"))["missing"]
out = {k: t for k, v in miss.items() if (t := tr(v))}
print(len(out), "/", len(miss), [v for k, v in miss.items() if k not in out])
Path("tr/batch_07_unify_gen.json").write_text(json.dumps({"unify": out}, ensure_ascii=False, indent=1), encoding="utf-8")
