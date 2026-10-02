# refinedtypes(Refined Storageのエネルギー/ソース/魂ストレージ)の訳を生成
import re, sys
sys.stdout.reconfigure(encoding='utf-8')
T = {'Energy':'エネルギー','Source':'ソース','Soul':'魂'}
FIX = {
 'refinedtypes.configuration.title':'Refined Types','refinedtypes.configuration.section.refinedtypes.common.toml':'Refined Types',
 'refinedtypes.configuration.section.refinedtypes.common.toml.title':'Refined Types','misc.refinedtypes.resource_type.energy':'エネルギー',
 'misc.refinedtypes.resource_type.source':'ソース','misc.refinedtypes.resource_type.soul':'魂','block.refinedtypes.network_energizer':'ネットワーク充電器',
 'item.refinedtypes.network_energizer.help':'ネットワーク内のエネルギーディスクに蓄えたエネルギーを自動で消費して、ネットワークを維持する。',
 'gui.refinedtypes.network_energizer.redstone_mode_help':'この装置が停止している間、ストレージネットワークの維持のためにエネルギーディスクのエネルギーは消費されない。',
 'item.refinedtypes.soul.help':'ヒント: レギュレーターアップグレードを使うと、エクスポーターが魂をすべて接続した魂のパイプに流し込むのを防げる',
}
out = ['## refinedtypes']
for line in open('cur_refinedtypes.txt', encoding='utf-8'):
    k, v = line.rstrip('\n').split('\t', 1)
    r = FIX.get(k)
    if r is None:
        m = re.fullmatch(r'(\w+|Infinite|Creative) (Energy|Source|Soul) Storage (Part|Disk|Block)', v)
        if m:
            size = {'Infinite':'無限の','Creative':'クリエイティブの'}.get(m.group(1), m.group(1)+' ')
            r = size + T[m.group(2)] + 'ストレージ' + {'Part':'パーツ','Disk':'ディスク','Block':'ブロック'}[m.group(3)]
    if r is None:
        m = re.fullmatch(r'Stores %s (Energy|FE|Source|Soul)\. When empty, use while holding to return the (\w+) Storage Part( and Machine Casing)?\. Upgradeable to a higher tier by combining with a \w+ Storage Part\.', v)
        if m:
            t = T.get(m.group(2)); unit = 'FE' if m.group(1)=='FE' else T[m.group(1)]
            ret = t+'ストレージパーツ' + ('と機械の外装' if m.group(3) else '')
            r = f'{unit}を%s蓄える。空のときに持って使うと{ret}に戻る。{t}ストレージパーツと組み合わせると上のティアに強化できる。'
    if r is None:
        m = re.fullmatch(r'Stores an infinite amount of (FE|Source|Soul)\.', v)
        if m: r = ('FE' if m.group(1)=='FE' else T[m.group(1)]) + 'を無限に蓄える。'
    if r is None:
        m = re.fullmatch(r'Has an infinitely amount of (FE|Source|Soul) already stored\.', v)
        if m: r = '最初から無限の' + ('FE' if m.group(1)=='FE' else T[m.group(1)]) + 'が蓄えられている。'
    if r is None:
        m = re.fullmatch(r'(\w+) Storage Disks', v)
        if m: r = T[m.group(1)] + 'ストレージディスク'
    if r is None:
        m = re.fullmatch(r'Storing (energies|sources|souls)', v)
        if m: r = {'energies':'エネルギーを蓄える','sources':'ソースを蓄える','souls':'魂を蓄える'}[m.group(1)]
    if r is None:
        m = re.fullmatch(r'Craft a (\w+) Storage Disk and put it in your Disk Drive', v)
        if m: r = T[m.group(1)] + 'ストレージディスクをクラフトしてディスクドライブに入れる'
    if r is None:
        m = re.fullmatch(r'(\w+) Storage Block', v)
        if m: r = T[m.group(1)] + 'ストレージブロック'
    if r is None:
        m = re.fullmatch(r'Configuration for the (\w+) Storage Blocks\.', v)
        if m: r = T[m.group(1)] + 'ストレージブロックの設定。'
    if r is None:
        m = re.fullmatch(r'(\w+|Infinite) (energy|source) usage', v)
        if m: r = ('無限' if m.group(1)=='Infinite' else m.group(1)) + 'の' + T[m.group(2).capitalize()] + '使用量'
    if r is None:
        m = re.fullmatch(r'The (energy|source) used by the (\w+|Infinite) (\w+) Storage Block\.', v)
        if m: r = ('無限の' if m.group(2)=='Infinite' else m.group(2)+' ') + T[m.group(3)] + 'ストレージブロックが使う' + T[m.group(1).capitalize()] + '。'
    if r: out.append(k+'\t'+r)
    else: print('miss', k, v)
open('tsv/v14_rt_gen.tsv','w',encoding='utf-8').write('\n'.join(out)+'\n')
print(len(out)-1)
