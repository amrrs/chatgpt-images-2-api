// GPT Image 2 edit example: turn any image into a vinyl album cover.
// Source: https://fal.ai/models/openai/gpt-image-2/edit/examples
import "dotenv/config";
import { fal } from "@fal-ai/client";
import { saveResult } from "../lib/save.js";

const INPUT_URL =
  "https://v3b.fal.media/files/b/0a8691af/9Se_1_VX1wzTjjTOpWbs9_bb39c2eb-1a41-4749-b1d0-cf134abc8bbf.png";

const prompt = [
  "Transform this into a vinyl album cover. Add a bold album title \"DISTANCES\" in a",
  "clean condensed sans-serif across the top. Artist name \"CLARA VEIL\" in smaller",
  "type below it. A parental advisory sticker in the bottom right corner. The image",
  "gains a slight halftone print texture and the colors shift toward faded vintage",
  "tones. Add a thin white border around the entire image like a physical print.",
  "A small record label logo in the bottom left corner reading \"MERIDIAN RECORDS\".",
  "It should look like you're holding an actual vinyl sleeve.",
].join(" ");

const result = await fal.subscribe("openai/gpt-image-2/edit", {
  input: {
    prompt,
    image_urls: [INPUT_URL],
    image_size: { width: 3000, height: 2000 },
    quality: "high",
  },
  logs: true,
  onQueueUpdate: (u) => u.status === "IN_PROGRESS" && u.logs?.forEach((l) => console.log(l.message)),
});

for (const p of await saveResult(result.data, { prefix: "vinyl-album-edit" })) {
  console.log(`Saved: ${p}`);
}
