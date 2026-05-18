#!/usr/bin/env python3
"""Generate a base64-encoded ModelScope article payload safely on Windows.

Usage:
    python gen_payload.py --id 433474 \
        --title "文章标题" \
        --desc "文章简介" \
        --content-draft '["root",{},...]' \
        --subjects '["数据集"]' \
        --domains '["人工智能"]' \
        --image-url "https://..." \
        --output payload.json
"""
import argparse
import base64
import json
import sys


def main():
    parser = argparse.ArgumentParser(description="Generate ModelScope article payload")
    parser.add_argument("--id", type=int, required=True, help="Article ID")
    parser.add_argument("--title", required=True, help="Article title")
    parser.add_argument("--desc", required=True, help="Article description/summary")
    parser.add_argument("--content-draft", required=True, help="ContentDraft JSON string")
    parser.add_argument("--subjects", default='[]', help="Subjects JSON array string")
    parser.add_argument("--domains", default='[]', help="Domains JSON array string")
    parser.add_argument("--image-url", default="", help="Cover image URL")
    parser.add_argument("--status", type=int, default=0, help="Article status (0=draft)")
    parser.add_argument("--output", required=True, help="Output JSON file path")
    parser.add_argument("--b64-output", help="Optional base64 output file path")
    args = parser.parse_args()

    payload = {
        "Id": args.id,
        "Title": args.title,
        "Description": args.desc,
        "ContentDraft": args.content_draft,
        "Status": args.status,
        "Subjects": args.subjects,
        "Domains": args.domains,
        "ImageUrl": args.image_url,
    }

    json_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    with open(args.output, "wb") as f:
        f.write(json_bytes)

    if args.b64_output:
        b64 = base64.b64encode(json_bytes).decode("ascii")
        with open(args.b64_output, "w", encoding="ascii") as f:
            f.write(b64)
        print(f"Base64 payload written to: {args.b64_output}")
    else:
        # Print base64 to stdout for shell capture
        b64 = base64.b64encode(json_bytes).decode("ascii")
        print(b64)

    print(f"JSON payload written to: {args.output}")


if __name__ == "__main__":
    main()
