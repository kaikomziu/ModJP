# rsgauges の .help(改行数固定)を和訳文から自動で行分割して tsv/v11_rsg_gen.tsv に出す
import json, re
d = json.load(open('extracted/rsgauges.json', encoding='utf-8')); en = d['en_us']
J = {
"block.rsgauges.arrow_target.help":"矢が当たるか手で作動させると、取り付けたブロックにレッドストーンのパルスを送る的。",
"block.rsgauges.door_sensor_switch.help":"ドアの上の壁に取り付けるプレイヤー検出器。§r",
"block.rsgauges.elevator_button.help":"設置時に壁のどこをクリックしたかによって、上、下、または両方向を指す。",
"block.rsgauges.glass_contact_mat.help":"上から機械的な圧力(誰かが乗るなど)を受けたとき、そして圧力がなくなってから少しの間、色が変わってレッドストーン信号を出すガラスの床板。出力は前面と下面。音は出さない。センサーは高感度。",
"block.rsgauges.glass_day_timer.help":"設定した開始時刻から終了時刻までレッドストーン信号を出す小さなガラスの装置。時間帯は正面のボタンで設定する(24時間表記、06:00が日の出)。このボタンで出力の強さとランダム値も設定できる。ランダム値は、オン/オフの切り替えをランダムな時間だけ遅らせるもので、値が大きいほど遅延が長くなる。出力はセンサーを設置したブロックへ。切り替え音は出さない。",
"block.rsgauges.glass_door_contact_mat.help":"上から機械的な圧力(誰かが乗るなど)を受けたとき、そして圧力がなくなってから少しの間、色が変わってレッドストーン信号を出すガラスの床板。出力は前面と下面。音は出さない。",
"block.rsgauges.glass_entity_detector.help":"決まった範囲を監視し、エンティティを見つけるとレッドストーン信号を出す小さなガラスの装置。範囲は上下2ブロック、前方と左右に「範囲」分(180度をカバー)。範囲は正面の小さなボタンで、出力の強さ、検出するエンティティ数、検出するエンティティの種類(モブ、プレイヤー、動物など)と一緒に設定できる。出力はセンサーを設置したブロックへ。切り替え音は出さない。",
"block.rsgauges.glass_interval_timer.help":"決まったオン時間とオフ時間で信号を出す。正面のボタンで設定する:|- §1青: オン時間§r|- §6黄: オフ時間§r|- §2緑: 信号の立ち上がり/立ち下がり§r|- §4赤: 出力の強さ§r|設定のためタイマーは待機モードで置かれる。正面をクリックすると動作モードになる。出力はセンサーを設置したブロックへ。|スイッチリンクの対象にすると、タイマーは動作モードと待機モードを切り替える。",
"block.rsgauges.glass_linear_entity_detector.help":"一方向を監視し、エンティティを感知するとレッドストーン信号を出す小さなガラスの装置。監視範囲は前方に「範囲」ブロック、左右に半ブロック。範囲は正面の小さなボタンで、出力の強さ、検出するエンティティ数、検出するエンティティの種類(モブ、プレイヤー、動物など)と一緒に設定できる。出力はセンサーを設置したブロックへ。切り替え音は出さない。",
"block.rsgauges.industrial_alarm_lamp.help":"取り付けたブロックからのレッドストーン信号を検出すると点滅する赤いランプ。作動中は光る。",
"block.rsgauges.industrial_alarm_siren.help":"取り付けたブロックからのレッドストーン信号を検出すると、頻繁に警報音を鳴らすサイレン。",
"block.rsgauges.industrial_analog_angular_gauge.help":"固体ブロックに取り付けて、そのブロックのレッドストーン出力を表示する装置。ブロック自体が動力を出せる場合はその出力を使い、そうでない場合は隣接ブロックからそのブロックが受けている動力を間接的に測る。強い動力と弱い動力の両方に対応。間接的な弱い動力の測定は少し遅れることがある。",
"block.rsgauges.industrial_block_detector.help":"前方の1つ以上のブロックが設定した分類に一致すると、レッドストーン信号を出す。背面のボタンで設定する:|- §1範囲§r(どこまで監視するか)|- §6しきい値§r(一致する数)|- §3チャタリング防止§r(揺らぎ防止の遅延)|§4- 出力の強さ§r|- §2フィルター§r(固体、液体、原木)",
"block.rsgauges.industrial_comparator_switch.help":"取り付けたブロックのコンパレーター出力レベル、インベントリの統計、またはレッドストーン信号に応じて、レッドストーン信号を出す小さな装置。正面のボタンで出力の強さ、オンになるコンパレーター値、オフになるコンパレーター値、動作モード(「コンパレーター、空きスロット、使用スロット…」)を設定できる。レッドストーン信号モードでは、スイッチは動力を出さないが、スイッチリンクの送信元として使える。",
"block.rsgauges.industrial_contact_mat.help":"上から機械的な圧力(誰かが乗るなど)を受けたとき、そして圧力がなくなってから少しの間、レッドストーン信号を出す工業用の床の接触マット。出力は前面と下面。",
"block.rsgauges.industrial_day_timer.help":"設定した開始時刻から終了時刻までレッドストーン信号を出す小さな装置。時間帯は正面のボタンで設定する(24時間表記、06:00が日の出)。このボタンで出力の強さとランダム値も設定できる。ランダム値は、オン/オフの切り替えをランダムな時間だけ遅らせるもので、値が大きいほど遅延が長くなる。出力はセンサーを設置したブロックへ。",
"block.rsgauges.industrial_dimmer.help":"工業用の手動レッドストーン調光器。装置の背面に0〜15の出力信号を手動で設定できる。クリックする縦の位置で信号の強さが決まる。",
"block.rsgauges.industrial_door_contact_mat.help":"上から機械的な圧力(誰かが乗るなど)を受けたとき、そして圧力がなくなってから少しの間、レッドストーン信号を出す工業用の床の接触マット。出力は前面と下面。",
"block.rsgauges.industrial_entity_detector.help":"決まった範囲を監視し、エンティティを見つけるとレッドストーン信号を出す小さな装置。範囲は上下2ブロック、前方と左右に「範囲」分(180度をカバー)。範囲は正面の小さなボタンで、出力の強さ、検出するエンティティ数、検出するエンティティの種類(モブ、プレイヤー、動物など)と一緒に設定できる。出力はセンサーを設置したブロックへ。",
"block.rsgauges.industrial_estop_switch.help":"飛び道具で撃って止めることもできる。",
"block.rsgauges.industrial_fallthrough_detector.help":"何かが通り抜けて落ちるとレッドストーン信号を出す工業用のセンサーフレーム。出力は取り付けたブロックへ。",
"block.rsgauges.industrial_green_blinking_led.help":"約0.5Hzの周期で点滅する。",
"block.rsgauges.industrial_red_blinking_led.help":"約0.5Hzの周期で点滅する。",
"block.rsgauges.industrial_white_blinking_led.help":"約0.5Hzの周期で点滅する。",
"block.rsgauges.industrial_yellow_blinking_led.help":"約0.5Hzの周期で点滅する。",
"block.rsgauges.industrial_high_sensitive_trapdoor.help":"誰かや何かが落ちてきたとき、またはスニークせずに上を歩いたときに開いてレッドストーン信号を出す工業用の床のトラップドア。出力は取り付けたブロックへ。",
"block.rsgauges.industrial_interval_timer.help":"決まったオン時間とオフ時間で信号を出す。正面のボタンで設定する:|- §1青: オン時間§r|- §6黄: オフ時間§r|- §2緑: 信号の立ち上がり/立ち下がり§r|- §4赤: 出力の強さ§r|設定のためタイマーは待機モードで置かれる。正面をクリックすると動作モードになる。出力はセンサーを設置したブロックへ。|スイッチリンクの対象にすると、タイマーは動作モードと待機モードを切り替える。",
"block.rsgauges.industrial_knock_button.help":"向いている側の隣接ブロックがクリックされると、レッドストーンのパルスを出す。",
"block.rsgauges.industrial_knock_switch.help":"向いている側の隣接ブロックがクリックされると、オン/オフが切り替わる。§r",
"block.rsgauges.industrial_light_sensor.help":"設置場所の明るさを測り、正面の小さなボタンで設定したオン/オフのしきい値に応じてレッドストーン信号を出す小さな装置。§rこのボタンで出力の強さとチャタリング防止も設定できる。チャタリング防止は明るさが安定するまで切り替えを遅らせるもので、値が大きいほどノイズをよく除去するが、切り替えの遅延も長くなる。オンとオフの設定が同じ場合、測った明るさが設定値とぴったり一致する必要がある。出力はセンサーを設置したブロックへ。",
"block.rsgauges.industrial_lightning_sensor.help":"空気中の高い電位、つまり雷雨を感知するとレッドストーン信号を出す、壁に取り付ける小さな装置。§r正面のボタンで出力の強さを設定できる。出力はセンサーを設置したブロックへ。",
"block.rsgauges.industrial_linear_entity_detector.help":"一方向を監視し、エンティティを感知するとレッドストーン信号を出す小さな装置。§r監視範囲は前方に「範囲」ブロック、左右に半ブロック。範囲は正面の小さなボタンで、出力の強さ、検出するエンティティ数、検出するエンティティの種類(モブ、プレイヤー、動物など)と一緒に設定できる。出力はセンサーを設置したブロックへ。",
"block.rsgauges.industrial_rain_sensor.help":"雨が当たるとレッドストーン信号を出す、壁に取り付ける小さな装置。正面のボタンで出力の強さを設定できる。出力はセンサーを設置したブロックへ。",
"block.rsgauges.industrial_shock_sensitive_contact_mat.help":"上からの機械的な衝撃(何かが落ちてくるなど)を受けると、レッドストーンのパルスを出す工業用の接触マット。出力は前面と下面。強さは常に15。",
"block.rsgauges.industrial_shock_sensitive_trapdoor.help":"誰かや何かが落ちてくると開いてレッドストーン信号を出す工業用の床のトラップドア。出力は取り付けたブロックへ。",
"block.rsgauges.industrial_switchlink_cased_pulse_receiver.help":"スイッチリンクの対象として使うのに最適化された、フルブロックの工業用パルススイッチ装置。普通のパルススイッチと同じく、手でクリックするかスイッチリンクで作動させると短時間オンになる。内部のリレーは消音されていてとても静か。",
"block.rsgauges.industrial_switchlink_cased_receiver.help":"スイッチリンクの対象として使うのに最適化された、フルブロックの工業用双安定スイッチ装置。内部のリレーは消音されていてとても静か。レバーのように手で作動させることもできる。",
"block.rsgauges.industrial_switchlink_pulse_receiver.help":"スイッチリンクの対象として使うのに最適化された、小型の工業用パルススイッチ装置。普通のパルススイッチと同じく、手でクリックするかスイッチリンクで作動させると短時間オンになる。内部のリレーは消音されていてとても静か。",
"block.rsgauges.industrial_switchlink_pulse_relay.help":"レッドストーン入力のスイッチリンク中継器として使うのに最適化された、小型の工業用パルススイッチ装置。信号は出せないが、取り付けたブロックのレッドストーン動力が変化すると、中のリンクパールを作動させる。入力が0からそれより大きい値に変わると短時間作動する。素手でダブル左クリックすると、入力の極性と感度(デフォルトは弱)を変えられる。",
"block.rsgauges.industrial_switchlink_receiver.help":"スイッチリンクの対象として使うのに最適化された、小型の工業用双安定スイッチ装置。内部のリレーは消音されていてとても静か。レバーのように手で作動させることもできる。",
"block.rsgauges.industrial_switchlink_receiver_analog.help":"受け取ったスイッチリンク信号からアナログのレッドストーン信号を出力する小さな装置。アナログリンク送信機、コンパレータースイッチ、調光器と組み合わせて使える。|.",
"block.rsgauges.industrial_switchlink_relay.help":"レッドストーン入力のスイッチリンク中継器として使うのに最適化された、小型の工業用スイッチ装置。この中継器はレッドストーン信号を出せず、代わりに取り付けたブロックのレッドストーン動力が変化すると、中のリンクパールを作動させる。素手でダブル左クリックすると、入力の極性(反転はアクティブローの意味)と強さの感度(デフォルトは弱、強はリンクの作動に強い動力が必要という意味)を変えられる。消音されているのでとても静か。テスト用にレバーのように手で作動させることもできる。",
"block.rsgauges.industrial_switchlink_relay_analog.help":"検出したレッドストーン信号を、アナログ情報としてスイッチリンクの対象へ無線で送る小さな装置。自身ではレッドストーン信号を出せない。",
"block.rsgauges.industrial_white_led.help":"ブロックに取り付けて、そのブロックに動力が入っているかを示す小さな装置。ブロック自体が動力を出せる場合はその出力を使い、そうでない場合は隣接ブロックからそのブロックが受けている動力を調べる。染料で左クリックするとLEDの色を変えられる。",
"block.rsgauges.red_power_plant.help":"ポピーにそっくりな人工の赤い花。何かが触れると(接触板のように)前面と下面にレッドストーン信号を出す。",
"block.rsgauges.yellow_power_plant.help":"タンポポにそっくりな人工の黄色い花。何かが触れると(接触板のように)前面と下面にレッドストーン信号を出す。",
"block.rsgauges.rustic_contact_plate.help":"上から機械的な圧力(誰かが乗るなど)を受けたとき、そして圧力がなくなってから少しの間、レッドストーン信号を出す金属板。出力は前面と下面。",
"block.rsgauges.rustic_door_contact_plate.help":"上から機械的な圧力(誰かが乗るなど)を受けたとき、そして圧力がなくなってから少しの間、レッドストーン信号を出す金属板。出力は前面と下面。",
"block.rsgauges.rustic_fallthrough_detector.help":"何かが触れると開いてレッドストーン信号を出す金属のトラップドア。出力は取り付けたブロックへ。",
"block.rsgauges.rustic_high_sensitive_trapdoor.help":"誰かや何かが落ちてきたとき、またはスニークせずに上を歩いたときに開いてレッドストーン信号を出す金属の床のトラップドア。出力は取り付けたブロックへ。",
"block.rsgauges.rustic_semaphore.help":"表示器を取り付けたブロックに動力が入ると旗が上がる、信号旗付きの小さな金属ケース。ブロック自体が動力を出せる場合はその出力を使い、そうでない場合は隣接ブロックからそのブロックが受けている動力を調べる。染料で左クリックすると旗を着色できる。",
"block.rsgauges.rustic_shock_sensitive_plate.help":"上からの機械的な衝撃(何かが落ちてくるなど)を受けると、レッドストーンのパルスを出す金属板。出力は前面と下面。強さは常に15。",
"block.rsgauges.rustic_shock_sensitive_trapdoor.help":"誰かや何かが落ちてくると開いてレッドストーン信号を出す金属の床のトラップドア。出力は取り付けたブロックへ。",
"block.rsgauges.sensitive_glass_block.help":"レッドストーンランプのように、レッドストーン信号で動力が入ると光るガラスブロック。",
"block.rsgauges.stained_sensitiveglass.help":"レッドストーン信号で動力が入ると、透明から色付きに変わるガラスブロック。動力がない状態では、うっすらとした破線の枠で色がわかる。",
"item.rsgauges.switchlink_pearl.help":"エンダーパールでスイッチを左クリックすると作れる。使う(スニーククリック)か、別の(送信元の)スイッチに差し込むと、その(対象の)スイッチを遠隔で作動させる。スイッチリンクパールで対象をクリックするとリンクのオプションを変えられる(オプションを順に切り替え)。1つのスイッチに複数のパールを差し込める。パールは負荷がかかりすぎたり対象が見つからないと文句を言うので、音でわかる。スイッチがリンクの送信元や対象に適さない場合も、パールは文句を言う。スイッチの種類によってリンクの作動への反応は異なる(少し試してみよう)。",
"rsgauges.switch.feature.colortinting.help":"染料で左クリックするとスイッチを着色できる。",
"rsgauges.switch.feature.contactmat.offdelay.help":"レッドストーンのスタックで左クリックすると、保持時間を0.1秒(1)〜6.4秒(64)に設定できる。",
"rsgauges.switch.feature.contactmat.touch.help":"タッチ設定の上下ボタンをクリックすると、出力の強さ、エンティティのフィルター、エンティティ数、感度を設定できる。",
"rsgauges.switch.feature.linksource.help":"スイッチリンクパールでクリックすると、このスイッチをリンクの送信元として使える。",
"rsgauges.switch.feature.linktarget.help":"エンダーパールでクリックすると、このスイッチにリンクしたスイッチリンクパールが得られる。",
"rsgauges.switch.feature.outputconfig.help":"レッドストーントーチでクリックすると出力を設定できる(このスイッチが対応するオプションを順に切り替え)。",
"rsgauges.switch.feature.pulseextend.help":"作動中にもう一度作動させるとパルスの時間を延ばせる。",
"rsgauges.switch.feature.pulsetime.help":"レッドストーンのスタックで左クリックすると、固定のパルス時間を0.1秒(1)〜6.4秒(64)に設定できる。",
"rsgauges.switch.feature.typebistable.help":"レバーのように手でオン/オフを切り替えるスイッチ。",
"rsgauges.switch.feature.typepulse.help":"ボタンのように短時間レッドストーン信号を出すスイッチ。",
}
REF = re.compile(r'\$\{[^}]+\}')
PUNCT = '、。)」'

