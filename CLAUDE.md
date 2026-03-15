# HBR Learning Library — Project Rules

## Quick Reference

| What | Where |
|------|-------|
| System prompt (v1.6) | `hbr-claude-code/system_prompt.xml` |
| Article HTMLs | `docs/YYYY-MM-DD_short-title.html` |
| Dashboard | `docs/index.html` (auto-generated article list) |
| Index builder | `build_index.py` — run after adding articles |
| Single article command | `/hbr-single` |
| Batch command | `/hbr-batch` |
| Git remote | `git@github.com:Eaglemamba/Harvard-Business-Review.git` |

---

## Workflow — Adding a New Article

```
1. /hbr-single   (paste article text)
   OR
   /hbr-batch    (paste multiple articles separated by ---END---)

2. build_index.py runs automatically at the end of each command
   → rewrites docs/index.html article list from meta tags

3. git commit + push happens automatically
```

**Do not manually edit the `const articles = [...]` block in `docs/index.html`.**
It is auto-generated. Always use `python3 build_index.py` to regenerate it.

---

## File Naming Convention

- Pattern: `YYYY-MM-DD_short-title.html`
- All lowercase, hyphens only, no spaces or special characters
- Date = date the article was processed (not original publication date)
- Short title = 3-5 words that identify the article

Examples:
- `2026-02-24_ai-upending-marketing.html`
- `2026-03-15_context-competitive-advantage.html`

---

## Document Structure (v1.6)

Each article HTML must include all of these in `<head>`:

```html
<meta name="doc-date"    content="YYYY-MM-DD">
<meta name="doc-title"   content="Article title (max 60 chars)">
<meta name="doc-source"  content="Author / Outlet">
<meta name="doc-tags"    content="Agent,LLM,Tool">
<meta name="doc-rating"  content="4.1">
<meta name="doc-summary" content="One-line Chinese summary (max 80 chars)">
<meta name="doc-file"    content="YYYY-MM-DD_short-title.html">
```

Valid tags: `Agent`, `Tool`, `LLM`, `Prompt`, `Framework`, `Analysis`,
`Automation`, `Security`, `Content`, `API`, `Research`

---

## build_index.py Details

- Scans all `docs/*.html` (excluding `index.html`)
- Reads `doc-*` meta tags from each file
- Sorts articles newest-first
- Replaces the `AUTO-GENERATED START / END` block in `docs/index.html`
- Skips files missing `doc-date`, `doc-title`, or `doc-file` tags

Run manually: `python3 build_index.py`

---

## Known Pitfalls

### Do not edit the articles array manually
The `const articles = [...]` block in `docs/index.html` is between
`AUTO-GENERATED START` and `AUTO-GENERATED END` markers. It gets
overwritten every time `build_index.py` runs. Use meta tags in article
HTML files as the source of truth.

### system_prompt.xml path
The commands reference `system_prompt.xml` as "in the project root" but
the actual path is `hbr-claude-code/system_prompt.xml`. Always use the
full path when reading it.

### Adding new tags
If a new tag appears in articles but is not in `docs/index.html`:
1. Add CSS class `.tag-newtag` to the `<style>` block
2. Add pill active color `.pill-tag-NewTag.active`
3. Add `"NewTag": "tag-newtag"` to the `tagClasses` object

---

## Scale Plan (future)

When articles exceed ~200, restructure `docs/` into monthly subfolders:
- `docs/2026-02/`, `docs/2026-03/`, etc.
- Per-month index files + master `docs/index.html`
- Update `build_index.py` to handle subdirectories
