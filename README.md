# GPT Image 2 (gpt-image-2) — Python & Node.js API Examples

> **Drop-in Python (`fal-client`) and Node.js (`@fal-ai/client`) examples for OpenAI's GPT Image 2.0 model — the image generation model behind ChatGPT's image features — powered by [fal.ai](https://fal.ai/models/openai/gpt-image-2). Text-to-image and image editing, plus an optional `gpt-image-2` Python wrapper and CLI.**

<sub>Also known as: **ChatGPT Image 2**, **ChatGPT Images 2.0**, **GPT Image 2.0 API**, **OpenAI gpt-image-2 API**, **ChatGPT image generator API**.</sub>

[![fal.ai](https://img.shields.io/badge/Powered%20by-fal.ai-000)](https://fal.ai/models/openai/gpt-image-2)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](#python-quickstart)
[![Node 18+](https://img.shields.io/badge/Node-18%2B-339933?logo=node.js&logoColor=white)](#nodejs-quickstart)

**What is this repo?** Copy-paste-ready **Python** and **Node.js** examples for calling **GPT Image 2** (`gpt-image-2`) — OpenAI's GPT Image 2.0 image model, the same model that powers **ChatGPT's image generation** — through fal.ai's hosted API. It covers both endpoints: **text-to-image** (`openai/gpt-image-2`) and **image editing** (`openai/gpt-image-2/edit`). Every Python snippet below uses the official [`fal-client`](https://pypi.org/project/fal-client/) SDK directly, with zero extra abstractions — the kind of code you'd actually paste into your own project. This repo also ships an optional tiny wrapper (`pip install gpt-image-2`) and a `gpt-image-2` CLI for ergonomics.

> **Searching for "ChatGPT Image 2 API" or "ChatGPT Images 2.0"?** You're in the right place. ChatGPT's in-product image generator is powered by OpenAI's `gpt-image-2` model — the same model this repo calls through fal.ai. See the [ChatGPT vs gpt-image-2 FAQ](./docs/faq.md#is-gpt-image-2-the-same-as-the-chatgpt-image-generator) for the full clarification.

> ▶ **Try GPT Image 2 on the fal.ai playground:** [Text-to-image](https://fal.ai/models/openai/gpt-image-2) · [Edit / image-to-image](https://fal.ai/models/openai/gpt-image-2/edit) · [API docs](https://fal.ai/models/openai/gpt-image-2/api) · [Prompt examples](https://fal.ai/models/openai/gpt-image-2/examples)

---

## Table of contents

- [Features](#features)
- [Python quickstart](#python-quickstart)
- [Node.js quickstart](#nodejs-quickstart)
- [Text-to-image API](#text-to-image-api)
- [Image edit API](#image-edit-api)
- [Streaming and queue](#streaming-and-queue)
- [Image sizes & quality](#image-sizes--quality)
- [Prompts gallery](#prompts-gallery)
- [CLI](#cli)
- [FAQ](#faq)
- [Resources](#resources)

---

## Features

- **Drop-in Python examples** using `fal-client` directly — paste straight into your project.
- Matching **Node.js** examples using `@fal-ai/client`.
- Covers text-to-image **and** image editing (with optional mask).
- Streaming (`stream`), queue (`submit` / `status` / `result`), and webhook support.
- Resolutions up to **3840 px edge** (~4K), strong typography, commercial-use friendly.
- Optional tiny wrapper: `pip install gpt-image-2` for a one-liner API and a `gpt-image-2` CLI.
- MIT licensed.

## Why gpt-image-2 (via fal.ai)?

- **Best-in-class typography.** gpt-image-2 renders clean on-image text reliably — great for infographics, posters, and album art.
- **Fine-grained edits.** The [`/edit`](https://fal.ai/models/openai/gpt-image-2/edit) endpoint accepts one or more reference images plus an optional mask.
- **Up to 3840 px edge** with flexible aspect ratios up to 3:1.
- **Fal.ai hosting** gives you commercial licensing, streaming, and a queue + webhook flow out of the box.

## Python quickstart

### 1. Install

```bash
pip install fal-client
```

### 2. Set your fal.ai API key

```bash
export FAL_KEY="your-fal-api-key"    # get one at https://fal.ai/dashboard/keys
```

### 3. Generate an image

```python
import fal_client

def on_queue_update(update):
    if update.status == "IN_PROGRESS":
        for log in update.logs or []:
            print(log["message"])

result = fal_client.subscribe(
    "openai/gpt-image-2",
    arguments={
        "prompt": "a cinematic product shot of a red sneaker on wet asphalt, 4k",
        "image_size": "landscape_16_9",
        "quality": "high",
    },
    with_logs=True,
    on_queue_update=on_queue_update,
)
print(result["images"][0]["url"])
```

### 4. Edit an image

```python
import fal_client

result = fal_client.subscribe(
    "openai/gpt-image-2/edit",
    arguments={
        "prompt": "Wrap the bus with this branding as a full livery. Keep everything else unchanged.",
        "image_urls": [
            "https://example.com/bus.png",
            "https://example.com/livery.png",
        ],
        "image_size": "auto",
        "quality": "high",
    },
    with_logs=True,
)
print(result["images"][0]["url"])
```

Also see the ready-to-run scripts in [`python/`](./python):

- [`python/text_to_image.py`](./python/text_to_image.py)
- [`python/edit_image.py`](./python/edit_image.py)
- [`python/text_to_image_stream.py`](./python/text_to_image_stream.py)
- [`python/queue_submit.py`](./python/queue_submit.py)
- [`python/examples/`](./python/examples) — runnable versions of every prompt in the [prompts gallery](./docs/prompts-gallery.md).

### Optional: `gpt-image-2` wrapper + CLI

For one-liners and a CLI, install the thin wrapper shipped in this repo:

```bash
pip install gpt-image-2                 # or:  pip install -e .  (from this repo)
```

```python
import gpt_image_2
print(gpt_image_2.generate("a cute corgi astronaut, 4k").first_url)
```

```bash
gpt-image-2 generate "a cute corgi astronaut" --size landscape_16_9 --quality high
gpt-image-2 edit "make it night-time" --image https://example.com/scene.png
```

## Node.js quickstart

### 1. Install

```bash
cd node
npm install
```

### 2. Set your fal.ai API key

```bash
export FAL_KEY="your-fal-api-key"
```

### 3. Generate an image

```bash
node text-to-image.js "a cinematic product shot of a red sneaker on wet asphalt, 4k"
```

Or in code:

```js
import { fal } from "@fal-ai/client";

const result = await fal.subscribe("openai/gpt-image-2", {
  input: {
    prompt: "a cinematic product shot of a red sneaker on wet asphalt, 4k",
    image_size: "landscape_16_9",
    quality: "high",
  },
  logs: true,
});
console.log(result.data.images[0].url);
```

Full Node.js examples: [`node/`](./node).

## Text-to-image API

Endpoint: [`openai/gpt-image-2`](https://fal.ai/models/openai/gpt-image-2/api)

| Field | Type | Default | Notes |
| --- | --- | --- | --- |
| `prompt` | string (required) | — | The prompt. Use quotes for any exact on-image text. |
| `image_size` | preset or `{width, height}` | `landscape_4_3` | Both dims multiples of 16, max edge 3840 px, aspect ≤ 3:1. |
| `quality` | `low` \| `medium` \| `high` | `high` | |
| `num_images` | integer | `1` | |
| `output_format` | `jpeg` \| `png` \| `webp` | `png` | |
| `sync_mode` | boolean | `false` | If `true`, returns a data URI. |

Presets: `square_hd`, `square`, `portrait_4_3`, `portrait_16_9`, `landscape_4_3`, `landscape_16_9`.

Full docs: [docs/text-to-image.md](./docs/text-to-image.md).

## Image edit API

Endpoint: [`openai/gpt-image-2/edit`](https://fal.ai/models/openai/gpt-image-2/edit/api)

| Field | Type | Default | Notes |
| --- | --- | --- | --- |
| `prompt` | string (required) | — | Edit instruction. |
| `image_urls` | list<string> (required) | — | One or more reference images. URL or `data:` URI. |
| `mask_url` | string | none | Optional mask for region-specific edits. |
| `image_size` | preset, `auto`, or `{width, height}` | `auto` | `auto` inherits input dims. |
| `quality` | `low` \| `medium` \| `high` | `high` | |
| `num_images` | integer | `1` | |
| `output_format` | `jpeg` \| `png` \| `webp` | `png` | |

Full docs: [docs/edit-image.md](./docs/edit-image.md).

## Streaming and queue

```python
# Python streaming with fal-client
import fal_client
for event in fal_client.stream(
    "openai/gpt-image-2",
    arguments={"prompt": "a surreal oil painting of Mars at sunrise"},
):
    print(event)
```

```python
# Python queue + webhook with fal-client
import fal_client

handle = fal_client.submit(
    "openai/gpt-image-2",
    arguments={"prompt": "a cinematic sunset over the Himalayas, 4k"},
    webhook_url="https://your.app/api/fal/webhook",
)
result = fal_client.result("openai/gpt-image-2", request_id=handle.request_id)
```

```js
// Node.js streaming
import { fal } from "@fal-ai/client";
const stream = await fal.stream("openai/gpt-image-2", { input: { prompt: "…" } });
for await (const event of stream) console.log(event);
```

Full guide: [docs/streaming.md](./docs/streaming.md).

## Image sizes & quality

| Preset | Typical dims |
| --- | --- |
| `square_hd` | 1024 x 1024 |
| `square` | 512 x 512 |
| `portrait_4_3` | ~ 768 x 1024 |
| `portrait_16_9` | ~ 720 x 1280 |
| `landscape_4_3` | ~ 1024 x 768 |
| `landscape_16_9` | ~ 1280 x 720 |
| `auto` (edit only) | inferred from input |

Constraints: multiples of 16; max edge 3840 px; aspect ≤ 3:1; total pixels 655,360–8,294,400. Full cheatsheet: [docs/image-sizes.md](./docs/image-sizes.md).

## Prompts gallery

Runnable, copy-paste prompts lifted from fal.ai's [text-to-image](https://fal.ai/models/openai/gpt-image-2/examples) and [edit](https://fal.ai/models/openai/gpt-image-2/edit/examples) example galleries:

- Recursive hero infographic — [python](./python/examples/hero_infographic.py) · [node](./node/examples/hero-infographic.js)
- Photorealistic corporate boardroom — [python](./python/examples/boardroom.py) · [node](./node/examples/boardroom.js)
- Broadcast news anchor ("BREAKING: GPT-IMAGE-2 NOW LIVE ON fal") — [python](./python/examples/news_anchor.py) · [node](./node/examples/news-anchor.js)
- Creative studio review wall — [python](./python/examples/studio_wall.py) · [node](./node/examples/studio-wall.js)
- Vinyl album cover edit — [python](./python/examples/vinyl_album_edit.py) · [node](./node/examples/vinyl-album-edit.js)
- Bus livery multi-image edit — [python](./python/examples/bus_livery_edit.py) · [node](./node/examples/bus-livery-edit.js)

More: [docs/prompts-gallery.md](./docs/prompts-gallery.md).

## CLI (optional wrapper)

The optional `gpt-image-2` wrapper ships a CLI:

```bash
pip install gpt-image-2
gpt-image-2 generate "a cinematic product shot of a red sneaker" --size landscape_16_9 --quality high
gpt-image-2 generate "poster art" --size 1280x720 -n 2 --format webp
gpt-image-2 edit "make it night-time, neon reflections" --image https://example.com/in.png
```

Run `gpt-image-2 --help` for full flags. Prefer raw `fal-client`? Every example in this repo's [`python/`](./python) folder is written that way.

## FAQ

See [docs/faq.md](./docs/faq.md). A few highlights:

- **What is gpt-image-2?** OpenAI's next-gen image model, focused on high-res output, strong typography, and fine-grained editing. Hosted on fal.ai as `openai/gpt-image-2` and `openai/gpt-image-2/edit`.
- **Is gpt-image-2 the same as the ChatGPT image generator?** ChatGPT's in-product image generation is powered *by* `gpt-image-2` — the model this repo calls directly. So "ChatGPT Image 2 API", "ChatGPT Images 2.0 API", and "gpt-image-2 API" are all the same underlying model. ChatGPT is the product; `gpt-image-2` is the model id.
- **Do I need the wrapper?** No. Every example in this repo uses `fal-client` directly. The `gpt-image-2` pip package is just optional sugar + a CLI.
- **Max resolution?** 3840 px max edge, up to ~8.3 MP total, aspect ≤ 3:1.
- **Does it support editing?** Yes — the [`/edit`](https://fal.ai/models/openai/gpt-image-2/edit) endpoint accepts one or more reference images and an optional mask.
- **Is there streaming?** Yes — both endpoints support streaming and a queue/webhook flow.
- **Can I use it commercially?** Yes, fal.ai's model page marks it as commercial-use-friendly. This wrapper is MIT licensed.

## Resources

- **fal.ai playground (text-to-image):** <https://fal.ai/models/openai/gpt-image-2>
- **fal.ai playground (edit):** <https://fal.ai/models/openai/gpt-image-2/edit>
- **API reference (text-to-image):** <https://fal.ai/models/openai/gpt-image-2/api>
- **API reference (edit):** <https://fal.ai/models/openai/gpt-image-2/edit/api>
- **Prompt examples (text-to-image):** <https://fal.ai/models/openai/gpt-image-2/examples>
- **Prompt examples (edit):** <https://fal.ai/models/openai/gpt-image-2/edit/examples>

## Contributing

PRs are welcome — especially new prompt examples. Add a script under `python/examples/` and `node/examples/`, then extend [docs/prompts-gallery.md](./docs/prompts-gallery.md).

## License

[MIT](./LICENSE). "GPT Image 2", "gpt-image-2", and "OpenAI" are trademarks of their respective owners — this project is an independent, unofficial wrapper.

---

> **Powered by [fal.ai](https://fal.ai/models/openai/gpt-image-2).** If you build something cool with GPT Image 2, tag fal on X — they feature community work.
