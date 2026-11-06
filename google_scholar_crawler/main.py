#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Refresh the citation data shown on the homepage.

The legacy job imports scholarly before creating results/. Its unbounded
bibtexparser dependency can install the incompatible version 2 API and fail
at import time. Free-proxy discovery and cloud IP blocking are additional
failure points. See docs/CITATION-DATA-FIX.md for verified evidence.

This version:

* talks to Google Scholar directly (optionally through a proxy you provide),
* falls back to the OpenAlex API when Scholar cannot be reached (configure
  OPENALEX_API_KEY to avoid the shared anonymous quota),
* keeps the exact JSON schema the site consumes (``_data/gs_data.json``),
* rewrites the files only when data actually changed, so the daily cron
  does not create empty commits,
* exits non-zero (instead of silently doing nothing) when no source worked.

Environment variables
---------------------
GOOGLE_SCHOLAR_ID            Scholar profile id          (default: 40KXmRMAAAAJ)
GOOGLE_SCHOLAR_PROXY         optional proxy, e.g. http://user:pass@host:port
ORCID_ID                     ORCID for the OpenAlex fallback
CITATION_OPENALEX_FALLBACK   "true" (default) / "false"
SCHOLAR_TIMEOUT              seconds to wait for Scholar (default: 180)
OPENALEX_API_KEY             optional OpenAlex API key (recommended for Actions)
"""

from __future__ import annotations

import argparse
import copy
import json
import math
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

DEFAULT_SCHOLAR_ID = "40KXmRMAAAAJ"
DEFAULT_ORCID = "0000-0002-7150-5239"
OPENALEX = "https://api.openalex.org"
MAILTO = "jiarong.chen@sjtu.edu.cn"
TZ = timezone(timedelta(hours=8))

SOURCES = ("auto", "scholar", "openalex")


# --------------------------------------------------------------------------- #
# small helpers
# --------------------------------------------------------------------------- #
def now() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")


def log(message: str, level: str = "info") -> None:
    prefix = {"info": "", "warn": "WARNING: ", "error": "ERROR: "}.get(level, "")
    print(f"[{now()}] {prefix}{redact(message)}", flush=True)


def redact(message: str) -> str:
    for name in ("GOOGLE_SCHOLAR_PROXY", "OPENALEX_API_KEY"):
        secret = (os.environ.get(name) or "").strip()
        if secret:
            message = message.replace(secret, "[REDACTED]")
            message = message.replace(urllib.parse.quote(secret, safe=""), "[REDACTED]")
    return re.sub(r"(https?://)[^/\s@]+@", r"\1[REDACTED]@", message)


def load_json(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return data if isinstance(data, dict) else {}
    except FileNotFoundError:
        return {}
    except (OSError, ValueError) as exc:
        log(f"cannot read {path} ({exc}); starting from scratch", "warn")
        return {}


def write_json(path: str, data: dict) -> None:
    directory = os.path.dirname(os.path.abspath(path)) or "."
    os.makedirs(directory, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=directory, prefix=".gs-data-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        os.replace(tmp, path)  # atomic: never leave a half-written file behind
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def norm_title(title) -> str:
    text = str(title or "").lower()
    for dash in ("\u2010", "\u2011", "\u2013", "\u2014", "\u2212"):
        text = text.replace(dash, "-")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


# --------------------------------------------------------------------------- #
# source 1: Google Scholar
# --------------------------------------------------------------------------- #
def fetch_scholar(scholar_id: str, timeout: float) -> dict:
    """Bound the entire operation, including imports and proxy setup, on Windows too.

    scholarly retries some 403/captcha responses indefinitely and can catch
    TimeoutError itself. A signal around search_author_id cannot stop that.
    """
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("SCHOLAR_TIMEOUT must be a positive finite number")
    with tempfile.TemporaryDirectory(prefix="scholar-") as directory:
        output = os.path.join(directory, "author.json")
        try:
            result = subprocess.run(
                [sys.executable, os.path.abspath(__file__), "--scholar-worker", scholar_id, output],
                capture_output=True, text=True, encoding="utf-8", errors="replace",
                timeout=timeout,
            )
        except subprocess.TimeoutExpired as exc:
            raise TimeoutError(f"Google Scholar exceeded {timeout:g}s; worker stopped") from exc
        if result.returncode:
            detail = result.stdout.strip() or result.stderr.strip() or "worker failed"
            raise RuntimeError(redact(detail[-2000:]))
        return load_json(output)


def scholar_worker(scholar_id: str) -> dict:
    from scholarly import ProxyGenerator, scholarly

    scholarly.set_timeout(20)
    scholarly.set_retries(2)
    proxy = (os.environ.get("GOOGLE_SCHOLAR_PROXY") or "").strip()
    if proxy:
        generator = ProxyGenerator()
        if not generator.SingleProxy(http=proxy, https=proxy):
            raise RuntimeError("GOOGLE_SCHOLAR_PROXY is not a usable proxy")
        # With just one argument, scholarly silently calls FreeProxies() for
        # its secondary connection. Both must use the configured proxy.
        scholarly.use_proxy(generator, generator)
        log("using the proxy from GOOGLE_SCHOLAR_PROXY")
    else:
        log("no proxy configured, talking to Google Scholar from this IP")

    author = scholarly.search_author_id(scholar_id)
    scholarly.fill(author, sections=["basics", "indices", "counts", "publications"])

    if not author:
        raise RuntimeError(f"Google Scholar returned nothing for id {scholar_id}")

    publications = author.get("publications") or []
    keyed = {}
    for pub in publications:
        pub_id = pub.get("author_pub_id")
        if pub_id:
            keyed[pub_id] = pub
    author["publications"] = keyed
    return author


def payload_from_scholar(author: dict, scholar_id: str) -> dict:
    data = dict(author)
    data.setdefault("container_type", "Author")
    data["scholar_id"] = data.get("scholar_id") or scholar_id
    data["citation_source"] = "google_scholar"
    data["updated"] = now()
    validate_payload(data, scholar_id)
    return data


def validate_payload(data: dict, scholar_id: str) -> None:
    """Never turn a partial response, login page or schema change into zero citations."""
    if not isinstance(data, dict) or not data.get("name"):
        raise ValueError("citation response is missing the author name")
    if data.get("scholar_id") != scholar_id:
        raise ValueError("citation response belongs to a different Scholar profile")
    for field in ("citedby", "hindex", "i10index"):
        value = data.get(field)
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"citation response has invalid/missing {field}")
    publications = data.get("publications")
    if not isinstance(publications, dict):
        raise ValueError("citation response has no publication dictionary")
    for publication in publications.values():
        if not isinstance(publication, dict):
            raise ValueError("citation response has an invalid publication")
        value = publication.get("num_citations")
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError("publication has invalid/missing num_citations")
    if data["citedby"] > 0 and not publications:
        raise ValueError("nonzero citation total with no publications; refusing partial data")


# --------------------------------------------------------------------------- #
# source 2: OpenAlex (fallback)
# --------------------------------------------------------------------------- #
def http_json(url: str, timeout: float = 30) -> dict:
    headers = {
        "Accept": "application/json",
        "User-Agent": f"citation-crawler/2.1 (mailto:{MAILTO})",
    }
    api_key = (os.environ.get("OPENALEX_API_KEY") or "").strip()
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    request = urllib.request.Request(
        url, headers=headers,
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
            if not isinstance(data, dict) or data.get("error"):
                raise ValueError("OpenAlex returned an invalid/error response")
            return data
        except urllib.error.HTTPError as exc:
            detail = exc.read(4096).decode("utf-8", errors="replace")
            if exc.code in (401, 403, 409, 429):
                hint = "Check OPENALEX_API_KEY in repository Actions secrets and its quota."
            else:
                hint = ""
            retry_after = exc.headers.get("Retry-After", "")
            wait = float(retry_after) if retry_after.isdigit() else 2 ** attempt
            exhausted = any(word in detail.lower() for word in ("budget", "quota", "credits"))
            if (exc.code == 429 or exc.code >= 500) and not exhausted and wait <= 5 and attempt < 2:
                time.sleep(wait)
                continue
            raise RuntimeError(redact(f"OpenAlex HTTP {exc.code}: {detail[:800]} {hint}")) from None
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt == 2:
                raise RuntimeError(f"OpenAlex network request failed: {redact(str(exc))}") from None
            time.sleep(2 ** attempt)


def fetch_openalex(orcid: str) -> tuple[dict, list]:
    author = http_json(f"{OPENALEX}/authors/orcid:{urllib.parse.quote(orcid)}?mailto={MAILTO}")
    author_id = str(author.get("id") or "").rsplit("/", 1)[-1]
    if not re.fullmatch(r"A\d+", author_id):
        raise ValueError("OpenAlex author response is missing its ID")
    if str(author.get("orcid") or "").rstrip("/").rsplit("/", 1)[-1] != orcid:
        raise ValueError("OpenAlex returned a different ORCID")

    works: list = []
    # Basic paging works without a key, and 100 is the supported page size.
    # Use the resolved author's ID so the totals and publication set agree.
    for page_number in range(1, 101):
        query = urllib.parse.urlencode({
            "filter": f"authorships.author.id:{author_id}",
            "per_page": 100, "page": page_number,
            "select": "id,doi,title,publication_year,cited_by_count", "mailto": MAILTO,
        })
        url = f"{OPENALEX}/works?{query}"
        page = http_json(url)
        results = page.get("results")
        count = (page.get("meta") or {}).get("count")
        if not isinstance(results, list) or not isinstance(count, int) or count < 0:
            raise ValueError("OpenAlex works response is missing results/meta.count")
        for work in results:
            if not isinstance(work, dict):
                raise ValueError("OpenAlex returned an invalid work")
            citations = work.get("cited_by_count")
            if isinstance(citations, bool) or not isinstance(citations, int) or citations < 0:
                raise ValueError("OpenAlex work has invalid/missing cited_by_count")
        works.extend(results)
        if len(works) >= count:
            return author, works
        if not results:
            raise ValueError("OpenAlex returned an incomplete publication list")
    raise ValueError("OpenAlex publication list exceeds the basic paging limit")


def merge_publication_counts(publications: dict, works: list) -> dict:
    """Refresh per-paper citation counts, keeping the Scholar publication ids."""
    publications = copy.deepcopy(publications)
    if not publications:
        merged = {}
        for work in works:
            work_id = work.get("id") or work.get("doi")
            if not work_id:
                continue
            merged[work_id] = {
                "container_type": "Publication",
                "source": "OPENALEX",
                "bib": {
                    "title": work.get("title") or "",
                    "pub_year": str(work.get("publication_year") or ""),
                },
                "author_pub_id": work_id,
                "num_citations": int(work.get("cited_by_count") or 0),
                "num_citations_source": "openalex",
            }
        return merged

    by_title = {}
    for work in works:
        key = norm_title(work.get("title"))
        if key:
            by_title.setdefault(key, work)

    matched = 0
    for publication in publications.values():
        publication.setdefault("num_citations_source", "google_scholar")
        key = norm_title((publication.get("bib") or {}).get("title"))
        work = by_title.get(key)
        if work is None:
            continue
        publication["num_citations"] = int(work.get("cited_by_count") or 0)
        publication["num_citations_source"] = "openalex"
        matched += 1
    log(f"OpenAlex matched {matched}/{len(publications)} publications by title")
    return publications


def payload_from_openalex(
    author: dict, works: list, previous: dict, scholar_id: str, orcid: str
) -> dict:
    stats = author.get("summary_stats") or {}
    data = {
        "container_type": "Author",
        "source": "OPENALEX",
        "citation_source": "openalex",
        "filled": ["basics", "publications", "indices", "counts"],
        "scholar_id": scholar_id,
        "orcid": orcid,
        "name": author.get("display_name") or previous.get("name") or "Jiarong Chen",
        "affiliation": previous.get("affiliation") or "",
        "homepage": previous.get("homepage") or "",
        "interests": previous.get("interests") or [],
        "citedby": author.get("cited_by_count"),
        "hindex": stats.get("h_index"),
        "i10index": stats.get("i10_index"),
        "works_count": int(author.get("works_count") or 0),
        "publications": merge_publication_counts(
            dict(previous.get("publications") or {}), works
        ),
        "updated": now(),
    }
    validate_payload(data, scholar_id)
    return data


# --------------------------------------------------------------------------- #
# change detection
# --------------------------------------------------------------------------- #
def same_numbers(new: dict, old: dict) -> bool:
    """True when nothing worth a commit changed (timestamps are ignored)."""
    # Publication metadata, source, and identity changes must be persisted too.
    return bool(old) and {k: v for k, v in new.items() if k != "updated"} == {
        k: v for k, v in old.items() if k != "updated"
    }


# --------------------------------------------------------------------------- #
# entry point
# --------------------------------------------------------------------------- #
def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Refresh citation data for the homepage")
    parser.add_argument(
        "--source",
        choices=SOURCES,
        default=os.environ.get("CITATION_SOURCE", "auto"),
        help="auto = Scholar first, OpenAlex as fallback",
    )
    parser.add_argument("--out", default="_data", help="output directory (default: _data)")
    parser.add_argument(
        "--scholar-id",
        default=(os.environ.get("GOOGLE_SCHOLAR_ID") or DEFAULT_SCHOLAR_ID).strip(),
    )
    parser.add_argument(
        "--orcid", default=(os.environ.get("ORCID_ID") or DEFAULT_ORCID).strip()
    )
    parser.add_argument(
        "--force", action="store_true", help="rewrite files even when nothing changed"
    )
    args = parser.parse_args(argv)

    data_path = os.path.join(args.out, "gs_data.json")
    badge_path = os.path.join(args.out, "gs_data_shieldsio.json")

    previous = load_json(data_path)
    log(
        "previous snapshot: "
        f"citedby={previous.get('citedby')} "
        f"source={previous.get('citation_source') or previous.get('source')} "
        f"updated={previous.get('updated')}"
    )

    allow_fallback = os.environ.get("CITATION_OPENALEX_FALLBACK", "true").strip().lower() not in {
        "0",
        "false",
        "no",
        "off",
    }
    try:
        scholar_timeout = float(os.environ.get("SCHOLAR_TIMEOUT", "180"))
        if not math.isfinite(scholar_timeout) or scholar_timeout <= 0:
            raise ValueError
    except ValueError:
        log("SCHOLAR_TIMEOUT must be a positive finite number", "error")
        return 1

    # Never apply another researcher's counts to publication IDs in an old file.
    if previous.get("scholar_id") != args.scholar_id or (
        previous.get("orcid") and previous["orcid"] != args.orcid
    ):
        previous = {}

    errors: list[str] = []
    payload = None

    if args.source in ("auto", "scholar"):
        log("source 1/2: Google Scholar")
        try:
            author = fetch_scholar(args.scholar_id, scholar_timeout)
            payload = payload_from_scholar(author, args.scholar_id)
            log(f"Google Scholar OK: citedby={payload.get('citedby')}")
        except Exception as exc:  # noqa: BLE001 - any failure means "try the next source"
            errors.append(f"google scholar: {exc}")
            log(f"Google Scholar failed: {exc}", "warn")

    if payload is None and args.source in ("auto", "openalex"):
        if args.source == "auto" and not allow_fallback:
            log("OpenAlex fallback is disabled (CITATION_OPENALEX_FALLBACK=false)", "warn")
        else:
            log("source 2/2: OpenAlex")
            try:
                author, works = fetch_openalex(args.orcid)
                payload = payload_from_openalex(
                    author, works, previous, args.scholar_id, args.orcid
                )
                log(
                    "OpenAlex OK: "
                    f"citedby={payload.get('citedby')} works={len(works)}"
                )
            except Exception as exc:  # noqa: BLE001
                errors.append(f"openalex: {exc}")
                log(f"OpenAlex failed: {exc}", "error")

    if payload is None:
        log("no citation source worked, leaving the previous snapshot untouched", "error")
        for item in errors:
            log(f"  - {item}", "error")
        return 1

    badge = {"schemaVersion": 1, "label": "citations", "message": str(payload["citedby"])}
    if same_numbers(payload, previous) and load_json(badge_path) == badge and not args.force:
        log(
            "citation numbers unchanged since "
            f"{previous.get('updated')}, nothing written"
        )
        return 0

    write_json(data_path, payload)
    write_json(
        badge_path,
        badge,
    )
    log(
        f"wrote {data_path} and {badge_path} "
        f"(citedby={payload['citedby']}, source={payload.get('citation_source')})"
    )
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "--scholar-worker":
        try:
            write_json(sys.argv[3], scholar_worker(sys.argv[2]))
        except Exception as exc:
            log(f"{type(exc).__name__}: {exc}", "error")
            sys.exit(1)
        sys.exit(0)
    sys.exit(main())
