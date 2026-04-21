# GPT Image 2 Image Sizes & Quality Cheatsheet

Reference for `image_size`, `quality`, and `output_format` on the **gpt-image-2** API.

## Presets

| Preset | Typical dims | Notes |
| --- | --- | --- |
| `square_hd` | 1024 x 1024 | Safe default for avatars / thumbnails |
| `square` | 512 x 512 | Smaller square |
| `portrait_4_3` | e.g. 768 x 1024 | Posters, social stories |
| `portrait_16_9` | e.g. 720 x 1280 | Phone wallpapers |
| `landscape_4_3` | e.g. 1024 x 768 | Default preset for text-to-image |
| `landscape_16_9` | e.g. 1280 x 720 | YouTube thumbnails, desktop wallpapers |
| `auto` (edit only) | inferred | Matches the input image |

## Custom sizes

Pass an object:

```json
"image_size": { "width": 1280, "height": 720 }
```

Constraints:

- Both dimensions must be **multiples of 16**.
- Max edge ≤ **3840 px**.
- Aspect ratio ≤ **3:1**.
- Total pixels between **655,360** and **8,294,400**.

## Quality

- `low` — fastest, cheapest; good for exploration
- `medium` — balanced
- `high` (default) — best typography and detail; use this for hero shots

## Output formats

- `png` (default) — lossless, best for text and crisp edges
- `jpeg` — smaller, good for photographic scenes
- `webp` — smallest; great for web delivery

## Related

- [text-to-image.md](./text-to-image.md)
- [edit-image.md](./edit-image.md)
