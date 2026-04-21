// GPT Image 2 example: recursive hero infographic.
// Source: https://fal.ai/models/openai/gpt-image-2/examples
import "dotenv/config";
import { fal } from "@fal-ai/client";
import { saveResult } from "../lib/save.js";

const prompt = [
  "A single hero infographic titled something like \"GPT Image 2 is here\"",
  "that demonstrates the very capabilities it's announcing. Think periodic-table",
  "or anatomical-diagram aesthetic: clean grid of 16-24 mini-renders showing",
  "different styles (oil painting, anime, blueprint, isometric, photoreal,",
  "watercolor, etc.). Electric aesthetic, color! The genius is recursive - to",
  "make this teaser you literally need a model that's god-tier at infographics.",
  "This is your strongest play because it doesn't need a caption to flex.",
  "No date involved.",
].join(" ");

const result = await fal.subscribe("openai/gpt-image-2", {
  input: {
    prompt,
    image_size: { width: 2000, height: 1152 },
    quality: "high",
  },
  logs: true,
  onQueueUpdate: (u) => u.status === "IN_PROGRESS" && u.logs?.forEach((l) => console.log(l.message)),
});

for (const p of await saveResult(result.data, { prefix: "hero-infographic" })) {
  console.log(`Saved: ${p}`);
}
