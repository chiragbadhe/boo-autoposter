#!/usr/bin/env python3
"""Boo autopost: publish the next queued post to Instagram.

Each post is a folder in queue/ (processed in name order) holding either:
  01.jpg, 02.jpg, ...   1 image = single post, 2-20 images = carousel (JPEG only)
or
  reel.mp4              a Reel (vertical 9:16 MP4, H.264 + AAC)
  cover.jpg             the Reel's cover image (optional)
plus
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
        files = os.listdir(path)
        caption = ""
        caption_file = os.path.join(path, "caption.txt")
        if os.path.exists(caption_file):
            with open(caption_file, encoding="utf-8") as fh:
                caption = fh.read().strip()
        if "reel.mp4" in files:
            cover = "cover.jpg" if "cover.jpg" in files else None
            return folder, "reel", ["reel.mp4"], caption, cover
        images = sorted(f for f in files if f.lower().endswith(IMAGE_EXT))
        if images:
            return folder, "images", images, caption, None
    return None


class GraphError(Exception):
    """A Graph API error, with Meta's message pulled out of the response."""
    # Codes/subcodes Meta uses for "could not fetch the media" and temporary trouble.
    RETRY_CODES = {1, 2, 4, 9004, 36000, 36001}
    RETRY_SUBCODES = {2207003, 2207020, 2207052, 2207001}

    def __init__(self, status, method, path, body):
        self.status, self.method, self.path, self.body = status, method, path, body
        try:
            err = json.loads(body).get("error", {})
        except ValueError:
            err = {}
        self.code = err.get("code")
        self.subcode = err.get("error_subcode")
        self.message = err.get("error_user_msg") or err.get("message") or body[:300]
        self.short = f"code {self.code}" + (f"/{self.subcode}" if self.subcode else "")
        super().__init__(self.describe())

    @property
    def retryable(self):
        return self.code in self.RETRY_CODES or self.subcode in self.RETRY_SUBCODES

    def describe(self):
        hint = ""
        if self.code == 190:
            hint = "\nFix: the access token expired or is invalid. Make a new long-lived token and update the IG_ACCESS_TOKEN secret."
        elif self.code in (10, 200) or self.code == 3:
            hint = "\nFix: the token is missing a permission (instagram_content_publish) or the app lacks access."
        elif self.subcode in self.RETRY_SUBCODES or self.code == 9004:
            hint = "\nFix: Instagram could not download the image. Open the image link from a dry run to check it loads."
        elif self.code == 4 or self.code == 32 or self.code == 613:
            hint = "\nFix: rate limit reached. It will work again on the next run."
        # Never print the token: Meta's error body does not echo it.
        return (f"Instagram API error on {self.method} {self.path}\n"
                f"  HTTP {self.status}, {self.short}\n  Meta says: {self.message}{hint}")


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
            raise GraphError(err.code, method, path, body) from None

    def create_container(self, params, tries=4):
        """Create a media container, retrying when Meta can't fetch the image yet."""
        for attempt in range(1, tries + 1):
            try:
                return self.call("POST", f"{self.user_id}/media", params)["id"]
            except GraphError as e:
                if attempt == tries or not e.retryable:
                    raise
                wait = 15 * attempt
                print(f"  Instagram couldn't take the image yet ({e.short}); retrying in {wait}s", flush=True)
                time.sleep(wait)

    def wait_ready(self, container_id, timeout=600):
        deadline = time.time() + timeout
        while time.time() < deadline:
            info = self.call("GET", container_id, {"fields": "status_code,status"})
            status = info.get("status_code")
            if status == "FINISHED":
                return
            if status in ("ERROR", "EXPIRED"):
                sys.exit(f"Instagram could not process an image ({status}): {info.get('status', 'no details')}")
            time.sleep(5)
        sys.exit(f"Container {container_id} not ready after {timeout}s")

    def publish(self, container_id):
        return self.call("POST", f"{self.user_id}/media_publish", {"creation_id": container_id})["id"]


def check_images(urls):
    """Fetch every image once: warms the CDN and fails early with a clear message."""
    for u in urls:
        for attempt in range(1, 5):
            try:
                req = urllib.request.Request(u, headers={"User-Agent": "boo-autopost"})
                with urllib.request.urlopen(req, timeout=60) as resp:
                    ctype = resp.headers.get("Content-Type", "")
                    resp.read()
                if resp.status == 200 and ("jpeg" in ctype or "mp4" in ctype):
                    break
                problem = f"HTTP {resp.status}, type {ctype or 'unknown'}"
            except urllib.error.URLError as e:
                problem = str(getattr(e, "code", "") or e.reason)
            if attempt == 4:
                sys.exit(f"Image not reachable for Instagram: {u}\n  ({problem}). "
                         "Check that the repo is public and the file is a JPEG or MP4.")
            time.sleep(10 * attempt)
    print(f"  All {len(urls)} files reachable.", flush=True)


def main():
    found = next_post()
    if not found:
        print("Queue is empty: nothing to post.")
        return
    folder, kind, images, caption, cover = found
    base_url = env("IMAGE_BASE_URL", required=True).rstrip("/")
    def url_of(name):
        return f"{base_url}/queue/{urllib.parse.quote(folder)}/{urllib.parse.quote(name)}"
    urls = [url_of(img) for img in images]
    cover_url = url_of(cover) if cover else None

    if len(urls) > 20:
        sys.exit(f"{folder}: {len(urls)} images; Instagram carousels hold at most 20.")

    what = "reel" if kind == "reel" else f"{len(urls)} image{'s' if len(urls) != 1 else ''}"
    print(f"Next post: {folder} ({what})", flush=True)
    if env("DRY_RUN") == "1":
        for u in urls:
            print("  image:", u)
        print("  caption:", (caption[:80] + "…") if len(caption) > 80 else caption)
        print("DRY_RUN=1, nothing posted.")
        return

    check_images(urls + ([cover_url] if cover_url else []))

    graph = Graph(
        env("GRAPH_HOST", "graph.instagram.com"),
        env("GRAPH_VERSION", ""),
        env("IG_ACCESS_TOKEN", required=True),
        env("IG_USER_ID", required=True),
    )

    if kind == "reel":
        params = {"media_type": "REELS", "video_url": urls[0], "caption": caption, "share_to_feed": "true"}
        if cover_url:
            params["cover_url"] = cover_url
        container = graph.create_container(params)
        print("  Reel uploaded; waiting for Instagram to process the video…", flush=True)
    elif len(urls) == 1:
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
    try:
        main()
    except GraphError as e:
        sys.exit(str(e))
