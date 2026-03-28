#!/usr/bin/env python3
"""Fetch English Quran translation and save as individual JSON files per surah."""

import json
import os
import re
import time
import urllib.error
import urllib.request

OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "quran_english"
)
TOTAL_SURAHS = 114

EDITIONS = ["en.asad", "en.sahih"]


def fetch_json(url, timeout=30):
    """Fetch JSON from a URL with retry logic."""
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "QuranFetcher/1.0"}
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            TimeoutError,
            OSError,
        ) as e:
            if attempt < 2:
                time.sleep(1 + attempt)
            else:
                print(f"    Failed after 3 attempts: {e}")
    return None


def slugify(name):
    """Convert surah name to a filesystem-friendly slug."""
    name = name.lower().strip()
    name = re.sub(r"[''`]", "", name)
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_")


def fetch_surah(surah_num, edition):
    """Fetch a single surah from AlQuran Cloud API."""
    url = f"https://api.alquran.cloud/v1/surah/{surah_num}/{edition}"
    data = fetch_json(url)
    if not data or data.get("code") != 200:
        return None

    s = data["data"]
    return {
        "surah_number": s["number"],
        "surah_name": s["englishName"],
        "surah_name_english": s["englishNameTranslation"],
        "total_verses": s["numberOfAyahs"],
        "revelation_type": s["revelationType"],
        "verses": [
            {"verse_number": a["numberInSurah"], "text": a["text"]} for a in s["ayahs"]
        ],
    }


def main():
    print("=" * 60)
    print("Fetching English Quran Translation (per-surah)")
    print("=" * 60)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    edition = EDITIONS[0]
    saved = 0
    failed = []

    for num in range(1, TOTAL_SURAHS + 1):
        surah = None
        for ed in EDITIONS:
            surah = fetch_surah(num, ed)
            if surah:
                if ed != edition:
                    edition = ed
                break

        if not surah:
            print(f"  FAILED: Surah {num}")
            failed.append(num)
            continue

        slug = slugify(surah["surah_name"])
        filename = f"{num:03d}_{slug}.json"
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(surah, f, ensure_ascii=False, indent=2)
        saved += 1

        if saved % 10 == 0 or num == TOTAL_SURAHS:
            print(f"  Progress: {saved}/{TOTAL_SURAHS} saved (surah {num})")

        # Small delay to be polite to the API
        time.sleep(0.15)

    print(f"\nSaved {saved}/{TOTAL_SURAHS} surahs.")
    if failed:
        print(f"Failed surahs: {failed}")
    return saved == TOTAL_SURAHS


if __name__ == "__main__":
    success = main()

    if success:
        print("\n" + "=" * 60)
        print("Verification")
        print("=" * 60)
        files = sorted(f for f in os.listdir(OUTPUT_DIR) if f.endswith(".json"))
        print(f"Total JSON files: {len(files)}")
        print(f"First 5: {files[:5]}")
        print(f"Last 5:  {files[-5:]}")

        with open(os.path.join(OUTPUT_DIR, files[0]), "r") as f:
            sample = json.load(f)
        print(f"\nSample - {sample['surah_name']} ({sample['surah_name_english']}):")
        print(f"  Verses: {sample['total_verses']}")
        print(f"  First verse: {sample['verses'][0]['text'][:120]}...")
    else:
        exit(1)
