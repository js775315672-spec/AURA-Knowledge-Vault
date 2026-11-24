import unittest
import json
from pathlib import Path
from engine.contract import validate, PROJECTS
class ContractTests(unittest.TestCase):
    def fixture(self):
        return dict(id="KNOW-DEMO-1", project="QuizNote", status="UNVERIFIED", sha256="a"*64, synthetic=True)
    def test_projects(self):
        for project in PROJECTS:
            self.assertTrue(validate(dict(self.fixture(), project=project)))
    def test_reject(self):
        for change in (dict(status="VERIFIED"), dict(synthetic=False), dict(sha256="bad"), dict(id="../bad"), dict(secret="demo"), dict(project="other")):
            with self.subTest(change=change), self.assertRaises(ValueError):
                validate(dict(self.fixture(), **change))
    def test_registry(self):
        r=json.loads(Path("registry.json").read_text())
        self.assertEqual({s["project"] for s in r["sources"]}, PROJECTS)
        self.assertTrue(all(s["access"]=="read-only" and not s["enabled"] for s in r["sources"]))
        self.assertFalse(r["schedule_enabled"])
        self.assertFalse(r["auto_merge"])
