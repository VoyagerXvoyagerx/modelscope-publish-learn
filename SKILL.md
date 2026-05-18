---
name: modelscope-publish-learn
description: |
  Publish articles to ModelScope.cn 研习社 (Learn/Study section). Use this skill whenever the user wants to write, create, edit, or publish an article on ModelScope's learning community. Handles the full workflow from article creation to metadata editing to final publication via browser automation and API calls.
---

# ModelScope 研习社文章发布

## Prerequisites

- Ensure kimi-webbridge daemon is running (`~/.kimi-webbridge/bin/kimi-webbridge status`). If not, start it.
- User must be logged in to ModelScope in their browser.

## Workflow Overview

```
1. Create draft  →  POST /api/v1/articles (or click "下一步" on /learn/create)
2. Edit content   →  PUT /api/v1/articles with ContentDraft
3. Edit metadata  →  Navigate to /learn/editor/{id}
4. Publish        →  Click "发 布" then confirm
```

## Key API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/articles` | POST | Create new article draft |
| `/api/v1/articles` | PUT | Update article (title, desc, content, metadata) |
| `/api/v1/articles/{id}` | GET | Read article data |
| `/api/v1/articles/{id}/publish` | PUT | Publish article |

## Critical Field Mapping

- **PUT payload uses `Description`** for the article summary/blurb
- **GET response returns it as `Desc`**
- **Always include ALL fields in PUT** — partial payloads clear missing fields

## ContentDraft Format

The editor uses a custom JSON array format. Each paragraph:

```json
["p",{},["span",{"data-type":"text"},["span",{"data-type":"leaf"},"PARAGRAPH TEXT"]]]
```

Full document wrapper:
```json
["root",{},["p",{},[...]],["p",{},[...]],...]
```

## Encoding Safety (Windows)

**NEVER pass Chinese characters through inline bash/python `-c` commands** on Windows — the console uses GBK and will corrupt UTF-8.

**Always use the helper script with file input or write arguments to a file first:**

```bash
python ~/.kimi/skills/modelscope-publish-learn/scripts/gen_payload.py \
  --id 433474 \
  --title "文章标题" \
  --desc "文章简介" \
  --content-draft 'JSON_STRING' \
  --subjects '["数据集"]' \
  --domains '["人工智能"]' \
  --image-url "COVER_IMAGE_URL" \
  --output ~/.kimi/skills/modelscope-publish-learn/scripts/payload.json
```

Then send via browser fetch with `TextDecoder`:

```javascript
const b64 = 'BASE64_FROM_FILE';
const bytes = Uint8Array.from(atob(b64), c => c.charCodeAt(0));
const json = new TextDecoder().decode(bytes);
fetch('https://modelscope.cn/api/v1/articles', {
  method: 'PUT',
  headers: {'Content-Type':'application/json'},
  credentials: 'include',
  body: json
});
```

## Metadata Page Form Fields

Navigate to `https://modelscope.cn/learn/editor/{id}`

| Field | Selector | How to Fill |
|-------|----------|-------------|
| Title | `input#Title` | Use `fill` tool |
| Description | `textarea#Description` | Use native setter + dispatch input event (see script) |
| Subject | `input#Subjects` | Type and press Enter |
| Domain | `input#Domains` | Type and press Enter |
| Cover | Click default image | `img[src*="learn_blue.png"]` etc. |

Use `scripts/fill_metadata.py` to programmatically fill all metadata fields.

## Publish Button Sequence

1. Click "发 布" (usually index 6 in the button list)
2. Wait for confirmation modal
3. Click "知道了" (usually the last button)
4. Page redirects to `/my/myspace?activeTab=learn`

## Common Pitfalls

- The rich text editor (`modelscope_ding_editor_`) is canvas-like and **resists all standard automation** — use the API for content instead.
- The `PUT /api/v1/articles` endpoint does **full replacement**, not partial update.
- The listing page (`/my/myspace`) may cache old data briefly; the article detail page (`/learn/{id}`) is the source of truth.
- On Windows, Python printing Chinese characters to the console may **look garbled** due to GBK encoding, but the actual bytes in the generated files are correct UTF-8. Trust the file output, not the console display.
