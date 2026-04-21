"""Helpers to download generated images from fal.ai URLs to disk."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Iterable, List, Union
from urllib.parse import urlparse

import requests

from .models import GenerationResult, ImageFile

_SAFE_CHARS = re.compile(r"[^a-zA-Z0-9._-]+")


def _safe_name(name: str) -> str:
    return _SAFE_CHARS.sub("_", name).strip("._") or "image"


def save_image(
    image: Union[ImageFile, str],
    output_dir: Union[str, os.PathLike] = "outputs",
    filename: Union[str, None] = None,
    timeout: int = 120,
) -> Path:
    """Download a single ImageFile (or URL) to ``output_dir``.

    Returns the path to the written file.
    """
    url = image.url if isinstance(image, ImageFile) else image
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if filename is None:
        if isinstance(image, ImageFile) and image.file_name:
            filename = image.file_name
        else:
            parsed = urlparse(url)
            filename = Path(parsed.path).name or "image.png"
    filename = _safe_name(filename)

    path = out_dir / filename
    resp = requests.get(url, timeout=timeout, stream=True)
    resp.raise_for_status()
    with open(path, "wb") as fh:
        for chunk in resp.iter_content(chunk_size=64 * 1024):
            if chunk:
                fh.write(chunk)
    return path


def save_result(
    result: GenerationResult,
    output_dir: Union[str, os.PathLike] = "outputs",
    prefix: Union[str, None] = None,
    timeout: int = 120,
) -> List[Path]:
    """Download every image in a GenerationResult to ``output_dir``.

    If ``prefix`` is provided, files are named ``{prefix}_{i}{ext}``.
    """
    paths: List[Path] = []
    images: Iterable[ImageFile] = result.images
    for i, img in enumerate(images):
        if prefix is not None:
            ext = ""
            if img.file_name and "." in img.file_name:
                ext = "." + img.file_name.rsplit(".", 1)[-1]
            elif img.content_type and "/" in img.content_type:
                ext = "." + img.content_type.split("/", 1)[-1]
            else:
                ext = ".png"
            name = f"{prefix}_{i}{ext}"
            paths.append(save_image(img, output_dir=output_dir, filename=name, timeout=timeout))
        else:
            paths.append(save_image(img, output_dir=output_dir, timeout=timeout))
    return paths
