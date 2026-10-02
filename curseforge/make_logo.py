# CurseForge用のプロジェクトロゴ(400x400)を pack.png と同じ配色で描き直す
from PIL import Image, ImageDraw, ImageFont
S = 400
BG, GOLD, WHITE = (31, 34, 43), (232, 178, 58), (245, 245, 245)
im = Image.new("RGB", (S, S), BG)
d = ImageDraw.Draw(im)
d.rectangle([10, 10, S - 11, S - 11], outline=GOLD, width=12)
big = ImageFont.truetype("C:/Windows/Fonts/BIZ-UDGothicB.ttc", 128)
mid = ImageFont.truetype("C:/Windows/Fonts/BIZ-UDGothicB.ttc", 74)
small = ImageFont.truetype("C:/Windows/Fonts/BIZ-UDGothicB.ttc", 30)
def center(y, text, font, fill):
    w = d.textlength(text, font=font)
    d.text(((S - w) / 2, y), text, font=font, fill=fill)
center(62, "MOD", big, WHITE)
center(212, "日本語化", mid, GOLD)
center(318, "1.20.1 Forge", small, (170, 175, 190))
im.save("curseforge/logo_400.png")
print("saved")
