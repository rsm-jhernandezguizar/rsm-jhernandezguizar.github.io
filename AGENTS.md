# Working conventions

- Preserve the English professional portfolio; Crea Circuitos maintains its own Spanish-language site.
- Edit shared professional facts in `data/profile.json`, recording source and review date.
- Do not invent accomplishments, dates, endorsements, credentials, or financial outcomes.
- Render affected Quarto pages and commit their generated `docs/` files alongside sources; GitHub Pages serves `main:/docs`.
- Submit changes in a PR, check the current commit's CI after each push, and fix failures before handoff.
- Use squash and source-branch deletion when a merge is authorized.
- Do not publish new profile claims without the author's review.
- Make review as easy as possible: after website changes, start a tested preview, open it in the app, and provide a clickable URL. Do not hand the author terminal commands when you can run them yourself.
- Use `python3 scripts/preview.py --skip-render --no-open` for an already-rendered PR; `Preview website.command` is the author's double-click fallback. Explain when a URL is local and temporary.
