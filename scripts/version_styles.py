"""Give the custom stylesheet a content-based URL after each Quarto render."""

import hashlib
import os
import re
from pathlib import Path

STYLESHEET_LINK = re.compile(
    r'(?P<start><link\b[^>]*\bhref=["\'])'
    r'(?P<prefix>(?:\.\./)*)styles(?:\.[a-f0-9]{12})?\.css'
    r'(?P<end>["\'])',
    re.IGNORECASE,
)


def version_styles(output_dir, output_files):
    pages = [path for path in output_files if path.suffix == ".html"]
    if not pages:
        return
    stylesheet = (output_dir / "styles.css").read_bytes()
    digest = hashlib.sha256(stylesheet).hexdigest()[:12]
    filename = f"styles.{digest}.css"
    asset = output_dir / filename
    for page in pages:
        content = page.read_text(encoding="utf-8")
        updated, matches = STYLESHEET_LINK.subn(
            lambda match: (
                match["start"] + match["prefix"] + filename + match["end"]
            ),
            content,
        )
        if matches and not asset.exists():
            asset.write_bytes(stylesheet)
        if updated != content:
            page.write_text(updated, encoding="utf-8")
    # Retain earlier hashed assets so cached HTML can still load its own version.


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    output = root / os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "docs")
    paths = [root / path for path in os.environ.get("QUARTO_PROJECT_OUTPUT_FILES", "").splitlines() if path]
    if not paths:
        raise SystemExit("Run this script through Quarto's post-render hook.")
    version_styles(output, paths)
