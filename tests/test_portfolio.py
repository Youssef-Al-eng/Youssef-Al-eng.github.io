from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_REPOS = ["durable-workflow-runtime", "risk-aware-tool-router", "long-context-memory-benchmark", "domain-adapter-arena", "personalized-creative-adaptation", "industrial-anomaly-localization", "multilingual-document-retrieval"]
REQUIRED_IDS = {"home", "expertise", "projects", "deep-dives", "applied-work", "interests", "experience", "education", "contact"}

class Markup(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=set(); self.links=[]; self.meta=[]; self.buttons=[]; self.resources=[]
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if attrs.get("id"): self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("href"): self.links.append(attrs["href"])
        if tag == "meta": self.meta.append((attrs.get("property") or attrs.get("name"), attrs.get("content")))
        if tag == "link" and attrs.get("href"): self.resources.append(attrs["href"])
        if tag == "button": self.buttons.append(attrs)

class PortfolioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home=(ROOT/"index.html").read_text(encoding="utf-8"); cls.parsed=Markup(); cls.parsed.feed(cls.home)
    def test_required_sections_exist(self):
        self.assertTrue(REQUIRED_IDS <= self.parsed.ids, f"missing: {sorted(REQUIRED_IDS-self.parsed.ids)}")
    def test_all_seven_research_repositories_are_linked(self):
        links=set(self.parsed.links); missing=[repo for repo in EXPECTED_REPOS if f"https://github.com/Youssef-Al-eng/{repo}" not in links]; self.assertEqual(missing,[])
    def test_homepage_metadata_and_favicon_exist(self):
        meta=dict(self.parsed.meta)
        for name in ("description","og:title","og:description","og:url","theme-color"): self.assertTrue(meta.get(name),f"missing {name}")
        self.assertTrue(any("favicon.svg" in href for href in self.parsed.resources)); self.assertIn('rel="canonical"',self.home)
    def test_published_sources_contain_no_local_absolute_paths(self):
        for path in [*ROOT.glob("*.html"),*ROOT.glob("*.css"),*ROOT.glob("*.js")]: self.assertNotRegex(path.read_text(encoding="utf-8"),r"[A-Z]:\\|/Users/|/home/")
    def test_navigation_and_project_filters_have_accessible_defaults(self):
        self.assertTrue(any(b.get("aria-expanded")=="false" and b.get("aria-controls")=="site-nav" for b in self.parsed.buttons)); self.assertTrue(any(b.get("data-filter")=="all" for b in self.parsed.buttons)); self.assertGreaterEqual(self.home.count('class="project-card'),7)
    def test_legacy_routes_point_to_matching_sections(self):
        targets={"about.html":"expertise","projects.html":"projects","research.html":"deep-dives","experience.html":"experience","education.html":"education","contact.html":"contact"}
        for filename,target in targets.items(): self.assertIn(f"index.html#{target}",(ROOT/filename).read_text(encoding="utf-8"))
    def test_not_found_page_has_recovery_links(self):
        page=Markup(); page.feed((ROOT/"404.html").read_text(encoding="utf-8")); self.assertIn("index.html",page.links); self.assertIn("index.html#projects",page.links)

if __name__ == "__main__": unittest.main()
