# Neo Vitae のアップグレードの書(JEI説明)を段落ごとに訳して組み立てる
import json
from pathlib import Path
d = json.loads(Path("extracted/neovitae.json").read_text(encoding="utf-8"))["en_us"]
P = {
"Imposed by the Ritual of Sentient Penance: stand on the master stone in your Sentient set and throw the catalyst item onto the stone. Each application adds one level of this curse and frees Upgrade Points to spend elsewhere.":
 "意志ある悔悟の儀式で課される: 意志ある装備一式を着てマスター石の上に立ち、触媒のアイテムを石に投げ入れる。1回ごとにこの呪いが1レベル増え、そのぶん強化ポイントが空いて他に使えるようになる。",
"Remove it with the Sentient Extraction ritual, which returns it as a tome.": "意志ある抽出の儀式で取り除ける。取り除いた呪いは書物として戻ってくる。",
"Obtain the tome from dungeon loot (The Mines and the Foreman's hoard), the Sentient Extraction ritual, or by combining two duplicate tomes at a crafting table.":
 "書物はダンジョンの戦利品(鉱山と現場監督の財宝)、意志ある抽出の儀式、または作業台で同じ書物を2冊組み合わせて手に入れる。",
"Not trained through activity; apply the tome directly to a worn Sentient set.": "活動では鍛えられない。着ている意志ある装備一式に書物を直接使う。",
"Inscribe this tome in the Tabula Vitae from a written book, a shulker shell, an ender pearl, and a gold ingot (Tier 3, 5,000 Essentia Vitae).":
 "この書物はタブラ・ヴィータで、記入済みの本、シュルカーの殻、エンダーパール、金インゴットから刻む(ティア3、エッセンティア・ヴィータ5,000)。",
"If you go too long without combat, the armor saps your hunger.": "長く戦わずにいると、防具が満腹度を吸い取る。",
"Locks your off-hand, leaving only one arm usable.": "オフハンドが使えなくなり、片腕しか使えない。",
"Adds Curios accessory sockets to your Sentient set (requires the Curios mod).": "意志ある装備一式にCuriosのアクセサリー枠を追加する(Curios MODが必要)。",
"Reduces your mining speed.": "採掘速度が下がる。",
"Grants elytra-style gliding from the chestplate.": "チェストプレートでエリトラのように滑空できるようになる。",
"Piglins treat you as neutral, as though you wore gold.": "金を身に着けているかのように、ピグリンが敵対しなくなる。",
"Increases maximum health.": "最大体力が増える。",
"The armor constantly gnaws at your hunger.": "防具が絶えず満腹度をむしばむ。",
"Increases the Luck attribute, improving loot rolls.": "幸運の値が上がり、戦利品の抽選が良くなる。",
"Reduces your melee attack damage.": "近接攻撃のダメージが下がる。",
"Reduces incoming non-projectile damage, such as melee and explosions, as it levels.": "レベルが上がるにつれ、近接や爆発など投射物以外のダメージを軽減する。",
"The armor periodically floods your veins with poison.": "防具がときどき血管に毒を流し込む。",
"Prevents you from drinking potions.": "ポーションが飲めなくなる。",
"Slowly mends the chestplate's durability over time.": "時間とともにチェストプレートの耐久値をゆっくり回復する。",
"Increases the Essentia Vitae gained from self-sacrifice.": "自己犠牲で得るエッセンティア・ヴィータが増える。",
"Reduces the healing you receive.": "受ける回復量が減る。",
"Reduces your movement speed.": "移動速度が下がる。",
"Spoils your aim, scattering the projectiles you fire.": "狙いが狂い、撃った投射物がばらける。",
"Reduces your swimming speed.": "泳ぐ速さが下がる。",
"Reduces incoming projectile damage as it levels.": "レベルが上がるにつれ、投射物のダメージを軽減する。",
"Increases mining speed.": "採掘速度が上がる。",
"Increases the experience gained from orbs.": "経験値オーブから得る経験値が増える。",
"Reduces fall damage as it levels.": "レベルが上がるにつれ、落下ダメージを軽減する。",
"Periodically grants Fire Resistance.": "ときどき火炎耐性を与える。",
"Increases jump height and reduces fall damage.": "ジャンプの高さが上がり、落下ダメージが減る。",
"Increases knockback resistance, and at higher levels maximum health.": "ノックバック耐性が上がり、高レベルでは最大体力も増える。",
"Increases melee attack damage.": "近接攻撃のダメージが上がる。",
"Adds armor and armor toughness.": "防御力と防具強度が上がる。",
"Periodically cleanses Poison.": "ときどき毒を消す。",
"Increases movement speed.": "移動速度が上がる。",
"Adds bonus damage and knockback to sprint attacks.": "ダッシュ攻撃に追加のダメージとノックバックを与える。",
}
TR = {"take projectile damage": "投射物のダメージを受ける", "break blocks": "ブロックを壊す", "pick up experience": "経験値を拾う",
"take fall damage": "落下ダメージを受ける", "spend time on fire": "燃えている時間を過ごす",
"restore health through regeneration, potions, or vitaemantic healing": "再生、ポーション、ヴィータの治癒で体力を回復する",
"rise through the air by jumping": "ジャンプで空中に上がる", "eat food": "食べ物を食べる", "deal melee damage": "近接ダメージを与える",
"take non-projectile damage": "投射物以外のダメージを受ける", "spend time poisoned": "毒の状態で過ごす", "travel across the ground": "地上を移動する",
"take self-sacrifice damage by bleeding into your blood orb or from an altar": "血のオーブや祭壇に血を流して自己犠牲のダメージを受ける"}
def para(p):
    if p in P: return P[p]
    if p.startswith("Trained: deal damage while sprinting and wearing the full Sentient set."):
        return "鍛え方: 意志ある装備一式を着てダッシュ中にダメージを与える。"
    if p == "Trained: as the chestplate's durability is restored while you wear the full Sentient set.":
        return "鍛え方: 意志ある装備一式を着ている間にチェストプレートの耐久値が回復する。"
    if p.startswith("Trained: ") and p.endswith(" while wearing the full Sentient set."):
        a = p[9:-37]
        if a in TR: return f"鍛え方: 意志ある装備一式を着て{TR[a]}。"
    if p.startswith("Inscribe this tome in the Tabula Vitae from a diamond, a written book, a netherite ingot, and a shulker shell (Master orb, 10,000 Essentia Vitae"):
        rest = p[len("Inscribe this tome in the Tabula Vitae from a diamond, a written book, a netherite ingot, and a shulker shell (Master orb, 10,000 Essentia Vitae"):]
        if rest == ").": return "この書物はタブラ・ヴィータで、ダイヤモンド、記入済みの本、ネザライトインゴット、シュルカーの殻から刻む(マグスのオーブ、エッセンティア・ヴィータ10,000)。"
    return None
out, miss = ["## neovitae"], []
for k, v in d.items():
    if k.startswith("jei.neovitae.upgrade_tome.") and k.endswith(".info"):
        ps = [para(p) for p in v.split("\n\n")]
        if all(ps): out.append(k + "\t" + "\\n\\n".join(ps))
        else: miss.append((k, [p for p in v.split("\n\n") if not para(p)]))
Path("tsv/v14_nv_tome.tsv").write_text("\n".join(out) + "\n", encoding="utf-8")
print(len(out) - 1, miss)
