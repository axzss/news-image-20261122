#!/usr/bin/env python3
"""THE WORLD - Sunday 22 November 2026 (news-image-20261122).

Entrypoint for the make.fun bounty "Sum up 22 November's world news in
one image". The entry image is rendered at build time by render.py (a PIL
newspaper front page: masthead, a generated dusk photograph of tankers in
the Strait of Hormuz, the day's lead stories, an ALSO TODAY strip and a
markets line) and bundled at assets/entry.png. This program only copies
that bundled image to the output path, so it is deterministic, needs no
network, and produces a byte-identical file on every run.
"""
import argparse
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUNDLED = HERE / "assets" / "entry.png"


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Write the entry image to the output path.")
    parser.add_argument(
        "--output", default="/output/entry.png",
        help="Where to write the image (default: /output/entry.png)")
    args = parser.parse_args(argv)

    if not BUNDLED.is_file():
        print(f"bundled image missing: {BUNDLED}", file=sys.stderr)
        return 1
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(BUNDLED, out)
    print(f"wrote {out} ({out.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
