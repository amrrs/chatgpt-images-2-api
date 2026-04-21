// Streaming example for GPT Image 2 (gpt-image-2) via fal.ai.
// Streams live events from the queue and prints each as it arrives.
//
// Usage: node text-to-image-stream.js "your prompt"

import "dotenv/config";
import { fal } from "@fal-ai/client";

const prompt =
  process.argv.slice(2).join(" ") || "a surreal oil painting of Mars at sunrise";

const stream = await fal.stream("openai/gpt-image-2", {
  input: {
    prompt,
    image_size: "landscape_4_3",
    quality: "high",
  },
});

for await (const event of stream) {
  console.log(event);
}

const result = await stream.done();
console.log("Done:", JSON.stringify(result, null, 2));
