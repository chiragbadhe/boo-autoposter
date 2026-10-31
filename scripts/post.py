#!/usr/bin/env python3
"""Boo autopost: publish the next queued post to Instagram.

Each post is a folder in queue/ (processed in name order) holding:
  01.jpg, 02.jpg, ...   1 image = single post, 2-20 images = carousel (JPEG only)
  caption.txt           the caption (optional)

Images are fetched by Meta from a public URL, built from IMAGE_BASE_URL.
After a successful publish the folder is moved to posted/ by the workflow.

Environment:
  IG_ACCESS_TOKEN   long-lived access token (GitHub secret)
  IG_USER_ID        Instagram professional account ID (GitHub secret)
  GRAPH_HOST        graph.instagram.com (Instagram Login, default)
                    or graph.facebook.com (Facebook Login for Business)
  GRAPH_VERSION     e.g. v23.0; leave empty to use the unversioned endpoint
  IMAGE_BASE_URL    public URL of the repo root, e.g.
                    https://cdn.jsdelivr.net/gh/<user>/<repo>@<commit-sha>
  DRY_RUN           "1" = print what would be posted, call nothing
Prints the posted folder name to stdout as: POSTED=<folder>
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "queue")
IMAGE_EXT = (".jpg", ".jpeg")


def env(name, default=None, required=False):
    value = os.environ.get(name, default)
    if required and not value:
        sys.exit(f"Missing environment variable: {name}")
    return value


def next_post():
    if not os.path.isdir(QUEUE):
        return None
    folders = sorted(
        d for d in os.listdir(QUEUE)
        if os.path.isdir(os.path.join(QUEUE, d)) and not d.startswith(".")
    )
    for folder in folders:
        path = os.path.join(QUEUE, folder)
        images = sorted(f for f in os.listdir(path) if f.lower().endswith(IMAGE_EXT))
        if images:
            caption_file = os.path.join(path, "caption.txt")
            caption = ""
            if os.path.exists(caption_file):
                with open(caption_file, encoding="utf-8") as fh:
                    caption = fh.read().strip()
            return folder, images, caption
    return None


class Graph:
    def __init__(self, host, version, token, user_id):
        prefix = f"https://{host}/"
        self.base = prefix + (f"{version}/" if version else "")
        self.token = token
        self.user_id = user_id

    def call(self, method, path, params=None):
        params = dict(params or {})
        params["access_token"] = self.token
        data = urllib.parse.urlencode(params)
        url = self.base + path
        if method == "GET":
            req = urllib.request.Request(f"{url}?{data}")
        else:
            req = urllib.request.Request(url, data=data.encode(), method="POST")
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as err:
            body = err.read().decode(errors="replace")
            # Never print the token: the body comes from Meta and does not echo it.
            sys.exit(f"Graph API error {err.code} on {method} {path}: {body}")

    def create_container(self, params):
        return self.call("POST", f"{self.user_id}/media", params)["id"]

    def wait_ready(self, container_id, timeout=300):
        deadline = time.time() + timeout
        while time.time() < deadline:
            status = self.call("GET", container_id, {"fields": "status_code"}).get("status_code")
            if status == "FINISHED":
                return
            if status in ("ERROR", "EXPIRED"):
                sys.exit(f"Container {container_id} failed with status {status}")
            time.sleep(5)
        sys.exit(f"Container {container_id} not ready after {timeout}s")

    def publish(self, container_id):
        return self.call("POST", f"{self.user_id}/media_publish", {"creation_id": container_id})["id"]


def main():
    found = next_post()
    if not found:
        print("Queue is empty: nothing to post.")
        return
    folder, images, caption = found
    base_url = env("IMAGE_BASE_URL", required=True).rstrip("/")
    urls = [f"{base_url}/queue/{urllib.parse.quote(folder)}/{urllib.parse.quote(img)}" for img in images]

    if len(urls) > 20:
        sys.exit(f"{folder}: {len(urls)} images; Instagram carousels hold at most 20.")

    print(f"Next post: {folder} ({len(urls)} image{'s' if len(urls) != 1 else ''})")
    if env("DRY_RUN") == "1":
        for u in urls:
            print("  image:", u)
        print("  caption:", (caption[:80] + "…") if len(caption) > 80 else caption)
        print("DRY_RUN=1, nothing posted.")
        return

    graph = Graph(
        env("GRAPH_HOST", "graph.instagram.com"),
        env("GRAPH_VERSION", ""),
        env("IG_ACCESS_TOKEN", required=True),
        env("IG_USER_ID", required=True),
    )

    if len(urls) == 1:
        container = graph.create_container({"image_url": urls[0], "caption": caption})
    else:
        children = []
        for u in urls:
            child = graph.create_container({"image_url": u, "is_carousel_item": "true"})
            graph.wait_ready(child)
            children.append(child)
        container = graph.create_container(
            {"media_type": "CAROUSEL", "children": ",".join(children), "caption": caption}
        )
    graph.wait_ready(container)
    media_id = graph.publish(container)
    print(f"Published {folder} as media {media_id}")
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as fh:
            fh.write(f"posted={folder}\n")
    print(f"POSTED={folder}")


if __name__ == "__main__":
    main()
