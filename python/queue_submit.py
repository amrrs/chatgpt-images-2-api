"""Queue-based (async) example for GPT Image 2 (gpt-image-2) via fal.ai.

Shows the submit -> status -> result flow that you'd use when pairing
GPT Image 2 with a webhook or a long-running backend job.

Usage
-----
    export FAL_KEY=...
    python queue_submit.py --prompt "a surreal oil painting of Mars at sunrise"
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import fal_client
import requests
from dotenv import load_dotenv

_SAFE_CHARS = re.compile(r"[^a-zA-Z0-9._-]+")
APP_ID = "openai/gpt-image-2"


def _save(url: str, output_dir: str, filename: str | None = None) -> Path:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    if not filename:
        filename = Path(urlparse(url).path).name or "gpt-image-2-queue.png"
    filename = _SAFE_CHARS.sub("_", filename).strip("._") or "image"
    path = Path(output_dir) / filename
    r = requests.get(url, timeout=120, stream=True)
    r.raise_for_status()
    with open(path, "wb") as fh:
        for chunk in r.iter_content(64 * 1024):
            fh.write(chunk)
    return path


def main() -> int:
    load_dotenv()
    p = argparse.ArgumentParser(description="Queue submit/status/result with gpt-image-2")
    p.add_argument("--prompt", required=True)
    p.add_argument("--size", default="landscape_4_3")
    p.add_argument("--webhook-url", default=None)
    p.add_argument("--poll-interval", type=float, default=2.0)
    args = p.parse_args()

    if not os.environ.get("FAL_KEY"):
        print("FAL_KEY not set. Get one at https://fal.ai/dashboard/keys", file=sys.stderr)
        return 1

    handle = fal_client.submit(
        APP_ID,
        arguments={
            "prompt": args.prompt,
            "image_size": args.size,
            "quality": "high",
        },
        webhook_url=args.webhook_url,
    )
    request_id = handle.request_id
    print(f"Submitted. request_id = {request_id}")

    while True:
        status = fal_client.status(APP_ID, request_id=request_id, with_logs=True)
        state = type(status).__name__
        print(f"status = {state}")
        if state in {"Completed", "CompletedWithErrors", "Failed"}:
            break
        time.sleep(args.poll_interval)

    result = fal_client.result(APP_ID, request_id=request_id)
    images = result.get("images", [])
    print(f"Got {len(images)} image(s).")
    for i, img in enumerate(images):
        path = _save(img["url"], "outputs", f"gpt-image-2-queue_{i}.png")
        print(f"Saved: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
