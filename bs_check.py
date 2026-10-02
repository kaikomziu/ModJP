# 英文と訳文でリテラルのバックスラッシュ数が違うキーを列挙する
import json, glob, os
B = chr(92)
bad = 0
for f in glob.glob('pack/assets/*/lang/ja_jp.json'):
    ns = os.path.basename(os.path.dirname(os.path.dirname(f)))
    ja = json.load(open(f, encoding='utf-8'))
    ex = 'extracted/%s.json' % ns
    if not os.path.exists(ex):
        continue
    en = json.load(open(ex, encoding='utf-8'))['en_us']
    for k, v in ja.items():
        e = en.get(k)
        if isinstance(e, str) and isinstance(v, str) and e.count(B) != v.count(B):
            bad += 1
            print(ns, k, e.count(B), v.count(B))
print('total', bad)
