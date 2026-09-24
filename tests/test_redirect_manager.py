import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from redirect_manager.cli import main
from redirect_manager.core import RedirectRule, export_rules, load_rules, resolve_chain, validate_rules

class RedirectManagerTests(unittest.TestCase):
    def test_valid_chain_and_resolve(self):
        rules = [RedirectRule("/a", "/b", 301), RedirectRule("/b", "/c", 308)]
        self.assertTrue(validate_rules(rules).ok)
        self.assertEqual(resolve_chain(rules, "/a"), ["/a", "/b", "/c"])

    def test_cycle_is_detected_once(self):
        report = validate_rules([RedirectRule("/a", "/b"), RedirectRule("/b", "/a")])
        self.assertFalse(report.ok)
        self.assertEqual(sum(f.code == "redirect-cycle" for f in report.findings), 1)

    def test_conflict_and_status(self):
        report = validate_rules([RedirectRule("/a", "/b", 200), RedirectRule("/a", "/c")])
        codes = {f.code for f in report.findings}
        self.assertIn("invalid-status", codes); self.assertIn("conflicting-source", codes)

    def test_export_formats(self):
        rules = [RedirectRule("/old", "/new", 301)]
        self.assertEqual(export_rules(rules, "netlify"), "/old /new 301\n")
        self.assertIn("Redirect 301 /old /new", export_rules(rules, "apache"))
        self.assertIn("return 301 /new", export_rules(rules, "nginx"))

    def test_load_csv_and_unicode_json(self):
        with tempfile.TemporaryDirectory() as d:
            csv_path = Path(d) / "r.csv"
            csv_path.write_text("source,target,status\n/old,/new,301\n", encoding="utf-8")
            self.assertEqual(load_rules(csv_path)[0].target, "/new")
            json_path = Path(d) / "r.json"
            json_path.write_text(json.dumps([{"source":"/قديم","target":"/جديد"}], ensure_ascii=False), encoding="utf-8")
            self.assertEqual(load_rules(json_path)[0].source, "/قديم")

    def test_bad_path_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "r.json"; p.write_text('[{"source":"old","target":"/new"}]')
            with self.assertRaisesRegex(ValueError, "site path"):
                load_rules(p)

    def test_cli_validation_exit_codes(self):
        with tempfile.TemporaryDirectory() as d:
            good = Path(d) / "good.csv"; good.write_text("source,target,status\n/a,/b,301\n")
            bad = Path(d) / "bad.csv"; bad.write_text("source,target,status\n/a,/a,301\n")
            with patch("builtins.print"):
                self.assertEqual(main(["validate", str(good)]), 0)
                self.assertEqual(main(["validate", str(bad)]), 1)

if __name__ == "__main__": unittest.main()
