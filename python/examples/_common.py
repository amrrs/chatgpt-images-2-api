"""Shared helpers for the gpt-image-2 featured-prompt examples.

Keeps each example file focused on the prompt itself.
"""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlparse

import requests

_SAFE_CHARS = re.compile(r"[^a-zA-Z0-9._-]+")


def on_queue_update(update) -> None:
    """Print fal.ai queue logs as they arrive."""
    if getattr(update, "status", None) == "IN_PROGRESS":
        for log in getattr(update, "logs", None) or []:
            msg = log.get("message") if isinstance(log, dict) else str(log)
            if msg:
                print(msg)


def save_images(result: dict, prefix: str, output_dir: str = "outputs") -> list[Path]:
    """Download all images in a fal.ai result dict to ``output_dir``."""
    paths: list[Path] = []
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    for i, img in enumerate(result.get("images", [])):
        url = img["url"]
        ext = ""
        if img.get("file_name") and "." in img["file_name"]:
            ext = "." + img["file_name"].rsplit(".", 1)[-1]
        else:
            name = Path(urlparse(url).path).name
            ext = "." + name.rsplit(".", 1)[-1] if "." in name else ".png"
        filename = _SAFE_CHARS.sub("_", f"{prefix}_{i}{ext}").strip("._") or f"image_{i}"
        path = Path(output_dir) / filename
        r = requests.get(url, timeout=120, stream=True)
        r.raise_for_status()
        with open(path, "wb") as fh:
            for chunk in r.iter_content(64 * 1024):
                fh.write(chunk)
        paths.append(path)
    return paths
