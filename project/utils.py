# File: project/utils.py
# Author: Kai Solter (ksolter@bu.edu), 4/30/2026
# Description: Shared utilities for the project app

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


def classify_topic(text):
    """
    Return the best-matching Topic DB object for the given text.
    Falls back to 'Uncategorized' if no keywords match.
    """
    from .models import Topic
    lower = text.lower()
    for topic_name, keywords in TOPIC_KEYWORDS.items():
        if any(kw in lower for kw in keywords):
            topic, _ = Topic.objects.get_or_create(topic=topic_name, defaults={'description': ''})
            return topic
    uncategorized, _ = Topic.objects.get_or_create(topic='Uncategorized', defaults={'description': ''})
    return uncategorized
