import tempfile
import unittest
from pathlib import Path
from engine.vault import bootstrap, PROJECTS
class VaultTests(unittest.TestCase):
    def test_bootstrap_and_preserve(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp)
            root=bootstrap(base/"vault",base/"code")
            home=root/"00_Dashboard"/"Home.md"
            self.assertEqual(home.read_text(encoding="utf-8").count("[["),6)
            for i,p in enumerate(PROJECTS,1):
                self.assertTrue((root/f"{i:02}_{p}"/"Index.md").is_file())
            home.write_text("user edit")
            bootstrap(root,base/"code")
            self.assertEqual(home.read_text(),"user edit")
    def test_checkout_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp)
            for root in (base,base/"code",base/"code"/"vault"):
                with self.assertRaises(ValueError):
                    bootstrap(root,base/"code")
    def test_git_ancestor_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp)
            (base/"repo"/".git").mkdir(parents=True)
            with self.assertRaises(ValueError):
                bootstrap(base/"repo"/"vault",base/"code")
