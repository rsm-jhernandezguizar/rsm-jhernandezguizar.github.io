import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OLD = "portfolio/mision-15/index.html"
NEW = "portfolio/1-por-ciento-cada-dia/index.html"
CREA = "portfolio/crea-circuitos-youtube/index.html"


class PortfolioProjectsTest(unittest.TestCase):
    def test_legacy_url_has_a_static_fallback_and_keeps_link_context(self):
        published = (DOCS / OLD).read_text(encoding="utf-8")
        self.assertEqual(published, (ROOT / OLD).read_text(encoding="utf-8"))
        self.assertIn('href="../1-por-ciento-cada-dia/"', published)
        self.assertIn("window.location.search + window.location.hash", published)
        self.assertIn('content="noindex, follow"', published)

    def test_listing_and_search_point_to_current_routes(self):
        listing = (DOCS / "portfolio.html").read_text(encoding="utf-8")
        entries = json.loads((DOCS / "search.json").read_text(encoding="utf-8"))
        paths = {entry["href"].split("#")[0] for entry in entries}
        for route in (NEW, CREA):
            self.assertIn(f'href="./{route}"', listing)
            self.assertIn(route, paths)
        self.assertNotIn(OLD, listing)
        self.assertNotIn(OLD, paths)

    def test_both_entries_explain_tradeoffs_and_ai_assistance(self):
        for route in (NEW, CREA):
            with self.subTest(route=route):
                page = (DOCS / route).read_text(encoding="utf-8")
                self.assertIn('id="how-it-works"', page)
                self.assertIn('id="how-i-built-it"', page)
                self.assertIn("Why I built it this way", page)
                self.assertIn("I used AI assistance", page)
