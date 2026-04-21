# GPT Image 2 FAQ

Frequently asked questions about **GPT Image 2** (`gpt-image-2`), OpenAI's GPT Image 2.0 model, and how to use it via fal.ai.

---

### What is GPT Image 2?

GPT Image 2 (model id `gpt-image-2`) is OpenAI's next-generation image generation model. It supports flexible resolutions up to 4K, multiple model variants, and is particularly strong at **typography**, **infographics**, and **fine-grained image editing**. It is hosted on fal.ai at [`openai/gpt-image-2`](https://fal.ai/models/openai/gpt-image-2).

### Is gpt-image-2 the same as the "ChatGPT image generator"?

**Effectively, yes — at the model layer.** When you generate an image inside ChatGPT, the underlying model is OpenAI's `gpt-image-2`. What differs is the *surface*:

| Surface | What it is | How you use it |
| --- | --- | --- |
| **ChatGPT** (chat.openai.com / mobile apps) | The consumer product. No direct API for image generation in this surface. | Type a prompt in the chat UI. |
| **OpenAI API** (`gpt-image-2`) | The raw image model from OpenAI. | `openai.images.generate(model="gpt-image-2", ...)` |
| **fal.ai** (`openai/gpt-image-2`) | A hosted/commercial-friendly deployment of the same model with streaming, queue, webhooks, and a generous resolution ceiling. | What this repo uses. |

So when people search for "**ChatGPT Image 2 API**", "**ChatGPT Images 2.0 API**", "**ChatGPT 2 image generator API**", or "**ChatGPT image generation API**", they almost always mean **`gpt-image-2`** — and the examples in this repo are what they want.

### Is there an official "gpt-image-2" Python SDK?

There isn't an OpenAI-branded package. The officially supported path is to call the fal.ai endpoint using the [`fal-client`](https://pypi.org/project/fal-client/) Python SDK (or [`@fal-ai/client`](https://www.npmjs.com/package/@fal-ai/client) on Node) — every example in this repo shows exactly that. As optional sugar, this repo also ships a tiny **Python wrapper** called `gpt-image-2` (import as `gpt_image_2`) that adds `generate()` / `edit()` / `stream()` one-liners and a `gpt-image-2` CLI. Use whichever you prefer.

### How do I get an API key?

Create a fal.ai account and grab a key from <https://fal.ai/dashboard/keys>. Export it as `FAL_KEY` in your shell or put it in a `.env` file at the project root.

### Does gpt-image-2 support image editing?

Yes. The edit endpoint is [`openai/gpt-image-2/edit`](https://fal.ai/models/openai/gpt-image-2/edit). It accepts one or more reference images via `image_urls`, plus an optional `mask_url`. See [edit-image.md](./edit-image.md).

### What's the maximum resolution?

- Max edge: **3840 px**
- Aspect ratio: ≤ **3:1**
- Total pixel budget: **655,360 – 8,294,400**
- Both dimensions must be multiples of 16.

### What image sizes can I pass?

Either a preset name (`square_hd`, `square`, `portrait_4_3`, `portrait_16_9`, `landscape_4_3`, `landscape_16_9`) or an object like `{ "width": 1280, "height": 720 }`. For edits you can also pass `"auto"` to inherit the input image's dimensions. Full reference: [image-sizes.md](./image-sizes.md).

### What output formats are supported?

`png` (default, lossless — best for text), `jpeg`, or `webp`.

### How does pricing work?

Pricing is set by fal.ai and scales with resolution, quality, and the number of images. Check the model page for current pricing: <https://fal.ai/models/openai/gpt-image-2>.

### Does it stream?

Yes. Both the text-to-image and edit endpoints support streaming — see [streaming.md](./streaming.md). You can also use the queue (`queue.submit` / `queue.status` / `queue.result`) with an optional `webhook_url` for fully async workflows.

### Can I pass base64 images for editing?

Yes. Anywhere the API accepts a URL, you can pass a `data:` URI (base64). For large inputs, uploading to fal.ai's storage or your own host is faster.

### How is gpt-image-2 different from DALL·E 3 or GPT Image 1?

GPT Image 2 is a newer generation of OpenAI's image model, focused on higher resolutions, sharper typography, and better editing. If you need exact text rendering, tight multi-image edits, or 4K outputs, gpt-image-2 is usually the right pick.

### Can I use this commercially?

Yes — this wrapper is MIT-licensed. For fal.ai and OpenAI terms around the generated images, consult the [fal.ai model page](https://fal.ai/models/openai/gpt-image-2) (marked "Commercial use") and OpenAI's usage policies.

### Where can I see more example prompts?

- In this repo: [prompts-gallery.md](./prompts-gallery.md)
- On fal.ai: [text-to-image examples](https://fal.ai/models/openai/gpt-image-2/examples) · [edit examples](https://fal.ai/models/openai/gpt-image-2/edit/examples)
