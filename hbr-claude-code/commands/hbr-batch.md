# HBR Batch Processor

The user will paste one or more HBR article texts below. If multiple articles are provided, they are separated by `---END---`.

## Processing Strategy

1. **Split**: Parse the input text and split it into individual articles using `---END---` as the delimiter.

2. **Dispatch in parallel**: For each article, launch a separate subagent (using the Task tool) to process it concurrently. Each subagent should:
   - Read the v1.6 AI Expert Learning System prompt from `hbr-claude-code/system_prompt.xml`
   - Generate a complete educational HTML document following the full v1.6 document structure: dashboard_meta, header, executive_summary with Rating Bar, learning_objectives, framework_visual (if applicable), content_sections, key_takeaways, practice (accordion), bottom_line, and footer
   - Use the `YYYY-MM-DD_short-title.html` naming convention from the doc-file meta tag
   - Save the HTML file to the `docs/` folder
   - Skip the score confirmation step -- always proceed with generation regardless of rating

3. **Rebuild index**: After ALL subagents have completed, run `python3 build_index.py` to auto-update `docs/index.html`.

4. **Git push**: Stage all new HTML files and the updated index.html, commit with message "Add [N] HBR articles - YYYY-MM-DD", and push to GitHub in a single commit.

5. **Report**: List all generated files with their ratings and filenames.

## Important

- All subagents run in PARALLEL to minimize total processing time
- Each subagent gets its own context window, so article length is not a concern
- If only one article is pasted (no `---END---` delimiter), process it directly without dispatching a subagent
- Always run `build_index.py` before committing — never manually edit the articles array in index.html

$ARGUMENTS
