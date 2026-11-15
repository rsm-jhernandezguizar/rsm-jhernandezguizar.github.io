# Working conventions

- Preserve the English professional portfolio; Crea Circuitos maintains its own Spanish-language site.
- Prefer small, targeted changes and preserve the existing layout unless the author explicitly asks for a redesign. Highlight changes in review previews, not in production pages.
- Do not invent accomplishments, dates, endorsements, credentials, or financial outcomes.
- Before presenting professional copy, use the `professional-profile-review` skill (when available) and review it through editorial, director-level executive, and expert systems-engineering perspectives. Treat these as review lenses, not independent people.
- Distinguish company tenure from the start of the latest role; show prior progression when needed to avoid false employment gaps. Preserve natural sentences rather than pasting titles into existing prose.
- Keep résumé experience consistent: company and overall dates in the heading, location beneath, then role and role dates. Avoid a separate "Company tenure" label. Use selective bolding and concise bullets for responsibilities.
- Render affected Quarto pages and commit their generated `docs/` files alongside sources; GitHub Pages serves `main:/docs`.
- Submit changes in a PR, check the current commit's CI after each push, and fix failures before handoff.
- Use squash and source-branch deletion when a merge is authorized.
- Do not publish new profile claims without the author's review.
- Make review as easy as possible: after website changes, start a tested preview, open it in the app, and provide a clickable URL. Do not hand the author terminal commands when you can run them yourself.
- Use `python3 scripts/preview.py --skip-render --no-open` for an already-rendered PR; `Preview website.command` is the author's double-click fallback. Explain when a URL is local and temporary.
- Once GitHub Actions can run successfully again, require the `render` status check on `main`. Until then, preserve PR protection without that required check and clearly report the billing blocker.
