#!/usr/bin/env python3
"""Entry point: write the pre-rendered front page to the output directory.

The image is rendered ahead of time by draw.py and committed as entry.png.
This program uses only the standard library, needs no network, and never
writes into the repository: it reads the bundled image next to this file
and writes it to the output directory, honouring MAKEFUN_OUTPUT_DIR.
"""

import os
import shutil
from pathlib import Path


def run():
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        raise SystemExit("entry.png is missing next to main.py")
    with source.open("rb") as handle:
        if handle.read(8) != b"\x89PNG\r\n\x1a\n":
            raise SystemExit("entry.png is not a PNG image")
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"
    shutil.copyfile(source, target)
    print("wrote {} ({} bytes)".format(target, target.stat().st_size))


if __name__ == "__main__":
    run()
