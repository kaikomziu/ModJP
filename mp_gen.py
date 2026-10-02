# mcwpaths(Macaw's Paths)の名前を素材×模様で生成
import sys
sys.stdout.reconfigure(encoding='utf-8')
MAT = {'Oak Planks':'オークの板材','Spruce Planks':'トウヒの板材','Birch Planks':'シラカバの板材','Jungle Planks':'ジャングルの板材',
 'Acacia Planks':'アカシアの板材','Dark Oak Planks':'ダークオークの板材','Crimson Planks':'真紅の板材','Warped Planks':'歪んだ板材',
 'Mangrove Planks':'マングローブの板材','Cherry Planks':'サクラの板材','Bamboo Planks':'竹の板材','Pale Oak Planks':'ペールオークの板材',
 'Andesite':'安山岩','Diorite':'閃緑岩','Granite':'花崗岩','Red Sandstone':'赤い砂岩','Sandstone':'砂岩','Brick':'レンガ',
 'Mossy Cobblestone':'苔むした丸石','Cobblestone':'丸石','Cobbled Deepslate':'深層岩の丸石','Deepslate':'深層岩','Mud Brick':'泥レンガ',
 'Blackstone':'ブラックストーン','Dark Prismarine':'ダークプリズマリン','Mossy Stone':'苔むした石','Stone':'石'}
PAT = [('Diamond Paving','のひし形舗装'),('Basket Weave Paving','のかご編み舗装'),('Square Paving','の四角舗装'),('Honeycomb Paving','のハニカム舗装'),
 ('Clover Paving','のクローバー舗装'),('Dumble Paving','のダンベル舗装'),
 ('Running Bond Slab','の長手積みのハーフブロック'),('Running Bond Path','の長手積みの小道'),('Running Bond Stairs','の長手積みの階段'),('Running Bond','の長手積み'),
 ('Strewn Rocky Path','の石の散らばった小道'),
 ('Windmill Weave Path','の風車編みの小道'),('Windmill Weave Slab','の風車編みのハーフブロック'),('Windmill Weave Stairs','の風車編みの階段'),('Windmill Weave','の風車編み'),
 ('Flagstone Path','の敷石の小道'),('Flagstone Slab','の敷石のハーフブロック'),('Flagstone Stairs','の敷石の階段'),('Flagstone','の敷石'),
 ('Crystal Floor Path','の結晶模様の床の小道'),('Crystal Floor Slab','の結晶模様の床のハーフブロック'),('Crystal Floor Stairs','の結晶模様の床の階段'),('Crystal Floor','の結晶模様の床'),
 ('Path','の小道')]
FIX = {"Macaw's Paths & Pavings":"Macaw's Paths & Pavings",'Engrave by Right Clicking w/Pickaxe':'ツルハシで右クリックすると彫刻できる',
 'Flatten by Right Clicking w/Shovel':'シャベルで右クリックすると平らにできる','Dirt Path Block':'土の道ブロック','Podzol Path Block':'ポドゾルの道ブロック',
 'Sand Path Block':'砂の道ブロック','Red Sand Path Block':'赤い砂の道ブロック','Gravel Path Block':'砂利の道ブロック'}
def name(v):
    if v in FIX: return FIX[v]
    for m in sorted(MAT, key=len, reverse=True):
        if v.startswith(m+' '):
            rest = v[len(m)+1:]
            for p, t in PAT:
                if rest == p: return MAT[m]+t
    return None
out = ['## mcwpaths']; miss = []
for line in open('cur_mp.txt', encoding='utf-8'):
    k, v = line.rstrip('\n').split('\t', 1)
    r = name(v)
    (out.append(k+'\t'+r) if r else miss.append(line.strip()))
open('tsv/v14_mp_gen.tsv','w',encoding='utf-8').write('\n'.join(out)+'\n')
print(len(out)-1, miss)
