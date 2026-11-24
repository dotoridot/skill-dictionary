import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class PublishingTest(unittest.TestCase):
    def setUp(self):
        workspace = tempfile.TemporaryDirectory()
        self.addCleanup(workspace.cleanup)
        self.root = Path(workspace.name)
        source = Path(__file__).resolve().parents[1]
        for name in ["skills", "site"]:
            shutil.copytree(source / name, self.root / name)
        shutil.copy(source / "build.py", self.root)
        catalogs = self.root / "catalogs"
        catalogs.mkdir()
        self.catalog = catalogs / "example.json"
        self.data = {
            "id": "first", "title": "예시", "description": "시험용 사전",
            "items": [{"id": "example", "name": "test", "summary": "예시 항목",
                       "category": "작성", "when": "원고 검토", "privateNote": "EDITOR-ONLY"}],
        }

    def build(self):
        self.catalog.write_text(json.dumps(self.data), encoding="utf-8")
        subprocess.run([sys.executable, self.root / "build.py"], check=True)

    def test_public_fields_and_search_index(self):
        self.build()
        index = (self.root / "public/index.html").read_text()
        detail = (self.root / "public/first/index.html").read_text()
        self.assertNotIn("EDITOR-ONLY", detail)
        self.assertNotIn("EDITOR-ONLY", index)
        self.assertIn("원고 검토", index)

    def test_home_groups_collections_and_links_to_each_field(self):
        self.data["field"] = "설계 & 구현"
        second = self.data | {"id": "second", "title": "두 번째"}
        (self.catalog.parent / "second.json").write_text(json.dumps(second))
        self.build()
        page = (self.root / "public/index.html").read_text()
        self.assertEqual(page.count("<h3>설계 &amp; 구현</h3>"), 1)
        self.assertIn('href="#field-1"', page)
        self.assertIn('id="field-1"', page)
        self.assertIn('href="first/index.html"', page)
        self.assertIn('href="second/index.html"', page)

    def test_renamed_dictionary_retires_only_its_generated_page(self):
        self.build()
        public = self.root / "public"
        other = public / "first/notes.txt"
        other.write_text("keep")
        self.data["id"] = "second"
        self.build()
        self.assertTrue((public / "second/index.html").exists())
        self.assertFalse((public / "first/index.html").exists())
        self.assertEqual(other.read_text(), "keep")
