# v1.5: luminax(32色)・crystalix(16色×3種)・geore(鉱石×形状)・mcwpaths(1.20.1版)の名前を生成
import sys, re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
TD = Path(sys.argv[1])
COL = {'White':'白色','Orange':'橙色','Magenta':'赤紫色','Light Blue':'空色','Yellow':'黄色','Lime':'黄緑色','Pink':'桃色','Gray':'灰色',
 'Light Gray':'薄灰色','Cyan':'青緑色','Purple':'紫色','Blue':'青色','Brown':'茶色','Green':'緑色','Red':'赤色','Black':'黒色'}
def todo(ns):
    for line in open(TD / f'{ns}.txt', encoding='utf-8'):
        k, v = line.rstrip('\n').split('\t', 1)
        yield k, v

def color(s):
    for c in sorted(COL, key=len, reverse=True):
        if s.startswith(c + ' '): return COL[c], s[len(c)+1:]
    return None, s

out = []
# luminax
LSHAPE = {'Block':'ブロック','Button':'ボタン','Pressure Plate':'感圧板','Slab':'ハーフブロック','Stairs':'階段','Wall':'壁'}
out.append('## luminax'); miss = []
for k, v in todo('luminax'):
    dim = v.startswith('Dim ')
    c, rest = color(v[4:] if dim else v)
    m = re.fullmatch(r'Luminax (.+)', rest)
    if c and m and m.group(1) in LSHAPE:
        out.append(f"{k}\t{'暗い' if dim else ''}{c}のルミナックス{'' if m.group(1)=='Block' else 'の'}{LSHAPE[m.group(1)]}")
    elif k == 'itemGroup.luminax': out.append(f'{k}\tLuminax')
    else: miss.append(v)
# crystalix
CX = {'config.jade.plugin_crystalix.crystalix_block':'クリスタリックスのブロック','crystalix.configuration.max_wand_edit':'杖で一度に編集できる最大数',
 'crystalix.networking.cycle_property.failed':'クリスタリックスの設定変更をサーバーに送れなかった:','crystalix.property.ghost':'すり抜けモード',
 'crystalix.property.ghost.allow_all':'§2許可 §8すべて','crystalix.property.ghost.allow_animal':'§2許可 §a動物','crystalix.property.ghost.allow_monster':'§2許可 §cモンスター',
 'crystalix.property.ghost.allow_player':'§2許可 §bプレイヤー','crystalix.property.ghost.block_all':'§4遮断 §8すべて','crystalix.property.ghost.block_animal':'§4遮断 §a動物',
 'crystalix.property.ghost.block_monster':'§4遮断 §cモンスター','crystalix.property.ghost.block_player':'§4遮断 §bプレイヤー','crystalix.property.light':'光モード',
 'crystalix.property.light.dark':'§8暗い','crystalix.property.light.fake_light':'§5見せかけの光','crystalix.property.light.light':'§6光る','crystalix.property.light.none':'§7なし',
 'crystalix.property.reinforced':'補強モード','crystalix.property.reinforced.disabled':'無効','crystalix.property.reinforced.enabled':'有効',
 'crystalix.property.shadeless':'陰影なしモード','crystalix.property.shadeless.disabled':'無効','crystalix.property.shadeless.enabled':'有効',
 'crystalix.wand.bulk':'§7Shiftを押したままでまとめて編集','item.crystalix.crystalix_wand':'クリスタリックスの杖','itemGroup.crystalix':'Crystalix',
 'key.crystalix.category':'Crystalix','key.crystalix.cycle_ghost':'すり抜けモードを切り替え','key.crystalix.cycle_light':'光モードを切り替え',
 'key.crystalix.cycle_reinforced':'補強モードを切り替え','key.crystalix.cycle_shadeless':'陰影なしモードを切り替え'}
out.append('## crystalix')
for k, v in todo('crystalix'):
    if k in CX: out.append(f'{k}\t{CX[k]}'); continue
    c, rest = color(v)
    t = {'Crystalix Glass':'クリスタリックスガラス','Bordered Crystalix Glass':'縁取りのクリスタリックスガラス','Clear Crystalix Glass':'透明なクリスタリックスガラス'}.get(rest)
    (out.append(f'{k}\t{c}の{t}') if c and t else miss.append(v))
# geore
MAT = {'Allthemodium':'Allthemodium','Aluminum':'アルミニウム','Ancient Debris':'古代の残骸','Black Quartz':'ブラッククォーツ','Coal':'石炭','Copper':'銅',
 'Diamond':'ダイヤモンド','Emerald':'エメラルド','Gold':'金','Iron':'鉄','Lapis':'ラピスラズリ','Lead':'鉛','Monazite':'モナザイト','Nickel':'ニッケル',
 'Osmium':'オスミウム','Platinum':'プラチナ','Quartz':'クォーツ','Redstone':'レッドストーン','Ruby':'ルビー','Sapphire':'サファイア','Silver':'銀',
 'Tin':'スズ','Topaz':'トパーズ','Tungsten':'タングステン','Unobtainium':'アンオブタニウム','Uraninite':'閃ウラン鉱','Uranium':'ウラン',
 'Vibranium':'ヴィブラニウム','Zinc':'亜鉛'}
MR = '|'.join(sorted(map(re.escape, MAT), key=len, reverse=True))
GP = [(rf'Block Of ({MR}) GeOre', '{}のジオアブロック'), (rf'({MR}) GeOre Cluster', '{}のジオアの群晶'), (rf'({MR}) Tinted Glass', '{}の遮光ガラス'),
      (rf'Budding ({MR}) GeOre', '芽生えた{}のジオア'), (rf'Small ({MR}) GeOre Bud', '{}のジオアの小さな芽'), (rf'Medium ({MR}) GeOre Bud', '{}のジオアの中くらいの芽'),
      (rf'Large ({MR}) GeOre Bud', '{}のジオアの大きな芽'), (rf'({MR}) GeOre Shard', '{}のジオアのかけら'), (rf'({MR}) GeOre Spyglass', '{}のジオアの望遠鏡')]
out.append('## geore')
for k, v in todo('geore'):
    if k == 'itemGroup.geore': out.append(f'{k}\tGeOre'); continue
    for p, t in GP:
        m = re.fullmatch(p, v)
        if m: out.append(f'{k}\t' + t.format(MAT[m.group(1)])); break
    else: miss.append(v)
# mcwpaths(mp_gen.py の辞書を流用)
src = open('mp_gen.py', encoding='utf-8').read().split('def name')[0]
ns = {}; exec(src, ns)
out.append('## mcwpaths')
for k, v in todo('mcwpaths'):
    r = ns['FIX'].get(v)
    if not r:
        for m in sorted(ns['MAT'], key=len, reverse=True):
            if v.startswith(m + ' '):
                r = next((ns['MAT'][m] + t for p, t in ns['PAT'] if v[len(m)+1:] == p), None); break
    (out.append(f'{k}\t{r}') if r else miss.append(v))
Path('tsv/v15_gen.tsv').write_text('\n'.join(out) + '\n', encoding='utf-8')
print(len(out), 'miss', miss)
