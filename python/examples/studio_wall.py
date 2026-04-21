"""GPT Image 2 example: creative studio review wall with pinned prints and
grease-pencil annotations.
Source: https://fal.ai/models/openai/gpt-image-2/examples
"""

import fal_client
from dotenv import load_dotenv

from _common import on_queue_update, save_images

PROMPT = (
    "Candid photograph of a creative studio's review wall covered in a neat grid of "
    "printed image sheets and loose pinned photographs showing a range of AI generated "
    "visuals: product shots, portraits, landscapes, abstract compositions. Some prints "
    "circled in red grease pencil, a few with handwritten sticky notes saying "
    "\"RERUN\", \"FINAL\", and \"GPT-IMAGE-2 ON fal\". Warm desk-lamp light from below, "
    "the corner of a monitor and a keyboard visible in the foreground, a chair back "
    "partially in frame. An honest, working-studio feel. No real brand logos, no watermark."
)


def main() -> None:
    load_dotenv()
    result = fal_client.subscribe(
        "openai/gpt-image-2",
        arguments={
            "prompt": PROMPT,
            "image_size": {"width": 3500, "height": 2500},
            "quality": "high",
        },
        with_logs=True,
        on_queue_update=on_queue_update,
    )
    for path in save_images(result, prefix="studio-wall"):
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
