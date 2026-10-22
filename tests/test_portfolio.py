from html.parser import HTMLParser
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit
import unittest
import html
import re

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_REPOS = ["durable-workflow-runtime", "risk-aware-tool-router", "long-context-memory-benchmark", "domain-adapter-arena", "personalized-creative-adaptation", "industrial-anomaly-localization", "multilingual-document-retrieval"]
REQUIRED_IDS = {"home", "skills", "projects", "deep-dives", "applied-work", "interests", "experience", "education", "contact"}

class Markup(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.links=[]; self.meta=[]; self.buttons=[]; self.resources=[]
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if attrs.get("id"): self.ids.append(attrs["id"])
        if tag == "a" and attrs.get("href"): self.links.append(attrs["href"])
        if tag == "meta": self.meta.append((attrs.get("property") or attrs.get("name"), attrs.get("content")))
        if tag in {"link", "script", "img"} and (attrs.get("href") or attrs.get("src")):
            self.resources.append(attrs.get("href") or attrs.get("src"))
        if tag == "button": self.buttons.append(attrs)

class PortfolioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home=(ROOT/"index.html").read_text(encoding="utf-8"); cls.parsed=Markup(); cls.parsed.feed(cls.home)
    def test_required_sections_exist(self):
        self.assertTrue(REQUIRED_IDS <= set(self.parsed.ids), f"missing: {sorted(REQUIRED_IDS-set(self.parsed.ids))}")
    def test_industry_projects_precede_research_and_engineering(self):
        industry=self.home.index('id="applied-work"'); research=self.home.index('id="projects"')
        self.assertLess(self.home.index('id="home"'),industry); self.assertLess(industry,research)
        self.assertIn("Industry Projects",self.home); self.assertIn("Research &amp; Engineering",self.home)
    def test_featured_applied_projects_link_to_verified_repositories(self):
        for repo in ("Laptop-recommendation-system","Schindler-AI-Maintenance-Intelligence-Platform","Banking-Rag-Agent","AI-Physio-Shoulder-CDS","Smart-Cable-Inspection-System-ElSewedy-Defect-Detection","Smart-Cable-Drum-Monitoring-System"):
            self.assertIn(f"https://github.com/Youssef-Al-eng/{repo}",self.parsed.links,repo)
        self.assertGreaterEqual(self.home.count('class="applied-card'),6)
    def test_profile_photo_is_local_and_used_as_navbar_avatar(self):
        self.assertIn('src="assets/profile-photo.jpg?v=portfolio-v3"',self.home)
        self.assertTrue((ROOT/"assets"/"profile-photo.jpg").is_file())
        self.assertRegex(self.home,r'<a class="wordmark"[^>]*>\s*<span class="wordmark-mark"><img[^>]+alt=""')
        self.assertNotIn('class="hero-visual"', self.home)
        self.assertNotRegex(self.home, r'<img[^>]+Portrait of Youssef')
    def test_professional_background_includes_new_roles_without_invented_dates(self):
        self.assertIn("Attijariwafa Bank · RAG Systems &amp; Machine Learning",self.home); self.assertIn("AI Intern",self.home)
        self.assertNotRegex(self.home, r"[\u0600-\u06ff]"); self.assertNotIn("Commercial International Bank",self.home)
        self.assertIn("JUNE–JULY",self.home); self.assertIn("Silicon Valley Education Company",self.home)
        self.assertIn("Part-time",self.home); self.assertIn("Current",self.home)
    def test_motion_is_accessible_and_reduced_on_mobile(self):
        style=(ROOT/"style.css").read_text(encoding="utf-8")
        self.assertIn("prefers-reduced-motion:reduce",style.replace(" ",""))
        self.assertIn("@media (max-width:600px)",style)
        self.assertIn("@media(max-width:760px)",style.replace(" ",""))
        self.assertNotRegex(self.home,r"(?i)skills?[^<]{0,30}\b\d{1,3}%")
    def test_all_seven_research_repositories_are_linked(self):
        links=set(self.parsed.links); missing=[repo for repo in EXPECTED_REPOS if f"https://github.com/Youssef-Al-eng/{repo}" not in links]; self.assertEqual(missing,[])
    def test_homepage_metadata_and_favicon_exist(self):
        meta=dict(self.parsed.meta)
        for name in ("description","og:title","og:description","og:url","theme-color"): self.assertTrue(meta.get(name),f"missing {name}")
        self.assertTrue(any("favicon.svg?v=portfolio-v3" in href for href in self.parsed.resources)); self.assertIn('rel="canonical"',self.home)
        self.assertIn('href="style.css?v=portfolio-v3"',self.home); self.assertIn('src="nav.js?v=portfolio-v3"',self.home)
    def test_published_sources_contain_no_local_absolute_paths(self):
        for path in [*ROOT.glob("*.html"),*ROOT.glob("*.css"),*ROOT.glob("*.js")]: self.assertNotRegex(path.read_text(encoding="utf-8"),r"[A-Z]:\\|/Users/|/home/")
    def test_navigation_and_project_filters_have_accessible_defaults(self):
        self.assertTrue(any(b.get("aria-expanded")=="false" and b.get("aria-controls")=="site-nav" for b in self.parsed.buttons)); self.assertTrue(any(b.get("data-filter")=="all" for b in self.parsed.buttons)); self.assertGreaterEqual(self.home.count('class="project-card'),7)
    def test_legacy_routes_point_to_matching_sections(self):
        targets={"about.html":"skills","projects.html":"projects","research.html":"deep-dives","experience.html":"experience","education.html":"education","contact.html":"contact"}
        for filename,target in targets.items(): self.assertIn(f"index.html#{target}",(ROOT/filename).read_text(encoding="utf-8"))
    def test_not_found_page_has_recovery_links(self):
        page=Markup(); page.feed((ROOT/"404.html").read_text(encoding="utf-8")); self.assertIn("index.html",page.links); self.assertIn("index.html#projects",page.links)

    def test_homepage_ids_and_internal_anchors_are_valid(self):
        duplicates=[item for item,count in Counter(self.parsed.ids).items() if count > 1]
        self.assertEqual(duplicates, [], f"duplicate IDs: {duplicates}")
        for href in self.parsed.links:
            parts=urlsplit(href)
            if parts.scheme or parts.netloc or not parts.fragment: continue
            self.assertIn(parts.fragment, self.parsed.ids, f"broken anchor: {href}")

    def test_local_assets_exist_and_obsolete_section_reference_is_gone(self):
        for reference in self.parsed.resources:
            parts=urlsplit(reference)
            if parts.scheme or parts.netloc: continue
            self.assertTrue((ROOT/parts.path).is_file(), f"missing local asset: {reference}")
        source_files=[*ROOT.glob("*.html"),*ROOT.glob("*.css"),*ROOT.glob("*.js")]
        source="\n".join(path.read_text(encoding="utf-8") for path in source_files)
        self.assertNotIn('id="expertise"', source)
        self.assertNotIn('href="#expertise"', source)
        self.assertNotIn('index.html#expertise', source)

    def test_local_links_and_fragments_resolve_on_every_html_page(self):
        for page_path in ROOT.glob("*.html"):
            page=Markup(); page.feed(page_path.read_text(encoding="utf-8"))
            for href in page.links:
                parts=urlsplit(href)
                if parts.scheme or parts.netloc: continue
                target=(page_path.parent/parts.path) if parts.path else page_path
                self.assertTrue(target.is_file(), f"{page_path.name} has a broken link: {href}")
                if parts.fragment:
                    target_markup=Markup(); target_markup.feed(target.read_text(encoding="utf-8"))
                    self.assertIn(parts.fragment, target_markup.ids, f"{page_path.name} has a broken fragment: {href}")

    def test_visible_html_copy_contains_no_arabic_script(self):
        for page_path in ROOT.glob("*.html"):
            decoded=html.unescape(page_path.read_text(encoding="utf-8"))
            self.assertNotRegex(decoded, r"[\u0600-\u06ff]", page_path.name)

    def test_primary_and_muted_text_palette_meets_wcag_aa_on_white(self):
        style=(ROOT/"style.css").read_text(encoding="utf-8")
        colors=dict(re.findall(r"--(ink|muted|teal):#([0-9a-fA-F]{6})", style))
        self.assertEqual(set(colors), {"ink", "muted", "teal"})

        def luminance(color):
            channels=[int(color[index:index+2],16)/255 for index in (0,2,4)]
            linear=[channel/12.92 if channel<=0.04045 else ((channel+0.055)/1.055)**2.4 for channel in channels]
            return sum(weight*value for weight,value in zip((0.2126,0.7152,0.0722),linear))

        for role,color in colors.items():
            ratio=(1.05)/(luminance(color)+0.05)
            self.assertGreaterEqual(ratio,4.5,f"{role} contrast is {ratio:.2f}:1")

if __name__ == "__main__": unittest.main()
