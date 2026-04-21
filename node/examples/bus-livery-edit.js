// GPT Image 2 edit example: wrap a double-decker bus with a second image as livery.
// Source: https://fal.ai/models/openai/gpt-image-2/edit/examples
import "dotenv/config";
import { fal } from "@fal-ai/client";
import { saveResult } from "../lib/save.js";

// Replace with your own input image URLs before running.
const BUS_URL = "https://example.com/your-bus.png";
const LIVERY_URL = "https://example.com/your-livery.png";

const prompt =
  "Wrap the double-decker bus from the first image with the exact branding design " +
  "from the second image as a full bus livery. Keep the street scene, people, and " +
  "background unchanged.";

const result = await fal.subscribe("openai/gpt-image-2/edit", {
  input: {
    prompt,
    image_urls: [BUS_URL, LIVERY_URL],
    image_size: { width: 1024, height: 1024 },
    quality: "high",
  },
  logs: true,
  onQueueUpdate: (u) => u.status === "IN_PROGRESS" && u.logs?.forEach((l) => console.log(l.message)),
});

for (const p of await saveResult(result.data, { prefix: "bus-livery-edit" })) {
  console.log(`Saved: ${p}`);
}
