"""Streaming text-to-image example for GPT Image 2 (gpt-image-2) via fal.ai.

Streams live events from the fal.ai queue using the official `fal-client` SDK.

Usage
-----
    export FAL_KEY=...
    python text_to_image_stream.py --prompt "a cute corgi astronaut, 4k"
"""

from __future__ import annotations

import argparse
import os
import sys

import fal_client
from dotenv import load_dotenv


def main() -> int:
    load_dotenv()
    p = argparse.ArgumentParser(description="Stream gpt-image-2 events")
    p.add_argument("--prompt", required=True)
    p.add_argument("--size", default="landscape_4_3")
    p.add_argument("--quality", default="high", choices=["low", "medium", "high"])
    args = p.parse_args()

    if not os.environ.get("FAL_KEY"):
        print("FAL_KEY not set. Get one at https://fal.ai/dashboard/keys", file=sys.stderr)
        return 1

    for event in fal_client.stream(
        "openai/gpt-image-2",
        arguments={
            "prompt": args.prompt,
            "image_size": args.size,
            "quality": args.quality,
        },
    ):
        print(event)
    return 0


if __name__ == "__main__":
    sys.exit(main())
