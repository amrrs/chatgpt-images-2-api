"""Image editing example for GPT Image 2 (gpt-image-2/edit) via fal.ai.

Uses the official `fal-client` Python SDK directly.

Usage
-----
    export FAL_KEY=...
    python edit_image.py \
        --prompt "Wrap the double-decker bus with this livery design" \
        --image https://example.com/bus.png \
        --image https://example.com/livery.png

Docs:
- Edit API: https://fal.ai/models/openai/gpt-image-2/edit/api
- Examples: https://fal.ai/models/openai/gpt-image-2/edit/examples
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
        filename = Path(urlparse(url).path).name or "gpt-image-2-edit.png"
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
    p = argparse.ArgumentParser(description="Image edit with gpt-image-2 via fal.ai")
    p.add_argument("--prompt", required=True, help="Edit instruction prompt")
    p.add_argument(
        "-i", "--image",
        dest="image_urls",
        action="append",
        required=True,
        help="Input image URL (repeatable). http(s) URL or data: URI.",
    )
    p.add_argument("--mask", dest="mask_url", default=None,
                   help="Optional mask URL indicating what to edit")
    p.add_argument("--size", default="auto", help="preset, 'auto', or WxH")
    p.add_argument("--quality", default="high", choices=["low", "medium", "high"])
    p.add_argument("-n", "--num-images", type=int, default=1)
    p.add_argument("--format", dest="output_format", default="png",
                   choices=["jpeg", "png", "webp"])
    p.add_argument("--output-dir", default="outputs")
    args = p.parse_args()

    if not os.environ.get("FAL_KEY"):
        print("FAL_KEY not set. Get one at https://fal.ai/dashboard/keys", file=sys.stderr)
        return 1

    arguments = {
        "prompt": args.prompt,
        "image_urls": args.image_urls,
        "image_size": _parse_size(args.size),
        "quality": args.quality,
        "num_images": args.num_images,
        "output_format": args.output_format,
    }
    if args.mask_url:
        arguments["mask_url"] = args.mask_url

    result = fal_client.subscribe(
        "openai/gpt-image-2/edit",
        arguments=arguments,
        with_logs=True,
        on_queue_update=_on_queue_update,
    )

    images = result.get("images", [])
    print(f"Generated {len(images)} edited image(s):")
    for i, img in enumerate(images):
        print(f"  - {img['url']} ({img.get('width')}x{img.get('height')})")
        path = _save(
            img["url"],
            output_dir=args.output_dir,
            filename=f"gpt-image-2-edit_{i}.{args.output_format}",
        )
        print(f"    saved: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
