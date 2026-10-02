"""各MOD jarを展開せずに読み、en_us / ja_jp を取り出して未翻訳キーを抽出する。"""
import json, re, zipfile, sys
from pathlib import Path

MODS = Path(r"C:\Users\4yoma\curseforge\minecraft\Instances\____ (2)\mods")
WORK = Path(__file__).parent
OUT = WORK / "extracted"
BROKEN = []
LANG_RE = re.compile(r"^assets/([^/]+)/lang/(en_us|ja_jp)\.json$", re.I)


def load_json(raw: bytes):
    text = raw.decode("utf-8-sig", errors="replace")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # 一部MODはコメントや末尾カンマ入りのJSONを同梱している
        text = re.sub(r"^\s*//.*$", "", text, flags=re.M)
        text = re.sub(r",(\s*[}\]])", r"\1", text)
        # 行末のカンマ抜け(twilightforest の ja_jp など)。ゲーム側ではファイルごと読み飛ばされる
        text = re.sub(r'"(\s*\n\s*")', r'",\1', text)
        BROKEN.append(True)
        return json.loads(text, strict=False)


def main():
    OUT.mkdir(exist_ok=True)
    summary = []
    seen = set()
    # 別バージョン(ATM11: 26.1.2)から借りてきたjarは最後に処理し、既にある名前空間には混ぜない
    low = set((WORK / "atm11_added.txt").read_text(encoding="utf-8").split()) if (WORK / "atm11_added.txt").exists() else set()
    main_ns = set()
    for jar in sorted(MODS.glob("*.jar"), key=lambda j: (j.name in low, j.name)):
        with zipfile.ZipFile(jar) as z:
            langs = {}
            for name in z.namelist():
                m = LANG_RE.match(name)
                if m:
                    ns, lang = m.group(1), m.group(2).lower()
                    try:
                        BROKEN.clear()
                        langs.setdefault(ns, {})[lang] = load_json(z.read(name))
                        if BROKEN and lang == "ja_jp":
                            langs[ns]["ja_broken"] = True
                    except Exception as e:
                        print(f"!! parse error {jar.name}:{name}: {e}", file=sys.stderr)
        for ns, d in sorted(langs.items()):
            if jar.name in low and ns in main_ns:
                continue
            if jar.name not in low:
                main_ns.add(ns)
            en = {k: v for k, v in d.get("en_us", {}).items() if isinstance(v, str)}
            ja = d.get("ja_jp", {})
            if not en:
                continue
            prev = OUT / f"{ns}.json"
            if prev.exists() and ns in seen:
                p = json.loads(prev.read_text(encoding="utf-8"))
                en = {**p["en_us"], **en}; ja = {**p["ja_jp"], **ja}
            seen.add(ns)
            missing = {k: v for k, v in en.items() if k not in ja and v.strip() and not k.startswith("_")}
            (OUT / f"{ns}.json").write_text(json.dumps({
                "jar": jar.name, "namespace": ns,
                "en_us": en, "ja_jp": ja, "missing": missing,
                "ja_broken": d.get("ja_broken", False),
                "other_version": jar.name in low,
            }, ensure_ascii=False, indent=1), encoding="utf-8")
            summary.append((jar.name, ns, len(en), len(en) - len(missing), len(missing)))
    (WORK / "extract_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    for s in summary:
        print(*s, sep="\t")
    print("TOTAL missing:", sum(s[4] for s in summary))


if __name__ == "__main__":
    main()
