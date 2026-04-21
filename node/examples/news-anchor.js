// GPT Image 2 example: broadcast news anchor with "BREAKING: GPT-IMAGE-2 NOW LIVE ON fal" ticker.
// Source: https://fal.ai/models/openai/gpt-image-2/examples
import "dotenv/config";
import { fal } from "@fal-ai/client";
import { saveResult } from "../lib/save.js";

const prompt = [
  "Broadcast news still captured mid-broadcast: a single professional news anchor",
  "seated at a sleek modern desk, caught mid-sentence. Behind the anchor, a large",
  "curved LED wall screen displaying a stylized world map in deep navy and cool cyan.",
  'A clean lower-third news ticker reads exactly: "BREAKING: GPT-IMAGE-2 NOW LIVE ON fal"',
  '(with "fal" in lowercase as a stylized brand name). Crisp even key lighting, soft',
  "rim light, polished reflective floor. Navy blue and cool steel gray palette with",
  "electric cyan accents. Medium shot, rule-of-thirds, 50mm cinema look, broadcast",
  "clarity. No real network logos, no watermarks.",
].join(" ");

const result = await fal.subscribe("openai/gpt-image-2", {
  input: { prompt, image_size: { width: 3500, height: 2500 }, quality: "high" },
  logs: true,
  onQueueUpdate: (u) => u.status === "IN_PROGRESS" && u.logs?.forEach((l) => console.log(l.message)),
});

for (const p of await saveResult(result.data, { prefix: "news-anchor" })) {
  console.log(`Saved: ${p}`);
}
