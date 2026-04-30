"""
Outline script: process extracted organization rows into Django Organization objects.

This file is intentionally a scaffold only.
No enrichment, API calls, parsing, or database writes are implemented yet.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

import django
from django.db.models import Q

api_key = os.getenv("OPENAI_API_KEY")

from openai import OpenAI
LLM = OpenAI(api_key=api_key)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cs412.settings")
django.setup()

from project.models import Organization


# -----------------------------------------------------------------------------
# Config / constants (outline only)
# -----------------------------------------------------------------------------
DEFAULT_INPUT_CSV = Path("project/organization_creator/org_counts.csv")
DEFAULT_DRY_RUN_REPORT = Path("project/organization_creator/org_import_plan.json")
COMMON_SUBDOMAIN_PREFIXES = ("www.", "m.")


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------
def parse_args() -> argparse.Namespace:
    """Define command-line interface for the organization creation workflow."""
    parser = argparse.ArgumentParser(
        description="Outline: create Organization objects from aggregated source data."
    )
    parser.add_argument(
        "--input-csv",
        default=str(DEFAULT_INPUT_CSV),
        help="CSV containing extracted organizations and sample URLs.",
    )
    parser.add_argument(
        "--min-count",
        type=int,
        default=5,
        help="Minimum frequency threshold for candidate organizations.",
    )
    parser.add_argument(
        "--dry-run-report",
        default=str(DEFAULT_DRY_RUN_REPORT),
        help="Path for planned actions report (no DB writes in dry run).",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="When implemented, apply writes to DB. For now this is unused.",
    )
    parser.add_argument(
        "--model",
        default="",
        help="When implemented, model name used for owner/description enrichment.",
    )
    return parser.parse_args()


# -----------------------------------------------------------------------------
# Pipeline outline stages (no implementation yet)
# -----------------------------------------------------------------------------
def load_candidates(input_csv: Path, min_count: int):
    """
    Stage 1: Load candidate organizations from CSV.

    - Read org name, count, sample URLs, source_id.
    - Filter rows below min_count.
    - Return normalized candidate records.
    """
    candidates = []

    if not input_csv.exists():
        raise FileNotFoundError(f"Input CSV not found: {input_csv}")

    with input_csv.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = (row.get("organization") or "").strip()
            if not name:
                continue

            try:
                count = int((row.get("count") or "0").strip())
            except ValueError:
                continue

            if count < min_count:
                continue

            sample_urls_raw = (row.get("sample_urls") or "").strip()
            sample_urls = [u.strip() for u in sample_urls_raw.split(";") if u.strip()]

            candidate = {
                "source_name": name,
                "count": count,
                "source_id": (row.get("source_id") or "").strip(),
                "sample_urls": sample_urls,
                "num_unique_urls": int((row.get("num_unique_urls") or "0").strip() or 0),
            }
            candidates.append(candidate)

    candidates.sort(key=lambda c: c["count"], reverse=True)
    return candidates


def normalize_candidate(candidate):
    """
    Stage 2: Normalize organization name + URL/domain.

    - Trim punctuation/casing artifacts from source names.
    - Extract canonical homepage from sample article URLs.
    - Apply alias map for common naming variants.
    """
    source_name = (candidate.get("source_name") or "").strip()
    normalized_name = " ".join(source_name.replace(".com", " .com").split())
    normalized_name_key = normalized_name.casefold().replace(" ", "")

    sample_urls = candidate.get("sample_urls") or []
    primary_url = sample_urls[0] if sample_urls else ""

    parsed = urlparse(primary_url) if primary_url else None
    domain = (parsed.netloc or "").casefold() if parsed else ""
    for prefix in COMMON_SUBDOMAIN_PREFIXES:
        if domain.startswith(prefix):
            domain = domain[len(prefix):]

    if domain.startswith("news.") and domain.count(".") >= 2:
        domain = domain[5:]

    canonical_url = f"https://{domain}/" if domain else ""

    normalized = dict(candidate)
    normalized.update(
        {
            "normalized_name": normalized_name,
            "normalized_name_key": normalized_name_key,
            "primary_url": primary_url,
            "canonical_domain": domain,
            "canonical_url": canonical_url,
        }
    )
    return normalized


def match_existing_organization(candidate):
    """
    Stage 3: Match against existing Organization rows.

    Planned behavior:
    - Try exact name match.
    - Try domain/homepage match.
    - Try alias-based match.
    """
    normalized_name = (candidate.get("normalized_name") or candidate.get("source_name") or "").strip()
    normalized_name_key = (candidate.get("normalized_name_key") or "").strip()
    canonical_domain = (candidate.get("canonical_domain") or "").strip()
    canonical_url = (candidate.get("canonical_url") or "").strip()

    if not normalized_name and not canonical_domain:
        return None

    exact_name_match = Organization.objects.filter(name=normalized_name).first()
    if exact_name_match:
        return {
            "organization": exact_name_match,
            "match_type": "exact_name",
            "matched_value": normalized_name,
        }

    all_name_candidates = Organization.objects.all()
    for organization in all_name_candidates:
        org_name_key = "".join((organization.name or "").casefold().split())
        if normalized_name_key and org_name_key == normalized_name_key:
            return {
                "organization": organization,
                "match_type": "normalized_name",
                "matched_value": normalized_name,
            }

    if canonical_url:
        exact_url_match = Organization.objects.filter(url=canonical_url).first()
        if exact_url_match:
            return {
                "organization": exact_url_match,
                "match_type": "exact_url",
                "matched_value": canonical_url,
            }

    if canonical_domain:
        url_candidates = Organization.objects.filter(
            Q(url__icontains=canonical_domain) | Q(url__icontains=f"www.{canonical_domain}")
        )
        domain_match = url_candidates.first()
        if domain_match:
            return {
                "organization": domain_match,
                "match_type": "domain",
                "matched_value": canonical_domain,
            }

    return None


def enrich_with_llm(candidate):
    """
    Stage 4: Fill owner + description with LLM.

    Sends source name, homepage, and sample URLs to gpt-5.4-mini and returns
    a dict with 'owner' and 'description'. Returns None on failure.
    """
    payload = {
        "organization": candidate.get("normalized_name") or candidate.get("source_name", ""),
        "count": candidate.get("count", 0),
        "sample_urls": (candidate.get("sample_urls") or [])[:3],
        "source_id": candidate.get("source_id", ""),
        "canonical_url": candidate.get("canonical_url", ""),
    }

    prompt = (
        "Return ONLY valid JSON with keys owner and description. "
        "Use the organization evidence below and infer likely ownership and a concise description "
        "(the description should be of the news site itself, not the owner).\n\n"
        f"Evidence: {json.dumps(payload)}"
    )

    try:
        response = LLM.responses.create(
            model="gpt-5.4-mini",
            input=prompt,
        )
        raw_text = response.output_text
        parsed = json.loads(raw_text)
        return {
            "owner": (parsed.get("owner") or "").strip(),
            "owner_confidence": float(parsed.get("owner_confidence") or 0),
            "description": (parsed.get("description") or "").strip(),
        }
    except (json.JSONDecodeError, Exception) as exc:
        print(f"  [enrich] failed for {payload['organization']!r}: {exc}")
        return None


def create_object_from_candidate(candidate, existing_match, enrichment, apply: bool = False):
    """
    Stage 5: Create/update one Organization directly from match + enrichment.

    Behavior:
    - If no match, create a new Organization.
    - If matched, only fill empty fields (owner/description/url).
    - If apply=False, return planned action without writing.
    """
    name = candidate.get("normalized_name") or candidate.get("source_name") or ""
    url = (candidate.get("canonical_url") or "").strip()
    owner = ((enrichment or {}).get("owner") or "").strip()
    description = ((enrichment or {}).get("description") or "").strip()

    if existing_match is None:
        if apply:
            obj = Organization.objects.create(
                name=name,
                url=url,
                owner=owner,
                description=description,
                independent=False,
            )
            return {"action": "created", "organization_id": obj.pk, "name": obj.name}
        return {
            "action": "would_create",
            "name": name,
            "fields": {
                "url": url,
                "owner": owner,
                "description": description,
                "independent": False,
            },
        }

    org = existing_match["organization"]
    updates = {}
    if not (org.owner or "").strip() and owner:
        updates["owner"] = owner
    if not (org.description or "").strip() and description:
        updates["description"] = description
    if not (org.url or "").strip() and url:
        updates["url"] = url

    if not updates:
        return {"action": "skipped", "organization_id": org.pk, "name": org.name}

    if apply:
        Organization.objects.filter(pk=org.pk).update(**updates)
        return {
            "action": "updated",
            "organization_id": org.pk,
            "name": org.name,
            "updated_fields": sorted(updates.keys()),
        }

    return {
        "action": "would_update",
        "organization_id": org.pk,
        "name": org.name,
        "updated_fields": sorted(updates.keys()),
    }


# -----------------------------------------------------------------------------
# Entrypoint
# -----------------------------------------------------------------------------
def main() -> int:
    """Run the organization import workflow."""
    args = parse_args()

    input_csv = Path(args.input_csv)
    dry_run_report = Path(args.dry_run_report)

    # Stage 1: load
    print(f"Loading candidates from {input_csv} (min_count={args.min_count})...")
    candidates = load_candidates(input_csv, args.min_count)
    print(f"  {len(candidates)} candidates after filtering.")

    results = []
    for i, candidate in enumerate(candidates, 1):
        # Stage 2: normalize
        normalized = normalize_candidate(candidate)

        # Stage 3: match
        existing_match = match_existing_organization(normalized)

        # Stage 4: enrich (skip if already fully matched with data)
        enrichment = None
        if existing_match is None or not existing_match["organization"].owner:
            print(f"  [{i}/{len(candidates)}] Enriching {normalized['normalized_name']!r}...")
            enrichment = enrich_with_llm(normalized)

        # Stage 5: create/update directly
        result = create_object_from_candidate(
            normalized,
            existing_match,
            enrichment,
            apply=args.apply,
        )
        results.append(result)

    summary = {
        "created": sum(1 for r in results if r["action"] == "created"),
        "updated": sum(1 for r in results if r["action"] == "updated"),
        "skipped": sum(1 for r in results if r["action"] == "skipped"),
        "would_create": sum(1 for r in results if r["action"] == "would_create"),
        "would_update": sum(1 for r in results if r["action"] == "would_update"),
    }

    dry_run_report.parent.mkdir(parents=True, exist_ok=True)
    with dry_run_report.open("w", encoding="utf-8") as f:
        json.dump({"summary": summary, "results": results}, f, indent=2)

    if args.apply:
        print("Import complete.")
        print(
            f"  created={summary['created']} updated={summary['updated']} skipped={summary['skipped']}"
        )
    else:
        print("Dry run complete. No database writes were made.")
        print(
            f"  would_create={summary['would_create']} would_update={summary['would_update']} skipped={summary['skipped']}"
        )
    print(f"Report written to {dry_run_report}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
