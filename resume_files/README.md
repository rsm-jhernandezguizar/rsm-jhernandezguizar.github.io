# Editable PDF résumé

The current downloadable file is `Juan_Hernandez_Guizar_Resume.pdf`. The dated 2025 PDF remains unchanged as an archive.

## Rebuild

1. Edit `resume-content.json`; retain only author-confirmed facts and scope.
2. Install `reportlab` and `pypdf` in a Python virtual environment. The generator embeds installed Times New Roman fonts on macOS/Windows or Liberation Serif on Linux; `--font-dir` selects a custom font directory. Do not commit proprietary font files.
3. From the repository root, run `python scripts/build_resume_pdf.py`.
4. Render and visually inspect the resulting one-page PDF before committing it.

The generator creates `output/pdf/Juan_Hernandez_Guizar_Resume.pdf` and copies the candidate to the source and `docs/` download paths. Review it before publishing. The HTML résumé remains in `Resume.qmd`; keep its title and download link aligned when making changes. The PDF preserves the historical PDF's fuller experience and accomplishments rather than replacing them with the shorter web résumé.

## Revision evidence

- On 15 November 2026, the author confirmed the current function **Digital Twin Lead, Advanced Systems** and formal level **Aerospace Systems Engineer Sr (4)**.
- At the author's request, display the current level as **Aerospace Systems Engineer IV (Senior)**, consistent with the earlier II and III levels.
- The author separately confirmed the level 4 promotion in July 2026. The functional role and level therefore begin in the same month.
- Display only one main employment range for Blue Origin. Keep functional-role and level start dates in the editable source for factual continuity, but do not repeat them in the rendered PDF. Preserve the earlier III and II role ranges. Numeric PDF dates and work-experience dates in the web résumé use MM/YY; keep MM/YYYY in the source data to avoid ambiguity. Homepage employment ranges use years only.
- Company employment continues from October 2022. The previous III role is March 2025-July 2026; the II role is October 2022-March 2025. The earlier start dates come from the historical PDF and the July 2026 transition was confirmed by the author.
- After a draft message mentioned July 2022, the author explicitly reconfirmed October 2022 as the company start: display 2022-Present on the homepage and 10/22-Present in both résumés. Do not treat July 2022 as an employment fact.
- Accomplishments, financial figures, contacts and other employment dates are retained from the author's historical PDF, not independently verified in this revision. Minor grammar, punctuation and a duplicated GitHub entry are corrected without adding achievements.
- The author confirmed a direct transition from Rockwell Collins to Mercury Systems in May 2021, without a break. Both the PDF and web résumé therefore use May 2021 as the Rockwell Collins end month and Mercury Systems start month; no exact day is inferred.
