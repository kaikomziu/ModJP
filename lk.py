import json,sys
en=json.load(open('extracted/neovitae.json',encoding='utf-8'))['en_us']
ja=json.load(open('pack/assets/neovitae/lang/ja_jp.json',encoding='utf-8'))
for t in sys.argv[1:]:
    hits=[(k,ja.get(k)) for k,v in en.items() if v==t and not k.startswith('book.')]
    print(t,'=>',[h[1] for h in hits][:3])
