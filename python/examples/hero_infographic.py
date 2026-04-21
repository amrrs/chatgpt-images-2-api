"""GPT Image 2 example: recursive hero infographic that flexes the model's
infographic + typography abilities.
Source: https://fal.ai/models/openai/gpt-image-2/examples
"""

import fal_client
from dotenv import load_dotenv

from _common import on_queue_update, save_images

PROMPT = (
    "A single hero infographic titled something like \"GPT Image 2 is here\" "
    "that demonstrates the very capabilities it's announcing. Think periodic-table "
    "or anatomical-diagram aesthetic: clean grid of 16-24 mini-renders showing "
    "different styles (oil painting, anime, blueprint, isometric, photoreal, "
    "watercolor, etc.). Electric aesthetic, color! The genius is recursive - to "
    "make this teaser you literally need a model that's god-tier at infographics. "
    "This is your strongest play because it doesn't need a caption to flex. "
    "No date involved."
)


def main() -> None:
    load_dotenv()
    result = fal_client.subscribe(
        "openai/gpt-image-2",
        arguments={
            "prompt": PROMPT,
            "image_size": {"width": 2000, "height": 1152},
            "quality": "high",
        },
        with_logs=True,
        on_queue_update=on_queue_update,
    )
    for path in save_images(result, prefix="hero-infographic"):
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
