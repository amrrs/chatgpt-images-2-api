"""Streaming text-to-image example for GPT Image 2 (gpt-image-2) via fal.ai.

Streams live events from the fal.ai queue. Useful when you want progress
updates or partial payloads as they arrive.

Usage
-----
    export FAL_KEY=...
    python text_to_image_stream.py --prompt "a cute corgi astronaut, 4k"
"""

from __future__ import annotations

import argparse
import sys

from dotenv import load_dotenv

from gpt_image_2 import GPTImage2


def main() -> int:
    load_dotenv()
    p = argparse.ArgumentParser(description="Stream gpt-image-2 events")
    p.add_argument("--prompt", required=True)
    p.add_argument("--size", default="landscape_4_3")
    p.add_argument("--quality", default="high", choices=["low", "medium", "high"])
    args = p.parse_args()

    client = GPTImage2()
    for event in client.stream(args.prompt, image_size=args.size, quality=args.quality):
        print(event)
    return 0


if __name__ == "__main__":
    sys.exit(main())
