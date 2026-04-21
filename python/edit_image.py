"""Image editing example for GPT Image 2 (gpt-image-2/edit) via fal.ai.

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
import sys

from dotenv import load_dotenv

from gpt_image_2 import GPTImage2
from gpt_image_2.download import save_result


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
    p.add_argument("--size", default="auto")
    p.add_argument("--quality", default="high", choices=["low", "medium", "high"])
    p.add_argument("-n", "--num-images", type=int, default=1)
    p.add_argument("--format", dest="output_format", default="png",
                   choices=["jpeg", "png", "webp"])
    p.add_argument("--output-dir", default="outputs")
    args = p.parse_args()

    client = GPTImage2()
    result = client.edit(
        args.prompt,
        args.image_urls,
        image_size=args.size,
        quality=args.quality,
        num_images=args.num_images,
        output_format=args.output_format,
        mask_url=args.mask_url,
        with_logs=True,
    )

    print(f"Generated {len(result.images)} edited image(s):")
    for img in result.images:
        print(f"  - {img.url} ({img.width}x{img.height})")

    paths = save_result(result, output_dir=args.output_dir, prefix="gpt-image-2-edit")
    for path in paths:
        print(f"Saved: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
