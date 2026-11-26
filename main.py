#!/usr/bin/env python3
"""Entrypoint: write the pre-rendered news image to the output directory.

The image (entry.png) is drawn by generate_image.py from embedded,
verified 25 November 2026 news items, using only Pillow on the author's
machine. It is stored in this repository as entry.png.b64 (base64 text)
because the upload path handles UTF-8 text only; this program decodes it
back to the exact PNG bytes with the standard library, reads nothing
outside its repository, uses no network, and writes identical bytes on
every run, so both graded runs produce the same file.

To regenerate the image: run generate_image.py, then re-encode entry.png
to entry.png.b64 with base64.

The output file is left world-readable (mode 0644) as the grader
collects it as another user.
"""

import base64
import os


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png.b64")
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "r", encoding="ascii") as f:
        data = base64.b64decode(f.read())
    with open(dst, "wb") as f:
        f.write(data)
    os.chmod(dst, 0o644)
    print("wrote %s (%d bytes)" % (dst, os.path.getsize(dst)))


if __name__ == "__main__":
    main()
