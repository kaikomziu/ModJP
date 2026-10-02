"""RationCraft(rationcraft / chaseisration の2名前空間に同じ文言がある)の缶詰名を語辞書から生成する。"""
import json, re
from pathlib import Path

FOOD = {
    "Apple Slices": "スライスりんご", "Beef": "牛肉", "Beets": "ビートルート", "Borscht": "ボルシチ", "Bread": "パン",
    "Breaded Fish": "魚のフライ", "Breaded Ham": "ハムカツ", "Cake": "ケーキ", "Carrots": "ニンジン", "Cookies": "クッキー",
    "Fish": "魚", "Melon": "スイカ", "Mutton": "羊肉", "Pork": "豚肉", "Potato": "ジャガイモ", "Pumpkin Puree": "カボチャのピューレ",
    "Rabbit Stew": "ウサギシチュー", "Whole Chicken": "丸鶏", "Whole Rabbit": "ウサギの丸焼き", "Mushrooms": "キノコ",
    "Condensed Milk": "練乳",
}
FIXED = {
    "Arrow of Hunger": "空腹の矢", "Potion of Hunger": "空腹のポーション", "Splash Potion of Hunger": "空腹のスプラッシュポーション",
    "Lingering Potion of Hunger": "空腹の残留ポーション", "Citrus Beverage Base": "柑橘飲料の素", "Citrus Drink": "柑橘ドリンク",
    "Corned Beef": "コンビーフ", "Crate of Hardtack": "乾パンの木箱", "Cup Of Hot Water": "お湯入りカップ", "Cup Of Water": "水入りカップ",
    "Cup of Coffee": "コーヒー", "Cup of Hot Chocolate": "ホットチョコレート", "Cup of Hot Tea": "ホットティー",
    "Cup of Hot Water": "お湯入りカップ", "Cup of Iced Tea": "アイスティー", "Cup of Water": "水入りカップ", "Dry Sausage": "ドライソーセージ",
    "Glowberry Gum": "グロウベリーガム", "Hardtack": "乾パン", "Hot Chocolate Mix": "ホットチョコレートの素", "Instant Coffee": "インスタントコーヒー",
    "Iron Cup": "鉄のカップ", "It's just chocolate, we swear": "ただのチョコレートだよ、本当に", "It's just chocolate, we swear.": "ただのチョコレートだよ、本当に。",
    "Package Of Hardtack": "乾パンの包み", "Package Of Sugar Candy": "砂糖菓子の包み", "Ration Pack": "レーションパック",
    "Rationcraft - Cans": "Rationcraft - 缶詰", "Rationcraft - Misc": "Rationcraft - その他", "Rationcraft Drinks": "Rationcraft 飲み物",
    "Roasted Sausage": "焼きソーセージ", "Salted Pork": "塩漬け豚肉", "Scho-Ka-Kola": "ショカコーラ", "Milk Scho-Ka-Kola": "ミルクショカコーラ",
    "Sugar Candy": "砂糖菓子", "Sweetberry Gum": "スイートベリーガム", "Tea Bag": "ティーバッグ", "Used Can": "空き缶",
}
FR = "|".join(map(re.escape, sorted(FOOD, key=len, reverse=True)))


def tr(v):
    if v in FIXED:
        return FIXED[v]
    m = re.fullmatch(r"(1/4|1/2|3/4) (Milk )?Scho-Ka-Kola", v)
    if m:
        return ("ミルク" if m.group(2) else "") + f"ショカコーラ(残り{m.group(1)})"
    m = re.fullmatch(rf"(1/2 )?(Open )?(?:Canned|Can of) ({FR})", v)
    if m:
        half, opened, food = m.groups()
        s = FOOD[food] + "の缶詰"
        if half:
            return s + "(残り1/2)"
        return ("開けた" if opened else "") + s
    return None


out = {}
for ns in ["rationcraft", "chaseisration"]:
    p = Path(f"extracted/{ns}.json")
    if not p.exists():
        continue
    miss = json.loads(p.read_text(encoding="utf-8"))["missing"]
    out[ns] = {k: t for k, v in miss.items() if (t := tr(v))}
    left = [v for k, v in miss.items() if k not in out[ns]]
    print(ns, len(out[ns]), "/", len(miss), "未処理:", sorted(set(left)))
Path("tr/batch_06_rationcraft_gen.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
