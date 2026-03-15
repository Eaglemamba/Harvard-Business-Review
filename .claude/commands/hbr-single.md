# HBR Single Article Processor

The user will paste one HBR article text below.

1. Read the v1.6 AI Expert Learning System prompt from `hbr-claude-code/system_prompt.xml`.
2. Generate a complete educational HTML document following the full v1.6 document structure: dashboard_meta, header, executive_summary with Rating Bar, learning_objectives, framework_visual (if applicable), content_sections, key_takeaways, practice (accordion), bottom_line, and footer.
3. Use the `YYYY-MM-DD_short-title.html` naming convention from the doc-file meta tag.
4. Save the HTML file to the `docs/` folder.
5. Run `python3 build_index.py` to auto-update the dashboard index.
6. Stage all changed files, commit with message "Add [title] - YYYY-MM-DD", and push to GitHub.

Skip the score confirmation step -- always proceed with generation regardless of rating.

$ARGUMENTS
