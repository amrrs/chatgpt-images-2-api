"""gpt-image-2: a tiny Python wrapper / SDK for OpenAI's GPT Image 2.0 via fal.ai.

Primary entry points:

    from gpt_image_2 import GPTImage2, generate, edit, stream

    # One-liner text-to-image
    result = generate("a cinematic product shot of a red sneaker")

    # One-liner image edit
    result = edit(
        "Wrap the double-decker bus with this livery design",
        image_urls=["https://...input.png"],
    )

The wrapper targets the `openai/gpt-image-2` and `openai/gpt-image-2/edit`
endpoints hosted on fal.ai. Set the ``FAL_KEY`` environment variable, or pass
``api_key=`` to :class:`GPTImage2`.

Docs: https://github.com/amrrs/chatgpt-images-2-api
fal.ai: https://fal.ai/models/openai/gpt-image-2
"""

from .client import GPTImage2, edit, generate, stream
from .models import EditParams, GenerateParams, GenerationResult, ImageFile

__all__ = [
    "GPTImage2",
    "generate",
    "edit",
    "stream",
    "GenerateParams",
    "EditParams",
    "GenerationResult",
    "ImageFile",
]

__version__ = "0.1.0"
