"""tr/<ns>.json の翻訳を検証して ModJP_Pack リソースパックを書き出し、翻訳状況一覧を作る。

- 出力するのは「en_us にあって jar の ja_jp に無いキー」だけ(公式訳は上書きしない)。
- jar の ja_jp が壊れているMOD(ja_broken)も公式訳は同梱しない(他人の訳の再配布になるため)。
  BUNDLE_BROKEN_OFFICIAL を True にすると従来どおり公式訳ごと同梱する。
- 書式コード(%s, %1$s, %d, §a, \\n, {0} など)が原文と一致しない訳はエラーにする。
"""
import json, re, sys, glob, collections, shutil
from pathlib import Path

WORK = Path(__file__).parent
PACK = WORK / "pack"
BUNDLE_BROKEN_OFFICIAL = False
DESC = "§6MOD日本語化パック §7v1.6 (1.20.1)"
TR = WORK / "tr"
KEEP = TR / "_keep_english.json"   # {ns: {key: 理由}} 意味が判断できず英語のまま残すキー

FMT_RE = re.compile(r"%(?:\d+\$)?[-#+0,(]*\d*(?:\.\d+)?[sdfxXc%]|§[0-9a-fk-or]|\n|\{\d*\}|\$\([^)]*\)")


def fmt_tokens(s):
    # 語順を変えるために %s → %2$s のような位置指定に書き換えるのは正当なので、位置番号は無視して種類と個数で比べる
    return collections.Counter(re.sub(r"%\d+\$", "%", t) for t in FMT_RE.findall(s))


def load_translations():
    """tr/<ns>.json(単一MOD)と tr/batch_*.json({ns: {key: 訳}})をまとめて読む。"""
    all_tr = collections.defaultdict(dict)
    for p in sorted(TR.glob("*.json")):
        if p.name.startswith("_"):
            continue
        data = json.loads(p.read_text(encoding="utf-8"))
        if p.name.startswith("batch_"):
            for ns, d in data.items():
                dup = set(all_tr[ns]) & set(d)
                if dup:
                    print(f"[warn] {p.name}: {ns} の重複キー {sorted(dup)[:3]}")
                all_tr[ns].update(d)
        else:
            all_tr[p.stem].update(data)
    return all_tr


def official_keys():
    """ゲームが実際に読み込める公式訳のキー集合(ja_jpが壊れたMODの分は読み込めないので含めない)"""
    official = set(json.loads((WORK / "vanilla/ja_jp.json").read_text(encoding="utf-8")))
    for f in glob.glob(str(WORK / "extracted" / "*.json")):
        d = json.loads(Path(f).read_text(encoding="utf-8"))
        if d.get("ja_broken") and not BUNDLE_BROKEN_OFFICIAL:
            continue
        # 別バージョン(ATM11)から借りたjarの公式訳は、1.20.1の他MODのキーを隠す根拠にしない
        if d.get("other_version"):
            continue
        official |= set(d["ja_jp"])
    return official


def effective_missing(d, official):
    """訳すべきキー。ja_jpが壊れたMODは公式訳が読み込まれないので en_us 全体が対象"""
    src = d["en_us"] if (d.get("ja_broken") and not BUNDLE_BROKEN_OFFICIAL) else d["missing"]
    return {k: v for k, v in src.items() if k not in official}


def main():
    keep = json.loads(KEEP.read_text(encoding="utf-8")) if KEEP.exists() else {}
    all_tr = load_translations()
    rows, errors, kept_rows = [], [], []
    shutil.rmtree(PACK, ignore_errors=True)
    PACK.mkdir(parents=True, exist_ok=True)
    # 他のMOD(またはバニラ)が同じキーを公式に訳している場合はそちらを優先し、パックには入れない
    official = official_keys()
    for f in sorted(glob.glob(str(WORK / "extracted" / "*.json"))):
        d = json.loads(Path(f).read_text(encoding="utf-8"))
        ns, en, ja, missing = d["namespace"], d["en_us"], d["ja_jp"], d["missing"]
        missing = effective_missing(d, official)
        tr = all_tr.get(ns, {})
        kp = keep.get(ns, {})
        out = dict(ja) if (d.get("ja_broken") and BUNDLE_BROKEN_OFFICIAL) else {}
        done = 0
        for k, src in missing.items():
            if k in tr and tr[k] is not None:
                v = tr[k]
                if fmt_tokens(v) != fmt_tokens(src):
                    errors.append(f"{ns}:{k}\n  en: {src!r}\n  ja: {v!r}")
                    continue
                out[k] = v
                done += 1
            elif k in kp:
                kept_rows.append((d["jar"], ns, k, src, kp[k]))
        stray = set(tr) - set(missing)
        if stray:
            print(f"[warn] {ns}: 未翻訳リストに無いキー {len(stray)} 件を無視: {sorted(stray)[:3]}")
        left = len(missing) - done - sum(1 for k in missing if k in kp and k not in tr)
        rows.append((d["jar"], ns, len(en), len(en) - len(missing), len(missing), done,
                     len([k for k in missing if k in kp]), left, d.get("ja_broken")))
        if out:
            p = PACK / "assets" / ns / "lang" / "ja_jp.json"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    (PACK / "pack.mcmeta").write_text(json.dumps(
        {"pack": {"pack_format": 15, "description": DESC}}, ensure_ascii=False, indent=2), encoding="utf-8")

    write_status(rows, kept_rows)
    if errors:
        print(f"書式コード不一致 {len(errors)} 件:")
        print("\n".join(errors[:80]))
    tot = [sum(r[i] for r in rows) for i in (2, 3, 4, 5, 6, 7)]
    print(f"全キー {tot[0]} / 公式訳 {tot[1]} / 未翻訳 {tot[2]} / 今回訳 {tot[3]} / 英語のまま {tot[4]} / 残り {tot[5]}")
    return 1 if errors else 0


def write_status(rows, kept_rows):
    L = ["# 翻訳状況一覧", "",
         "「日本語済み」= jar同梱の公式ja_jpにあるキー数。「未翻訳」= en_usにあってja_jpに無いキー数(このパックの翻訳対象)。", "",
         "| MOD (jar) | 名前空間 | 全キー数 | 日本語済み | 未翻訳 | 今回翻訳 | 英語のまま | 備考 |",
         "|---|---|---:|---:|---:|---:|---:|---|"]
    for jar, ns, total, ja, miss, done, kept, left, broken in rows:
        note = []
        if broken:
            note.append("同梱ja_jpが壊れていて読み込まれないため公式訳ごと同梱")
        if left:
            note.append(f"未処理 {left}")
        L.append(f"| {jar} | {ns} | {total} | {ja} | {miss} | {done} | {kept} | {'; '.join(note)} |")
    s = lambda i: sum(r[i] for r in rows)
    L.append(f"| **合計** | | {s(2)} | {s(3)} | {s(4)} | {s(5)} | {s(6)} | |")
    L += ["", "## 英語のまま残したキー", "",
          "意味が判断できない・翻訳すると機能が壊れる等の理由で訳していないキー。", "",
          "| 名前空間 | キー | 原文 | 理由 |", "|---|---|---|---|"]
    esc = lambda t: t.replace("|", "\\|").replace("\n", "\\n")
    for jar, ns, k, src, why in kept_rows:
        L.append(f"| {ns} | `{k}` | {esc(src)} | {esc(why)} |")
    (WORK / "translation_status.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
