"""Core client for the gpt-image-2 Python wrapper.

Wraps the fal.ai ``openai/gpt-image-2`` (text-to-image) and
``openai/gpt-image-2/edit`` (image editing) endpoints behind a small,
typed, batteries-included API.
"""

from __future__ import annotations

import os
from typing import Any, Callable, Dict, Iterable, Iterator, List, Optional, Union

import fal_client

from .models import (
    EditImageSizePreset,
    EditParams,
    GenerateParams,
    GenerationResult,
    ImageSize,
    ImageSizePreset,
    OutputFormat,
    Quality,
)

#: fal.ai app id for text-to-image.
APP_ID_TEXT_TO_IMAGE = "openai/gpt-image-2"

#: fal.ai app id for image editing.
APP_ID_EDIT = "openai/gpt-image-2/edit"


LogHandler = Callable[[str], None]


def _default_log_handler(message: str) -> None:
    print(message)


class GPTImage2:
    """Python wrapper / SDK for GPT Image 2 (gpt-image-2) hosted on fal.ai.

    Parameters
    ----------
    api_key:
        Your fal.ai API key. Falls back to the ``FAL_KEY`` environment variable.
    text_to_image_app:
        Override the fal app id for text-to-image (defaults to ``openai/gpt-image-2``).
    edit_app:
        Override the fal app id for edits (defaults to ``openai/gpt-image-2/edit``).

    Example
    -------
    >>> from gpt_image_2 import GPTImage2
    >>> client = GPTImage2()
    >>> result = client.generate("a cinematic product shot of a red sneaker")
    >>> print(result.first_url)
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        text_to_image_app: str = APP_ID_TEXT_TO_IMAGE,
        edit_app: str = APP_ID_EDIT,
    ) -> None:
        key = api_key or os.environ.get("FAL_KEY")
        if key:
            os.environ["FAL_KEY"] = key
        self.text_to_image_app = text_to_image_app
        self.edit_app = edit_app

    # ------------------------------------------------------------------ generate
    def generate(
        self,
        prompt: str,
        *,
        image_size: Union[ImageSizePreset, ImageSize, Dict[str, int]] = "landscape_4_3",
        quality: Quality = "high",
        num_images: int = 1,
        output_format: OutputFormat = "png",
        sync_mode: bool = False,
        with_logs: bool = False,
        on_log: Optional[LogHandler] = None,
    ) -> GenerationResult:
        """Text-to-image generation via ``openai/gpt-image-2``."""
        params = GenerateParams(
            prompt=prompt,
            image_size=image_size,
            quality=quality,
            num_images=num_images,
            output_format=output_format,
            sync_mode=sync_mode,
        )
        return self._subscribe(self.text_to_image_app, params.to_payload(), with_logs, on_log)

    # ---------------------------------------------------------------------- edit
    def edit(
        self,
        prompt: str,
        image_urls: Union[str, Iterable[str]],
        *,
        image_size: Union[EditImageSizePreset, ImageSize, Dict[str, int]] = "auto",
        quality: Quality = "high",
        num_images: int = 1,
        output_format: OutputFormat = "png",
        sync_mode: bool = False,
        mask_url: Optional[str] = None,
        with_logs: bool = False,
        on_log: Optional[LogHandler] = None,
    ) -> GenerationResult:
        """Image editing via ``openai/gpt-image-2/edit``.

        ``image_urls`` accepts a single URL or a list of reference image URLs
        (public URL or base64 data URI).
        """
        if isinstance(image_urls, str):
            urls: List[str] = [image_urls]
        else:
            urls = list(image_urls)
        params = EditParams(
            prompt=prompt,
            image_urls=urls,
            image_size=image_size,
            quality=quality,
            num_images=num_images,
            output_format=output_format,
            sync_mode=sync_mode,
            mask_url=mask_url,
        )
        return self._subscribe(self.edit_app, params.to_payload(), with_logs, on_log)

    # ---------------------------------------------------------------- streaming
    def stream(
        self,
        prompt: str,
        *,
        image_size: Union[ImageSizePreset, ImageSize, Dict[str, int]] = "landscape_4_3",
        quality: Quality = "high",
        num_images: int = 1,
        output_format: OutputFormat = "png",
    ) -> Iterator[Dict[str, Any]]:
        """Stream events for a text-to-image request.

        Yields raw event dicts from fal.ai's streaming endpoint. The final event
        contains the same payload shape as :meth:`generate` would return.
        """
        params = GenerateParams(
            prompt=prompt,
            image_size=image_size,
            quality=quality,
            num_images=num_images,
            output_format=output_format,
        )
        yield from fal_client.stream(self.text_to_image_app, arguments=params.to_payload())

    def stream_edit(
        self,
        prompt: str,
        image_urls: Union[str, Iterable[str]],
        *,
        image_size: Union[EditImageSizePreset, ImageSize, Dict[str, int]] = "auto",
        quality: Quality = "high",
        num_images: int = 1,
        output_format: OutputFormat = "png",
        mask_url: Optional[str] = None,
    ) -> Iterator[Dict[str, Any]]:
        """Stream events for an image-edit request."""
        if isinstance(image_urls, str):
            urls: List[str] = [image_urls]
        else:
            urls = list(image_urls)
        params = EditParams(
            prompt=prompt,
            image_urls=urls,
            image_size=image_size,
            quality=quality,
            num_images=num_images,
            output_format=output_format,
            mask_url=mask_url,
        )
        yield from fal_client.stream(self.edit_app, arguments=params.to_payload())

    # -------------------------------------------------------------------- queue
    def submit(
        self,
        prompt: str,
        *,
        image_size: Union[ImageSizePreset, ImageSize, Dict[str, int]] = "landscape_4_3",
        quality: Quality = "high",
        num_images: int = 1,
        output_format: OutputFormat = "png",
        webhook_url: Optional[str] = None,
    ) -> str:
        """Submit a text-to-image request to the queue. Returns ``request_id``."""
        params = GenerateParams(
            prompt=prompt,
            image_size=image_size,
            quality=quality,
            num_images=num_images,
            output_format=output_format,
        )
        handle = fal_client.submit(
            self.text_to_image_app,
            arguments=params.to_payload(),
            webhook_url=webhook_url,
        )
        return handle.request_id

    def status(self, request_id: str, *, with_logs: bool = False) -> Dict[str, Any]:
        """Fetch the queue status for a submitted request."""
        status = fal_client.status(
            self.text_to_image_app, request_id=request_id, with_logs=with_logs
        )
        if hasattr(status, "__dict__"):
            return dict(status.__dict__)
        return dict(status)  # type: ignore[arg-type]

    def result(self, request_id: str) -> GenerationResult:
        """Fetch the final result of a queued request."""
        raw = fal_client.result(self.text_to_image_app, request_id=request_id)
        return GenerationResult.from_dict(raw, request_id=request_id)

    # ---------------------------------------------------------------- internal
    def _subscribe(
        self,
        app_id: str,
        payload: Dict[str, Any],
        with_logs: bool,
        on_log: Optional[LogHandler],
    ) -> GenerationResult:
        handler = on_log or (_default_log_handler if with_logs else None)

        def _on_update(update: Any) -> None:
            if handler is None:
                return
            status = getattr(update, "status", None) or (
                update.get("status") if isinstance(update, dict) else None
            )
            if status == "IN_PROGRESS":
                logs = getattr(update, "logs", None) or (
                    update.get("logs") if isinstance(update, dict) else None
                ) or []
                for entry in logs:
                    msg = entry.get("message") if isinstance(entry, dict) else str(entry)
                    if msg:
                        handler(msg)

        raw = fal_client.subscribe(
            app_id,
            arguments=payload,
            with_logs=with_logs,
            on_queue_update=_on_update if handler else None,
        )
        request_id = None
        if isinstance(raw, dict):
            request_id = raw.get("request_id")
        return GenerationResult.from_dict(raw, request_id=request_id)


# --------------------------------------------------------------------- helpers
# Module-level one-liner conveniences that reuse a default client.

_default_client: Optional[GPTImage2] = None


def _client() -> GPTImage2:
    global _default_client
    if _default_client is None:
        _default_client = GPTImage2()
    return _default_client


def generate(prompt: str, **kwargs: Any) -> GenerationResult:
    """One-liner: ``gpt_image_2.generate("a cute corgi astronaut")``."""
    return _client().generate(prompt, **kwargs)


def edit(prompt: str, image_urls: Union[str, Iterable[str]], **kwargs: Any) -> GenerationResult:
    """One-liner: ``gpt_image_2.edit("make it night-time", "https://...png")``."""
    return _client().edit(prompt, image_urls, **kwargs)


def stream(prompt: str, **kwargs: Any) -> Iterator[Dict[str, Any]]:
    """One-liner streaming: ``for event in gpt_image_2.stream("..."): ...``."""
    yield from _client().stream(prompt, **kwargs)
