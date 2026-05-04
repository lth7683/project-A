#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json
import math
import random

ROOT = Path(__file__).resolve().parents[1]
W, H = 1080, 1920


def font(size, bold=False):
    paths = [
        "C:/Windows/Fonts/malgunbd.ttf" if bold else "C:/Windows/Fonts/malgun.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def rounded(draw, box, fill, outline=None, width=1, radius=36):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def gradient(top, bottom):
    img = Image.new("RGB", (W, H), top)
    px = img.load()
    for y in range(H):
        t = y / (H - 1)
        for x in range(W):
            vignette = 0.08 * math.sin((x / W) * math.pi)
            tt = min(1, max(0, t + vignette))
            px[x, y] = tuple(int(top[i] * (1 - tt) + bottom[i] * tt) for i in range(3))
    return img


def person(draw, cx, cy, scale=1.0, coat=False, walking=False, seated=False, reaching=False):
    skin = (226, 174, 132)
    hair = (41, 36, 32)
    shirt = (37, 99, 135) if not coat else (248, 250, 252)
    pants = (38, 50, 70)
    r = int(62 * scale)
    draw.ellipse((cx - r, cy - 260 * scale, cx + r, cy - 135 * scale), fill=skin)
    draw.pieslice((cx - r - 8, cy - 285 * scale, cx + r + 8, cy - 135 * scale), 180, 360, fill=hair)
    rounded(draw, (cx - 95 * scale, cy - 125 * scale, cx + 95 * scale, cy + 160 * scale), shirt, radius=int(38 * scale))
    if coat:
        draw.line((cx, cy - 105 * scale, cx, cy + 150 * scale), fill=(203, 213, 225), width=int(10 * scale))
    if walking:
        draw.line((cx - 30 * scale, cy + 140 * scale, cx - 140 * scale, cy + 335 * scale), fill=pants, width=int(48 * scale))
        draw.line((cx + 35 * scale, cy + 140 * scale, cx + 135 * scale, cy + 315 * scale), fill=pants, width=int(48 * scale))
        draw.line((cx - 86 * scale, cy - 45 * scale, cx - 180 * scale, cy + 65 * scale), fill=shirt, width=int(42 * scale))
        draw.line((cx + 86 * scale, cy - 45 * scale, cx + 180 * scale, cy + 40 * scale), fill=shirt, width=int(42 * scale))
    elif seated:
        draw.line((cx - 40 * scale, cy + 145 * scale, cx - 160 * scale, cy + 235 * scale), fill=pants, width=int(50 * scale))
        draw.line((cx + 40 * scale, cy + 145 * scale, cx + 160 * scale, cy + 235 * scale), fill=pants, width=int(50 * scale))
    else:
        draw.line((cx - 45 * scale, cy + 145 * scale, cx - 70 * scale, cy + 350 * scale), fill=pants, width=int(50 * scale))
        draw.line((cx + 45 * scale, cy + 145 * scale, cx + 70 * scale, cy + 350 * scale), fill=pants, width=int(50 * scale))
    if reaching:
        draw.line((cx + 85 * scale, cy - 35 * scale, cx + 235 * scale, cy + 45 * scale), fill=shirt, width=int(42 * scale))
    else:
        draw.line((cx - 88 * scale, cy - 35 * scale, cx - 155 * scale, cy + 75 * scale), fill=shirt, width=int(42 * scale))
        draw.line((cx + 88 * scale, cy - 35 * scale, cx + 155 * scale, cy + 75 * scale), fill=shirt, width=int(42 * scale))


def plate(draw, cx, cy, r=170, rice=True, veg=True, protein=True):
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(248, 250, 252), outline=(203, 213, 225), width=8)
    if veg:
        for _ in range(16):
            a = random.random() * math.tau
            rr = random.randint(20, max(25, r - 60))
            x = cx + math.cos(a) * rr
            y = cy + math.sin(a) * rr
            draw.ellipse((x - 24, y - 16, x + 26, y + 18), fill=random.choice([(44, 125, 80), (74, 155, 72), (22, 101, 52)]))
    if protein:
        rounded(draw, (cx - 135, cy - 35, cx - 20, cy + 80), (236, 196, 139), radius=28)
        rounded(draw, (cx + 10, cy - 80, cx + 130, cy + 55), (226, 232, 240), radius=28)
    if rice:
        draw.ellipse((cx + 30, cy + 30, cx + 140, cy + 110), fill=(255, 255, 249), outline=(218, 226, 236), width=4)


def glucose_curve(draw, x0, y0, down=False):
    color = (220, 38, 38) if not down else (22, 163, 74)
    points = []
    for i in range(120):
        t = i / 119
        x = x0 + t * 650
        wave = math.sin(t * math.pi * (0.95 if not down else 0.8))
        y = y0 - wave * (300 if not down else 125) - (t * 80 if not down else -t * 30)
        points.append((x, y))
    draw.line(points, fill=color, width=16, joint="curve")
    ax, ay = points[-1]
    draw.polygon([(ax, ay), (ax - 42, ay + 16), (ax - 22, ay - 36)], fill=color)


def table(draw):
    rounded(draw, (90, 1120, 990, 1465), (126, 92, 66), radius=44)


