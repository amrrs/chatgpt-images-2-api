// Small helper to download gpt-image-2 results to disk in Node.js examples.
import { mkdir, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { URL } from "node:url";

export async function saveImage(image, { outputDir = "outputs", prefix, index = 0 } = {}) {
  const url = typeof image === "string" ? image : image.url;
  let filename;
  if (prefix) {
    const ext = inferExt(image);
    filename = `${prefix}_${index}${ext}`;
  } else if (typeof image !== "string" && image.file_name) {
    filename = image.file_name;
  } else {
    filename = new URL(url).pathname.split("/").pop() || `image_${index}.png`;
  }
  const path = join(outputDir, safeName(filename));
  await mkdir(dirname(path), { recursive: true });
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed to download ${url}: ${res.status}`);
  const buf = Buffer.from(await res.arrayBuffer());
  await writeFile(path, buf);
  return path;
}

export async function saveResult(data, opts = {}) {
  const images = data?.images || [];
  const paths = [];
  for (let i = 0; i < images.length; i++) {
    paths.push(await saveImage(images[i], { ...opts, index: i }));
  }
  return paths;
}

function inferExt(image) {
  if (typeof image !== "string") {
    if (image.file_name && image.file_name.includes(".")) {
      return "." + image.file_name.split(".").pop();
    }
    if (image.content_type && image.content_type.includes("/")) {
      return "." + image.content_type.split("/")[1];
    }
  }
  return ".png";
}

function safeName(name) {
  return name.replace(/[^a-zA-Z0-9._-]+/g, "_").replace(/^[._]+|[._]+$/g, "") || "image";
}
