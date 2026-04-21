# GPT Image 2 Edit API (a.k.a. ChatGPT Image 2 Edit)

> How to edit images with **GPT Image 2** (`gpt-image-2/edit`) — OpenAI's GPT Image 2.0 edit endpoint, the same model ChatGPT uses for in-app image edits — via fal.ai, in Python and Node.js.
>
> Also known as: ChatGPT Image 2 edit API, ChatGPT Images 2.0 edit, OpenAI gpt-image-2 edit API.

- fal.ai model: <https://fal.ai/models/openai/gpt-image-2/edit>
- fal.ai API docs: <https://fal.ai/models/openai/gpt-image-2/edit/api>
- fal.ai examples: <https://fal.ai/models/openai/gpt-image-2/edit/examples>

---

## Endpoint

| Field | Value |
| --- | --- |
| fal.ai app id | `openai/gpt-image-2/edit` |
| Capability | Image editing with one or more reference images |
| Mask support | Yes (optional `mask_url`) |
| Streaming | Yes |
| Queue | Yes |

## Input schema

| Field | Type | Default | Notes |
| --- | --- | --- | --- |
| `prompt` | string (required) | — | Edit instruction |
| `image_urls` | list<string> (required) | — | One or more reference images. Public URL or `data:` URI |
| `mask_url` | string | none | Optional mask indicating which region to edit |
| `image_size` | preset, `auto`, or `{width,height}` | `auto` | `auto` infers from input |
| `quality` | `low` \| `medium` \| `high` | `high` | |
| `num_images` | integer | `1` | |
| `output_format` | `jpeg` \| `png` \| `webp` | `png` | |
| `sync_mode` | boolean | `false` | |

## Python (`fal-client`)

```python
import fal_client

result = fal_client.subscribe(
    "openai/gpt-image-2/edit",
    arguments={
        "prompt": (
            "Wrap the double-decker bus with this branding as a full livery. "
            "Keep the street scene and people unchanged."
        ),
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

### Optional: the `gpt-image-2` wrapper

```python
import gpt_image_2
result = gpt_image_2.edit(
    "make it night-time, neon reflections",
    image_urls=["https://example.com/scene.png"],
)
print(result.first_url)
```

CLI:

```bash
gpt-image-2 edit "make it night-time, neon reflections" \
    --image https://example.com/scene.png
```

## Node.js

```js
import { fal } from "@fal-ai/client";

const result = await fal.subscribe("openai/gpt-image-2/edit", {
  input: {
    prompt: "Wrap the bus with this branding as a full livery",
    image_urls: [
      "https://example.com/bus.png",
      "https://example.com/livery.png",
    ],
    image_size: "auto",
    quality: "high",
  },
  logs: true,
});

console.log(result.data.images[0].url);
```

## Tips for better edits

- Put the **subject image first** in `image_urls` and the **style/reference image second**.
- Use concrete verbs: *replace*, *wrap*, *add*, *remove*, *re-light*, *restyle*.
- Explicitly list what should **stay unchanged** ("keep the background, people, and street unchanged").
- For region-specific edits, provide a `mask_url` with the editable region in white on a black background.

## See also

- [text-to-image.md](./text-to-image.md)
- [prompts-gallery.md](./prompts-gallery.md) — includes edit prompts (vinyl album, bus livery)
- [faq.md](./faq.md)
