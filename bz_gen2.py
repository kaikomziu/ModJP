# The Bumblezone の発光する蝋・古代の蝋の説明文(色違い)を生成する
from pathlib import Path
COL = {'red': '赤', 'purple': '紫', 'blue': '青', 'green': '緑', 'yellow': '黄', 'white': '白'}
TAIL = ('とても爆発に強い。\\n\\n剣かハサミで右クリックするとブロックの向きを変えられる。過去にハチの精髄を使ったプレイヤーがこのブロックの上に立つと、'
        '移動速度上昇、耐性、ハチエネルギーの効果を得る。\\n\\n過去にハチの精髄を使っていない者がこのブロックの上に立つと、代わりに移動速度低下、採掘速度低下、弱体化の効果を受ける…')
HEAD = {
    'channel': ('はかない不思議な力を宿した空の溝で、', '{c}色の異界の力を道に沿って導く溝で、'),
    'corner': ('不思議な力がまだ少し残っている空の角の溝で、', '{c}色の異界の力があふれる角の溝で、'),
    'node': ('不思議な力がまだ少し残っている空の節で、', '{c}色の異界の力があふれる節で、'),
}
out = ['## the_bumblezone']
for part, (empty, full) in HEAD.items():
    out.append(f'the_bumblezone.luminescent_wax_{part}.description\t {empty}{TAIL}')
    for c, j in COL.items():
        out.append(f'the_bumblezone.luminescent_wax_{part}_{c}.description\t {full.format(c=j)}{TAIL}')
WAX = '何世紀もかけて固くなった古い彫刻の蝋。正体不明の不思議な力が宿っていて、とても爆発に強い。'
out.append('= Old carved wax that has significantly hardened over centuries. It has become imbued with strange unknown power and is highly resistant to explosions. '
           "\\n\\nRight click with Sword or Shears to change this block's pattern. \\n\\nThose that have not consumed Essence of the Bees in past will get Slowness, "
           'Mining Fatigue, and Weakness instead when standing on this block...'
           f'\t {WAX}\\n\\n剣かハサミで右クリックするとブロックの模様を変えられる。\\n\\n過去にハチの精髄を使っていない者がこのブロックの上に立つと、代わりに移動速度低下、採掘速度低下、弱体化の効果を受ける…')
Path('tsv/v17_bz8_gen.tsv').write_text('\n'.join(out) + '\n', encoding='utf-8')
print(len(out) - 1)
