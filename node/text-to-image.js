// Minimal Node.js text-to-image example for GPT Image 2 (gpt-image-2) via fal.ai.
//
// Usage:
//   npm install
//   export FAL_KEY=...
//   node text-to-image.js "your prompt here"
//
// Docs:
// - Model: https://fal.ai/models/openai/gpt-image-2
// - API:   https://fal.ai/models/openai/gpt-image-2/api

import "dotenv/config";
import { fal } from "@fal-ai/client";
import { saveResult } from "./lib/save.js";

const prompt =
  process.argv.slice(2).join(" ") ||
  "a cinematic product shot of a red sneaker on wet asphalt, 4k, studio lighting";

const result = await fal.subscribe("openai/gpt-image-2", {
  input: {
    prompt,
    image_size: "landscape_4_3",
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

console.log(`Generated ${result.data.images.length} image(s).`);
for (const img of result.data.images) {
  console.log(`  - ${img.url} (${img.width}x${img.height})`);
}
const paths = await saveResult(result.data, { prefix: "gpt-image-2" });
for (const p of paths) console.log(`Saved: ${p}`);
