import re
WOOD = {"Oak": "オーク", "Spruce": "トウヒ", "Birch": "シラカバ", "Jungle": "ジャングル", "Acacia": "アカシア",
        "Dark Oak": "ダークオーク", "Mangrove": "マングローブ", "Cherry": "サクラ", "Bamboo": "竹",
        "Crimson": "真紅", "Warped": "歪んだ"}
COLOR = {"White": "白色", "Orange": "橙色", "Magenta": "赤紫色", "Light Blue": "空色", "Yellow": "黄色",
         "Lime": "黄緑色", "Pink": "桃色", "Gray": "灰色", "Light Gray": "薄灰色", "Cyan": "青緑色",
         "Purple": "紫色", "Blue": "青色", "Brown": "茶色", "Green": "緑色", "Red": "赤色", "Black": "黒色",
         "Beige": "ベージュ"}
STONE = {"Stone": "石", "Granite": "花崗岩", "Diorite": "閃緑岩", "Andesite": "安山岩", "Deepslate": "深層岩",
         "Blackstone": "ブラックストーン", "Polished Blackstone": "磨かれたブラックストーン", "Cobblestone": "丸石",
         "Mossy Cobblestone": "苔むした丸石", "Smooth Stone": "なめらかな石", "Sandstone": "砂岩", "Red Sandstone": "赤い砂岩",
         "Quartz": "クォーツ", "Calcite": "方解石", "Tuff": "凝灰岩", "Basalt": "玄武岩", "Prismarine": "プリズマリン",
         "Purpur": "プルプァ", "End Stone": "エンドストーン", "Nether Brick": "ネザーレンガ", "Brick": "レンガ",
         "Mud Brick": "泥レンガ", "Polished Andesite": "磨かれた安山岩", "Polished Diorite": "磨かれた閃緑岩",
         "Polished Granite": "磨かれた花崗岩", "Polished Deepslate": "磨かれた深層岩", "Cobbled Deepslate": "深層岩の丸石",
         "Light": "明るい", "Dark": "暗い"}
MAT = {**STONE, **COLOR, **WOOD}
for k, v in WOOD.items():
    MAT["Stripped " + k] = "樹皮を剥いだ" + v
MAT_RE = "|".join(sorted(map(re.escape, MAT), key=len, reverse=True))
NAME_RE = re.compile(rf"^({MAT_RE}) (.+?)(?: \((Light|Dark)\))?$")