def scene(idx):
    palettes = [
        ((232, 244, 247), (173, 216, 205)),
        ((246, 239, 228), (201, 218, 231)),
        ((239, 247, 236), (188, 219, 196)),
        ((244, 238, 226), (211, 223, 198)),
        ((238, 244, 232), (196, 224, 212)),
        ((245, 240, 232), (224, 207, 185)),
        ((235, 243, 247), (198, 223, 235)),
        ((233, 240, 235), (185, 213, 205)),
        ((239, 244, 248), (203, 217, 232)),
        ((241, 244, 235), (207, 220, 190)),
        ((242, 241, 237), (218, 225, 231)),
        ((238, 244, 246), (210, 226, 230)),
    ]
    img = gradient(*palettes[idx - 1])
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, W, H), outline=(255, 255, 255), width=24)
    for _ in range(16):
        x = random.randint(-120, W + 80)
        y = random.randint(260, H - 180)
        draw.ellipse((x, y, x + 80, y + 80), fill=(255, 255, 255), outline=None)
    img = img.filter(ImageFilter.GaussianBlur(0.15))
    draw = ImageDraw.Draw(img)

    if idx == 1:
        table(draw)
        person(draw, 560, 1000, 1.25, seated=True)
        plate(draw, 315, 1285, 115)
        glucose_curve(draw, 230, 755)
    elif idx == 2:
        table(draw)
        person(draw, 300, 1000, 1.0, seated=True, reaching=True)
        plate(draw, 635, 1195, 185, veg=False, protein=False)
        glucose_curve(draw, 260, 720)
    elif idx == 3:
        table(draw)
        person(draw, 225, 1030, 0.95, seated=True, reaching=True)
        plate(draw, 470, 1210, 120, rice=False, protein=False)
        plate(draw, 665, 1210, 120, rice=False, veg=False)
        plate(draw, 860, 1210, 120, veg=False, protein=False)
    elif idx == 4:
        table(draw)
        person(draw, 310, 1005, 1.05, seated=True, reaching=True)
        plate(draw, 705, 1200, 230)
        draw.arc((450, 890, 940, 1380), 205, 515, fill=(34, 197, 94), width=18)
    elif idx == 5:
        table(draw)
        person(draw, 270, 1000, 0.95, seated=True)
        plate(draw, 685, 1185, 245, rice=False)
        draw.ellipse((760, 950, 880, 1070), fill=(250, 204, 21))
    elif idx == 6:
        table(draw)
        person(draw, 280, 1020, 1.0, seated=True, reaching=True)
        draw.ellipse((555, 1040, 805, 1260), fill=(242, 245, 247), outline=(203, 213, 225), width=8)
        draw.ellipse((600, 1085, 760, 1215), fill=(181, 84, 61))
        draw.ellipse((815, 1085, 955, 1225), fill=(245, 245, 245), outline=(203, 213, 225), width=6)
        draw.line((555, 1350, 950, 1350), fill=(220, 38, 38), width=14)
    elif idx == 7:
        rounded(draw, (100, 1025, 980, 1425), (235, 239, 243), radius=42)
        person(draw, 305, 965, 1.05, seated=True, reaching=True)
        draw.rounded_rectangle((610, 930, 765, 1270), radius=34, fill=(180, 217, 235), outline=(100, 135, 165), width=6)
        draw.rounded_rectangle((810, 930, 955, 1270), radius=34, fill=(246, 157, 122), outline=(178, 87, 64), width=6)
    elif idx == 8:
        draw.rectangle((0, 1215, W, H), fill=(75, 115, 90))
        draw.rectangle((0, 990, W, 1215), fill=(196, 206, 210))
        draw.ellipse((120, 345, 315, 540), fill=(252, 211, 77))
        person(draw, 525, 950, 1.25, walking=True)
    elif idx == 9:
        rounded(draw, (100, 1080, 980, 1435), (255, 255, 255), radius=42)
        person(draw, 300, 980, 1.0, seated=True)
        draw.rounded_rectangle((600, 910, 785, 1185), radius=44, fill=(30, 41, 59))
        draw.ellipse((645, 975, 740, 1070), fill=(56, 189, 248))
        glucose_curve(draw, 325, 1335, down=True)
    elif idx == 10:
        rounded(draw, (105, 1110, 975, 1345), (115, 83, 63), radius=32)
        person(draw, 540, 900, 1.18)
        draw.rounded_rectangle((740, 710, 890, 870), radius=32, fill=(30, 41, 59))
        draw.ellipse((780, 750, 850, 820), outline=(250, 250, 250), width=8)
    elif idx == 11:
        table(draw)
        person(draw, 275, 1010, 0.95, seated=True, reaching=True)
        draw.rounded_rectangle((520, 890, 820, 1250), radius=28, fill=(245, 242, 232), outline=(200, 190, 170), width=6)
        for y in range(955, 1195, 58):
            draw.line((560, y, 780, y), fill=(191, 200, 210), width=4)
        draw.rounded_rectangle((800, 970, 965, 1135), radius=28, fill=(31, 41, 55))
    else:
        rounded(draw, (105, 1080, 975, 1385), (231, 238, 245), radius=42)
        person(draw, 350, 990, 1.0, seated=True)
        person(draw, 710, 990, 1.0, coat=True, seated=True)
        draw.rounded_rectangle((485, 1030, 610, 1160), radius=18, fill=(226, 232, 240), outline=(190, 200, 210), width=5)

    return img


def main():
    random.seed(77)
    scenes = json.loads((ROOT / "scenes.json").read_text(encoding="utf-8-sig"))
    out_dir = ROOT / "assets" / "images"
    out_dir.mkdir(parents=True, exist_ok=True)
    for item in scenes:
        img = scene(int(item["id"]))
        img.save(out_dir / f"scene-{int(item['id']):02}.png", quality=95)


if __name__ == "__main__":
    main()
