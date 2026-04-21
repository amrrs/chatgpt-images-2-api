"""GPT Image 2 example: photorealistic corporate boardroom scene.
Source: https://fal.ai/models/openai/gpt-image-2/examples
"""

from dotenv import load_dotenv

from gpt_image_2 import GPTImage2
from gpt_image_2.download import save_result

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
    client = GPTImage2()
    result = client.generate(
        PROMPT,
        image_size={"width": 3000, "height": 2000},
        quality="high",
        with_logs=True,
    )
    for path in save_result(result, prefix="boardroom"):
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
