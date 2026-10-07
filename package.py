"""pack/ を配布用zipにまとめる(pack.png と 説明書.txt を同梱)。インスタンスの resourcepacks にもコピーする。"""
import json, shutil, zipfile, datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WORK = Path(__file__).parent
PACK = WORK / "pack"
VERSION = "1.8"
ZIP_NAME = f"ModJP_1.20.1_v{VERSION}.zip"
DIST = WORK / "dist"
INSTANCE_RP = Path(r"C:/Users/4yoma/curseforge/minecraft/Instances/____ (2)/resourcepacks")


def make_icon(path):
    img = Image.new("RGBA", (128, 128), (28, 30, 40, 255))
    d = ImageDraw.Draw(img)
    d.rectangle([4, 4, 123, 123], outline=(230, 180, 60, 255), width=4)
    big = ImageFont.truetype("C:/Windows/Fonts/meiryob.ttc", 40)
    small = ImageFont.truetype("C:/Windows/Fonts/meiryob.ttc", 22)
    d.text((64, 46), "MOD", font=big, fill=(255, 255, 255, 255), anchor="mm")
    d.text((64, 92), "日本語化", font=small, fill=(230, 180, 60, 255), anchor="mm")
    img.save(path)


def readme(mod_rows):
    lines = [
        f"MOD日本語化パック v{VERSION} (Minecraft 1.20.1 / Forge)",
        "",
        "■ これは何？",
        "  英語のままのMODの文字を日本語にするリソースパックです。",
        "  MOD本体(jar)は一切いじらないので、MODを更新しても壊れません。",
        "  MODにもともと入っている公式の日本語訳は上書きしません(足りない部分だけ足します)。",
        "",
        "■ 使い方",
        "  1. このzipを解凍せずに、インスタンスの resourcepacks フォルダに入れる",
        "     (CurseForgeならインスタンスを右クリック →「フォルダを開く」→ resourcepacks)",
        "  2. ゲームの 設定 → 言語 を「日本語」にする",
        "  3. 設定 → リソースパック で「MOD日本語化パック」を右側(有効)に移して完了",
        "     ※他のリソースパックより上に置いてください",
        "",
        "■ 対応MOD(訳を追加したもの)",
    ]
    lines += [f"  - {jar}" for jar in mod_rows]
    lines += [
        "",
        "■ 注意",
        "  - 入っていないMODの分は単に使われないだけなので、MODが一部違っても問題ありません。",
        "  - MODのバージョンが違うと、新しく増えた文字は英語のままになることがあります。",
        "  - ガイドブック本文(Patchouli等)や、MODがプログラムに直接書いている文字は訳せません。",
        "",
        f"作成日: {datetime.date.today().isoformat()}",
    ]
    return "\r\n".join(lines) + "\r\n"


def main():
    status = (WORK / "translation_status.md").read_text(encoding="utf-8").splitlines()
    mods = []
    for row in status:
        cells = [c.strip() for c in row.split("|")]
        if len(cells) > 7 and cells[1].endswith(".jar") and cells[6].isdigit() and int(cells[6]) > 0:
            mods.append(cells[1])
    mods = sorted(set(mods), key=str.lower)
    make_icon(PACK / "pack.png")
    DIST.mkdir(exist_ok=True)
    out = DIST / ZIP_NAME
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(PACK.rglob("*")):
            if p.is_file():
                z.write(p, p.relative_to(PACK).as_posix())
        z.writestr("説明書.txt", readme(mods).encode("utf-8-sig"))
    (DIST / "説明書.txt").write_text(readme(mods), encoding="utf-8-sig", newline="")
    for old in INSTANCE_RP.glob("ModJP_1.20.1_v*.zip"):
        old.unlink()
    shutil.copy2(out, INSTANCE_RP / ZIP_NAME)
    print(out, out.stat().st_size // 1024, "KB /", len(mods), "MOD")


if __name__ == "__main__":
    main()
