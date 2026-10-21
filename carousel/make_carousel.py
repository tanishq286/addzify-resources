"""Addzify Instagram carousel generator (1080x1350 JPEG slides, 4:5).

Usage:
    python3 make_carousel.py <spec.json> <output_dir>

Spec format (JSON):
{
  "slug": "buyers-google-factory",
  "keyword": "BUYERS",                      # must match a live Zorcha DM keyword
  "hook_top": "Buyer ne aapki factory Google ki…",
  "hook_main": "…aur order kisi aur ko de diya.",
  "pill": "5 galtiyan. Swipe",
  "label": "GALTI",                          # shown as "GALTI #1"
  "box1_label": "BUYER SOCHTA HAI",
  "box2_label": "FIX",
  "points": [["title", "box1 text", "box2 text"], ...],   # 3-6 points
  "cta_offer": "Free “B2B Buyer Attraction Blueprint” chahiye?",
  "caption": "..."
}
Fonts: Poppins (Google Fonts). Uses system copy if present, else ./fonts/.
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
PAD = 90
BG = (11, 18, 32)
CARD = (22, 32, 52)
ACCENT = (255, 107, 26)
WHITE = (245, 247, 250)
MUTED = (160, 172, 192)
FONT_DIRS = [Path("/usr/share/fonts/truetype/google-fonts"), Path(__file__).parent / "fonts"]
REQUIRED = ["slug", "keyword", "hook_top", "hook_main", "pill", "points", "cta_offer", "caption"]


def font(weight, size):
    for d in FONT_DIRS:
        p = d / f"Poppins-{weight}.ttf"
        if p.exists():
            return ImageFont.truetype(str(p), size)
    raise FileNotFoundError(f"Poppins-{weight}.ttf not found in {FONT_DIRS}")


def wrap(draw, text, fnt, max_w):
    lines = []
    for para in text.split("\n"):
        line = ""
        for w in para.split():
            test = f"{line} {w}".strip()
            if draw.textlength(test, font=fnt) <= max_w:
                line = test
            else:
                if line:
                    lines.append(line)
                line = w
        lines.append(line)
    return lines


def draw_block(draw, text, fnt, color, x, y, max_w, gap=1.22):
    for ln in wrap(draw, text, fnt, max_w):
        draw.text((x, y), ln, font=fnt, fill=color)
        y += int(fnt.size * gap)
    return y


def frame(idx, total):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 14], fill=ACCENT)
    d.text((PAD, H - 110), "ADDZIFY", font=font("Bold", 30), fill=WHITE)
    d.text((PAD + 165, H - 106), "| Factory Marketing", font=font("Regular", 26), fill=MUTED)
    pg, f = f"{idx}/{total}", font("Medium", 26)
    d.text((W - PAD - d.textlength(pg, font=f), H - 106), pg, font=f, fill=MUTED)
    return img, d


def hook_slide(spec, total):
    img, d = frame(1, total)
    y = 330
    y = draw_block(d, spec["hook_top"], font("Medium", 58), MUTED, PAD, y, W - 2 * PAD)
    y += 30
    y = draw_block(d, spec["hook_main"], font("Bold", 104), WHITE, PAD, y, W - 2 * PAD, 1.1)
    y += 70
    pf = font("Bold", 42)
    tw = d.textlength(spec["pill"], font=pf)
    d.rounded_rectangle([PAD, y, PAD + tw + 170, y + 100], radius=50, fill=ACCENT)
    d.text((PAD + 44, y + 22), spec["pill"], font=pf, fill=BG)
    ax, ay = PAD + 44 + tw + 30, y + 50  # arrow drawn as a shape: Poppins lacks the glyph
    d.line([ax, ay, ax + 46, ay], fill=BG, width=7)
    d.polygon([(ax + 56, ay), (ax + 38, ay - 16), (ax + 38, ay + 16)], fill=BG)
    return img


def point_slide(spec, idx, total, num, title, box1, box2):
    img, d = frame(idx, total)
    tfont, body, lab = font("Bold", 84), font("Regular", 46), font("Bold", 34)
    inner = W - 2 * PAD - 80
    lh = int(body.size * 1.22)
    t_lines = wrap(d, title, tfont, W - 2 * PAD)
    b1, b2 = wrap(d, box1, body, inner), wrap(d, box2, body, inner)
    box_h = 50 + 50 + len(b1) * lh + 30 + 50 + len(b2) * lh + 40
    block_h = 70 + len(t_lines) * int(tfont.size * 1.12) + 60 + box_h
    top = max(130, (H - 140 - block_h) // 2)
    d.text((PAD, top), f"{spec.get('label', 'GALTI')} #{num}", font=font("Bold", 42), fill=ACCENT)
    y = draw_block(d, title, tfont, WHITE, PAD, top + 70, W - 2 * PAD, 1.12) + 60
    d.rounded_rectangle([PAD, y, W - PAD, y + box_h], radius=32, fill=CARD)
    cy = y + 50
    d.text((PAD + 40, cy), spec.get("box1_label", "BUYER SOCHTA HAI"), font=lab, fill=MUTED)
    cy = draw_block(d, box1, body, WHITE, PAD + 40, cy + 50, inner) + 30
    d.text((PAD + 40, cy), spec.get("box2_label", "FIX"), font=lab, fill=ACCENT)
    draw_block(d, box2, body, WHITE, PAD + 40, cy + 50, inner)
    return img


def cta_slide(spec, idx, total):
    img, d = frame(idx, total)
    y = draw_block(d, spec["cta_offer"], font("Bold", 72), WHITE, PAD, 250, W - 2 * PAD, 1.12) + 50
    y = draw_block(d, "Neeche comment karo:", font("Medium", 46), MUTED, PAD, y, W - 2 * PAD) + 20
    kf = font("Bold", 96)
    kw = d.textlength(spec["keyword"], font=kf)
    d.rounded_rectangle([PAD, y, PAD + kw + 120, y + 150], radius=30, fill=ACCENT)
    d.text((PAD + 60, y + 18), spec["keyword"], font=kf, fill=BG)
    y = draw_block(d, "DM mein bhej dunga.", font("Medium", 44), WHITE, PAD, y + 220, W - 2 * PAD) + 60
    d.line([PAD, y, W - PAD, y], fill=CARD, width=4)
    y = draw_block(d, "Apne partner ya sales head ko bhejo — unko bhi yeh jaanna chahiye.",
                   font("Regular", 40), MUTED, PAD, y + 50, W - 2 * PAD) + 30
    draw_block(d, "Follow @addzify62026 for factory marketing", font("Bold", 38), ACCENT, PAD, y, W - 2 * PAD)
    return img


def validate(spec):
    missing = [k for k in REQUIRED if not spec.get(k)]
    if missing:
        raise ValueError(f"spec missing fields: {missing}")
    if not 3 <= len(spec["points"]) <= 6:
        raise ValueError("points must have 3-6 items (Instagram allows max 10 slides)")
    for p in spec["points"]:
        if len(p) != 3 or not all(isinstance(x, str) and x.strip() for x in p):
            raise ValueError(f"each point needs [title, box1, box2]: {p}")
    if len(spec["caption"]) > 2200:
        raise ValueError("caption exceeds Instagram's 2200-char limit")


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: python3 make_carousel.py <spec.json> <output_dir>")
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    validate(spec)
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    total = len(spec["points"]) + 2
    slides = [hook_slide(spec, total)]
    for i, (t, b1, b2) in enumerate(spec["points"], start=1):
        slides.append(point_slide(spec, i + 1, total, i, t, b1, b2))
    slides.append(cta_slide(spec, total, total))
    for i, s in enumerate(slides, start=1):
        p = out / f"slide_{i:02d}.jpg"
        s.save(p, "JPEG", quality=92)
        print(p)


if __name__ == "__main__":
    main()
