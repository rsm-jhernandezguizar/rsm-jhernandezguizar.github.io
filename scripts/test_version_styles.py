"""Regression checks for custom CSS cache versioning; standard library only."""

import hashlib
import tempfile
import unittest
from pathlib import Path

from version_styles import version_styles


class VersionStylesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name)
        self.css = self.output / "styles.css"
        self.css.write_text("main strong > a { font-weight: 700; }\n")
        self.page = self.output / "index.html"
        self.original = '<link rel="stylesheet" href="styles.css"><h1>Approved copy</h1>'
        self.page.write_text(self.original)

    def test_versions_css_without_changing_approved_content(self):
        version_styles(self.output, [self.page])
        digest = hashlib.sha256(self.css.read_bytes()).hexdigest()[:12]
        name = f"styles.{digest}.css"
        self.assertEqual(self.page.read_text(), self.original.replace("styles.css", name))
        self.assertEqual((self.output / name).read_bytes(), self.css.read_bytes())

    def test_repeated_run_is_idempotent(self):
        version_styles(self.output, [self.page])
        first = self.page.read_bytes()
        version_styles(self.output, [self.page])
        self.assertEqual(first, self.page.read_bytes())
        self.assertEqual(len(list(self.output.glob("styles.*.css"))), 1)

    def test_changed_css_gets_a_new_url_and_preserves_old_asset(self):
        version_styles(self.output, [self.page])
        old_asset = next(self.output.glob("styles.*.css"))
        self.css.write_text("main strong > a { font-weight: 800; }\n")
        version_styles(self.output, [self.page])
        self.assertNotIn(old_asset.name, self.page.read_text())
        self.assertTrue(old_asset.exists())
        self.assertEqual(len(list(self.output.glob("styles.*.css"))), 2)

    def test_preserves_relative_paths_and_other_stylesheets(self):
        nested = self.output / "portfolio"
        nested.mkdir()
        page = nested / "index.html"
        page.write_text('<link href="../styles.css"><link href="other.css">')
        version_styles(self.output, [page])
        self.assertRegex(page.read_text(), r'href="\.\./styles\.[a-f0-9]{12}\.css"')
        self.assertIn('href="other.css"', page.read_text())

    def test_does_not_rewrite_unrendered_pages(self):
        other = self.output / "other.html"
        other.write_text(self.original)
        version_styles(self.output, [self.page])
        self.assertEqual(other.read_text(), self.original)


if __name__ == "__main__":
    unittest.main()
