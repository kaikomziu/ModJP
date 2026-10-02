# integrateddynamicscompat のエネルギー(RF/Tesla/EU)系定型文を生成して tsv/v11_idc_gen.tsv に出す
import json, re
en = json.load(open('extracted/integrateddynamicscompat.json', encoding='utf-8'))['en_us']
P = [
    (r"^Is (\w+) Handler$", "{0}を扱うか"),
    (r"^If the target in some way handles (\w+)$", "対象が何らかの形で{0}を扱うか"),
    (r"^Is (\w+) Receiver$", "{0}を受け取れるか"),
    (r"^If the target can receive (\w+)$", "対象が{0}を受け取れるか"),
    (r"^Is (\w+) Provider$", "{0}を供給できるか"),
    (r"^If the target can provide (\w+)$", "対象が{0}を供給できるか"),
    (r"^Can Extract (\w+)$", "{0}を搬出できるか"),
    (r"^If (\w+) can really be extracted from the target, takes into account storage$", "対象から実際に{0}を搬出できるか(保管量を考慮)"),
    (r"^Can Insert (\w+)$", "{0}を搬入できるか"),
    (r"^If (\w+) can really be inserted into the target, takes into account storage and capacity$", "対象に実際に{0}を搬入できるか(保管量と容量を考慮)"),
    (r"^Is (\w+) Buffer Full$", "{0}バッファが満タンか"),
    (r"^If the target's (\w+) buffer is completely full$", "対象の{0}バッファが完全に満タンか"),
    (r"^Is (\w+) Buffer Empty$", "{0}バッファが空か"),
    (r"^If the target's (\w+) buffer is completely empty$", "対象の{0}バッファが完全に空か"),
    (r"^Is (\w+) Buffer Not Empty$", "{0}バッファが空でないか"),
    (r"^If the target's (\w+) buffer is not empty$", "対象の{0}バッファが空でないか"),
    (r"^Stored (\w+)$", "蓄えた{0}"),
    (r"^The amount of (\w+) stored in the target$", "対象に蓄えられた{0}の量"),
    (r"^The formatted amount of (\w+) stored in the target$", "対象に蓄えられた{0}の量(整形済み)"),
    (r"^(\w+) Capacity$", "{0}容量"),
    (r"^The (\w+) capacity of the target$", "対象の{0}容量"),
    (r"^The formatted (\w+) capacity of the target$", "対象の{0}容量(整形済み)"),
    (r"^(\w+) Fill Ratio$", "{0}の充填率"),
    (r"^The amount of (\w+) in the target divided by its capacity$", "対象の{0}の量を容量で割ったもの"),
    (r"^The amount of (\w+) in the item divided by its capacity$", "アイテムの{0}の量を容量で割ったもの"),
    (r"^Is (\w+) Container$", "{0}容器か"),
    (r"^If the given item can hold (\w+)$", "指定したアイテムが{0}を保持できるか"),
    (r"^(\w+) Stored$", "蓄えた{0}"),
    (r"^The amount of (\w+) stored in this item$", "このアイテムに蓄えられた{0}の量"),
    (r"^The maximum amount of (\w+) that can be stored in this item$", "このアイテムに蓄えられる{0}の最大量"),
    (r"^If the given item can receiver (\w+)$", "指定したアイテムが{0}を受け取れるか"),
    (r"^If the given item can provide (\w+)$", "指定したアイテムが{0}を供給できるか"),
    (r"^If the given item is full of (\w+) energy$", "指定したアイテムの{0}エネルギーが満タンか"),
    (r"^If the given item has no (\w+) energy$", "指定したアイテムに{0}エネルギーがないか"),
    (r"^If the given item has (\w+) energy$", "指定したアイテムに{0}エネルギーがあるか"),
]
out = {}
for k, e in en.items():
    for pat, ja in P:
        m = re.match(pat, e)
        if m:
            out[k] = ja.format(m.group(1)); break
lines = ["## integrateddynamicscompat"] + [k + "\t" + v for k, v in out.items()]
open('tsv/v11_idc_gen.tsv', 'w', encoding='utf-8').write("\n".join(lines) + "\n")
print(len(out))
