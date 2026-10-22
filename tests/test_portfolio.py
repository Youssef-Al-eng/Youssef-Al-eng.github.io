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
    def test_industry_projects_precede_research_and_engineering(self):
        industry=self.home.index('id="applied-work"'); research=self.home.index('id="projects"')
        self.assertLess(self.home.index('id="home"'),industry); self.assertLess(industry,research)
        self.assertIn("Industry Projects",self.home); self.assertIn("Research &amp; Engineering",self.home)
    def test_featured_applied_projects_link_to_verified_repositories(self):
        for repo in ("Laptop-recommendation-system","Schindler-AI-Maintenance-Intelligence-Platform","Banking-Rag-Agent","AI-Physio-Shoulder-CDS","Smart-Cable-Inspection-System-ElSewedy-Defect-Detection","Smart-Cable-Drum-Monitoring-System"):
            self.assertIn(f"https://github.com/Youssef-Al-eng/{repo}",self.parsed.links,repo)
        self.assertGreaterEqual(self.home.count('class="applied-card'),6)
    def test_profile_photo_is_local_and_descriptive(self):
        self.assertIn('src="assets/profile-photo.jpg?v=portfolio-v2"',self.home)
        self.assertTrue((ROOT/"assets"/"profile-photo.jpg").is_file())
        self.assertRegex(self.home,r'<img[^>]+alt="Portrait of Youssef Alaa Abdelrady"')
    def test_professional_background_includes_new_roles_without_invented_dates(self):
        self.assertIn("Attijariwafa Bank",self.home); self.assertIn("AI Intern",self.home)
        self.assertIn("&#1575;&#1604;&#1578;&#1580;&#1575;&#1585;&#1610; &#1608;&#1601;&#1575; &#1576;&#1606;&#1603;",self.home); self.assertNotIn("Commercial International Bank",self.home)
        self.assertIn("JUNE&ndash;JULY",self.home); self.assertIn("Silicon Valley Education Company",self.home)
        self.assertIn("Part-time",self.home); self.assertIn("Current",self.home)
    def test_motion_is_accessible_and_reduced_on_mobile(self):
        style=(ROOT/"style.css").read_text(encoding="utf-8")
        self.assertIn("prefers-reduced-motion:reduce",style.replace(" ",""))
        self.assertIn("@media (max-width:600px)",style)
        self.assertNotRegex(self.home,r"(?i)skills?[^<]{0,30}\b\d{1,3}%")
    def test_all_seven_research_repositories_are_linked(self):
        links=set(self.parsed.links); missing=[repo for repo in EXPECTED_REPOS if f"https://github.com/Youssef-Al-eng/{repo}" not in links]; self.assertEqual(missing,[])
    def test_homepage_metadata_and_favicon_exist(self):
        meta=dict(self.parsed.meta)
        for name in ("description","og:title","og:description","og:url","theme-color"): self.assertTrue(meta.get(name),f"missing {name}")
        self.assertTrue(any("favicon.svg?v=portfolio-v2" in href for href in self.parsed.resources)); self.assertIn('rel="canonical"',self.home)
        self.assertIn('href="style.css?v=portfolio-v2"',self.home); self.assertIn('src="nav.js?v=portfolio-v2"',self.home)
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
