// GPT Image 2 example: photorealistic corporate boardroom.
// Source: https://fal.ai/models/openai/gpt-image-2/examples
import "dotenv/config";
import { fal } from "@fal-ai/client";
import { saveResult } from "../lib/save.js";

const prompt = [
  "Photorealistic corporate boardroom: a long polished mahogany conference table",
  "with leather executive chairs, a glass of water at each place setting, notepads",
  "and pens arranged neatly, a large flat-screen TV at the end showing a quarterly",
  "revenue chart going up. Floor-to-ceiling windows with a city skyline view.",
  "Serious, sterile corporate atmosphere. Several business executives in suits",
  "seated around the table in a meeting.",
].join(" ");

const result = await fal.subscribe("openai/gpt-image-2", {
  input: { prompt, image_size: { width: 3000, height: 2000 }, quality: "high" },
  logs: true,
  onQueueUpdate: (u) => u.status === "IN_PROGRESS" && u.logs?.forEach((l) => console.log(l.message)),
});

for (const p of await saveResult(result.data, { prefix: "boardroom" })) {
  console.log(`Saved: ${p}`);
}
