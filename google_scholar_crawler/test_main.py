"""Offline regressions for failures that previously stopped citation refreshes.

Run: python -m unittest discover -s google_scholar_crawler -p 'test_*.py' -v
"""
import copy
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch
import urllib.error
import urllib.parse

import main as crawler


ID = crawler.DEFAULT_SCHOLAR_ID
ORCID = crawler.DEFAULT_ORCID
PUB_ID = f"{ID}:paper"


def snapshot():
    return {
        "container_type": "Author", "scholar_id": ID, "name": "Test Author",
        "citation_source": "google_scholar", "citedby": 10, "hindex": 2,
        "i10index": 1, "updated": "2026-09-07 00:00:00",
        "publications": {PUB_ID: {
            "bib": {"title": "A Test Paper"}, "num_citations": 1,
        }},
    }


def oa_author():
    return {
        "id": "https://openalex.org/A123", "orcid": f"https://orcid.org/{ORCID}",
        "display_name": "Test Author", "cited_by_count": 10, "works_count": 1,
        "summary_stats": {"h_index": 2, "i10_index": 1},
    }


def work(count=2):
    return {"id": "https://openalex.org/W1", "title": "A Test Paper", "cited_by_count": count}


class CitationTests(unittest.TestCase):
    def setUp(self):
        # Keep test writes inside the project, including under restricted
        # Windows runners where creating files in the system Temp is denied.
        test_root = Path(__file__).resolve().parents[1] / ".citation-check"
        test_root.mkdir(exist_ok=True)
        self.directory = tempfile.TemporaryDirectory(dir=test_root)
        self.addCleanup(self.directory.cleanup)
        self.output = Path(self.directory.name)
        self.tempdir = patch.object(tempfile, "tempdir", str(self.output))
        self.tempdir.start()
        self.addCleanup(self.tempdir.stop)
        self.data_path = self.output / "gs_data.json"
        self.badge_path = self.output / "gs_data_shieldsio.json"
        self.env = patch.dict(os.environ, {
            "SCHOLAR_TIMEOUT": "20", "CITATION_OPENALEX_FALLBACK": "true",
            "GOOGLE_SCHOLAR_ID": ID, "ORCID_ID": ORCID,
            "OPENALEX_API_KEY": "", "GOOGLE_SCHOLAR_PROXY": "",
        })
        self.env.start()
        self.addCleanup(self.env.stop)

    def seed(self, data=None):
        crawler.write_json(str(self.data_path), data or snapshot())
        crawler.write_json(str(self.badge_path), {"schemaVersion": 1, "label": "citations", "message": "10"})

    def run_crawler(self, source="auto"):
        return crawler.main(["--source", source, "--out", str(self.output)])

    def test_clean_install_can_import_scholarly_and_legacy_bibtex_api(self):
        # Reproduces the actual clean-install failure with bibtexparser 2.x.
        from scholarly import scholarly
        from bibtexparser.bibdatabase import BibDatabase
        self.assertTrue(callable(scholarly.search_author_id))
        self.assertTrue(callable(BibDatabase))

    def test_both_sources_fail_preserves_both_files_byte_for_byte(self):
        self.seed()
        before = [p.read_bytes() for p in (self.data_path, self.badge_path)]
        with patch.object(crawler, "fetch_scholar", side_effect=RuntimeError("blocked")), patch.object(
            crawler, "fetch_openalex", side_effect=RuntimeError("quota exhausted")
        ):
            self.assertEqual(self.run_crawler(), 1)
        self.assertEqual(before, [p.read_bytes() for p in (self.data_path, self.badge_path)])

    def test_partial_scholar_response_does_not_overwrite_with_zero(self):
        self.seed()
        invalid = snapshot()
        del invalid["citedby"]
        before = self.data_path.read_bytes()
        with patch.object(crawler, "fetch_scholar", return_value=invalid):
            self.assertEqual(self.run_crawler("scholar"), 1)
        self.assertEqual(self.data_path.read_bytes(), before)

    def test_invalid_counts_are_rejected(self):
        for value in (None, True, -1, "12", 1.2):
            with self.subTest(value=value):
                invalid = snapshot()
                invalid["citedby"] = value
                with self.assertRaises(ValueError):
                    crawler.payload_from_scholar(invalid, ID)

    def test_wrong_profile_is_rejected(self):
        invalid = snapshot()
        invalid["scholar_id"] = "someone-else"
        with self.assertRaisesRegex(ValueError, "different Scholar profile"):
            crawler.payload_from_scholar(invalid, ID)

    def test_disabled_fallback_does_not_call_openalex(self):
        with patch.dict(os.environ, {"CITATION_OPENALEX_FALLBACK": "false"}), patch.object(
            crawler, "fetch_scholar", side_effect=RuntimeError("blocked")
        ), patch.object(crawler, "fetch_openalex") as fallback:
            self.assertEqual(self.run_crawler(), 1)
            fallback.assert_not_called()

    def test_explicit_scholar_never_switches_to_openalex(self):
        with patch.object(crawler, "fetch_scholar", side_effect=RuntimeError("blocked")), patch.object(
            crawler, "fetch_openalex"
        ) as fallback:
            self.assertEqual(self.run_crawler("scholar"), 1)
            fallback.assert_not_called()

    def test_auto_falls_back_and_records_the_actual_source(self):
        self.seed()
        with patch.object(crawler, "fetch_scholar", side_effect=TimeoutError("blocked")), patch.object(
            crawler, "fetch_openalex", return_value=(oa_author(), [work()])
        ):
            self.assertEqual(self.run_crawler(), 0)
        result = crawler.load_json(str(self.data_path))
        self.assertEqual(result["citation_source"], "openalex")
        self.assertEqual(result["publications"][PUB_ID]["num_citations"], 2)

    def test_per_paper_change_does_not_mutate_previous_snapshot(self):
        previous = crawler.payload_from_openalex(oa_author(), [work(1)], snapshot(), ID, ORCID)
        original = copy.deepcopy(previous)
        updated = crawler.payload_from_openalex(oa_author(), [work(2)], previous, ID, ORCID)
        self.assertEqual(previous, original)
        self.assertFalse(crawler.same_numbers(updated, previous))

    def test_per_paper_only_change_is_written_even_when_total_is_unchanged(self):
        previous = crawler.payload_from_openalex(oa_author(), [work(1)], snapshot(), ID, ORCID)
        self.seed(previous)
        with patch.object(crawler, "fetch_openalex", return_value=(oa_author(), [work(2)])):
            self.assertEqual(self.run_crawler("openalex"), 0)
        self.assertEqual(crawler.load_json(str(self.data_path))["publications"][PUB_ID]["num_citations"], 2)

    def test_unmatched_papers_keep_their_original_source(self):
        publications = snapshot()["publications"]
        merged = crawler.merge_publication_counts(publications, [])
        self.assertEqual(merged[PUB_ID]["num_citations"], 1)
        self.assertEqual(merged[PUB_ID]["num_citations_source"], "google_scholar")

    def test_changed_metadata_and_source_are_not_ignored(self):
        previous = snapshot()
        updated = copy.deepcopy(previous)
        updated["publications"][PUB_ID]["bib"]["title"] = "Corrected title"
        self.assertFalse(crawler.same_numbers(updated, previous))
        updated = copy.deepcopy(previous)
        updated["citation_source"] = "openalex"
        self.assertFalse(crawler.same_numbers(updated, previous))

    def test_unchanged_snapshot_does_not_create_daily_commits(self):
        self.seed()
        before = self.data_path.read_bytes()
        with patch.object(crawler, "fetch_scholar", return_value=snapshot()):
            self.assertEqual(self.run_crawler("scholar"), 0)
        self.assertEqual(before, self.data_path.read_bytes())

    def test_missing_badge_is_repaired_when_numbers_are_unchanged(self):
        self.seed()
        self.badge_path.unlink()
        with patch.object(crawler, "fetch_scholar", return_value=snapshot()):
            self.assertEqual(self.run_crawler("scholar"), 0)
        self.assertEqual(crawler.load_json(str(self.badge_path))["message"], "10")

    def test_proxy_is_used_for_both_scholarly_connections(self):
        fake = Mock()
        author = snapshot()
        author["publications"] = [{"author_pub_id": PUB_ID, "num_citations": 1}]
        fake.search_author_id.return_value = author
        generator = Mock()
        module = SimpleNamespace(scholarly=fake, ProxyGenerator=Mock(return_value=generator))
        with patch.dict(sys.modules, {"scholarly": module}), patch.dict(
            os.environ, {"GOOGLE_SCHOLAR_PROXY": "http://proxy.invalid:8080"}
        ):
            result = crawler.scholar_worker(ID)
        fake.use_proxy.assert_called_once_with(generator, generator)
        self.assertIn(PUB_ID, result["publications"])
        self.assertEqual(fake.fill.call_args.kwargs["sections"], ["basics", "indices", "counts", "publications"])

    def test_timeout_stops_a_real_blocking_subprocess(self):
        original_run = subprocess.run

        def blocked_worker(command, **kwargs):
            return original_run([sys.executable, "-c", "import time; time.sleep(60)"], **kwargs)

        start = time.monotonic()
        with patch.object(crawler.subprocess, "run", side_effect=blocked_worker):
            with self.assertRaisesRegex(TimeoutError, "worker stopped"):
                crawler.fetch_scholar(ID, 0.25)
        self.assertLess(time.monotonic() - start, 5)

    def test_invalid_timeout_fails_before_fetching(self):
        for timeout in ("nan", "inf", "0", "-2", "not-a-number"):
            with self.subTest(timeout=timeout), patch.dict(os.environ, {"SCHOLAR_TIMEOUT": timeout}), patch.object(
                crawler, "fetch_scholar"
            ) as fetch:
                self.assertEqual(self.run_crawler(), 1)
                fetch.assert_not_called()

    def test_openalex_uses_bearer_auth(self):
        response = io.BytesIO(b'{"id": "test"}')
        with patch.dict(os.environ, {"OPENALEX_API_KEY": "test-secret"}), patch.object(
            crawler.urllib.request, "urlopen", return_value=response
        ) as request:
            self.assertEqual(crawler.http_json("https://api.openalex.org/authors/A123"), {"id": "test"})
        self.assertEqual(request.call_args.args[0].get_header("Authorization"), "Bearer test-secret")
        self.assertNotIn("test-secret", request.call_args.args[0].full_url)

    def test_openalex_budget_error_is_actionable_and_does_not_wait_until_tomorrow(self):
        error = urllib.error.HTTPError("https://api.openalex.org/works", 429, "Too Many Requests",
                                       {"Retry-After": "36000"}, io.BytesIO(b'{"message": "budget exhausted"}'))
        with patch.object(crawler.urllib.request, "urlopen", side_effect=error), patch.object(
            crawler.time, "sleep"
        ) as sleep:
            with self.assertRaisesRegex(RuntimeError, "OPENALEX_API_KEY"):
                crawler.http_json("https://api.openalex.org/works")
            sleep.assert_not_called()

    def test_openalex_retries_transient_server_errors(self):
        error = urllib.error.HTTPError("https://api.openalex.org/works", 503, "Unavailable", {}, io.BytesIO(b'busy'))
        with patch.object(crawler.urllib.request, "urlopen", side_effect=[error, io.BytesIO(b'{"ok": true}')]), patch.object(
            crawler.time, "sleep"
        ):
            self.assertEqual(crawler.http_json("https://api.openalex.org/works"), {"ok": True})

    def test_openalex_paginates_by_author_id_without_cursor(self):
        pages = [oa_author(), {"meta": {"count": 3}, "results": [work(), work()]},
                 {"meta": {"count": 3}, "results": [work()]}]
        with patch.object(crawler, "http_json", side_effect=pages) as request:
            author, works = crawler.fetch_openalex(ORCID)
        self.assertEqual(len(works), 3)
        query = urllib.parse.parse_qs(urllib.parse.urlsplit(request.call_args.args[0]).query)
        self.assertEqual(query["filter"], ["authorships.author.id:A123"])
        self.assertEqual(query["per_page"], ["100"])
        self.assertEqual(query["page"], ["2"])
        self.assertNotIn("cursor", query)

    def test_openalex_rejects_incomplete_results_and_wrong_orcid(self):
        for response in ({"error": "budget exhausted"}, {"meta": {"count": 1}, "results": []}):
            with patch.object(crawler, "http_json", side_effect=[oa_author(), response]):
                with self.assertRaises(ValueError):
                    crawler.fetch_openalex(ORCID)
        author = oa_author()
        author["orcid"] = "https://orcid.org/someone-else"
        with patch.object(crawler, "http_json", return_value=author):
            with self.assertRaisesRegex(ValueError, "different ORCID"):
                crawler.fetch_openalex(ORCID)

    def test_secrets_are_removed_from_error_messages(self):
        proxy = "http://person:password@proxy.invalid:8080"
        with patch.dict(os.environ, {"GOOGLE_SCHOLAR_PROXY": proxy, "OPENALEX_API_KEY": "test-secret"}):
            result = crawler.redact(f"failed {proxy} api_key=test-secret")
        self.assertNotIn("password", result)
        self.assertNotIn("test-secret", result)


if __name__ == "__main__":
    unittest.main()
