"""Create: Dreams n' Desires の石材パレット・色付きブロックを Create本体の公式訳の語形に合わせて生成する。"""
import json, re
from pathlib import Path
from furn_common import COLOR

STONE = {"Amethyst Block": "アメジストブロック", "Basalt": "玄武岩", "Blackstone": "ブラックストーン",
         "Dolomite": "ドロマイト", "Gabbro": "斑れい岩", "Netherrack": "ネザーラック", "Packed Mud": "固めた泥",
         "Stone": "石", "Weathered Limestone": "風化した石灰岩"}
SHAPE = {"Slab": "ハーフブロック", "Stairs": "階段", "Wall": "塀"}
COL = {**COLOR, "Light": "明るい", "Raw": "未加工の"}
miss = json.loads(Path("extracted/create_dd.json").read_text(encoding="utf-8"))["missing"]
SR = "|".join(map(re.escape, sorted(STONE, key=len, reverse=True)))
CR = "|".join(map(re.escape, sorted(COL, key=len, reverse=True)))


def tr(v):
    m = re.fullmatch(rf"(Polished Cut |Cut |Small )?({SR})( Bricks?)?(?: (Slab|Stairs|Wall))?", v)
    if m:
        pre, st, brick, shape = m.groups()
        s = {"Polished Cut ": "磨かれた研がれた", "Cut ": "研がれた", "Small ": "小さな", None: ""}[pre] + STONE[st]
        if brick:
            s += "レンガ"
        if shape:
            s += "の" + SHAPE[shape]
        return s
    m = re.fullmatch(rf"Layered ({SR})", v)
    if m:
        return STONE[m.group(1)] + "の組石"
    m = re.fullmatch(rf"({SR}) Pillar", v)
    if m:
        return STONE[m.group(1)] + "の柱"
    m = re.fullmatch(rf"(?:({CR}) )?(Asphalt Block|Blueprint Block|Padded Rubber|Padded Mosaic Rubber|Padded Tiled Rubber)(?: (Slab|Stairs))?", v)
    if m:
        c, noun, shape = m.groups()
        n = {"Asphalt Block": "アスファルトブロック", "Blueprint Block": "設計図ブロック", "Padded Rubber": "クッションゴム",
             "Padded Mosaic Rubber": "モザイク模様のクッションゴム", "Padded Tiled Rubber": "タイル張りのクッションゴム"}[noun]
        s = (COL[c] + ("の" if c not in ("Light", "Raw") else "") if c else "") + n
        if shape:
            s += "の" + SHAPE[shape]
        return s
    return None


out = {k: t for k, v in miss.items() if (t := tr(v))}
# Light Blueprint Block は「明るい設計図ブロック」(light_blueprint_block)
Path("tr/batch_02_dd_gen.json").write_text(json.dumps({"create_dd": out}, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(out), "/", len(miss))
