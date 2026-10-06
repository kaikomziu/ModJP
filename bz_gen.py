# The Bumblezone の色違い・定型名を生成し、残りを td/the_bumblezone_rest.txt に書き出す
import sys, re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
TD = Path(sys.argv[1])
COL = {'white': '白色', 'orange': '橙色', 'magenta': '赤紫色', 'light_blue': '空色', 'yellow': '黄色', 'lime': '黄緑色', 'pink': '桃色',
       'gray': '灰色', 'light_gray': '薄灰色', 'cyan': '青緑色', 'purple': '紫色', 'blue': '青色', 'brown': '茶色', 'green': '緑色',
       'red': '赤色', 'black': '黒色'}
BANNER = {'bee': 'ハチ', 'honeycombs': 'ハニカム', 'swords': '剣', 'sun': '太陽', 'pluses': '十字', 'peace': 'ピースマーク', 'arrows': '矢', 'eyes': '目'}
out, rest = ['## the_bumblezone'], []
for line in open(TD / 'the_bumblezone.txt', encoding='utf-8'):
    k, v = line.rstrip('\n').split('\t', 1)
    t = None
    m = re.fullmatch(r'block\.the_bumblezone\.super_candle_base_(\w+)', k)
    if m and m.group(1) in COL: t = f'{COL[m.group(1)]}のスーパーキャンドルの台'
    m = re.fullmatch(r'item\.the_bumblezone\.super_candle_(\w+)', k)
    if m and m.group(1) in COL: t = f'{COL[m.group(1)]}のスーパーキャンドル'
    m = re.fullmatch(r'block\.the_bumblezone\.string_curtain_(\w+)', k)
    if m and m.group(1) in COL: t = f'{COL[m.group(1)]}の糸のカーテン'
    m = re.fullmatch(r'block\.the_bumblezone\.luminescent_wax_(channel|corner|node)(?:_(\w+))?', k)
    if m:
        part = {'channel': '溝', 'corner': '角', 'node': '節'}[m.group(1)]
        t = f"発光する蝋の{part}" + (f"({COL[m.group(2)].rstrip('色')})" if m.group(2) else '')
    m = re.fullmatch(r'block\.the_bumblezone\.essence_block_(\w+)', k)
    if m and m.group(1) in COL: t = f'{COL[m.group(1)]}の精髄ブロック'
    m = re.fullmatch(r'block\.minecraft\.banner\.the_bumblezone\.(\w+)\.(\w+)', k)
    if m and m.group(1) in BANNER and m.group(2) in COL: t = f'{COL[m.group(2)]}の{BANNER[m.group(1)]}'
    (out.append(f'{k}\t{t}') if t else rest.append(line.rstrip('\n')))
Path('tsv/v17_bz_gen.tsv').write_text('\n'.join(out) + '\n', encoding='utf-8')
(TD / 'the_bumblezone_rest.txt').write_text('\n'.join(rest) + '\n', encoding='utf-8')
print('gen', len(out) - 1, 'rest', len(rest))
