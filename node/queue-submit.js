// Queue-based (async) example for gpt-image-2 via fal.ai.
// Submits a request, polls status, then fetches the final result.
//
// Usage: node queue-submit.js "your prompt"

import "dotenv/config";
import { fal } from "@fal-ai/client";
import { saveResult } from "./lib/save.js";

const prompt =
  process.argv.slice(2).join(" ") || "a cute corgi astronaut exploring Jupiter, 4k";

const { request_id } = await fal.queue.submit("openai/gpt-image-2", {
  input: {
    prompt,
    image_size: "landscape_4_3",
    quality: "high",
  },
});
console.log(`Submitted. request_id=${request_id}`);

while (true) {
  const status = await fal.queue.status("openai/gpt-image-2", {
    requestId: request_id,
    logs: true,
  });
  console.log(`status = ${status.status}`);
  if (["COMPLETED", "COMPLETED_WITH_ERRORS", "FAILED"].includes(status.status)) break;
  await new Promise((r) => setTimeout(r, 2000));
}

const result = await fal.queue.result("openai/gpt-image-2", {
  requestId: request_id,
});
console.log(`Got ${result.data.images.length} image(s).`);
const paths = await saveResult(result.data, { prefix: "gpt-image-2-queue" });
for (const p of paths) console.log(`Saved: ${p}`);
