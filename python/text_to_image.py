"""Minimal text-to-image example for GPT Image 2 (gpt-image-2) via fal.ai.

Uses the official `fal-client` Python SDK directly — no extra wrapper required.
(If you'd like one-liners and a CLI, `pip install -e ..` also installs the
optional `gpt-image-2` wrapper shipped in this repo.)

Usage
-----
    pip install -r requirements.txt
    export FAL_KEY=...                # https://fal.ai/dashboard/keys
    python text_to_image.py \
        --prompt "a cinematic product shot of a red sneaker on wet asphalt" \
        --size landscape_16_9 \
        --quality high

Docs:
- Model: https://fal.ai/models/openai/gpt-image-2
- API:   https://fal.ai/models/openai/gpt-image-2/api
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import fal_client
import requests
from dotenv import load_dotenv

_SAFE_CHARS = re.compile(r"[^a-zA-Z0-9._-]+")


def _on_queue_update(update) -> None:
    if getattr(update, "status", None) == "IN_PROGRESS":
        for log in getattr(update, "logs", None) or []:
            msg = log.get("message") if isinstance(log, dict) else str(log)
            if msg:
                print(msg)


def _save(url: str, output_dir: str, filename: str | None = None) -> Path:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    if not filename:
        filename = Path(urlparse(url).path).name or "gpt-image-2.png"
    filename = _SAFE_CHARS.sub("_", filename).strip("._") or "image"
    path = Path(output_dir) / filename
    r = requests.get(url, timeout=120, stream=True)
    r.raise_for_status()
    with open(path, "wb") as fh:
        for chunk in r.iter_content(64 * 1024):
            fh.write(chunk)
    return path


def _parse_size(raw: str):
    if "x" in raw and raw.split("x", 1)[0].isdigit():
        w, h = raw.split("x", 1)
        return {"width": int(w), "height": int(h)}
    return raw


def main() -> int:
    load_dotenv()
    p = argparse.ArgumentParser(description="Text-to-image with gpt-image-2 via fal.ai")
    p.add_argument(
        "--prompt",
        default=(
            "A single hero infographic titled 'GPT Image 2 is here' demonstrating "
            "16 mini-renders of different art styles in a clean periodic-table grid."
        ),
    )
    p.add_argument("--size", default="landscape_4_3", help="preset or WxH, e.g. 1280x720")
    p.add_argument("--quality", default="high", choices=["low", "medium", "high"])
    p.add_argument("-n", "--num-images", type=int, default=1)
    p.add_argument("--format", dest="output_format", default="png",
                   choices=["jpeg", "png", "webp"])
    p.add_argument("--output-dir", default="outputs")
    args = p.parse_args()

    if not os.environ.get("FAL_KEY"):
        print("FAL_KEY not set. Get one at https://fal.ai/dashboard/keys", file=sys.stderr)
        return 1

    result = fal_client.subscribe(
        "openai/gpt-image-2",
        arguments={
            "prompt": args.prompt,
            "image_size": _parse_size(args.size),
            "quality": args.quality,
            "num_images": args.num_images,
            "output_format": args.output_format,
        },
        with_logs=True,
        on_queue_update=_on_queue_update,
    )

    images = result.get("images", [])
    print(f"Generated {len(images)} image(s):")
    for i, img in enumerate(images):
        print(f"  - {img['url']} ({img.get('width')}x{img.get('height')})")
        path = _save(
            img["url"],
            output_dir=args.output_dir,
            filename=f"gpt-image-2_{i}.{args.output_format}",
        )
        print(f"    saved: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
