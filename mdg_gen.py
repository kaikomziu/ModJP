# mekanismdieselgenerators の発電機名×部品、動作音の字幕を生成する(残りは tsv/v18_mdg*.tsv で手訳)
import json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
MAC = {'V16 Diesel Genset': 'V16ディーゼル発電機', 'V12 Diesel Genset': 'V12ディーゼル発電機', 'V8 Diesel Genset': 'V8ディーゼル発電機',
       'Inline-6 Diesel Genset': '直列6気筒ディーゼル発電機', 'Petrol V8 Genset': 'ガソリンV8発電機', 'Turboshaft Genset': 'ターボシャフト発電機',
       'Gas Turbine Genset': 'ガスタービン発電機', 'Marine 2-Stroke Genset': '船舶用2ストローク発電機', '1.9 TDI': '1.9 TDI',
       'Three-phase motor': '三相モーター'}
PART = {'Radiator': 'ラジエーター', 'Engine': 'エンジン', 'Generator': '発電部', 'Turbocharger': 'ターボチャージャー',
        'Generator Blower': '発電部の送風機', 'Control Cabinet': '制御盤', 'Turbine': 'タービン', 'Enclosure': '外装',
        'Air Filter House': '吸気フィルター室', 'Heat Recovery Steam Generator': '排熱回収ボイラー', 'Alternator': '交流発電機',
        'Bedplate': '台板', 'Scavenge Air': '掃気', 'Cylinders': 'シリンダー', 'Exhaust Receiver': '排気集合管'}
VERB = {'idles': 'がアイドリングする', 'slows down': 'が減速する', 'speeds up': 'が加速する', 'stops': 'が止まる', 'starts': 'が始動する',
        'shuts down': 'が停止する', 'runs at full power': 'が全開で動く', 'runs at half load': 'が半負荷で動く',
        'runs at full load': 'が全負荷で動く', 'starter cranks': 'のセルモーターが回る', 'runs': 'が動く', 'hums': 'がうなる',
        'runs down': 'が止まっていく'}
MR = '|'.join(sorted(map(re.escape, MAC), key=len, reverse=True))
PR = '|'.join(sorted(map(re.escape, PART), key=len, reverse=True))
VR = '|'.join(sorted(map(re.escape, VERB), key=len, reverse=True))
d = json.loads(Path('extracted/mekanismdieselgenerators.json').read_text(encoding='utf-8'))
out = ['## mekanismdieselgenerators']
for k, v in d['missing'].items():
    t = None
    m = re.fullmatch(rf'({MR}) \(({PR})\)', v)
    if m: t = f'{MAC[m.group(1)]}({PART[m.group(2)]})'
    m = re.fullmatch(rf'({MR})', v)
    if m and k.startswith('machine.'): t = MAC[v]
    m = re.fullmatch(rf'({MR}) ({VR})( \(\w+\))?', v, re.I)
    if m and k.startswith('subtitles.'):
        mac = next(x for x in MAC if x.lower() == m.group(1).lower())
        t = MAC[mac] + VERB[m.group(2)] + (m.group(3) or '')
    if t: out.append(f'{k}\t{t}')
Path('tsv/v18_mdg_gen.tsv').write_text('\n'.join(out) + '\n', encoding='utf-8')
print(len(out) - 1)
