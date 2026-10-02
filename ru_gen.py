# regions_unexplored のボート名を公式訳の木の名前で生成
W = {'baobab':'バオバブ','blackwood':'黒い木','cypress':'ヒノキ','dead':'枯れた木','eucalyptus':'ユーカリ','joshua':'ジョシュア','kapok':'カポック',
     'larch':'カラマツ','magnolia':'モクレン','maple':'カエデ','palm':'ヤシ','pine':'マツ','redwood':'セコイア','socotra':'リュウケツジュ',
     'willow':'ヤナギ','wisteria':'フジ'}
out = ['## regions_unexplored']
for w, j in W.items():
    for p in ('entity',):
        out.append(f'{p}.regions_unexplored.{w}_boat\t{j}のボート')
        out.append(f'{p}.regions_unexplored.{w}_chest_boat\tチェスト付きの{j}のボート')
open('tsv/v14_ru_gen.tsv', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
