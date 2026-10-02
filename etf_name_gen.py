"""ETF の Name プロパティ説明はバックスラッシュの例が多いので、英文の地の文だけを置換して訳す。"""
import json
from pathlib import Path
k = "config.entity_texture_features.property_explanation.name"
en = json.loads(Path("extracted/entity_texture_features.json").read_text(encoding="utf-8"))["missing"][k]
REP = [
    ("Name\nMatches to an entities name.", "名前\nエンティティの名前と照合します。"),
    ('A value starting with "!" performs a negative match (not).', '「!」で始まる値は否定一致(not)になります。'),
    ("Examples:", "例:"),
    (" - Match string: ", " - 文字列で一致: "),
    (" - Match special formatting: ", " - 特殊な書式で一致: "),
    ("(for best compatibility, use the escape sequence ", "(互換性のため、「§」ではなくエスケープシーケンス "),
    (" instead of \"§\")", " を使ってください)"),
    (' - Wildcards using "?" and "*": ', ' - 「?」と「*」のワイルドカード: '),
    (" - Wildcards, case insensitive: ", " - ワイルドカード(大文字小文字を区別しない): "),
    (" - Java regular expressions: ", " - Javaの正規表現: "),
    ("(see http", "(参照: http"),
    (" - Java regular expressions, case insensitive: ", " - Javaの正規表現(大文字小文字を区別しない): "),
    ("Any backslashes in the match string must be doubled.", "照合する文字列中のバックスラッシュはすべて2つ重ねる必要があります。"),
    ("Literal backslashes within a regular expression or wildcard must be quadrupled.", "正規表現やワイルドカード内の文字としてのバックスラッシュは4つ重ねる必要があります。"),
    ("Correct:", "正しい例:"),
    ("Wrong:", "誤った例:"),
]
ja = en
for a, b in REP:
    assert a in ja, a
    ja = ja.replace(a, b)
Path("tr/batch_04_etf_name.json").write_text(json.dumps({"entity_texture_features": {k: ja}}, ensure_ascii=False, indent=1), encoding="utf-8")
print(ja)
