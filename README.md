# Scripture Text Analysis

Fetching, parsing, and analyzing Quran and Bible texts using public APIs, with automated aggregation and statistical/linguistic analysis.

## Folder Structure

```
quran_parsing/
├── README.md
├── scripts/
│   ├── fetch_quran.py          # Fetch all 114 Quran chapters from quran.com API
│   ├── fetch_bible_data.py     # Fetch all 66 Bible books from bible-api.com
│   └── aggregate.py            # Combine chapter JSONs into full_quran.md
├── data/
│   ├── quran/
│   │   ├── chapters/           # 114 JSON files (chapter_1.json – chapter_114.json)
│   │   └── full_quran.md       # Aggregated Quran text in Markdown
│   └── bible/
│       └── *.json              # One JSON file per Bible book (66 books)
├── analysis/
│   ├── quran_analysis.ipynb    # Jupyter notebook with statistical & linguistic analysis
│   ├── quran_summary.md        # High-level summary of analysis results
│   └── quran_detailed_analysis.md  # In-depth analysis writeup
```

## Scripts

| Script | Description |
|---|---|
| `scripts/fetch_quran.py` | Downloads all 114 chapters of the Quran (Uthmani text + English translation) from the [Quran.com API](https://api.quran.com) and saves each chapter as a JSON file in `data/quran/chapters/`. |
| `scripts/fetch_bible_data.py` | Downloads all 66 books of the Bible (World English Bible translation) from [bible-api.com](https://bible-api.com) and saves each book as a JSON file in `data/bible/`. |
| `scripts/aggregate.py` | Reads the 114 chapter JSON files and combines them into a single Markdown file (`data/quran/full_quran.md`) for downstream analysis. |

## Analysis Files

| File | Description |
|---|---|
| `analysis/quran_analysis.ipynb` | Jupyter notebook performing chapter-level statistics, word/letter frequency analysis, verse length distributions, structural patterns, and recurring phrase detection. |
| `analysis/quran_summary.md` | Concise summary of key findings from the analysis. |
| `analysis/quran_detailed_analysis.md` | Comprehensive writeup with detailed statistical results and observations. |

## How to Run

1. **Fetch data**
   ```bash
   python scripts/fetch_quran.py
   python scripts/fetch_bible_data.py
   ```

2. **Aggregate Quran text**
   ```bash
   python scripts/aggregate.py
   ```

3. **Run analysis**
   Open `analysis/quran_analysis.ipynb` in Jupyter and run all cells, or:
   ```bash
   jupyter nbconvert --execute analysis/quran_analysis.ipynb
   ```
