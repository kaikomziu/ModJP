"""別インスタンスの mods から、____ (2) に無いMOD ID のjarだけをコピーする。
python copy_instance_mods.py "<インスタンス名>" <一覧ファイル名>"""
import zipfile, re, shutil, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
INST = Path(r"C:\Users\4yoma\curseforge\minecraft\Instances")
A = INST / sys.argv[1] / "mods"
B = INST / "____ (2)" / "mods"


def ids(j):
    try:
        z = zipfile.ZipFile(j)
        names = z.namelist()
        for n in ("META-INF/mods.toml", "fabric.mod.json"):
            if n in names:
                t = z.read(n).decode("utf-8", "replace")
                return set(re.findall(r'modId\s*=\s*"([^"]+)"', t)) or set(re.findall(r'"id"\s*:\s*"([^"]+)"', t)[:1])
    except Exception as e:
        print("err", j.name, e)
    return set()


have = set()
for j in B.glob("*.jar"):
    have |= ids(j)
copy, skip = [], []
for j in sorted(A.glob("*.jar")):
    if (B / j.name).exists():
        continue
    i = ids(j)
    (skip if i and i <= have else copy).append((j.name, sorted(i)))
print("COPY", len(copy))
for c in copy:
    print(" ", c)
print("SKIP(同じMOD IDの別バージョンが既にある)", len(skip))
for s in skip:
    print(" ", s)
for n, _ in copy:
    shutil.copy2(A / n, B / n)
(Path(__file__).parent / sys.argv[2]).write_text("\n".join(n for n, _ in copy) + "\n", encoding="utf-8")
