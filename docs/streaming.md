# GPT Image 2 Streaming & Queue Guide

Two ways to run **gpt-image-2** asynchronously on fal.ai.

---

## 1. Streaming (real-time events)

Use streaming when you want live progress events delivered to your process.

### Python

```python
from gpt_image_2 import GPTImage2

client = GPTImage2()
for event in client.stream("a surreal oil painting of Mars at sunrise"):
    print(event)
```

### Node.js

```js
import { fal } from "@fal-ai/client";

const stream = await fal.stream("openai/gpt-image-2", {
  input: { prompt: "a surreal oil painting of Mars at sunrise" },
});

for await (const event of stream) {
  console.log(event);
}

const result = await stream.done();
```

---

## 2. Queue (fire-and-forget + webhook)

Use the queue for long-running jobs or when you want a webhook to notify you.

### Python

```python
from gpt_image_2 import GPTImage2
import time

client = GPTImage2()
request_id = client.submit(
    "a cinematic sunset over the Himalayas, 4k",
    webhook_url="https://your.app/api/fal/webhook",
)

while True:
    s = client.status(request_id)
    if str(s.get("status")).upper() in {"COMPLETED", "FAILED"}:
        break
    time.sleep(2)

result = client.result(request_id)
print(result.first_url)
```

### Node.js

```js
import { fal } from "@fal-ai/client";

const { request_id } = await fal.queue.submit("openai/gpt-image-2", {
  input: { prompt: "a cinematic sunset over the Himalayas, 4k" },
  webhookUrl: "https://your.app/api/fal/webhook",
});

const status = await fal.queue.status("openai/gpt-image-2", {
  requestId: request_id,
  logs: true,
});

const result = await fal.queue.result("openai/gpt-image-2", {
  requestId: request_id,
});
```

## When to use which

| Scenario | Use |
| --- | --- |
| Server endpoint that returns an image in one request | `subscribe` (sync) |
| CLI or notebook with live progress | `stream` |
| Backend job, webhook callback, or retries | `queue.submit` + webhook |

## Related

- [text-to-image.md](./text-to-image.md)
- [edit-image.md](./edit-image.md)
- fal.ai queue docs: <https://fal.ai/models/openai/gpt-image-2/api>
