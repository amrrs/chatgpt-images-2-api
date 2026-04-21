"""GPT Image 2 example: photorealistic corporate boardroom scene.
Source: https://fal.ai/models/openai/gpt-image-2/examples
"""

import fal_client
from dotenv import load_dotenv

from _common import on_queue_update, save_images

PROMPT = (
    "Photorealistic corporate boardroom: a long polished mahogany conference table "
    "with leather executive chairs, a glass of water at each place setting, notepads "
    "and pens arranged neatly, a large flat-screen TV at the end showing a quarterly "
    "revenue chart going up. Floor-to-ceiling windows with a city skyline view. "
    "Serious, sterile corporate atmosphere. Several business executives in suits "
    "seated around the table in a meeting."
)


def main() -> None:
    load_dotenv()
    result = fal_client.subscribe(
        "openai/gpt-image-2",
        arguments={
            "prompt": PROMPT,
            "image_size": {"width": 3000, "height": 2000},
            "quality": "high",
        },
        with_logs=True,
        on_queue_update=on_queue_update,
    )
    for path in save_images(result, prefix="boardroom"):
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
