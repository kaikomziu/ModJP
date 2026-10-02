# 改行(\n)の数が固定の長文を、和訳文から自動で行分割して TSV に出す汎用ツール
# 使い方: python wrap_gen.py wrap/xxx.tsv   → tsv/v11_wrap_xxx.tsv を生成
# 入力: 1行目 "## ns"、以降 "キー<TAB>和訳"。和訳中の "|" は改行位置の希望(数が合わなければ自動調整)。
# 英文側の ${...} 参照はそのまま保持、行頭の空白も英文に合わせる。
import json, re, sys, os
REF = re.compile(r'\$\{[^}]+\}')
PUNCT = '、。)」:'
SOFT = 'をにがはでとへもや'

def chunk(s, n):
    if n <= 1:
        return [s]
    L = len(s); out = []; start = 0
    for i in range(1, n):
        t = round(L * i / n); best = t; found = False
        for chars in (PUNCT, SOFT):
            for dl in range(7):
                hit = [c for c in (t + dl, t - dl) if start < c < L and s[c - 1] in chars]
                if hit:
                    best = hit[0]; found = True; break
            if found:
                break
        best = min(max(best, start + 1), L - (n - i))
        while best < L and s[best - 1] == '§':
            best += 1
        out.append(s[start:best]); start = best
    out.append(s[start:])
    return out

def build(e, ja):
    slots = []
    for ln in e.split('\n'):
        m = REF.search(ln)
        slots.append([ln[:m.start()] if m else ln, ln[m.start():] if m else ''])
    prose = [i for i, (p, s) in enumerate(slots) if p.strip()]
    if not prose:
        return e
    segs = [x for x in ja.split('|')]
    while len(segs) < len(prose):
        j = max(range(len(segs)), key=lambda x: len(segs[x]))
        segs[j:j + 1] = chunk(segs[j], 2)
    while len(segs) > len(prose):
        segs[-2:] = [segs[-2] + segs[-1]]
    for i, sg in zip(prose, segs):
        slots[i][0] = (' ' if slots[i][0].startswith(' ') else '') + (sg.lstrip(' ') if slots[i][0].startswith(' ') else sg)
    return '\n'.join(p + s for p, s in slots)

src = sys.argv[1]
rows = open(src, encoding='utf-8').read().splitlines()
ns = rows[0][3:].strip()
en = json.load(open('extracted/%s.json' % ns, encoding='utf-8'))['en_us']
res = {}
for r in rows[1:]:
    if not r.strip() or '\t' not in r:
        continue
    k, ja = r.split('\t', 1)
    if k not in en:
        print('no key', k); continue
    out = build(en[k], ja)
    assert out.count('\n') == en[k].count('\n'), k
    assert REF.findall(out) == REF.findall(en[k]), k
    res[k] = out
name = os.path.splitext(os.path.basename(src))[0]
lines = ["## " + ns] + [k + "\t" + v.replace("\n", "\\n") for k, v in res.items()]
open('tsv/v11_wrap_%s.tsv' % name, 'w', encoding='utf-8').write("\n".join(lines) + "\n")
print(len(res))
