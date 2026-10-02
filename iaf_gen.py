# iceandfire の旗の模様の色違い説明・竜の卵/鱗/防具などを公式訳の用語で生成
import re, sys
sys.stdout.reconfigure(encoding='utf-8')
COL = {'black':'黒色','blue':'青色','brown':'茶色','cyan':'青緑色','gray':'灰色','green':'緑色','light_blue':'空色','light_gray':'薄灰色',
 'lime':'黄緑色','magenta':'赤紫色','orange':'橙色','pink':'桃色','purple':'紫色','red':'赤色','white':'白色','yellow':'黄色'}
PAT = {'amphithere':'アンピプテラ','bird':'鳥','dread':'恐怖軍','eye':'単眼','fae':'妖精の印章','feather':'羽','fire':'火竜','fire_head':'火竜の頭',
 'gorgon':'ゴルゴンの頭','hippocampus':'ヒッポカムポス','hippogryph_head':'ヒッポグリフの頭','ice':'氷竜','ice_head':'氷竜の頭','lightning':'雷竜',
 'lightning_head':'雷竜の頭','mermaid':'セイレーン','sea_serpent':'シーサーペント','troll':'トロールの頭','weezer':'Weezer'}
DC = {'red':'赤','green':'緑','bronze':'青銅','gray':'灰','blue':'青','white':'白','sapphire':'サファイア','silver':'銀','electric':'電気',
 'amethyst':'アメジスト','copper':'銅','black':'黒'}
SC = {'blue':'青','bronze':'青銅','deepblue':'深い青','green':'緑','purple':'紫','red':'赤','teal':'青緑'}
PART = {'helmet':'ヘルメット','chestplate':'チェストプレート','leggings':'レギンス','boots':'ブーツ'}
MAT = {'iron':'鉄','copper':'銅','silver':'銀','gold':'金','diamond':'ダイヤ','netherite':'ネザライト','dragon_steel_fire':'火竜鋼','dragon_steel_ice':'氷竜鋼',
 'dragon_steel_lightning':'雷竜鋼'}
DPART = {'head':'頭','neck':'首','body':'胴','tail':'尾'}
out = ['## iceandfire']
for line in open('cur_iaf.txt', encoding='utf-8'):
    k, v = line.rstrip('\n').split('\t', 1)
    r = None
    m = re.fullmatch(r'item\.iceandfire\.banner_pattern_(\w+?)\.desc\.(\w+)', k)
    if m and m.group(1) in PAT and m.group(2) in COL: r = COL[m.group(2)]+'の'+PAT[m.group(1)]
    m = re.fullmatch(r'item\.iceandfire\.dragonegg_(\w+)', k)
    if m and m.group(1) in DC: r = DC[m.group(1)]+'のドラゴンの卵'
    m = re.fullmatch(r'item\.iceandfire\.dragonscales_(\w+)', k)
    if m and m.group(1) in DC: r = DC[m.group(1)]+'のドラゴンの鱗'
    m = re.fullmatch(r'item\.iceandfire\.armor_(\w+?)_(helmet|chestplate|leggings|boots)', k)
    if m and m.group(1) in DC: r = DC[m.group(1)]+'のドラゴンの鱗の'+PART[m.group(2)]
    m = re.fullmatch(r'item\.iceandfire\.tide_(\w+?)_(helmet|chestplate|leggings|boots)', k)
    if m and m.group(1) in SC: r = SC[m.group(1)]+'のシーサーペントの鱗の'+PART[m.group(2)]
    m = re.fullmatch(r'item\.iceandfire\.dragonarmor_(\w+?)_(head|neck|body|tail)', k)
    if m and m.group(1) in MAT: r = MAT[m.group(1)]+'のドラゴン用装備(' + DPART[m.group(2)] + ')'
    m = re.fullmatch(r'item\.iceandfire\.dragonarmor_(dragon_steel_\w+|netherite)', k)
    if m and m.group(1) in MAT: r = MAT[m.group(1)]+'のドラゴン用装備'
    if r: out.append(k+'\t'+r)
open('tsv/v14_iaf_gen.tsv', 'w', encoding='utf-8').write('\n'.join(out)+'\n')
print(len(out)-1)
