// GPT Image 2 example: studio review wall with grease-pencil annotations.
// Source: https://fal.ai/models/openai/gpt-image-2/examples
import "dotenv/config";
import { fal } from "@fal-ai/client";
import { saveResult } from "../lib/save.js";

const prompt = [
  "Candid photograph of a creative studio's review wall covered in a neat grid of",
  "printed image sheets and loose pinned photographs showing a range of AI generated",
  "visuals: product shots, portraits, landscapes, abstract compositions. Some prints",
  'circled in red grease pencil, a few with handwritten sticky notes saying "RERUN",',
  '"FINAL", and "GPT-IMAGE-2 ON fal". Warm desk-lamp light from below, the corner of',
  "a monitor and keyboard visible in the foreground, a chair back partially in frame.",
  "An honest, working-studio feel. No real brand logos, no watermark.",
].join(" ");

const result = await fal.subscribe("openai/gpt-image-2", {
  input: { prompt, image_size: { width: 3500, height: 2500 }, quality: "high" },
  logs: true,
  onQueueUpdate: (u) => u.status === "IN_PROGRESS" && u.logs?.forEach((l) => console.log(l.message)),
});

for (const p of await saveResult(result.data, { prefix: "studio-wall" })) {
  console.log(`Saved: ${p}`);
}
