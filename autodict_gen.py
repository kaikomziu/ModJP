"""公式訳(バニラ+全jarのja_jp)と自前訳から「英文→訳」辞書を作り、
未訳キーのうち英文が辞書に完全一致するものを自動で訳す → tr/batch_20_autodict.json

- 同じ英文に複数の訳がある場合は最多の訳を採用(同数なら公式訳優先)。
- 数字だけ・1文字の英文、書式トークンが合わない訳は使わない。
- 「X socket」「§6X§r」(tetranomicon の宝石ソケット)のような単純パターンも辞書で組み立てる。
- tsv の手訳(batch_tsv_*)のほうが後に読み込まれるので、そちらが優先される。
"""
import json, re, glob, collections
from pathlib import Path
from build import fmt_tokens

WORK = Path(__file__).parent
TR = WORK / "tr"
OUT = TR / "batch_20_autodict.json"

votes = collections.defaultdict(collections.Counter)


def add(en, ja, w):
    if not isinstance(en, str) or not isinstance(ja, str):
        return
    en, ja = en.strip(), ja.strip()
    if not en or not ja or en == ja or len(en) < 2 or en.isdigit():
        return
    if fmt_tokens(en) != fmt_tokens(ja):
        return
    votes[en][ja] += w


ven = json.loads((WORK / "vanilla/en_us.json").read_text(encoding="utf-8"))
vja = json.loads((WORK / "vanilla/ja_jp.json").read_text(encoding="utf-8"))
for k, v in ven.items():
    if k in vja:
        add(v, vja[k], 3)

ext = {}
for f in glob.glob(str(WORK / "extracted" / "*.json")):
    d = json.loads(Path(f).read_text(encoding="utf-8"))
    ext[d["namespace"]] = d
    for k, v in d["en_us"].items():
        if k in d["ja_jp"]:
            add(v, d["ja_jp"][k], 2)

# 自前訳(この生成物自身は除く)。訳済みキーは自動訳の対象外にする
done = collections.defaultdict(set)
for p in sorted(TR.glob("batch_*.json")):
    if p == OUT:
        continue
    for ns, kv in json.loads(p.read_text(encoding="utf-8")).items():
        en = ext.get(ns, {}).get("en_us", {})
        done[ns] |= set(kv)
        for k, ja in kv.items():
            if k in en:
                add(en[k], ja, 1)

def agreed(c):
    """訳が割れている英文は使わない(1語の汎用語は文脈で訳が変わるため)。"""
    ja, top = c.most_common(1)[0]
    total = sum(c.values())
    return len(c) == 1 or top / total >= 0.6


dic = {en: c.most_common(1)[0][0] for en, c in votes.items() if agreed(c)}
# 他MODの誤訳を拾ってしまうものの手当て
dic.update({"Willow Sign": "ヤナギの看板", "Willow Wall Sign": "壁に付けられたヤナギの看板",
            "Olive": "オリーブ"})
# 大文字小文字違いでも引けるように(Title Case と小文字の差だけ)
low = {}
for en, ja in dic.items():
    low.setdefault(en.lower(), ja)

CODE = re.compile(r"^((?:§[0-9a-fk-or])*)(.*?)((?:§[0-9a-fk-or])*)$")


def lookup(s):
    if s in dic:
        return dic[s]
    if s.lower() in low and not re.search(r"[%§{\n]", s):
        return low[s.lower()]
    m = CODE.match(s)
    if m and (m.group(1) or m.group(3)) and m.group(2) in dic:
        return m.group(1) + dic[m.group(2)] + m.group(3)
    m = re.match(r"^(.+) socket$", s)
    if m and m.group(1) in dic:
        return dic[m.group(1)] + "のソケット"
    return None


# UI 文言は文脈で訳が変わる(String→糸 など)ので、名前系のキーだけ自動訳する
NAME_KEY = re.compile(r"^(item|block|entity|fluid|fluid_type|effect|biome|enchantment|painting|trim_material|trim_pattern)\.|\.material\.[^.]+(\.prefix)?$")
official = set(vja)
for d in ext.values():
    official |= set(d["ja_jp"])

out, n = {}, 0
for ns, d in sorted(ext.items()):
    for k, v in d["missing"].items():
        if k in official or k in done[ns] or not NAME_KEY.search(k):
            continue
        ja = lookup(v.strip())
        if ja and fmt_tokens(ja) == fmt_tokens(v):
            if v != v.strip():  # 前後の空白は原文に合わせる
                ja = v[: len(v) - len(v.lstrip())] + ja + v[len(v.rstrip()):]
            ja = re.sub(r"の塀看板$", "の壁掛け看板", ja)
            out.setdefault(ns, {})[k] = ja
            n += 1
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"辞書 {len(dic)} 語 / 自動訳 {n} 件")
for ns, kv in sorted(out.items(), key=lambda x: -len(x[1]))[:25]:
    print(ns, len(kv))
