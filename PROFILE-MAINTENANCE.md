# Professional profile maintenance

`data/profile.json` is the shared source for professional facts. Experience was checked against the author's LinkedIn profile on 2026-11-15. Education dates and contact details are retained from the existing website; they were not visible in that extraction.

1. Review the JSON facts and update `reviewed_on`.
2. Run `python3 scripts/render_profile.py` (also called by Quarto pre-render).
3. Render `index.qmd`, `Resume.qmd`, and the Crea Circuitos case study with Quarto.
4. Review the generated HTML in `docs/`, since GitHub Pages publishes `main:/docs`.
5. Submit source and generated HTML together in a PR; validate checks before merging.

No LinkedIn scraping is required to render this site. The reviewed JSON is authoritative for publication. Projected employer ROI figures are intentionally excluded pending author review. The previous PDF is archived; a refreshed PDF is a separate review item.

The generated Markdown includes in `_generated/` are tracked because Quarto resolves includes before project pre-render. Regenerate them after edits; CI verifies that the tracked includes match the data before rendering.
