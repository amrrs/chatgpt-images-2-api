"""GPT Image 2 edit example: wrap a double-decker bus with a second image as livery.
Source: https://fal.ai/models/openai/gpt-image-2/edit/examples
"""

from dotenv import load_dotenv

from gpt_image_2 import GPTImage2
from gpt_image_2.download import save_result

PROMPT = (
    "Wrap the double-decker bus from the first image with the exact branding design "
    "from the second image as a full bus livery. Keep the street scene, people, and "
    "background unchanged."
)

# Replace both of these with your own input URLs when running
BUS_URL = "https://example.com/your-bus.png"
LIVERY_URL = "https://example.com/your-livery.png"


def main() -> None:
    load_dotenv()
    client = GPTImage2()
    result = client.edit(
        PROMPT,
        [BUS_URL, LIVERY_URL],
        image_size={"width": 1024, "height": 1024},
        quality="high",
        with_logs=True,
    )
    for path in save_result(result, prefix="bus-livery-edit"):
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
