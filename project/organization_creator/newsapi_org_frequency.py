import argparse
import csv
import json
import os
import time
from collections import Counter
from pathlib import Path

import requests


NEWSAPI_EVERYTHING_URL = "https://newsapi.org/v2/everything"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run multiple NewsAPI searches and report the most common source organizations."
        )
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("NEWSAPI_KEY"),
        help="NewsAPI key. Defaults to NEWSAPI_KEY env var.",
    )
    parser.add_argument(
        "--queries",
        nargs="+",
        help="List of search queries. Example: --queries election climate ai",
    )
    parser.add_argument(
        "--query-file",
        help="Path to text file with one query per line.",
    )
    parser.add_argument(
        "--sort-by",
        default="publishedAt",
        choices=["relevancy", "popularity", "publishedAt"],
        help="NewsAPI sort order.",
    )
    parser.add_argument(
        "--language",
        default="en",
        help="Language filter (NewsAPI everything endpoint).",
    )
    parser.add_argument(
        "--page-size",
        type=int,
        default=100,
        help="Results per query page (max 100).",
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=1,
        help="How many pages to request per query.",
    )
    parser.add_argument(
        "--sleep-seconds",
        type=float,
        default=0.0,
        help="Optional delay between requests.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=20,
        help="Number of top organizations to print.",
    )
    parser.add_argument(
        "--out-csv",
        help="Optional output CSV path.",
    )
    parser.add_argument(
        "--out-json",
        help="Optional output JSON path.",
    )
    parser.add_argument(
        "--no-dedupe-urls",
        action="store_true",
        help="Count duplicate article URLs across queries/pages as separate hits.",
    )
    return parser.parse_args()


def load_queries(inline_queries, query_file) -> list[str]:
    queries = []

    if inline_queries:
        queries.extend(q.strip() for q in inline_queries if q and q.strip())

    if query_file:
        for line in Path(query_file).read_text(encoding="utf-8").splitlines():
            q = line.strip()
            if q and not q.startswith("#"):
                queries.append(q)

    # Preserve order but remove duplicates.
    seen = set()
    deduped = []
    for q in queries:
        if q not in seen:
            seen.add(q)
            deduped.append(q)

    return deduped


def fetch_articles_for_query(
    query: str,
    api_key: str,
    sort_by: str,
    language: str,
    page_size: int,
    pages: int,
    sleep_seconds: float,
) -> list[dict]:
    all_articles = []

    for page in range(1, pages + 1):
        params = {
            "q": query,
            "apiKey": api_key,
            "sortBy": sort_by,
            "language": language,
            "pageSize": max(1, min(100, page_size)),
            "page": page,
        }

        response = requests.get(NEWSAPI_EVERYTHING_URL, params=params, timeout=30)
        response.raise_for_status()
        payload = response.json()

        if payload.get("status") != "ok":
            message = payload.get("message", "Unknown NewsAPI error")
            raise RuntimeError(f"NewsAPI returned non-ok status for query '{query}': {message}")

        articles = payload.get("articles", [])
        if not articles:
            break

        all_articles.extend(articles)

        if sleep_seconds > 0:
            time.sleep(sleep_seconds)

    return all_articles


def count_organizations(articles: list[dict], dedupe_urls: bool = True) -> dict:
    """Count organizations and collect metadata about each."""
    org_data = {}
    seen_urls = set()

    for article in articles:
        source = article.get("source") or {}
        source_name = source.get("name")
        article_url = article.get("url")
        article_title = article.get("title", "")
        published_at = article.get("publishedAt", "")

        if not source_name:
            continue

        if dedupe_urls and article_url:
            if article_url in seen_urls:
                continue
            seen_urls.add(article_url)

        if source_name not in org_data:
            org_data[source_name] = {
                "count": 0,
                "urls": [],
                "titles": [],
                "published_dates": [],
                "source_id": source.get("id", ""),
            }

        org_data[source_name]["count"] += 1
        if article_url and article_url not in org_data[source_name]["urls"]:
            org_data[source_name]["urls"].append(article_url)
        if article_title and article_title not in org_data[source_name]["titles"]:
            org_data[source_name]["titles"].append(article_title)
        if published_at:
            org_data[source_name]["published_dates"].append(published_at)

    return org_data


def write_csv(path: str, org_data: dict) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "organization",
            "count",
            "sample_urls",
            "num_unique_urls",
            "source_id",
        ])
        # Sort by count descending
        for org, data in sorted(org_data.items(), key=lambda x: x[1]["count"], reverse=True):
            sample_urls = "; ".join(data["urls"][:5])  # Top 5 URLs
            writer.writerow([
                org,
                data["count"],
                sample_urls,
                len(data["urls"]),
                data["source_id"],
            ])


def write_json(path: str, org_data: dict) -> None:
    data = [
        {
            "organization": org,
            "count": org_info["count"],
            "num_unique_urls": len(org_info["urls"]),
            "sample_urls": org_info["urls"][:10],  # Top 10 URLs
            "sample_titles": org_info["titles"][:5],  # Top 5 titles
            "source_id": org_info["source_id"],
        }
        for org, org_info in sorted(
            org_data.items(), key=lambda x: x[1]["count"], reverse=True
        )
    ]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def main() -> int:
    args = parse_args()

    if not args.api_key:
        print("Error: Missing NewsAPI key. Use --api-key or set NEWSAPI_KEY.")
        return 1

    queries = load_queries(args.queries, args.query_file)
    if not queries:
        print("Error: Provide queries with --queries and/or --query-file.")
        return 1

    combined_articles = []
    for query in queries:
        try:
            articles = fetch_articles_for_query(
                query=query,
                api_key=args.api_key,
                sort_by=args.sort_by,
                language=args.language,
                page_size=args.page_size,
                pages=args.pages,
                sleep_seconds=args.sleep_seconds,
            )
            combined_articles.extend(articles)
            print(f"Query '{query}': fetched {len(articles)} articles")
        except requests.exceptions.RequestException as err:
            print(f"Query '{query}': request failed -> {err}")
        except RuntimeError as err:
            print(f"Query '{query}': API error -> {err}")

    counts = count_organizations(
        combined_articles,
        dedupe_urls=not args.no_dedupe_urls,
    )

    # Sort by count
    sorted_orgs = sorted(counts.items(), key=lambda x: x[1]["count"], reverse=True)

    print(f"\nTotal fetched articles: {len(combined_articles)}")
    print(f"Unique organizations found: {len(counts)}")
    print(f"\nTop {min(args.top, len(counts))} organizations:")
    for org, org_info in sorted_orgs[:args.top]:
        print(f"{org}: {org_info['count']} articles, {len(org_info['urls'])} unique URLs")
        if org_info["urls"]:
            print(f"  Sample URL: {org_info['urls'][0]}")

    if args.out_csv:
        write_csv(args.out_csv, counts)
        print(f"\nWrote CSV to {args.out_csv}")

    if args.out_json:
        write_json(args.out_json, counts)
        print(f"Wrote JSON to {args.out_json}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
