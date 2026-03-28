import json
from pathlib import Path

chapters_dir = Path(__file__).resolve().parent.parent / "data" / "quran" / "chapters"
output_path = (
    Path(__file__).resolve().parent.parent / "data" / "quran" / "full_quran.md"
)

lines = ["# The Holy Quran - Text Uthmani\n"]

for i in range(1, 115):
    filepath = chapters_dir / f"chapter_{i}.json"
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    lines.append(f"\n## Chapter {data['chapter']}\n")

    for verse in data["verses"]:
        lines.append(f"**{verse['verse_key']}** {verse['text_uthmani']}\n")

with open(output_path, "w", encoding="utf-8") as f:
    f.writelines(lines)

print(f"Written {output_path}")
