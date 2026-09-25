"""Generate web-sized copies of the images in Art/ for the science_art.html gallery.

Run from the repository root after adding an image to Art/:
    python assets/scripts/make_gallery_images.py

Creates (only when missing or older than the original):
    Art/thumbs/<name>.webp  - grid thumbnail, max 1000 px on the long side
    Art/web/<name>.webp     - lightbox preview, max 2400 px on the long side
Animated GIFs are skipped; the gallery uses the original GIF directly.
"""
import os
from PIL import Image

Image.MAX_IMAGE_PIXELS = None  # some originals are > 100 megapixels

ART = "Art"
SIZES = {"thumbs": 1000, "web": 2400}

for fname in sorted(os.listdir(ART)):
    src = os.path.join(ART, fname)
    stem, ext = os.path.splitext(fname)
    if not os.path.isfile(src) or ext.lower() not in (".png", ".jpg", ".jpeg"):
        continue
    for folder, max_px in SIZES.items():
        os.makedirs(os.path.join(ART, folder), exist_ok=True)
        dst = os.path.join(ART, folder, stem + ".webp")
        if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
            continue
        with Image.open(src) as im:
            im = im.convert("RGBA" if "A" in im.getbands() else "RGB")
            im.thumbnail((max_px, max_px), Image.LANCZOS)
            im.save(dst, "WEBP", quality=85, method=6)
        print(f"{dst}  {im.size[0]}x{im.size[1]}  {os.path.getsize(dst) // 1024} KB")
