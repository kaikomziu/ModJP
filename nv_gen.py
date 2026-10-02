# Neo Vitae(26.1.2)のダンジョン系ブロック名を生成
import re
from pathlib import Path
ASP = {"Ruina":"ルイナの","Nihilum":"ニヒルムの","Invictus":"インウィクトゥスの","Vindicta":"ウィンディクタの"}
BASE = {"Dungeon Brick":"ダンジョンレンガ","Dungeon Brick 2":"ダンジョンレンガ2","Dungeon Brick 3":"ダンジョンレンガ3",
"Dungeon Brick Gate":"ダンジョンレンガの門","Dungeon Brick Slab":"ダンジョンレンガのハーフブロック","Dungeon Brick Stairs":"ダンジョンレンガの階段",
"Dungeon Brick Wall":"ダンジョンレンガの塀","Dungeon Eye":"ダンジョンの目","Dungeon Metal":"ダンジョンの金属","Dungeon Pillar Cap":"ダンジョンの柱頭",
"Dungeon Pillar":"ダンジョンの柱","Special Dungeon Pillar":"特殊なダンジョンの柱","Polished Dungeon Stone":"磨かれたダンジョン石",
"Polished Dungeon Stone Gate":"磨かれたダンジョン石の門","Polished Dungeon Stone Slab":"磨かれたダンジョン石のハーフブロック",
"Polished Dungeon Stone Stairs":"磨かれたダンジョン石の階段","Polished Dungeon Stone Wall":"磨かれたダンジョン石の塀",
"Small Dungeon Brick":"小さなダンジョンレンガ","Dungeon Stone":"ダンジョン石","Dungeon Stone Slab":"ダンジョン石のハーフブロック",
"Dungeon Stone Stairs":"ダンジョン石の階段","Dungeon Stone Wall":"ダンジョン石の塀","Dungeon Tile":"ダンジョンタイル",
"Dungeon Tile Slab":"ダンジョンタイルのハーフブロック","Dungeon Tile Wall":"ダンジョンタイルの塀","Special Dungeon Tile":"特殊なダンジョンタイル"}
out = ["## neovitae"]
for l in open("cur_nv_ui.txt", encoding="utf-8"):
    k, v = l.rstrip("\n").split("\t", 1)
    if not k.startswith("block.neovitae.dungeon_"): continue
    a, _, b = v.partition(" ")
    if a in ASP and b in BASE: out.append(f"{k}\t{ASP[a]}{BASE[b]}")
    elif v in BASE: out.append(f"{k}\t{BASE[v]}")
Path("tsv/v14_nv_gen.tsv").write_text("\n".join(out) + "\n", encoding="utf-8")
print(len(out) - 1)
