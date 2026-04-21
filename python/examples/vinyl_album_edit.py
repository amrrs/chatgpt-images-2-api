"""GPT Image 2 edit example: turn any image into a vinyl album cover.
Source: https://fal.ai/models/openai/gpt-image-2/edit/examples
"""

from dotenv import load_dotenv

from gpt_image_2 import GPTImage2
from gpt_image_2.download import save_result

PROMPT = (
    "Transform this into a vinyl album cover. Add a bold album title \"DISTANCES\" in a "
    "clean condensed sans-serif across the top. Artist name \"CLARA VEIL\" in smaller "
    "type below it. A parental advisory sticker in the bottom right corner. The image "
    "gains a slight halftone print texture and the colors shift toward faded vintage "
    "tones. Add a thin white border around the entire image like a physical print. "
    "A small record label logo in the bottom left corner reading \"MERIDIAN RECORDS\". "
    "It should look like you're holding an actual vinyl sleeve."
)

# Replace with your own input URL when running
INPUT_URL = "https://v3b.fal.media/files/b/0a8691af/9Se_1_VX1wzTjjTOpWbs9_bb39c2eb-1a41-4749-b1d0-cf134abc8bbf.png"


def main() -> None:
    load_dotenv()
    client = GPTImage2()
    result = client.edit(
        PROMPT,
        [INPUT_URL],
        image_size={"width": 3000, "height": 2000},
        quality="high",
        with_logs=True,
    )
    for path in save_result(result, prefix="vinyl-album-edit"):
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
