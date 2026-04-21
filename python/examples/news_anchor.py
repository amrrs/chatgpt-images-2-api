"""GPT Image 2 example: broadcast news anchor mid-broadcast with a legible
"BREAKING: GPT-IMAGE-2 NOW LIVE ON fal" ticker.
Source: https://fal.ai/models/openai/gpt-image-2/examples
"""

from dotenv import load_dotenv

from gpt_image_2 import GPTImage2
from gpt_image_2.download import save_result

PROMPT = (
    "Broadcast news still captured mid-broadcast: a single professional news anchor "
    "seated at a sleek modern desk, caught mid-sentence with a natural speaking "
    "expression, lips slightly parted, eyes focused just off-camera toward an unseen "
    "lead camera. Subtle teleprompter reflection faintly visible on the polished glass "
    "surface of the desk. Behind the anchor, a large curved LED wall screen dominates "
    "the background, displaying a stylized world map in deep navy and cool cyan tones. "
    "A clean lower-third news ticker runs across the bottom of the background screen in "
    "bold uppercase sans-serif typography, reading exactly: "
    "\"BREAKING: GPT-IMAGE-2 NOW LIVE ON fal\" (with \"fal\" rendered in lowercase as a "
    "proper stylized brand name, kept intentionally small and distinct from the uppercase "
    "ticker text around it). Studio atmosphere: crisp, even key lighting on the anchor's "
    "face with a soft rim light separating them from the background, faint haze catching "
    "the backlight for subtle depth, polished reflective floor. Color palette: deep navy "
    "blue, cool steel gray, muted slate, tiny electric cyan accents. Medium shot, "
    "rule-of-thirds composition, 50mm cinema camera look, broadcast-grade clarity. "
    "Negative: no real-world network logos, no watermarks, no channel bugs, no visible "
    "brand names other than the stylized \"fal\" on the ticker."
)


def main() -> None:
    load_dotenv()
    client = GPTImage2()
    result = client.generate(
        PROMPT,
        image_size={"width": 3500, "height": 2500},
        quality="high",
        with_logs=True,
    )
    for path in save_result(result, prefix="news-anchor"):
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
