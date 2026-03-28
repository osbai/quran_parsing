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

## How the Analysis Was Generated

### 1. Data Collection & Aggregation

The full Quran text (`data/quran/full_quran.md`) was fetched from the [quran.com API](https://api.quran.com) using `scripts/fetch_quran.py`, which downloads all 114 chapters as individual JSON files containing the Arabic Uthmani script and English translations. These chapter files were then aggregated into a single Markdown file using `scripts/aggregate.py`.

### 2. Quick-Reference Summary — `analysis/quran_summary.md`

A concise quick-reference summary was generated using AI (Claude by Anthropic). The full Arabic Uthmani text from the dataset was read and each of the 114 chapters was summarized with its name, verse count, and key themes in a compact table format.

### 3. Comprehensive Scholarly Analysis — `analysis/quran_detailed_analysis.md`

A detailed scholarly analysis was produced by AI (Claude, Opus model with 1M context window). The entire Quran text from the dataset was read in chunks and analyzed to produce:

- **Detailed chapter summaries** — 5–10 sentence summaries for all 114 chapters
- **Thematic analysis** across 7 major topics: Tawheed (Oneness of God), Prophethood, Eschatology, Ethics & Morality, Islamic Law, Prophetic Stories, and Cosmology
- **Literary analysis** — rhetorical devices, structural patterns, Huruf Muqatta'at (disconnected letters), and Sajdah (prostration) verses
- **Chronological context** — Meccan vs. Medinan classification and the evolution of themes across revelation periods
- **Cross-references** — connections and thematic links between chapters

### 4. Statistical Analysis Notebook — `analysis/quran_analysis.ipynb`

A quantitative analysis notebook was built with Python (`pandas`, `matplotlib`, `seaborn`) to perform:

- Verse, word, and character counts per chapter
- Word and letter frequency distributions
- Verse length analysis and visualizations
- Identification of structural patterns (Huruf Muqatta'at chapters)
- Theological term frequency heatmaps
- N-gram analysis (bigrams and trigrams)

> **Note:** All AI-generated summaries and analyses were based on reading and analyzing the actual Arabic Uthmani text from the dataset (`data/quran/full_quran.md`), not from external sources or pre-existing summaries.

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
