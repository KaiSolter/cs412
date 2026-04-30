"""
Import a few recent NewsAPI articles per source into Django Article objects.

This script intentionally keeps summary/full_text lightweight:
- summary <- NewsAPI description (may be blank)
- full_text <- blank (to be handled in a separate pipeline)
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from pathlib import Path

import django
import requests

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cs412.settings")
django.setup()

from project.models import Article, Organization, Topic

DEFAULT_INPUT_CSV = PROJECT_ROOT / "project" / "organization_creator" / "org_counts.csv"
NEWSAPI_URL = "https://newsapi.org/v2/everything"

TOPIC_KEYWORDS = {
    "US Politics": ["white house", "congress", "senate", "house republicans", "gop", "democrat", "trump", "biden", "us election"],
    "Global Politics": ["prime minister", "parliament", "diplomacy", "foreign minister", "un", "geopolitics", "sanctions", "ceasefire"],
    "US Economy": ["us economy", "fed", "federal reserve", "inflation", "jobs report", "payrolls", "recession"],
    "Global Economy": ["world bank", "imf", "global economy", "g20", "trade war", "tariffs"],
    "US Finance": ["wall street", "nasdaq", "dow", "s&p 500", "earnings", "ipo", "sec"],
    "Global Finance": ["european central bank", "nikkei", "ftse", "global markets", "sovereign wealth"],
    "Markets and Investing": ["stocks", "shares", "bond yields", "investors", "market rally", "sell-off"],
    "Corporate Earnings and Deals": ["quarterly results", "q1", "q2", "q3", "q4", "merger", "acquisition", "buyout"],
    "Business and Industry": ["company", "industry", "manufacturing", "supply chain", "retail", "startup"],
    "Technology and AI": ["artificial intelligence", "ai", "machine learning", "openai", "google", "microsoft", "chip", "semiconductor"],
    "Cybersecurity": ["ransomware", "data breach", "malware", "hacking", "vulnerability", "zero-day", "phishing"],
    "Crypto and Blockchain": ["bitcoin", "ethereum", "crypto", "blockchain", "token", "defi", "nft"],
    "Science and Space": ["nasa", "spacex", "astronomy", "telescope", "scientists", "researchers", "study finds"],
    "Climate and Energy": ["renewable", "solar", "wind", "oil", "gas", "emissions", "climate"],
    "Environment and Natural Disasters": ["wildfire", "flood", "earthquake", "hurricane", "storm", "drought"],
    "Public Health and Medicine": ["health", "hospital", "cdc", "who", "vaccine", "virus", "disease", "medical"],
    "Law, Courts, and Regulation": ["supreme court", "lawsuit", "judge", "court", "regulator", "regulation", "antitrust"],
    "Elections and Campaigns": ["campaign", "ballot", "poll", "primary", "voters", "election"],
    "International Relations and Conflict": ["war", "military", "defense", "missile", "troops", "border", "conflict"],
    "Crime and Public Safety": ["police", "shooting", "arrest", "charged", "investigation", "crime"],
    "Entertainment and Pop Culture": ["movie", "film", "tv", "celebrity", "music", "award", "hollywood"],
    "Sports": ["nba", "nfl", "mlb", "fifa", "olympics", "match", "tournament", "coach"],
    "Education": ["school", "university", "college", "student", "teacher", "campus"],
    "Lifestyle and Consumer Trends": ["fashion", "travel", "food", "wellness", "consumer", "shopping"],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import a few recent articles per NewsAPI source into Article objects."
    )
    parser.add_argument(
        "--input-csv",
        default=str(DEFAULT_INPUT_CSV),
        help="Path to org_counts.csv containing organization and source_id columns.",
    )
    parser.add_argument(
        "--per-source",
        type=int,
        default=3,
        help="How many articles to request per source.",
    )
    parser.add_argument(
        "--max-sources",
        type=int,
        default=0,
        help="Optional cap on number of sources (0 means no cap).",
    )
    parser.add_argument(
        "--min-count",
        type=int,
        default=5,
        help="Only include sources with frequency >= min-count from CSV.",
    )
    parser.add_argument(
        "--default-topic",
        default="Uncategorized",
        help="Topic to assign when creating imported articles.",
    )
    parser.add_argument(
        "--api-key",
        default="",
        help="Optional NewsAPI key override (falls back to NEWSAPI_KEY env var).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Plan imports without creating Article rows.",
    )
    return parser.parse_args()


def load_source_candidates(input_csv: Path, min_count: int):
    """Load (organization_name, source_id, count) rows from CSV for known organizations."""
    if not input_csv.exists():
        raise FileNotFoundError(f"Input CSV not found: {input_csv}")

    candidates = []
    with input_csv.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            org_name = (row.get("organization") or "").strip()
            source_id = (row.get("source_id") or "").strip()
            if not org_name or not source_id:
                continue

            try:
                count = int((row.get("count") or "0").strip())
            except ValueError:
                continue

            if count < min_count:
                continue

            org = Organization.objects.filter(name=org_name).first()
            if not org:
                continue

            candidates.append(
                {
                    "organization": org,
                    "source_id": source_id,
                    "count": count,
                }
            )

    candidates.sort(key=lambda c: c["count"], reverse=True)

    unique_by_source = {}
    for c in candidates:
        unique_by_source.setdefault(c["source_id"], c)
    return list(unique_by_source.values())


def fetch_articles_for_source(source_id: str, api_key: str, page_size: int):
    """Fetch recent articles from one NewsAPI source_id."""
    response = requests.get(
        NEWSAPI_URL,
        params={
            "sources": source_id,
            "sortBy": "publishedAt",
            "language": "en",
            "pageSize": page_size,
            "apiKey": api_key,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json().get("articles", [])


def build_topic_lookup(default_topic_name: str):
    """Build topic map and ensure fallback default topic exists."""
    topic_map = {t.topic: t for t in Topic.objects.all()}
    default_topic = topic_map.get(default_topic_name)
    if not default_topic:
        default_topic, _ = Topic.objects.get_or_create(
            topic=default_topic_name,
            defaults={"description": ""},
        )
        topic_map[default_topic.topic] = default_topic
    return topic_map, default_topic


def choose_topic_for_article(title: str, summary: str, topic_map: dict, default_topic: Topic):
    """Pick the best Topic based on keyword scoring over title + summary."""
    text = f"{title} {summary}".lower()
    best_topic_name = None
    best_score = 0

    for topic_name, keywords in TOPIC_KEYWORDS.items():
        if topic_name not in topic_map:
            continue
        score = 0
        for keyword in keywords:
            if keyword in text:
                score += 1
        if score > best_score:
            best_score = score
            best_topic_name = topic_name

    if best_topic_name:
        return topic_map[best_topic_name]
    return default_topic


def create_articles_for_source(
    org: Organization,
    articles,
    topic_map: dict,
    default_topic: Topic,
    dry_run: bool = False,
):
    """Create Article rows (idempotent by URL) and return per-source stats."""
    created = 0
    existing = 0
    skipped = 0

    for item in articles:
        url = (item.get("url") or "").strip()
        title = (item.get("title") or "").strip()
        summary = (item.get("description") or "").strip()
        chosen_topic = choose_topic_for_article(title, summary, topic_map, default_topic)

        if not url or not title:
            skipped += 1
            continue

        if dry_run:
            if Article.objects.filter(url=url).exists():
                existing += 1
            else:
                created += 1
            continue

        _, was_created = Article.objects.get_or_create(
            url=url,
            defaults={
                "title": title,
                "summary": summary,
                "full_text": "",
                "organization": org,
                "topic": chosen_topic,
            },
        )

        if was_created:
            created += 1
        else:
            existing += 1

    return {"created": created, "existing": existing, "skipped": skipped}


def main() -> int:
    args = parse_args()

    api_key = args.api_key.strip() or os.getenv("NEWSAPI_KEY")
    if not api_key:
        raise RuntimeError("Missing NewsAPI key. Set NEWSAPI_KEY or pass --api-key.")

    input_csv = Path(args.input_csv)
    candidates = load_source_candidates(input_csv, args.min_count)

    if args.max_sources and args.max_sources > 0:
        candidates = candidates[: args.max_sources]

    topic_map, default_topic = build_topic_lookup(args.default_topic)

    totals = {
        "sources": len(candidates),
        "fetched": 0,
        "created": 0,
        "existing": 0,
        "skipped": 0,
        "errors": 0,
    }

    print(
        f"Import starting: sources={len(candidates)}, per_source={args.per_source}, "
        f"dry_run={args.dry_run}"
    )

    for idx, c in enumerate(candidates, start=1):
        org = c["organization"]
        source_id = c["source_id"]

        try:
            articles = fetch_articles_for_source(source_id, api_key, args.per_source)
            totals["fetched"] += len(articles)
            stats = create_articles_for_source(
                org,
                articles,
                topic_map=topic_map,
                default_topic=default_topic,
                dry_run=args.dry_run,
            )
            totals["created"] += stats["created"]
            totals["existing"] += stats["existing"]
            totals["skipped"] += stats["skipped"]

            print(
                f"[{idx}/{len(candidates)}] {org.name} ({source_id}) -> "
                f"fetched={len(articles)} created={stats['created']} "
                f"existing={stats['existing']} skipped={stats['skipped']}"
            )
        except Exception as exc:
            totals["errors"] += 1
            print(f"[{idx}/{len(candidates)}] ERROR {org.name} ({source_id}): {exc}")

    print("Done.")
    print(
        f"sources={totals['sources']} fetched={totals['fetched']} created={totals['created']} "
        f"existing={totals['existing']} skipped={totals['skipped']} errors={totals['errors']}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
