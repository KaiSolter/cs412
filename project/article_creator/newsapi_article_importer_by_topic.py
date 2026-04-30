"""
Import recent NewsAPI articles by Topic into Django Article objects.

This script mirrors the organization-level importer behavior, but searches by
Topic text so each Topic can accumulate articles.

Notes:
- topic <- current Topic being processed
- organization <- matched from article source/domain (must exist in DB)
- summary <- NewsAPI description (may be blank)
- full_text <- blank (handled in a separate pipeline)
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

import django
import requests

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cs412.settings")
django.setup()

from project.models import Article, Organization, Topic

NEWSAPI_URL = "https://newsapi.org/v2/everything"
COMMON_SUBDOMAIN_PREFIXES = ("www.", "m.", "news.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import a few recent NewsAPI articles per Topic into Article objects."
    )
    parser.add_argument(
        "--per-topic",
        type=int,
        default=4,
        help="How many articles to request per topic.",
    )
    parser.add_argument(
        "--max-topics",
        type=int,
        default=0,
        help="Optional cap on number of topics (0 means no cap).",
    )
    parser.add_argument(
        "--skip-topics-with-articles",
        action="store_true",
        help="Skip topics that already have at least one article.",
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


def fetch_articles_for_topic(topic_name: str, api_key: str, page_size: int):
    """Fetch recent articles for one topic query."""
    response = requests.get(
        NEWSAPI_URL,
        params={
            "q": topic_name,
            "sortBy": "publishedAt",
            "language": "en",
            "pageSize": page_size,
            "apiKey": api_key,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json().get("articles", [])


def normalized_name_key(text: str) -> str:
    return "".join((text or "").casefold().split())


def canonical_domain(article_url: str) -> str:
    parsed = urlparse(article_url or "")
    domain = (parsed.netloc or "").casefold()
    for prefix in COMMON_SUBDOMAIN_PREFIXES:
        if domain.startswith(prefix):
            domain = domain[len(prefix):]
    return domain


def match_organization_for_article(source_name: str, article_url: str):
    """Find best-matching Organization for a NewsAPI article source."""
    source_name = (source_name or "").strip()

    if source_name:
        org = Organization.objects.filter(name__iexact=source_name).first()
        if org:
            return org

    source_key = normalized_name_key(source_name)
    if source_key:
        for org in Organization.objects.all():
            if normalized_name_key(org.name) == source_key:
                return org

    domain = canonical_domain(article_url)
    if domain:
        org = Organization.objects.filter(url__icontains=domain).first()
        if org:
            return org

    return None


def create_articles_for_topic(topic: Topic, articles, dry_run: bool = False):
    """Create Article rows for one Topic (idempotent by URL)."""
    created = 0
    existing = 0
    skipped = 0
    missing_org = 0

    for item in articles:
        url = (item.get("url") or "").strip()
        title = (item.get("title") or "").strip()
        summary = (item.get("description") or "").strip()
        source = item.get("source") or {}
        source_name = (source.get("name") or "").strip()

        if not url or not title:
            skipped += 1
            continue

        org = match_organization_for_article(source_name, url)
        if not org:
            missing_org += 1
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
                "topic": topic,
            },
        )

        if was_created:
            created += 1
        else:
            existing += 1

    return {
        "created": created,
        "existing": existing,
        "skipped": skipped,
        "missing_org": missing_org,
    }


def main() -> int:
    args = parse_args()

    api_key = args.api_key.strip() or os.getenv("NEWSAPI_KEY")
    if not api_key:
        raise RuntimeError("Missing NewsAPI key. Set NEWSAPI_KEY or pass --api-key.")

    topics_qs = Topic.objects.all().order_by("topic")
    if args.skip_topics_with_articles:
        topics_qs = [t for t in topics_qs if not Article.objects.filter(topic=t).exists()]
    else:
        topics_qs = list(topics_qs)

    if args.max_topics and args.max_topics > 0:
        topics_qs = topics_qs[: args.max_topics]

    totals = {
        "topics": len(topics_qs),
        "fetched": 0,
        "created": 0,
        "existing": 0,
        "skipped": 0,
        "missing_org": 0,
        "errors": 0,
    }

    print(
        f"Import starting: topics={len(topics_qs)}, per_topic={args.per_topic}, "
        f"dry_run={args.dry_run}"
    )

    for idx, topic in enumerate(topics_qs, start=1):
        try:
            articles = fetch_articles_for_topic(topic.topic, api_key, args.per_topic)
            totals["fetched"] += len(articles)
            stats = create_articles_for_topic(topic, articles, dry_run=args.dry_run)
            totals["created"] += stats["created"]
            totals["existing"] += stats["existing"]
            totals["skipped"] += stats["skipped"]
            totals["missing_org"] += stats["missing_org"]

            print(
                f"[{idx}/{len(topics_qs)}] {topic.topic} -> "
                f"fetched={len(articles)} created={stats['created']} "
                f"existing={stats['existing']} skipped={stats['skipped']} "
                f"missing_org={stats['missing_org']}"
            )
        except Exception as exc:
            totals["errors"] += 1
            print(f"[{idx}/{len(topics_qs)}] ERROR {topic.topic}: {exc}")

    print("Done.")
    print(
        f"topics={totals['topics']} fetched={totals['fetched']} created={totals['created']} "
        f"existing={totals['existing']} skipped={totals['skipped']} "
        f"missing_org={totals['missing_org']} errors={totals['errors']}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
