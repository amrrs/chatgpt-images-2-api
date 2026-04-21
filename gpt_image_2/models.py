"""Typed data models for the gpt-image-2 wrapper.

Mirrors the fal.ai schema for ``openai/gpt-image-2`` (text-to-image) and
``openai/gpt-image-2/edit`` (image editing).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Literal, Optional, Union

ImageSizePreset = Literal[
    "square_hd",
    "square",
    "portrait_4_3",
    "portrait_16_9",
    "landscape_4_3",
    "landscape_16_9",
]

EditImageSizePreset = Literal[
    "square_hd",
    "square",
    "portrait_4_3",
    "portrait_16_9",
    "landscape_4_3",
    "landscape_16_9",
    "auto",
]

Quality = Literal["low", "medium", "high"]
OutputFormat = Literal["jpeg", "png", "webp"]


@dataclass
class ImageSize:
    """Custom image size. Both dims must be multiples of 16, max edge 3840px."""

    width: int = 512
    height: int = 512

    def to_dict(self) -> Dict[str, int]:
        return {"width": self.width, "height": self.height}


@dataclass
class GenerateParams:
    """Parameters for text-to-image generation with gpt-image-2."""

    prompt: str
    image_size: Union[ImageSizePreset, ImageSize, Dict[str, int]] = "landscape_4_3"
    quality: Quality = "high"
    num_images: int = 1
    output_format: OutputFormat = "png"
    sync_mode: bool = False

    def to_payload(self) -> Dict[str, Any]:
        size: Any = self.image_size
        if isinstance(size, ImageSize):
            size = size.to_dict()
        return {
            "prompt": self.prompt,
            "image_size": size,
            "quality": self.quality,
            "num_images": self.num_images,
            "output_format": self.output_format,
            "sync_mode": self.sync_mode,
        }


@dataclass
class EditParams:
    """Parameters for image editing with gpt-image-2/edit."""

    prompt: str
    image_urls: List[str] = field(default_factory=list)
    image_size: Union[EditImageSizePreset, ImageSize, Dict[str, int]] = "auto"
    quality: Quality = "high"
    num_images: int = 1
    output_format: OutputFormat = "png"
    sync_mode: bool = False
    mask_url: Optional[str] = None

    def to_payload(self) -> Dict[str, Any]:
        size: Any = self.image_size
        if isinstance(size, ImageSize):
            size = size.to_dict()
        payload: Dict[str, Any] = {
            "prompt": self.prompt,
            "image_urls": list(self.image_urls),
            "image_size": size,
            "quality": self.quality,
            "num_images": self.num_images,
            "output_format": self.output_format,
            "sync_mode": self.sync_mode,
        }
        if self.mask_url:
            payload["mask_url"] = self.mask_url
        return payload


@dataclass
class ImageFile:
    """One generated image returned by gpt-image-2."""

    url: str
    width: Optional[int] = None
    height: Optional[int] = None
    content_type: Optional[str] = None
    file_name: Optional[str] = None
    file_size: Optional[int] = None

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ImageFile":
        return cls(
            url=d["url"],
            width=d.get("width"),
            height=d.get("height"),
            content_type=d.get("content_type"),
            file_name=d.get("file_name"),
            file_size=d.get("file_size"),
        )


@dataclass
class GenerationResult:
    """Response wrapper containing the list of generated images and raw payload."""

    images: List[ImageFile]
    raw: Dict[str, Any]
    request_id: Optional[str] = None

    @classmethod
    def from_dict(cls, d: Dict[str, Any], request_id: Optional[str] = None) -> "GenerationResult":
        imgs = [ImageFile.from_dict(i) for i in d.get("images", [])]
        return cls(images=imgs, raw=d, request_id=request_id)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "images": [asdict(i) for i in self.images],
            "request_id": self.request_id,
        }

    @property
    def first_url(self) -> Optional[str]:
        return self.images[0].url if self.images else None
