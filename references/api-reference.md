# ModelScope 研习社 API Reference

## Article Object Fields

| Field | Type | PUT Field | GET Field | Required | Notes |
|-------|------|-----------|-----------|----------|-------|
| Id | int | ✓ | ✓ | Yes | Article ID |
| Title | string | ✓ | ✓ | Yes | Max 128 chars |
| Description | string | ✓ (as `Description`) | `Desc` | Yes | Summary blurb, max 200 chars |
| ContentDraft | string | ✓ | ✓ | Yes | Editor JSON format |
| Status | int | ✓ | ✓ | Yes | 0=draft, 1=published |
| Subjects | string | ✓ | ✓ | No | JSON array string e.g. `'["数据集"]'` |
| Domains | string | ✓ | ✓ | No | JSON array string e.g. `'["人工智能"]'` |
| ImageUrl | string | ✓ | ✓ | No | Cover image URL |
| ContentType | string | ✓ | ✓ | No | Usually empty |
| ContentUrl | string | ✓ | ✓ | No | Usually empty |

## ContentDraft Format

### Paragraph
```json
["p",{},["span",{"data-type":"text"},["span",{"data-type":"leaf"},"TEXT HERE"]]]
```

### Full Document
```json
["root",{},
  ["p",{},["span",{"data-type":"text"},["span",{"data-type":"leaf"},"First paragraph."]]],
  ["p",{},["span",{"data-type":"text"},["span",{"data-type":"leaf"},""]]],
  ["p",{},["span",{"data-type":"text"},["span",{"data-type":"leaf"},"Second paragraph."]]]
]
```

### Heading (Simulated)
Use bold text in a paragraph since the editor doesn't have true heading blocks in the draft format:
```json
["p",{},["span",{"data-type":"text"},["span",{"data-type":"leaf"},"一、章节标题"]]]
```

## API Examples

### Create Draft
```bash
curl -X POST https://modelscope.cn/api/v1/articles \
  -H "Content-Type: application/json" \
  -H "Cookie: ..." \
  -d '{"ContentDraft":"[\"root\",{},[\"p\",{},[\"span\",{\"data-type\":\"text\"},[\"span\",{\"data-type\":\"leaf\"},\"\"]]]]"}'
```

### Update Article
```bash
curl -X PUT https://modelscope.cn/api/v1/articles \
  -H "Content-Type: application/json" \
  -H "Cookie: ..." \
  -d @payload.json
```

### Publish
```bash
curl -X PUT https://modelscope.cn/api/v1/articles/{id}/publish \
  -H "Cookie: ..."
```

## URL Patterns

| Page | URL Pattern |
|------|-------------|
| Create article | `/learn/create` |
| Edit content | `/learn/edit/{id}` |
| Edit metadata | `/learn/editor/{id}` |
| View article | `/learn/{id}` |
| User articles | `/my/myspace?activeTab=learn` |
