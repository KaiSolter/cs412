"""
Seed comprehensive Topic rows for the project app.

Usage:
    python seed_topics.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import django

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cs412.settings")
django.setup()

from project.models import Topic


TOPICS_TO_SEED = [
    "US Economy",
    "Global Economy",
    "Markets and Investing",
    "Corporate Earnings and Deals",
    "Business and Industry",
    "Technology and AI",
    "Cybersecurity",
    "Crypto and Blockchain",
    "Science and Space",
    "Climate and Energy",
    "Environment and Natural Disasters",
    "Public Health and Medicine",
    "Law, Courts, and Regulation",
    "Elections and Campaigns",
    "International Relations and Conflict",
    "Crime and Public Safety",
    "Entertainment and Pop Culture",
    "Sports",
    "Education",
    "Lifestyle and Consumer Trends",
]


def main() -> int:
    created = 0
    existing = 0

    print(f"Seeding {len(TOPICS_TO_SEED)} topics...")

    for topic_name in TOPICS_TO_SEED:
        _, was_created = Topic.objects.get_or_create(
            topic=topic_name,
            defaults={"description": ""},
        )
        if was_created:
            created += 1
            print(f"  created: {topic_name}")
        else:
            existing += 1
            print(f"  exists:  {topic_name}")

    total_topics = Topic.objects.count()
    print("Done.")
    print(f"created={created} existing={existing} total_topics={total_topics}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
