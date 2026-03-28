import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

CHAPTERS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "quran", "chapters"
)
BASE_URL = "https://api.quran.com/api/v4/verses/by_chapter"
MAX_RETRIES = 3
PER_PAGE = 50

os.makedirs(CHAPTERS_DIR, exist_ok=True)


def fetch_chapter(chapter_number: int) -> dict | None:
    all_verses = []
    page = 1

    while True:
        params = urllib.parse.urlencode(
            {
                "page": page,
                "per_page": PER_PAGE,
                "fields": "text_uthmani,text_imlaei",
                "language": "en",
                "translations": "131",
            }
        )
        url = f"{BASE_URL}/{chapter_number}?{params}"

        data = None
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                req = urllib.request.Request(
                    url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                        "Accept": "application/json",
                    },
                )
                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                break
            except Exception as e:
                print(f"  [retry {attempt}/{MAX_RETRIES}] page {page} failed: {e}")
                if attempt < MAX_RETRIES:
                    time.sleep(2 * attempt)

        if data is None:
            print(f"  ERROR: could not fetch page {page} after {MAX_RETRIES} retries")
            return None

        all_verses.extend(data.get("verses", []))

        pagination = data.get("pagination", {})
        total_pages = pagination.get("total_pages", 1)
        if page >= total_pages:
            break
        page += 1

    return {
        "chapter": chapter_number,
        "total_verses": len(all_verses),
        "verses": all_verses,
    }


def main():
    failed = []
    for ch in range(1, 115):
        print(f"Fetching chapter {ch}/114 ...", end=" ", flush=True)
        result = fetch_chapter(ch)
        if result is None:
            print("FAILED")
            failed.append(ch)
            continue

        path = os.path.join(CHAPTERS_DIR, f"chapter_{ch}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"OK — {result['total_verses']} verses saved")
        time.sleep(0.3)

    print("\n--- Summary ---")
    files = sorted(os.listdir(CHAPTERS_DIR))
    print(f"Files in {CHAPTERS_DIR}: {len(files)}")
    if failed:
        print(f"Failed chapters: {failed}")
    else:
        print("All 114 chapters fetched successfully.")


if __name__ == "__main__":
    main()