def chunk(s, n):
    if n <= 1:
        return [s]
    L = len(s); out = []; start = 0
    for i in range(1, n):
        t = round(L * i / n); best = t
        found = False
        for chars in (PUNCT, 'をにがはでとへもや'):
            for dl in range(6):
                hit = [c for c in (t + dl, t - dl) if 0 < c < L and s[c - 1] in chars]
                if hit:
                    best = hit[0]; found = True; break
            if found:
                break
        best = min(max(best, start + 1), L - (n - i))
        out.append(s[start:best]); start = best
    out.append(s[start:])
    return out

res = {}
for k, ja in J.items():
    if k not in en:
        continue
    e = en[k]
    slots = []
    for ln in e.split('\n'):
        m = REF.search(ln)
        slots.append([ln[:m.start()] if m else ln, ln[m.start():] if m else ''])
    prose = [i for i, (p, s) in enumerate(slots) if p.strip()]
    segs = ja.split('|')
    while len(segs) < len(prose):
        j = max(range(len(segs)), key=lambda x: len(segs[x]))
        segs[j:j + 1] = chunk(segs[j], 2)
    while len(segs) > len(prose):
        segs[-2:] = [segs[-2] + segs[-1]]
    for i, sg in zip(prose, segs):
        slots[i][0] = (' ' if slots[i][0].startswith(' ') else '') + sg
    out = '\n'.join(p + s for p, s in slots)
    assert out.count('\n') == e.count('\n'), k
    assert REF.findall(out) == REF.findall(e), k
    res[k] = out
for k, e in en.items():
    if k.endswith('.help') and k not in res and not REF.sub('', e).replace('\n', '').strip():
        res[k] = e
lines = ["## rsgauges"] + [k + "\t" + v.replace("\n", "\\n") for k, v in res.items()]
open('tsv/v11_rsg_gen.tsv', 'w', encoding='utf-8').write("\n".join(lines) + "\n")
print(len(res))
