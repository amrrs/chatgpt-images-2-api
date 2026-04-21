# GPT Image 2 Prompts Gallery

Curated, copy-paste-ready prompts for **GPT Image 2** (`gpt-image-2`), drawn from fal.ai's official example gallery. Each prompt is paired with a runnable Python and Node.js script in this repo.

- Text-to-image playground: <https://fal.ai/models/openai/gpt-image-2>
- Edit playground: <https://fal.ai/models/openai/gpt-image-2/edit>
- Full fal.ai examples: <https://fal.ai/models/openai/gpt-image-2/examples> · <https://fal.ai/models/openai/gpt-image-2/edit/examples>

---

## Text-to-image

### 1. Recursive hero infographic

Recommended size: `2000 x 1152`

> A single hero infographic titled something like "GPT Image 2 is here" that demonstrates the very capabilities it's announcing. Think periodic-table or anatomical-diagram aesthetic: clean grid of 16-24 mini-renders showing different styles (oil painting, anime, blueprint, isometric, photoreal, watercolor, etc.). Electric aesthetic, color! The genius is recursive — to make this teaser you literally need a model that's god-tier at infographics. This is your strongest play because it doesn't need a caption to flex. No date involved.

Runnable: [`python/examples/hero_infographic.py`](../python/examples/hero_infographic.py) · [`node/examples/hero-infographic.js`](../node/examples/hero-infographic.js)

### 2. Photorealistic corporate boardroom

Recommended size: `3000 x 2000`

> Photorealistic corporate boardroom: a long polished mahogany conference table with leather executive chairs, a glass of water at each place setting, notepads and pens arranged neatly, a large flat-screen TV at the end showing a quarterly revenue chart going up. Floor-to-ceiling windows with a city skyline view. Serious, sterile corporate atmosphere. Several business executives in suits seated around the table in a meeting.

Runnable: [`python/examples/boardroom.py`](../python/examples/boardroom.py) · [`node/examples/boardroom.js`](../node/examples/boardroom.js)

### 3. Broadcast news anchor ("BREAKING: GPT-IMAGE-2 NOW LIVE ON fal")

Recommended size: `3500 x 2500`

> Broadcast news still captured mid-broadcast: a single professional news anchor seated at a sleek modern desk, caught mid-sentence with a natural speaking expression, lips slightly parted, eyes focused just off-camera toward an unseen lead camera. Subtle teleprompter reflection faintly visible on the polished glass surface of the desk, hinting at scrolling script text without being legible. Behind the anchor, a large curved LED wall screen dominates the background, displaying a stylized world map in deep navy and cool cyan tones with soft glowing connection lines arcing between continents. A clean lower-third news ticker runs across the bottom of the background screen in bold uppercase sans-serif typography, reading exactly: "BREAKING: GPT-IMAGE-2 NOW LIVE ON fal" (with "fal" rendered in lowercase as a proper stylized brand name, kept intentionally small and distinct from the uppercase ticker text around it). Studio atmosphere: crisp, even key lighting on the anchor's face with a soft rim light separating them from the background, faint haze catching the backlight for subtle depth, polished reflective floor adding a slight mirror effect beneath the desk. Color palette is restrained and professional, built around deep navy blue, cool steel gray, and muted slate, with tiny accents of electric cyan from the screen graphics. Composition: medium shot, anchor framed slightly off-center following the rule of thirds, composed upright posture, tailored blazer, minimal jewelry, neatly styled hair. Shallow depth of field with the background screen softly falling off but the ticker text remaining crisp and legible. Shot on a cinema camera look, 50mm equivalent, natural skin tones, broadcast-grade clarity. Negative: no real-world network logos, no watermarks, no channel bugs, no visible brand names other than the stylized "fal" on the ticker, no text overlays on the anchor, no distorted typography.

Runnable: [`python/examples/news_anchor.py`](../python/examples/news_anchor.py) · [`node/examples/news-anchor.js`](../node/examples/news-anchor.js)

### 4. Creative studio review wall

Recommended size: `3500 x 2500`

> Candid photograph of a creative studio's review wall covered in a neat grid of printed image sheets and loose pinned photographs showing a range of AI generated visuals: product shots, portraits, landscapes, abstract compositions. Some prints circled in red grease pencil, a few with handwritten sticky notes saying "RERUN", "FINAL", and "GPT-IMAGE-2 ON fal". Warm desk-lamp light from below, the corner of a monitor and a keyboard visible in the foreground, a chair back partially in frame. An honest, working-studio feel. No real brand logos, no watermark.

Runnable: [`python/examples/studio_wall.py`](../python/examples/studio_wall.py) · [`node/examples/studio-wall.js`](../node/examples/studio-wall.js)

---

## Edit (image-to-image)

### 5. Vinyl album cover transform

Recommended size: `3000 x 2000`

> Transform this into a vinyl album cover. Add a bold album title "DISTANCES" in a clean condensed sans-serif across the top. Artist name "CLARA VEIL" in smaller type below it. A parental advisory sticker in the bottom right corner. The image gains a slight halftone print texture and the colors shift toward faded vintage tones. Add a thin white border around the entire image like a physical print. A small record label logo in the bottom left corner reading "MERIDIAN RECORDS". It should look like you're holding an actual vinyl sleeve.

Runnable: [`python/examples/vinyl_album_edit.py`](../python/examples/vinyl_album_edit.py) · [`node/examples/vinyl-album-edit.js`](../node/examples/vinyl-album-edit.js)

### 6. Bus livery wrap (multi-image edit)

Recommended size: `1024 x 1024`

> Wrap the double-decker bus from the first image with the exact branding design from the second image as a full bus livery. Keep the street scene, people, and background unchanged.

Runnable: [`python/examples/bus_livery_edit.py`](../python/examples/bus_livery_edit.py) · [`node/examples/bus-livery-edit.js`](../node/examples/bus-livery-edit.js)

---

## Prompting tips that actually help with gpt-image-2

1. **Spell out on-image text in quotes.** gpt-image-2 is unusually good at typography — use exact quotes for any letters you want rendered.
2. **Declare aspect ratio intent.** Either pass a preset (`landscape_16_9`) or a custom `{width, height}` that's a multiple of 16.
3. **Use a negative list** at the end of the prompt: "Negative: no watermarks, no captions, no real logos."
4. **Anchor composition** with photography vocabulary: *medium shot*, *rule of thirds*, *50mm*, *shallow depth of field*, *rim light*.
5. **For edits, freeze the unchanged parts** explicitly: "Keep the background, people, and lighting unchanged."

## Contribute a prompt

Open a PR adding a new file under `python/examples/` and `node/examples/` and extend this gallery.
