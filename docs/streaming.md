# GPT Image 2 Streaming & Queue Guide

Two ways to run **gpt-image-2** asynchronously on fal.ai.

---

## 1. Streaming (real-time events)

Use streaming when you want live progress events delivered to your process.

### Python (`fal-client`)

```python
import fal_client

for event in fal_client.stream(
    "openai/gpt-image-2",
    arguments={"prompt": "a surreal oil painting of Mars at sunrise"},
):
    print(event)
```

Or with the optional wrapper:

```python
import gpt_image_2
for event in gpt_image_2.stream("a surreal oil painting of Mars at sunrise"):
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

### Python (`fal-client`)

```python
import time
import fal_client

APP_ID = "openai/gpt-image-2"

handle = fal_client.submit(
    APP_ID,
    arguments={"prompt": "a cinematic sunset over the Himalayas, 4k"},
    webhook_url="https://your.app/api/fal/webhook",
)
request_id = handle.request_id

while True:
    status = fal_client.status(APP_ID, request_id=request_id, with_logs=True)
    if type(status).__name__ in {"Completed", "CompletedWithErrors", "Failed"}:
        break
    time.sleep(2)

result = fal_client.result(APP_ID, request_id=request_id)
print(result["images"][0]["url"])
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
