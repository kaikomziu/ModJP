"""Integrated Dynamics の定型キー(楽器の音・パーティクル)を生成 → tr/batch_14_id_gen.json"""
import json, re
from pathlib import Path

WORK = Path(__file__).parent
miss = json.loads((WORK / "extracted/integrateddynamics.json").read_text(encoding="utf-8"))["missing"]

INSTR = {"harp": "ハープ", "basedrum": "バスドラム", "snare": "スネアドラム", "hat": "ハイハット", "bass": "ベース",
         "flute": "フルート", "bell": "ベル", "guitar": "ギター", "chime": "チャイム", "xylophone": "木琴",
         "iron_xylophone": "鉄琴", "cow_bell": "カウベル", "didgeridoo": "ディジュリドゥ", "bit": "ビット",
         "banjo": "バンジョー", "pling": "プリング"}
PART = {
    "Ambient Entity": "環境エンティティ", "Angry Villager": "怒った村人", "Bubble": "泡", "Cloud": "雲",
    "Crit": "クリティカル", "Damage Indicator": "ダメージ表示", "Dragon Breath": "ドラゴンブレス",
    "Dripping Lava": "滴る溶岩", "Falling Lava": "落ちる溶岩", "Landing Lava": "着地した溶岩",
    "Dripping Water": "滴る水", "Falling Water": "落ちる水", "Effect": "効果", "Elder Guardian": "エルダーガーディアン",
    "Enchanted Hit": "エンチャントされた攻撃", "Enchanted": "エンチャント", "End Rod": "エンドロッド",
    "Entity": "エンティティ", "Explosion Emitter": "爆発エミッター", "Explosion": "爆発", "Sonic Boom": "ソニックブーム",
    "Firework": "花火", "Fishing": "釣り", "Flame": "炎", "Soul Fire Flame": "魂の炎", "Sculk Soul": "スカルクの魂",
    "Sculk Charge Pop": "スカルクのチャージ破裂", "Soul": "魂", "Flash": "閃光", "Happy Villager": "喜ぶ村人",
    "Composter": "コンポスター", "Heart": "ハート", "Instant Effect": "即時効果", "Slime": "スライム",
    "Snowball": "雪玉", "Large Smoke": "大きな煙", "Lava": "溶岩", "Mycelium": "菌糸", "Note": "音符",
    "Poof": "ポフッ", "Portal": "ポータル", "Rain": "雨", "Smoke": "煙", "Sneeze": "くしゃみ", "Spit": "つば",
    "Squid Ink": "イカスミ", "Sweep Attack": "なぎ払い攻撃", "Totem of Undying": "不死のトーテム",
    "Underwater": "水中", "Splash": "しぶき", "Witch": "ウィッチ", "Bubble Pop": "泡の破裂",
    "Downwards Current": "下向きの水流", "Upwards Current": "上向きの水流", "Nautilus": "オウムガイ",
    "Dolphin": "イルカ", "Cosy Campfire Smoke": "焚き火の煙", "Signal Campfire Smoke": "のろしの煙",
    "Dripping Honey": "滴るハチミツ", "Falling Honey": "落ちるハチミツ", "Landing Honey": "着地したハチミツ",
    "Falling Nectar": "落ちる蜜", "Falling Spore Blossom": "落ちる胞子の花", "Ash": "灰",
    "Crimson Spore": "真紅の胞子", "Warped Spore": "歪んだ胞子", "Spore Blossom Air": "胞子の花の空気",
    "Dripping Obsidian Tear": "滴る黒曜石の涙", "Falling Obsidian Tear": "落ちる黒曜石の涙",
    "Landing Obsidian Tear": "着地した黒曜石の涙", "Reverse Portal": "逆ポータル", "White Ash": "白い灰",
    "Small Flame": "小さな炎", "Snowflake": "雪の結晶", "Dripping Dripstone Lava": "鍾乳石から滴る溶岩",
    "Falling Dripstone Lava": "鍾乳石から落ちる溶岩", "Dripping Dripstone Water": "鍾乳石から滴る水",
    "Falling Dripstone Water": "鍾乳石から落ちる水", "Glow Squid Ink": "輝くイカスミ", "Glow": "輝き",
    "Wax On": "蝋付け", "Wax Off": "蝋落とし", "Electric Spark": "電気の火花", "Scrape": "削り",
}
out = {}
for k, v in miss.items():
    m = re.match(r"aspect\.integrateddynamics\.(read|write)\.integer\.audio\.instrument\.(\w+)(\.info)?$", k)
    if m and m.group(2) in INSTR:
        name = INSTR[m.group(2)]
        if not m.group(3):
            out[k] = f"{name}の音"
        elif m.group(1) == "read":
            out[k] = f"{name}の音を読み取る。想定範囲は[0, 24]"
        else:
            out[k] = f"{name}の音を出力する。想定範囲は[0, 24]"
        continue
    if ".effect.particle." in k:
        if not k.endswith(".info"):
            p = v.replace("Particle: ", "")
            if p in PART:
                out[k] = f"パーティクル: {PART[p]}"
        else:
            base = miss.get(k[:-5], "").replace("Particle: ", "")
            if base in PART:
                out[k] = f"一定の速度で{PART[base]}のパーティクルを放つ。"
(WORK / "tr/batch_14_id_gen.json").write_text(json.dumps({"integrateddynamics": out}, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(out))
