"""____ (2)/mods 内で同じMOD ID(mods.toml の [[mods]] 部分)を持つjarが複数ないか調べる"""
import zipfile, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
B = Path(r"C:\Users\4yoma\curseforge\minecraft\Instances\____ (2)\mods")


def prim(j):
    z = zipfile.ZipFile(j); n = z.namelist()
    if 'META-INF/mods.toml' in n:
        t = z.read('META-INF/mods.toml').decode('utf-8', 'replace')
        t = re.split(r'\[\[\s*dependencies', t)[0]
        return set(re.findall(r'modId\s*=\s*"([^"]+)"', t))
    if 'fabric.mod.json' in n:
        return set(re.findall(r'"id"\s*:\s*"([^"]+)"', z.read('fabric.mod.json').decode('utf-8', 'replace'))[:1])
    return set()


ids = {}
for j in sorted(B.glob('*.jar')):
    try:
        for i in prim(j):
            ids.setdefault(i, []).append((j.stat().st_mtime, j.name))
    except Exception as e:
        print('err', j.name, e)
for i, js in sorted(ids.items()):
    if len(js) > 1:
        print(i, [n for _, n in sorted(js)])
