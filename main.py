#!/usr/bin/env python3
"""Entrypoint: copy the pre-rendered entry.png to the output directory.

The image is rendered ahead of time by draw.py and committed as entry.png.
This program needs no network and never writes into the repository: it only
reads the bundled image next to this file and writes it to the output
directory, honouring MAKEFUN_OUTPUT_DIR for local runs. Standard library
only, so it runs unchanged in the grading sandbox.
"""

import os
import shutil
from pathlib import Path


def main():
    here = Path(__file__).resolve().parent
    src = here / "entry.png"
    if not src.is_file():
        raise SystemExit("entry.png is missing next to main.py")
    with src.open("rb") as f:
        if f.read(8) != b"\x89PNG\r\n\x1a\n":
            raise SystemExit("entry.png is not a PNG image")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(src, dest)
    print(f"wrote {dest} ({dest.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
