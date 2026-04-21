# GPT Image 2 Text-to-Image API (a.k.a. ChatGPT Image 2 API)

> How to generate images with **GPT Image 2** (`gpt-image-2`) — OpenAI's GPT Image 2.0 model, the same model behind **ChatGPT's image generator** — using the fal.ai hosted endpoint, in **Python** and **Node.js**.
>
> Also known as: ChatGPT Image 2, ChatGPT Images 2.0, ChatGPT image generator API, OpenAI gpt-image-2 API.

- fal.ai model: <https://fal.ai/models/openai/gpt-image-2>
- fal.ai API docs: <https://fal.ai/models/openai/gpt-image-2/api>
- fal.ai examples: <https://fal.ai/models/openai/gpt-image-2/examples>

---

## Endpoint

| Field | Value |
| --- | --- |
| fal.ai app id | `openai/gpt-image-2` |
| Capability | Text-to-image |
| Streaming | Yes |
| Queue | Yes (submit / status / result / webhook) |
| Max edge | 3840 px |
| Aspect ratio | ≤ 3:1 |
| Pixel budget | 655,360 – 8,294,400 |

## Input schema

| Field | Type | Default | Notes |
| --- | --- | --- | --- |
| `prompt` | string (required) | — | The text prompt |
| `image_size` | preset or `{width,height}` | `landscape_4_3` | See [image-sizes.md](./image-sizes.md) |
| `quality` | `low` \| `medium` \| `high` | `high` | |
| `num_images` | integer | `1` | |
| `output_format` | `jpeg` \| `png` \| `webp` | `png` | |
| `sync_mode` | boolean | `false` | If `true`, returns a data URI |

Preset sizes: `square_hd`, `square`, `portrait_4_3`, `portrait_16_9`, `landscape_4_3`, `landscape_16_9`.

## Output schema

```json
{
  "images": [
    {
      "url": "https://v3b.fal.media/files/.../abcd.png",
      "width": 1024,
      "height": 1024,
      "content_type": "image/png",
      "file_name": "abcd.png"
    }
  ]
}
```

## Python (`fal-client`)

```bash
pip install fal-client
export FAL_KEY=...   # https://fal.ai/dashboard/keys
```

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
        "num_images": 1,
        "output_format": "png",
    },
    with_logs=True,
    on_queue_update=on_queue_update,
)
print(result["images"][0]["url"])
```

### Optional: the `gpt-image-2` wrapper

If you'd rather use the tiny typed wrapper shipped in this repo:

```bash
pip install gpt-image-2
```

```python
import gpt_image_2
print(gpt_image_2.generate("a cute corgi astronaut, 4k").first_url)
```

CLI:

```bash
gpt-image-2 generate "a cute corgi astronaut" --size landscape_16_9 --quality high
```

## Node.js (`@fal-ai/client`)

```js
import { fal } from "@fal-ai/client";

const result = await fal.subscribe("openai/gpt-image-2", {
  input: {
    prompt: "a cinematic product shot of a red sneaker on wet asphalt",
    image_size: "landscape_16_9",
    quality: "high",
  },
  logs: true,
});

console.log(result.data.images[0].url);
```

## See also

- [edit-image.md](./edit-image.md) — image-to-image editing with gpt-image-2
- [streaming.md](./streaming.md) — stream events as they arrive
- [image-sizes.md](./image-sizes.md) — preset sizes and pixel budget
- [prompts-gallery.md](./prompts-gallery.md) — curated prompts to copy-paste
- [faq.md](./faq.md) — frequently asked questions
