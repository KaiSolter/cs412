# File: project/topic_creator/generate_topic_descriptions.py
# Author: Kai Solter (ksolter@bu.edu), 4/30/2026
# Description: Use OpenAI to generate Topic descriptions for topics with blank descriptions

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import django
from openai import OpenAI

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cs412.settings")
django.setup()

from project.models import Topic


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate descriptions for Topic rows that do not have one."
    )
    parser.add_argument(
        "--model",
        default="gpt-5.4-mini",
        help="OpenAI model to use for description generation.",
    )
    parser.add_argument(
        "--max-topics",
        type=int,
        default=0,
        help="Optional cap on number of topics to process (0 means no cap).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate descriptions but do not save to DB.",
    )
    return parser.parse_args()


def build_prompt(topic_name: str) -> str:
    return (
        "You write short, neutral topic descriptions for a news aggregation app. "
        "Return ONLY valid JSON with one key: description. "
        "The description should be 1 sentence, 15-30 words, plain-language, and describe "
        "the kind of news covered by the topic.\n\n"
        "Examples:\n"
        "Topic: Cybersecurity\n"
        "JSON: {\"description\":\"News about cyber threats, breaches, digital defense, software vulnerabilities, and policy or business responses to security incidents.\"}\n\n"
        "Topic: Markets and Investing\n"
        "JSON: {\"description\":\"Coverage of stock and bond markets, investor behavior, portfolio trends, and major economic signals that influence investment decisions.\"}\n\n"
        f"Topic: {topic_name}"
    )


def generate_description(client: OpenAI, model: str, topic_name: str) -> str:
    prompt = build_prompt(topic_name)
    response = client.responses.create(
        model=model,
        input=prompt,
    )

    raw_text = response.output_text or ""
    parsed = json.loads(raw_text)
    description = (parsed.get("description") or "").strip()
    return description


def main() -> int:
    args = parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY environment variable.")

    client = OpenAI(api_key=api_key)

    topics = Topic.objects.filter(description__isnull=False)
    topics = [t for t in topics if not (t.description or "").strip()]

    if args.max_topics and args.max_topics > 0:
        topics = topics[: args.max_topics]

    print(
        f"Generating descriptions for {len(topics)} topics using model={args.model} "
        f"(dry_run={args.dry_run})"
    )

    updated = 0
    failed = 0

    for idx, topic in enumerate(topics, start=1):
        try:
            description = generate_description(client, args.model, topic.topic)
            if not description:
                failed += 1
                print(f"[{idx}/{len(topics)}] {topic.topic}: FAILED (empty description)")
                continue

            if args.dry_run:
                print(f"[{idx}/{len(topics)}] {topic.topic}: {description}")
            else:
                topic.description = description
                topic.save(update_fields=["description"])
                updated += 1
                print(f"[{idx}/{len(topics)}] {topic.topic}: updated")
        except Exception as exc:
            failed += 1
            print(f"[{idx}/{len(topics)}] {topic.topic}: FAILED ({exc})")

    print(f"Done. updated={updated} failed={failed} total={len(topics)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
