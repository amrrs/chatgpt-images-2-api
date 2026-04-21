// Node.js image edit example for GPT Image 2 (gpt-image-2/edit) via fal.ai.
//
// Usage:
//   node edit-image.js "edit instruction" https://.../input.png [extra.png ...]
//
// Docs:
// - Edit API: https://fal.ai/models/openai/gpt-image-2/edit/api
// - Examples: https://fal.ai/models/openai/gpt-image-2/edit/examples

import "dotenv/config";
import { fal } from "@fal-ai/client";
import { saveResult } from "./lib/save.js";

const [prompt, ...imageUrls] = process.argv.slice(2);

if (!prompt || imageUrls.length === 0) {
  console.error(
    'Usage: node edit-image.js "edit instruction" <image-url-1> [image-url-2 ...]'
  );
  process.exit(2);
}

const result = await fal.subscribe("openai/gpt-image-2/edit", {
  input: {
    prompt,
    image_urls: imageUrls,
    image_size: "auto",
    quality: "high",
    num_images: 1,
    output_format: "png",
  },
  logs: true,
  onQueueUpdate: (update) => {
    if (update.status === "IN_PROGRESS") {
      update.logs?.map((l) => l.message).forEach((m) => m && console.log(m));
    }
  },
});

console.log(`Generated ${result.data.images.length} edited image(s).`);
for (const img of result.data.images) {
  console.log(`  - ${img.url} (${img.width}x${img.height})`);
}
const paths = await saveResult(result.data, { prefix: "gpt-image-2-edit" });
for (const p of paths) console.log(`Saved: ${p}`);
