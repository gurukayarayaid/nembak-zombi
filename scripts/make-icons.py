#!/usr/bin/env python
"""Membuat semua ikon Nembak Zombi dari satu gambar programatik.

Pemakaian:  python scripts/make-icons.py

Menghasilkan (di assets/):
  favicon-48.png          favicon PNG kecil
  icon-192.png / icon-512.png          ikon PWA standar (latar lingkaran)
  icon-maskable-192.png / icon-maskable-512.png   varian maskable Android
  apple-touch-icon.png    ikon homescreen iOS (latar penuh)
"""
from PIL import Image, ImageDraw
import os

os.chdir(os.path.join(os.path.dirname(__file__), "..", "assets"))

DARK = (13, 20, 28)          # warna luar latar (#0d141c)


def draw_zombie(size: int, maskable: bool = False, full_bg: bool = False) -> Image.Image:
    """Menggambar ikon pada `size` px. Konten diskalakan 85% utk maskable/iOS."""
    S8 = size * 8                                   # supersampling 8x
    k = S8 / 64.0                                   # ruang desain 64 -> piksel

    def sc(*vals):
        if maskable or full_bg:
            return [32.0 * k + (v * k - 32.0 * k) * 0.85 for v in vals]
        return [v * k for v in vals]

    img = Image.new('RGBA', (S8, S8), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    if full_bg:
        d.rectangle([0, 0, S8, S8], fill=DARK + (255,))

    # latar radial (lingkaran konsentris)
    inner, outer = (36, 56, 74), DARK
    steps = 48
    for i in range(steps):
        t = i / (steps - 1)
        col = tuple(round(inner[j] + (outer[j] - inner[j]) * t) for j in range(3)) + (255,)
        r = 32 * k * (1 - t)
        d.ellipse([32 * k - r, 32 * k - r, 32 * k + r, 32 * k + r], fill=col)

    # bulan + kawah
    d.ellipse(sc(44, 8, 54, 18), fill=(244, 233, 200, 255))
    d.ellipse(sc(45.9, 9.9, 48.1, 12.1), fill=(217, 203, 164, 255))
    d.ellipse(sc(50.2, 15.2, 51.8, 16.8), fill=(217, 203, 164, 255))

    # kulit gradasi + kepala rounded-rect
    top, bot = (143, 212, 96), (78, 154, 61)
    grad = Image.new('RGBA', (S8, S8))
    gd = ImageDraw.Draw(grad)
    y0, y1 = sc(16)[0], sc(52)[0]
    for y in range(int(y0), int(y1)):
        t = (y - y0) / (y1 - y0)
        c = tuple(round(top[j] + (bot[j] - top[j]) * t) for j in range(3)) + (255,)
        gd.line([(0, y), (S8, y)], fill=c)
    mask = Image.new('L', (S8, S8), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle(sc(12, 16, 52, 52), radius=17 * (S8 / 64.0) * (0.85 if (maskable or full_bg) else 1), fill=255)
    img.paste(grad, (0, 0), mask)

    d.rounded_rectangle(sc(12, 16, 52, 52), radius=17 * k, outline=(43, 84, 35, 255), width=max(1, int(2.5 * k)))

    dark = (43, 84, 35, 255)
    w = max(1, int(2 * k))
    d.line(sc(28, 17.5, 31, 23), fill=dark, width=w)          # jahitan atas
    d.line(sc(31, 23, 27, 25.5), fill=dark, width=w)
    w = max(1, int(1.8 * k))
    d.line(sc(15, 40, 21, 40), fill=dark, width=w)            # bopeng silang
    d.line(sc(17.5, 37.5, 17.5, 42.5), fill=dark, width=w)
    blotch = (93, 166, 68, 191)                               # bopeng oval
    d.ellipse(sc(39.8, 20, 46.2, 24), fill=blotch)
    d.ellipse(sc(42.6, 40.4, 47.4, 43.6), fill=blotch)

    # mata
    d.ellipse(sc(17.5, 24, 30.5, 38), fill=(248, 246, 238, 255), outline=(38, 52, 60, 255), width=max(1, int(1.5 * k)))
    d.ellipse(sc(36, 25.5, 46, 36.5), fill=(248, 246, 238, 255), outline=(38, 52, 60, 255), width=max(1, int(1.5 * k)))
    d.ellipse(sc(22.9, 29.4, 28.1, 34.6), fill=(28, 28, 28, 255))
    d.ellipse(sc(37.6, 29.8, 42, 34.2), fill=(28, 28, 28, 255))
    d.arc(sc(19.5, 26.5, 24.5, 31.5), start=200, end=290, fill=(211, 79, 79, 255), width=max(1, int(k)))

    # mulut & gigi
    d.rounded_rectangle(sc(21, 43, 43, 51), radius=3 * k, fill=(51, 37, 31, 255))
    for x0 in (23.5, 30, 36.5):
        d.rounded_rectangle(sc(x0, 43, x0 + 4, 47.2), radius=k, fill=(243, 239, 226, 255))
    for x0 in (26.5, 33):
        d.rounded_rectangle(sc(x0, 47.8, x0 + 4, 51), radius=k, fill=(232, 226, 207, 255))

    return img.resize((size, size), Image.LANCZOS)


draw_zombie(48).save('favicon-48.png')
draw_zombie(192).save('icon-192.png')
draw_zombie(512).save('icon-512.png')
draw_zombie(192, maskable=True, full_bg=True).save('icon-maskable-192.png')
draw_zombie(512, maskable=True, full_bg=True).save('icon-maskable-512.png')
draw_zombie(180, full_bg=True).save('apple-touch-icon.png')
print('Semua ikon dibuat di assets/')
