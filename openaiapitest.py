import os
import csv
import json
from pathlib import Path

api_key = os.getenv("OPENAI_API_KEY")
from openai import OpenAI

LLM = OpenAI(api_key=api_key)


def test_openai_api():
    response = LLM.responses.create(
        model="gpt-5.4-mini",
        input="Write a one-sentence joke about a cat and/or a dog.",
    )

    print("OpenAI API text:", response.output_text)

def test_openai_json():
    csv_path = Path("project/organization_creator/org_counts.csv")
    if not csv_path.exists():
        print(f"CSV not found: {csv_path}")
        return

    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        row = next(reader, None)

    if not row:
        print("CSV has no rows to test with.")
        return

    sample_payload = {
        "organization": row.get("organization", ""),
        "count": row.get("count", ""),
        "sample_urls": [
            u.strip() for u in (row.get("sample_urls", "") or "").split(";") if u.strip()
        ][:3],
        "source_id": row.get("source_id", ""),
    }

    prompt = (
        "Return ONLY valid JSON with keys owner, owner_confidence, and description."
        "Use the organization evidence below and infer likely ownership (with owner_confidence representing your confidence that your asserted owner is correct 0-1) and a concise description (note the description should be of the news site itself not of the owner of the news site).\n\n"
        f"Evidence: {json.dumps(sample_payload)}"
    )

    response = LLM.responses.create(
        model="gpt-5.4-mini",
        input=prompt,
    )

    raw_text = response.output_text
    try:
        parsed = json.loads(raw_text)
        print("OpenAI API JSON:", json.dumps(parsed, indent=2))
    except json.JSONDecodeError:
        print("Model did not return valid JSON. Raw output:")
        print(raw_text)

if __name__ == "__main__":
    # test_openai_api()
    test_openai_json()