"""Queue-based (async) example for GPT Image 2 (gpt-image-2) via fal.ai.

Demonstrates the submit -> status -> result flow that you'd use when pairing
GPT Image 2 with a webhook or long-running backend job.

Usage
-----
    export FAL_KEY=...
    python queue_submit.py --prompt "a surreal oil painting of Mars at sunrise"
"""

from __future__ import annotations

import argparse
import sys
import time

from dotenv import load_dotenv

from gpt_image_2 import GPTImage2
from gpt_image_2.download import save_result


def main() -> int:
    load_dotenv()
    p = argparse.ArgumentParser(description="Queue submit/status/result with gpt-image-2")
    p.add_argument("--prompt", required=True)
    p.add_argument("--size", default="landscape_4_3")
    p.add_argument("--webhook-url", default=None)
    p.add_argument("--poll-interval", type=float, default=2.0)
    args = p.parse_args()

    client = GPTImage2()

    request_id = client.submit(args.prompt, image_size=args.size, webhook_url=args.webhook_url)
    print(f"Submitted. request_id = {request_id}")

    while True:
        status = client.status(request_id, with_logs=True)
        state = status.get("status") or status.get("state") or type(status).__name__
        print(f"status = {state}")
        if str(state).upper() in {"COMPLETED", "COMPLETED_WITH_ERRORS", "FAILED"}:
            break
        time.sleep(args.poll_interval)

    result = client.result(request_id)
    print(f"Got {len(result.images)} image(s).")
    for path in save_result(result, prefix="gpt-image-2-queue"):
        print(f"Saved: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
