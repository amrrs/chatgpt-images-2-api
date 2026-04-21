"""Command-line interface for gpt-image-2.

Installed as the ``gpt-image-2`` console script via ``pyproject.toml``.

Examples
--------
    $ export FAL_KEY=...
    $ gpt-image-2 generate "a cinematic product shot of a red sneaker"
    $ gpt-image-2 generate "poster art" --size portrait_16_9 --quality high -n 2
    $ gpt-image-2 edit "make it night-time" --image https://example.com/in.png
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import List, Optional

from . import __version__
from .client import GPTImage2
from .download import save_result


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="gpt-image-2",
        description=(
            "Generate and edit images with GPT Image 2 (gpt-image-2) "
            "via fal.ai. https://fal.ai/models/openai/gpt-image-2"
        ),
    )
    p.add_argument("--version", action="version", version=f"gpt-image-2 {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    # ---- generate ----
    g = sub.add_parser("generate", help="Text-to-image with gpt-image-2")
    g.add_argument("prompt", help="The text prompt to generate an image from")
    g.add_argument(
        "--size",
        default="landscape_4_3",
        help=(
            "Image size preset or WxH (e.g. 1280x720). "
            "Presets: square_hd, square, portrait_4_3, portrait_16_9, landscape_4_3, landscape_16_9"
        ),
    )
    g.add_argument("--quality", default="high", choices=["low", "medium", "high"])
    g.add_argument("-n", "--num-images", type=int, default=1)
    g.add_argument("--format", dest="output_format", default="png", choices=["jpeg", "png", "webp"])
    g.add_argument("--logs", action="store_true", help="Stream fal.ai logs to stderr")
    g.add_argument("--output-dir", default="outputs", help="Where to save images")
    g.add_argument("--prefix", default=None, help="Filename prefix for saved images")
    g.add_argument("--no-save", action="store_true", help="Don't download, just print JSON")

    # ---- edit ----
    e = sub.add_parser("edit", help="Image edit with gpt-image-2/edit")
    e.add_argument("prompt", help="The edit instruction prompt")
    e.add_argument(
        "-i", "--image",
        action="append",
        required=True,
        dest="image_urls",
        help="Input image URL (repeatable). Accepts http(s) URL or data: URI.",
    )
    e.add_argument("--mask", dest="mask_url", default=None)
    e.add_argument(
        "--size",
        default="auto",
        help="Image size preset, 'auto', or WxH",
    )
    e.add_argument("--quality", default="high", choices=["low", "medium", "high"])
    e.add_argument("-n", "--num-images", type=int, default=1)
    e.add_argument("--format", dest="output_format", default="png", choices=["jpeg", "png", "webp"])
    e.add_argument("--logs", action="store_true")
    e.add_argument("--output-dir", default="outputs")
    e.add_argument("--prefix", default=None)
    e.add_argument("--no-save", action="store_true")

    return p


def _parse_size(raw: str):
    if "x" in raw and raw.split("x", 1)[0].isdigit():
        w, h = raw.split("x", 1)
        return {"width": int(w), "height": int(h)}
    return raw


def main(argv: Optional[List[str]] = None) -> int:
    args = _parser().parse_args(argv)
    client = GPTImage2()

    def _log(msg: str) -> None:
        print(msg, file=sys.stderr)

    if args.command == "generate":
        result = client.generate(
            args.prompt,
            image_size=_parse_size(args.size),
            quality=args.quality,
            num_images=args.num_images,
            output_format=args.output_format,
            with_logs=args.logs,
            on_log=_log if args.logs else None,
        )
    elif args.command == "edit":
        result = client.edit(
            args.prompt,
            args.image_urls,
            image_size=_parse_size(args.size),
            quality=args.quality,
            num_images=args.num_images,
            output_format=args.output_format,
            mask_url=args.mask_url,
            with_logs=args.logs,
            on_log=_log if args.logs else None,
        )
    else:  # pragma: no cover
        _parser().print_help()
        return 2

    if not args.no_save:
        paths = save_result(result, output_dir=args.output_dir, prefix=args.prefix)
        for p in paths:
            print(str(p))
    else:
        print(json.dumps(result.to_dict(), indent=2))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
