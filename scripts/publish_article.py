#!/usr/bin/env python3
"""End-to-end ModelScope 研习社 article publisher.

Generates a properly encoded payload and outputs browser-compatible JS code
to send it via fetch(). Run this script, then copy-paste the JS into
a browser evaluate() call.

Usage:
    python publish_article.py \
        --title "文章标题" \
        --desc "文章简介" \
        --content-file article_content.txt \
        --subjects 数据集 \
        --domains 人工智能 \
        --output payload.b64

Then in browser evaluate():
    const b64 = '...paste base64 here...';
    const bytes = Uint8Array.from(atob(b64), c => c.charCodeAt(0));
    const json = new TextDecoder().decode(bytes);
    fetch('https://modelscope.cn/api/v1/articles', {
      method: 'PUT',
      headers: {'Content-Type':'application/json'},
      credentials: 'include',
      body: json
    });
"""
import argparse
import base64
import json
import re
import sys


def text_to_content_draft(text: str) -> str:
    """Convert plain text (paragraphs separated by blank lines) to ModelScope ContentDraft JSON."""
    paragraphs = []
    current = ""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "":
            if current:
                paragraphs.append(current)
                current = ""
            # Add empty paragraph for visual spacing
            paragraphs.append("")
        else:
            if current:
                current += "\n" + stripped
            else:
                current = stripped
    if current:
        paragraphs.append(current)

    # Remove trailing empty paragraphs
    while paragraphs and paragraphs[-1] == "":
        paragraphs.pop()

    draft_nodes = []
    for para in paragraphs:
        escaped = para.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        node = f'["p",{{}},["span",{{"data-type":"text"}},["span",{{"data-type":"leaf"}},"{escaped}"]]]'
        draft_nodes.append(node)

    return '["root",{},' + ",".join(draft_nodes) + "]"


def main():
    parser = argparse.ArgumentParser(description="Generate ModelScope article payload")
    parser.add_argument("--id", type=int, default=0, help="Existing article ID (0 to create new)")
    parser.add_argument("--title", required=True, help="Article title")
    parser.add_argument("--desc", required=True, help="Article description")
    parser.add_argument("--content", help="Article content as string")
    parser.add_argument("--content-file", help="File containing article content")
    parser.add_argument("--content-draft", help="Raw ContentDraft JSON (overrides --content)")
    parser.add_argument("--subjects", default="数据集", help="Comma-separated subjects")
    parser.add_argument("--domains", default="人工智能", help="Comma-separated domains")
    parser.add_argument("--image-url", default="https://resources.modelscope.cn/medal/learn-cover-v1/learn_blue.png", help="Cover image URL")
    parser.add_argument("--status", type=int, default=0, help="0=draft, 1=published")
    parser.add_argument("--output", required=True, help="Output base64 file")
    args = parser.parse_args()

    if args.content_draft:
        draft = args.content_draft
    elif args.content_file:
        with open(args.content_file, "r", encoding="utf-8") as f:
            draft = text_to_content_draft(f.read())
    elif args.content:
        draft = text_to_content_draft(args.content)
    else:
        draft = '["root",{},["p",{},["span",{"data-type":"text"},["span",{"data-type":"leaf"},""]]]]'

    subjects_json = json.dumps(args.subjects.split(","), ensure_ascii=False)
    domains_json = json.dumps(args.domains.split(","), ensure_ascii=False)

    payload = {
        "Id": args.id,
        "Title": args.title,
        "Description": args.desc,
        "ContentDraft": draft,
        "Status": args.status,
        "Subjects": subjects_json,
        "Domains": domains_json,
        "ImageUrl": args.image_url,
    }

    json_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    b64 = base64.b64encode(json_bytes).decode("ascii")

    with open(args.output, "w", encoding="ascii") as f:
        f.write(b64)

    print(f"Base64 payload written to: {args.output}")
    print(f"Payload size: {len(b64)} chars")
    print("\nBrowser JS snippet:")
    print("-" * 60)
    b64_preview = b64[:80]
    print(f"""const b64 = '{b64_preview}...'; // full string in file
const bytes = Uint8Array.from(atob(b64), c => c.charCodeAt(0));
const json = new TextDecoder().decode(bytes);
fetch('https://modelscope.cn/api/v1/articles', {{
  method: 'PUT',
  headers: {{'Content-Type':'application/json'}},
  credentials: 'include',
  body: json
}}).then(r => r.json()).then(d => console.log(d));""")
    print("-" * 60)


if __name__ == "__main__":
    main()
