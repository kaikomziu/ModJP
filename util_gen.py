# utilitarian の色付き勧誘お断りカーペットを生成
COL = {'black':'黒色','blue':'青色','brown':'茶色','cyan':'青緑色','gray':'灰色','green':'緑色','light_blue':'空色','light_gray':'薄灰色',
 'lime':'黄緑色','magenta':'赤紫色','orange':'橙色','pink':'桃色','purple':'紫色','red':'赤色','white':'白色','yellow':'黄色'}
out = ['## utilitarian']
for c, j in COL.items():
    out.append(f'block.utilitarian.{c}_soliciting_carpet\t{j}の勧誘お断りカーペット')
    out.append(f'block.utilitarian.{c}_trapped_soliciting_carpet\t{j}の仕掛け勧誘お断りカーペット')
open('tsv/v14_util_gen.tsv', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
