"""Minimal text-to-image example for GPT Image 2 (gpt-image-2) via fal.ai.

Runs with the tiny `gpt_image_2` Python wrapper shipped in this repo.

Usage
-----
    pip install -e ..            # or: pip install gpt-image-2
    export FAL_KEY=...           # https://fal.ai/dashboard/keys
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
import sys

from dotenv import load_dotenv

from gpt_image_2 import GPTImage2
from gpt_image_2.download import save_result


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
    p.add_argument("--size", default="landscape_4_3")
    p.add_argument("--quality", default="high", choices=["low", "medium", "high"])
    p.add_argument("-n", "--num-images", type=int, default=1)
    p.add_argument("--format", dest="output_format", default="png",
                   choices=["jpeg", "png", "webp"])
    p.add_argument("--output-dir", default="outputs")
    args = p.parse_args()

    client = GPTImage2()
    result = client.generate(
        args.prompt,
        image_size=args.size,
        quality=args.quality,
        num_images=args.num_images,
        output_format=args.output_format,
        with_logs=True,
    )

    print(f"Generated {len(result.images)} image(s):")
    for img in result.images:
        print(f"  - {img.url} ({img.width}x{img.height})")

    paths = save_result(result, output_dir=args.output_dir, prefix="gpt-image-2")
    for path in paths:
        print(f"Saved: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
