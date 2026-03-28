#!/usr/bin/env python3
"""Run all notebook cells and capture outputs."""
import io
import sys
import traceback

# Redirect matplotlib to non-interactive backend
import matplotlib

matplotlib.use("Agg")

import re
import warnings
from collections import Counter

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

warnings.filterwarnings("ignore")
import json
import os

# ============================================================
# CELL 1 (index 1): Imports & Setup
# ============================================================
print("--- Cell 1 ---")
matplotlib.rcParams["figure.dpi"] = 100
matplotlib.rcParams["figure.figsize"] = (12, 6)
sns.set_style("whitegrid")
sns.set_palette("viridis")
print("Libraries loaded successfully.")

# ============================================================
# CELL 3 (index 3): Data Parsing
# ============================================================
print("\n--- Cell 3 ---")
QURANIC_MARKS = re.compile(r"[\u06D6-\u06DC\u06DD-\u06DE\u06DF-\u06E8\u06EA-\u06ED۞ۖۗۘۙۚۛۜ]")

with open("full_quran.md", "r", encoding="utf-8") as f:
    content = f.read()

rows = []
current_chapter = None

for line in content.split("\n"):
    line = line.strip()
    chapter_match = re.match(r"^## Chapter (\d+)", line)
    if chapter_match:
        current_chapter = int(chapter_match.group(1))
        continue
    verse_match = re.match(r"^\*\*(\d+):(\d+)\*\*\s*(.*)", line)
    if verse_match and current_chapter is not None:
        ch = int(verse_match.group(1))
        verse_num = int(verse_match.group(2))
        text = verse_match.group(3).strip()
        text_clean = QURANIC_MARKS.sub("", text).strip()
        words = [w for w in text_clean.split() if w.strip()]
        word_count = len(words)
        char_count = len(text_clean.replace(" ", ""))
        rows.append(
            {
                "chapter": ch,
                "verse_number": verse_num,
                "text": text_clean,
                "word_count": word_count,
                "char_count": char_count,
            }
        )

df = pd.DataFrame(rows)
print(f"Total verses parsed: {len(df)}")
print(f'Total chapters: {df["chapter"].nunique()}')
print(f'Total words: {df["word_count"].sum():,}')
print(f'Total characters (no spaces): {df["char_count"].sum():,}')
print()
print(df.head(10).to_string())

# ============================================================
# CELL 5 (index 5): Verses per Chapter
# ============================================================
print("\n--- Cell 5 ---")
chapter_stats = (
    df.groupby("chapter")
    .agg(
        verse_count=("verse_number", "count"),
        total_words=("word_count", "sum"),
        total_chars=("char_count", "sum"),
        avg_verse_words=("word_count", "mean"),
        avg_verse_chars=("char_count", "mean"),
        max_verse_words=("word_count", "max"),
        min_verse_words=("word_count", "min"),
    )
    .reset_index()
)

fig, ax = plt.subplots(figsize=(14, 5))
ax.bar(
    chapter_stats["chapter"],
    chapter_stats["verse_count"],
    color=sns.color_palette("viridis", len(chapter_stats)),
    width=0.8,
)
ax.set_xlabel("Chapter Number", fontsize=12)
ax.set_ylabel("Number of Verses", fontsize=12)
ax.set_title("Number of Verses per Chapter", fontsize=14, fontweight="bold")
ax.set_xlim(0, 115)
plt.tight_layout()
plt.savefig("/tmp/cell5_plot.png")
plt.close()
print("[Plot: Number of Verses per Chapter - saved]")

# ============================================================
# CELL 7 (index 7): Words per Chapter
# ============================================================
print("\n--- Cell 7 ---")
fig, ax = plt.subplots(figsize=(14, 5))
colors = plt.cm.plasma(
    chapter_stats["total_words"] / chapter_stats["total_words"].max()
)
ax.bar(chapter_stats["chapter"], chapter_stats["total_words"], color=colors, width=0.8)
ax.set_xlabel("Chapter Number", fontsize=12)
ax.set_ylabel("Total Words", fontsize=12)
ax.set_title("Total Words per Chapter", fontsize=14, fontweight="bold")
ax.set_xlim(0, 115)
plt.tight_layout()
plt.savefig("/tmp/cell7_plot.png")
plt.close()
print("[Plot: Total Words per Chapter - saved]")

# ============================================================
# CELL 9 (index 9): Average Verse Length
# ============================================================
print("\n--- Cell 9 ---")
fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(
    chapter_stats["chapter"],
    chapter_stats["avg_verse_words"],
    color="teal",
    linewidth=1.5,
    marker="o",
    markersize=3,
)
ax.fill_between(
    chapter_stats["chapter"], chapter_stats["avg_verse_words"], alpha=0.2, color="teal"
)
ax.set_xlabel("Chapter Number", fontsize=12)
ax.set_ylabel("Average Words per Verse", fontsize=12)
ax.set_title("Average Verse Length (Words) per Chapter", fontsize=14, fontweight="bold")
ax.set_xlim(1, 114)
plt.tight_layout()
plt.savefig("/tmp/cell9_plot.png")
plt.close()
print("[Plot: Average Verse Length (Words) per Chapter - saved]")

# ============================================================
# CELL 11 (index 11): Top 10 Longest/Shortest Chapters
# ============================================================
print("\n--- Cell 11 ---")
top10_longest = chapter_stats.nlargest(10, "total_words")[
    ["chapter", "verse_count", "total_words"]
]
top10_shortest = chapter_stats.nsmallest(10, "total_words")[
    ["chapter", "verse_count", "total_words"]
]

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].barh(
    top10_longest["chapter"].astype(str),
    top10_longest["total_words"],
    color=sns.color_palette("Reds_r", 10),
)
axes[0].set_xlabel("Total Words")
axes[0].set_title("Top 10 Longest Chapters", fontweight="bold")
axes[0].invert_yaxis()
for i, v in enumerate(top10_longest["total_words"]):
    axes[0].text(v + 20, i, str(v), va="center", fontsize=9)

axes[1].barh(
    top10_shortest["chapter"].astype(str),
    top10_shortest["total_words"],
    color=sns.color_palette("Blues_r", 10),
)
axes[1].set_xlabel("Total Words")
axes[1].set_title("Top 10 Shortest Chapters", fontweight="bold")
axes[1].invert_yaxis()
for i, v in enumerate(top10_shortest["total_words"]):
    axes[1].text(v + 1, i, str(v), va="center", fontsize=9)

plt.tight_layout()
plt.savefig("/tmp/cell11_plot.png")
plt.close()
print("[Plot: Top 10 Longest/Shortest Chapters - saved]")

print("\nTop 10 Longest Chapters:")
print(top10_longest.to_string(index=False))
print("\nTop 10 Shortest Chapters:")
print(top10_shortest.to_string(index=False))

# ============================================================
# CELL 13 (index 13): Top 10 Longest/Shortest Verses
# ============================================================
print("\n--- Cell 13 ---")
df["verse_ref"] = df["chapter"].astype(str) + ":" + df["verse_number"].astype(str)

top10_long_verses = df.nlargest(10, "word_count")[
    ["verse_ref", "word_count", "char_count"]
]
top10_short_verses = df.nsmallest(10, "word_count")[
    ["verse_ref", "word_count", "char_count"]
]

print("Top 10 Longest Verses (by word count):")
print(top10_long_verses.to_string(index=False))
print("\nTop 10 Shortest Verses (by word count):")
print(top10_short_verses.to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].barh(
    top10_long_verses["verse_ref"], top10_long_verses["word_count"], color="coral"
)
axes[0].set_xlabel("Word Count")
axes[0].set_title("Top 10 Longest Verses", fontweight="bold")
axes[0].invert_yaxis()
axes[1].barh(
    top10_short_verses["verse_ref"], top10_short_verses["word_count"], color="skyblue"
)
axes[1].set_xlabel("Word Count")
axes[1].set_title("Top 10 Shortest Verses", fontweight="bold")
axes[1].invert_yaxis()
plt.tight_layout()
plt.savefig("/tmp/cell13_plot.png")
plt.close()
print("[Plot: Top 10 Longest/Shortest Verses - saved]")

# ============================================================
# CELL 15 (index 15): Top 50 Most Frequent Words
# ============================================================
print("\n--- Cell 15 ---")
all_words = []
for text in df["text"]:
    words = text.split()
    all_words.extend(words)

word_counts = Counter(all_words)
top50 = word_counts.most_common(50)

words_list, counts_list = zip(*top50)

fig, ax = plt.subplots(figsize=(12, 10))
ax.barh(
    range(len(words_list)),
    counts_list,
    color=sns.color_palette("viridis", len(words_list)),
)
ax.set_yticks(range(len(words_list)))
ax.set_yticklabels(words_list, fontsize=10)
ax.invert_yaxis()
ax.set_xlabel("Frequency", fontsize=12)
ax.set_title("Top 50 Most Frequent Words in the Quran", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("/tmp/cell15_plot.png")
plt.close()
print("[Plot: Top 50 Most Frequent Words - saved]")

# ============================================================
# CELL 17 (index 17): Meaningful Words
# ============================================================
print("\n--- Cell 17 ---")
stop_words = {
    "وَ",
    "فِى",
    "مِن",
    "عَلَىٰ",
    "إِلَىٰ",
    "لَا",
    "مَا",
    "هُمْ",
    "وَلَا",
    "ٱلَّذِينَ",
    "فِيهَا",
    "لَهُمْ",
    "وَمَا",
    "إِنَّ",
    "كَانُوا۟",
    "ٱلَّذِى",
    "بِهِ",
    "قَالَ",
    "ثُمَّ",
    "وَلَهُمْ",
    "إِلَّا",
    "عَلَيْهِمْ",
    "وَإِذَا",
    "فَلَا",
    "أَنَّ",
    "هُوَ",
    "كُلِّ",
    "بِمَا",
    "لَكُمْ",
    "أَن",
    "قُلْ",
    "كَانَ",
    "ذَٰلِكَ",
    "بِهِۦ",
    "وَهُوَ",
    "فَإِنَّ",
    "لَّهُمْ",
    "وَمَنْ",
    "وَإِن",
    "أَوْ",
    "فِيهِ",
    "بَعْدِ",
    "قَبْلِ",
    "إِذَا",
    "هُمُ",
    "وَقَالَ",
    "وَلَقَدْ",
    "إِنَّهُ",
    "قَدْ",
    "لَمْ",
    "بِهِمْ",
    "وَكَانَ",
    "وَلَوْ",
    "حَتَّىٰ",
    "كُلَّ",
    "إِنَّا",
    "وَعَلَىٰ",
}

filtered = {w: c for w, c in word_counts.items() if w not in stop_words and len(w) > 3}

top40_meaningful = Counter(filtered).most_common(40)
words_m, counts_m = zip(*top40_meaningful)

fig, ax = plt.subplots(figsize=(12, 9))
ax.barh(range(len(words_m)), counts_m, color=sns.color_palette("magma", len(words_m)))
ax.set_yticks(range(len(words_m)))
ax.set_yticklabels(words_m, fontsize=10)
ax.invert_yaxis()
ax.set_xlabel("Frequency", fontsize=12)
ax.set_title(
    "Top 40 Meaningful Words (Particles Filtered)", fontsize=14, fontweight="bold"
)
plt.tight_layout()
plt.savefig("/tmp/cell17_plot.png")
plt.close()
print("[Plot: Top 40 Meaningful Words - saved]")

# ============================================================
# CELL 19 (index 19): Word Cloud
# ============================================================
print("\n--- Cell 19 ---")
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    from wordcloud import WordCloud

    full_text = " ".join(df["text"])
    reshaped_text = arabic_reshaper.reshape(full_text)
    bidi_text = get_display(reshaped_text)

    wc = WordCloud(
        width=1200,
        height=600,
        background_color="white",
        max_words=200,
        colormap="viridis",
        font_path=None,
    ).generate(bidi_text)

    fig, ax = plt.subplots(figsize=(14, 7))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    ax.set_title("Word Cloud of the Quran", fontsize=16, fontweight="bold")
    plt.tight_layout()
    plt.savefig("/tmp/cell19_plot.png")
    plt.close()
    print("[Plot: Word Cloud - saved]")
except ImportError as e:
    print(f"Word cloud skipped — missing package: {e}")
    print("Install with: pip install wordcloud arabic-reshaper python-bidi")

    full_text = " ".join(df["text"])
    try:
        from wordcloud import WordCloud as WC2

        wc = WC2(
            width=1200,
            height=600,
            background_color="white",
            max_words=200,
            colormap="viridis",
        ).generate(full_text)
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        ax.set_title(
            "Word Cloud of the Quran (raw, no reshaping)",
            fontsize=16,
            fontweight="bold",
        )
        plt.tight_layout()
        plt.savefig("/tmp/cell19_plot.png")
        plt.close()
        print("[Plot: Word Cloud (raw) - saved]")
    except Exception:
        print("WordCloud package not available. Skipping word cloud.")

# ============================================================
# CELL 21 (index 21): Letter/Character Frequency
# ============================================================
print("\n--- Cell 21 ---")


def strip_tashkeel(text):
    tashkeel_pattern = re.compile(
        r"[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06DC\u06DF-\u06E8\u06EA-\u06ED\u08D3-\u08E1\u08E3-\u08FF\uFE70-\uFE7F]"
    )
    text = tashkeel_pattern.sub("", text)
    text = text.replace("\u0640", "")
    return text


def extract_arabic_letters(text):
    arabic_letters = re.findall(r"[\u0621-\u064A\u0671-\u06D3]", text)
    return arabic_letters


full_text = " ".join(df["text"])
clean_text = strip_tashkeel(full_text)
letters = extract_arabic_letters(clean_text)

letter_counts = Counter(letters)
letter_freq = pd.DataFrame(letter_counts.most_common(), columns=["letter", "count"])

print(f"Total Arabic letters (no diacritics): {len(letters):,}")
print(f"Unique letters: {len(letter_counts)}")
print()

fig, ax = plt.subplots(figsize=(14, 6))
colors_lf = plt.cm.coolwarm(letter_freq["count"] / letter_freq["count"].max())
ax.bar(letter_freq["letter"], letter_freq["count"], color=colors_lf)
ax.set_xlabel("Arabic Letter", fontsize=12)
ax.set_ylabel("Frequency", fontsize=12)
ax.set_title(
    "Arabic Letter Frequency Distribution (Diacritics Stripped)",
    fontsize=14,
    fontweight="bold",
)
plt.tight_layout()
plt.savefig("/tmp/cell21_plot.png")
plt.close()
print("[Plot: Letter Frequency Distribution - saved]")

print("\nTop 10 most frequent letters:")
for _, row in letter_freq.head(10).iterrows():
    print(f"  {row['letter']}: {row['count']:,}")

# ============================================================
# CELL 23 (index 23): Verse Length Distribution
# ============================================================
print("\n--- Cell 23 ---")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(df["word_count"], bins=50, color="teal", edgecolor="white", alpha=0.8)
axes[0].set_xlabel("Word Count per Verse", fontsize=12)
axes[0].set_ylabel("Number of Verses", fontsize=12)
axes[0].set_title(
    "Distribution of Verse Lengths (Words)", fontsize=13, fontweight="bold"
)
axes[0].axvline(
    df["word_count"].mean(),
    color="red",
    linestyle="--",
    label=f"Mean: {df['word_count'].mean():.1f}",
)
axes[0].axvline(
    df["word_count"].median(),
    color="orange",
    linestyle="--",
    label=f"Median: {df['word_count'].median():.1f}",
)
axes[0].legend()

axes[1].hist(df["char_count"], bins=50, color="coral", edgecolor="white", alpha=0.8)
axes[1].set_xlabel("Character Count per Verse", fontsize=12)
axes[1].set_ylabel("Number of Verses", fontsize=12)
axes[1].set_title(
    "Distribution of Verse Lengths (Characters)", fontsize=13, fontweight="bold"
)
axes[1].axvline(
    df["char_count"].mean(),
    color="red",
    linestyle="--",
    label=f"Mean: {df['char_count'].mean():.1f}",
)
axes[1].axvline(
    df["char_count"].median(),
    color="orange",
    linestyle="--",
    label=f"Median: {df['char_count'].median():.1f}",
)
axes[1].legend()

plt.tight_layout()
plt.savefig("/tmp/cell23_plot.png")
plt.close()
print("[Plot: Verse Length Distribution - saved]")

print(
    f"Word count stats: mean={df['word_count'].mean():.1f}, median={df['word_count'].median():.0f}, "
    f"std={df['word_count'].std():.1f}, min={df['word_count'].min()}, max={df['word_count'].max()}"
)

# ============================================================
# CELL 25 (index 25): Box Plot by Chapter Thirds
# ============================================================
print("\n--- Cell 25 ---")


def chapter_group(ch):
    if ch <= 38:
        return "Chapters 1-38 (Early/Long)"
    elif ch <= 76:
        return "Chapters 39-76 (Middle)"
    else:
        return "Chapters 77-114 (Late/Short)"


df["chapter_group"] = df["chapter"].apply(chapter_group)

fig, ax = plt.subplots(figsize=(12, 6))
group_order = [
    "Chapters 1-38 (Early/Long)",
    "Chapters 39-76 (Middle)",
    "Chapters 77-114 (Late/Short)",
]
sns.boxplot(
    data=df, x="chapter_group", y="word_count", order=group_order, palette="Set2", ax=ax
)
ax.set_xlabel("Chapter Group", fontsize=12)
ax.set_ylabel("Words per Verse", fontsize=12)
ax.set_title(
    "Verse Length Distribution by Chapter Group", fontsize=14, fontweight="bold"
)

for i, grp in enumerate(group_order):
    subset = df[df["chapter_group"] == grp]["word_count"]
    ax.text(
        i,
        subset.max() + 2,
        f"n={len(subset)}\nμ={subset.mean():.1f}",
        ha="center",
        fontsize=9,
    )

plt.tight_layout()
plt.savefig("/tmp/cell25_plot.png")
plt.close()
print("[Plot: Verse Length by Chapter Group - saved]")

# ============================================================
# CELL 27 (index 27): Muqatta'at
# ============================================================
print("\n--- Cell 27 ---")
muqattaat_chapters = []

for ch in df["chapter"].unique():
    first_verse = df[df["chapter"] == ch].iloc[0]
    text = first_verse["text"].strip()
    clean = strip_tashkeel(text).replace(" ", "")
    if len(clean) <= 5 and first_verse["word_count"] <= 3:
        arabic_only = re.sub(r"[^\u0621-\u064A\u0671-\u06D3]", "", clean)
        if len(arabic_only) >= 1 and len(arabic_only) <= 5:
            muqattaat_chapters.append(
                {"chapter": ch, "muqattaat": text, "letters_clean": arabic_only}
            )

muq_df = pd.DataFrame(muqattaat_chapters)
print(f"Chapters beginning with Huruf Muqattaat: {len(muq_df)}\n")
for _, row in muq_df.iterrows():
    print(
        f"  Chapter {row['chapter']:>3}: {row['muqattaat']}  (base letters: {row['letters_clean']})"
    )

# ============================================================
# CELL 29 (index 29): Verse Count Progression
# ============================================================
print("\n--- Cell 29 ---")
fig, ax = plt.subplots(figsize=(14, 5))
ax.scatter(
    chapter_stats["chapter"],
    chapter_stats["verse_count"],
    c=chapter_stats["verse_count"],
    cmap="viridis",
    s=40,
    alpha=0.8,
    edgecolors="k",
    linewidths=0.3,
)
ax.plot(
    chapter_stats["chapter"],
    chapter_stats["verse_count"],
    color="gray",
    alpha=0.3,
    linewidth=0.8,
)
ax.set_xlabel("Chapter Number", fontsize=12)
ax.set_ylabel("Number of Verses", fontsize=12)
ax.set_title("Verse Count Progression Across Chapters", fontsize=14, fontweight="bold")

for _, row in chapter_stats.nlargest(5, "verse_count").iterrows():
    ax.annotate(
        f"Ch {int(row['chapter'])}",
        (row["chapter"], row["verse_count"]),
        textcoords="offset points",
        xytext=(5, 5),
        fontsize=8,
    )

ax.set_xlim(0, 115)
plt.tight_layout()
plt.savefig("/tmp/cell29_plot.png")
plt.close()
print("[Plot: Verse Count Progression - saved]")

# ============================================================
# CELL 31 (index 31): Bigrams and Trigrams
# ============================================================
print("\n--- Cell 31 ---")
from itertools import islice


def get_ngrams(text_series, n):
    ngram_counts = Counter()
    for text in text_series:
        words = text.split()
        for i in range(len(words) - n + 1):
            ngram = " ".join(words[i : i + n])
            ngram_counts[ngram] += 1
    return ngram_counts


bigrams = get_ngrams(df["text"], 2)
trigrams = get_ngrams(df["text"], 3)

top20_bi = bigrams.most_common(20)
top20_tri = trigrams.most_common(20)

fig, axes = plt.subplots(1, 2, figsize=(16, 8))

bi_words, bi_counts = zip(*top20_bi)
axes[0].barh(
    range(len(bi_words)), bi_counts, color=sns.color_palette("viridis", len(bi_words))
)
axes[0].set_yticks(range(len(bi_words)))
axes[0].set_yticklabels(bi_words, fontsize=9)
axes[0].invert_yaxis()
axes[0].set_xlabel("Frequency")
axes[0].set_title("Top 20 Bigrams", fontsize=13, fontweight="bold")

tri_words, tri_counts = zip(*top20_tri)
axes[1].barh(
    range(len(tri_words)), tri_counts, color=sns.color_palette("magma", len(tri_words))
)
axes[1].set_yticks(range(len(tri_words)))
axes[1].set_yticklabels(tri_words, fontsize=9)
axes[1].invert_yaxis()
axes[1].set_xlabel("Frequency")
axes[1].set_title("Top 20 Trigrams", fontsize=13, fontweight="bold")

plt.tight_layout()
plt.savefig("/tmp/cell31_plot.png")
plt.close()
print("[Plot: Top 20 Bigrams and Trigrams - saved]")

# ============================================================
# CELL 33 (index 33): Key Theological Terms Heatmap
# ============================================================
print("\n--- Cell 33 ---")


def strip_tashkeel_for_search(text):
    pattern = re.compile(
        r"[\u064B-\u065F\u0610-\u061A\u0670\u06D6-\u06DC\u06DF-\u06E8\u06EA-\u06ED]"
    )
    return pattern.sub("", text)


full_text_raw = " ".join(df["text"])
full_text_stripped = strip_tashkeel_for_search(full_text_raw)

key_terms = {
    "Allah": r"\bٱلله|\bلله|\bبٱلله|\bوٱلله",
    "Rabb": r"رب",
    "Yawm": r"يوم",
    "Jannah": r"جن[ةـ]|جنت",
    "Nar": r"ٱلنار|نار",
    "Rahmah": r"رحم|رحيم|ٱلرحمـن|ٱلرحمن",
    "Adhab": r"عذاب",
    "Iman": r"ءامن|يؤمن|مؤمن|ٱلمؤمن",
}

term_chapter_data = {}
for term_name, pattern in key_terms.items():
    counts_per_chapter = []
    for ch in range(1, 115):
        ch_text = " ".join(df[df["chapter"] == ch]["text"])
        ch_stripped = strip_tashkeel_for_search(ch_text)
        count = len(re.findall(pattern, ch_stripped))
        counts_per_chapter.append(count)
    term_chapter_data[term_name] = counts_per_chapter

term_df = pd.DataFrame(term_chapter_data, index=range(1, 115))
term_df.index.name = "Chapter"

fig, ax = plt.subplots(figsize=(14, 10))
sns.heatmap(
    term_df.T,
    cmap="YlOrRd",
    ax=ax,
    cbar_kws={"label": "Occurrences"},
    xticklabels=5,
    yticklabels=True,
)
ax.set_xlabel("Chapter Number", fontsize=12)
ax.set_ylabel("Key Term", fontsize=12)
ax.set_title(
    "Key Theological Terms Frequency Across Chapters (Heatmap)",
    fontsize=14,
    fontweight="bold",
)
plt.tight_layout()
plt.savefig("/tmp/cell33_plot.png")
plt.close()
print("[Plot: Key Theological Terms Heatmap - saved]")

# ============================================================
# CELL 34 (index 34): Total Term Frequency Bar Chart
# ============================================================
print("\n--- Cell 34 ---")
total_per_term = term_df.sum().sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(
    total_per_term.index,
    total_per_term.values,
    color=sns.color_palette("Set2", len(total_per_term)),
)
ax.set_xlabel("Total Occurrences Across All Chapters", fontsize=12)
ax.set_title("Total Frequency of Key Theological Terms", fontsize=14, fontweight="bold")
for i, v in enumerate(total_per_term.values):
    ax.text(v + 10, i, str(v), va="center", fontsize=10)
plt.tight_layout()
plt.savefig("/tmp/cell34_plot.png")
plt.close()
print("[Plot: Total Theological Terms Frequency - saved]")

# ============================================================
# CELL 36 (index 36): Summary
# ============================================================
print("\n--- Cell 36 ---")
print("=== Quran Analysis Summary ===")
print(f'Total chapters: {df["chapter"].nunique()}')
print(f"Total verses: {len(df):,}")
print(f'Total words: {df["word_count"].sum():,}')
print(f'Total characters: {df["char_count"].sum():,}')
print(f'Average words per verse: {df["word_count"].mean():.1f}')
print(
    f'Longest chapter: Ch {chapter_stats.loc[chapter_stats["total_words"].idxmax(), "chapter"]} ({chapter_stats["total_words"].max():,} words)'
)
print(
    f'Shortest chapter: Ch {chapter_stats.loc[chapter_stats["total_words"].idxmin(), "chapter"]} ({chapter_stats["total_words"].min()} words)'
)
print(f"Chapters with Muqattaat: {len(muq_df)}")
print("Analysis complete.")

# ============================================================
# PART 2: JSON-based analysis (cells 38-48)
# ============================================================

# ============================================================
# CELL 38 (index 38): Imports for Part 2
# ============================================================
print("\n--- Cell 38 ---")
print("All imports loaded successfully.")

# ============================================================
# CELL 39 (index 39): Load All 114 Chapters
# ============================================================
print("\n--- Cell 39 ---")
chapters_dir = "/Users/sbaio/quran_parsing/chapters/"

all_chapters = []
all_verses_json = []

for i in range(1, 115):
    filepath = os.path.join(chapters_dir, f"chapter_{i}.json")
    with open(filepath, "r", encoding="utf-8") as f:
        chapter_data = json.load(f)
    all_chapters.append(chapter_data)
    for verse in chapter_data["verses"]:
        verse["chapter_number"] = chapter_data["chapter"]
        all_verses_json.append(verse)

print(f"Loaded {len(all_chapters)} chapters with {len(all_verses_json)} total verses.")
print(f"\nSample verse structure (Chapter 1, Verse 1):")
for key, value in all_verses_json[0].items():
    print(f"  {key}: {repr(value)}")

# ============================================================
# CELL 40 (index 40): Build DataFrames
# ============================================================
print("\n--- Cell 40 ---")
verses_records = []
for v in all_verses_json:
    text_ar = v["text_uthmani"]
    word_count_arabic = len(text_ar.split())
    verses_records.append(
        {
            "chapter_number": v["chapter_number"],
            "verse_number": v["verse_number"],
            "verse_key": v["verse_key"],
            "text_uthmani": text_ar,
            "text_imlaei": v["text_imlaei"],
            "word_count_arabic": word_count_arabic,
            "juz_number": v["juz_number"],
            "hizb_number": v["hizb_number"],
            "page_number": v["page_number"],
            "ruku_number": v["ruku_number"],
        }
    )

verses_df = pd.DataFrame(verses_records)

chapters_agg = (
    verses_df.groupby("chapter_number")
    .agg(
        verse_count=("verse_number", "count"),
        total_word_count=("word_count_arabic", "sum"),
        avg_words_per_verse=("word_count_arabic", "mean"),
        min_verse_words=("word_count_arabic", "min"),
        max_verse_words=("word_count_arabic", "max"),
    )
    .reset_index()
)

chapters_df = chapters_agg.copy()
chapters_df["avg_words_per_verse"] = chapters_df["avg_words_per_verse"].round(2)

print(f"verses_df shape: {verses_df.shape}")
print(f"chapters_df shape: {chapters_df.shape}")
print(f"\nverses_df columns: {list(verses_df.columns)}")
print(f"chapters_df columns: {list(chapters_df.columns)}")
print(f"\nverses_df head:")
print(verses_df.head().to_string())

# ============================================================
# CELL 41 (index 41): Basic Statistics
# ============================================================
print("\n--- Cell 41 ---")
print("=" * 60)
print("BASIC QURAN STATISTICS")
print("=" * 60)
print(f"Total chapters (surahs): {len(chapters_df)}")
print(f"Total verses (ayahs):    {len(verses_df)}")
print(f"\nVerses per chapter:")
print(f'  Average: {chapters_df["verse_count"].mean():.1f}')
print(
    f'  Min:     {chapters_df["verse_count"].min()} (Chapter {chapters_df.loc[chapters_df["verse_count"].idxmin(), "chapter_number"]})'
)
print(
    f'  Max:     {chapters_df["verse_count"].max()} (Chapter {chapters_df.loc[chapters_df["verse_count"].idxmax(), "chapter_number"]})'
)
print(f'  Median:  {chapters_df["verse_count"].median():.0f}')

print(f'\n{"─" * 60}')
print("TOP 10 LONGEST CHAPTERS (by verse count):")
print("─" * 60)
top10_longest_j = chapters_df.nlargest(10, "verse_count")[
    ["chapter_number", "verse_count", "total_word_count"]
]
for _, row in top10_longest_j.iterrows():
    print(
        f'  Chapter {int(row["chapter_number"]):>3}: {int(row["verse_count"]):>4} verses, {int(row["total_word_count"]):>5} words'
    )

print(f'\n{"─" * 60}')
print("TOP 10 SHORTEST CHAPTERS (by verse count):")
print("─" * 60)
top10_shortest_j = chapters_df.nsmallest(10, "verse_count")[
    ["chapter_number", "verse_count", "total_word_count"]
]
for _, row in top10_shortest_j.iterrows():
    print(
        f'  Chapter {int(row["chapter_number"]):>3}: {int(row["verse_count"]):>4} verses, {int(row["total_word_count"]):>5} words'
    )

# ============================================================
# CELL 42 (index 42): Distribution of Chapter Lengths
# ============================================================
print("\n--- Cell 42 ---")
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

axes[0].hist(
    chapters_df["verse_count"],
    bins=30,
    color="steelblue",
    edgecolor="white",
    alpha=0.85,
)
axes[0].set_title("Distribution of Verses per Chapter")
axes[0].set_xlabel("Number of Verses")
axes[0].set_ylabel("Number of Chapters")
axes[0].axvline(
    chapters_df["verse_count"].mean(),
    color="red",
    linestyle="--",
    linewidth=1.5,
    label=f'Mean: {chapters_df["verse_count"].mean():.1f}',
)
axes[0].axvline(
    chapters_df["verse_count"].median(),
    color="orange",
    linestyle="--",
    linewidth=1.5,
    label=f'Median: {chapters_df["verse_count"].median():.0f}',
)
axes[0].legend()

axes[1].boxplot(
    chapters_df["verse_count"],
    vert=True,
    patch_artist=True,
    boxprops=dict(facecolor="steelblue", alpha=0.7),
)
axes[1].set_title("Box Plot of Verses per Chapter")
axes[1].set_ylabel("Number of Verses")
axes[1].set_xticklabels(["All Chapters"])

plt.tight_layout()
plt.savefig("/tmp/cell42_plot.png")
plt.close()
print("[Plot: Distribution of Chapter Lengths - saved]")

# ============================================================
# CELL 43 (index 43): Arabic Text Analysis
# ============================================================
print("\n--- Cell 43 ---")
print("=" * 60)
print("ARABIC TEXT ANALYSIS")
print("=" * 60)

total_words_j = verses_df["word_count_arabic"].sum()
print(f"Total Arabic word count: {total_words_j:,}")
print(f'Average words per verse: {verses_df["word_count_arabic"].mean():.2f}')
print(f'Average words per chapter: {chapters_df["total_word_count"].mean():.1f}')
print(f'Median words per verse: {verses_df["word_count_arabic"].median():.0f}')

longest_idx = verses_df["word_count_arabic"].idxmax()
longest = verses_df.loc[longest_idx]
print(f'\n{"─" * 60}')
print(f'LONGEST VERSE ({longest["word_count_arabic"]} words) — {longest["verse_key"]}:')
text_preview = longest["text_uthmani"]
if len(text_preview) > 200:
    print(f"  {text_preview[:200]}...")
else:
    print(f"  {text_preview}")

shortest_idx = verses_df["word_count_arabic"].idxmin()
shortest = verses_df.loc[shortest_idx]
print(
    f'\nSHORTEST VERSE ({shortest["word_count_arabic"]} words) — {shortest["verse_key"]}:'
)
print(f'  {shortest["text_uthmani"]}')

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
axes[0].hist(
    verses_df["word_count_arabic"], bins=50, color="teal", edgecolor="white", alpha=0.85
)
axes[0].set_title("Distribution of Verse Lengths (Arabic Word Count)")
axes[0].set_xlabel("Words per Verse")
axes[0].set_ylabel("Number of Verses")
axes[0].axvline(
    verses_df["word_count_arabic"].mean(),
    color="red",
    linestyle="--",
    label=f'Mean: {verses_df["word_count_arabic"].mean():.1f}',
)
axes[0].legend()

sorted_wc = sorted(verses_df["word_count_arabic"])
cdf = [i / len(sorted_wc) for i in range(1, len(sorted_wc) + 1)]
axes[1].plot(sorted_wc, cdf, color="teal", linewidth=2)
axes[1].set_title("Cumulative Distribution of Verse Lengths")
axes[1].set_xlabel("Words per Verse")
axes[1].set_ylabel("Cumulative Proportion")
axes[1].axhline(0.5, color="gray", linestyle=":", alpha=0.5)
axes[1].axhline(0.9, color="gray", linestyle=":", alpha=0.5)

plt.tight_layout()
plt.savefig("/tmp/cell43_plot.png")
plt.close()
print("[Plot: Verse Lengths Distribution and CDF - saved]")

# ============================================================
# CELL 44 (index 44): Arabic Word Frequency Top 30
# ============================================================
print("\n--- Cell 44 ---")
all_arabic_words = []
for text in verses_df["text_uthmani"]:
    words = text.split()
    all_arabic_words.extend(words)

arabic_word_counts = Counter(all_arabic_words)
top30_arabic = arabic_word_counts.most_common(30)

print(f"Total Arabic words: {len(all_arabic_words):,}")
print(f"Unique Arabic words: {len(arabic_word_counts):,}")
print(f"\nTop 30 most common Arabic words:")
for i, (word, count) in enumerate(top30_arabic, 1):
    print(f"  {i:>2}. {word:>30}  — {count:>5} occurrences")

fig, ax = plt.subplots(figsize=(14, 10))
words_list_ar = [w for w, c in top30_arabic]
counts_list_ar = [c for w, c in top30_arabic]
ax.barh(range(len(words_list_ar)), counts_list_ar, color="darkcyan", edgecolor="white")
ax.set_yticks(range(len(words_list_ar)))
ax.set_yticklabels(words_list_ar, fontsize=14)
ax.invert_yaxis()
ax.set_xlabel("Frequency")
ax.set_title("Top 30 Most Common Arabic Words in the Quran (Uthmani Script)")
for i, count in enumerate(counts_list_ar):
    ax.text(count + 20, i, str(count), va="center", fontsize=10)
plt.tight_layout()
plt.savefig("/tmp/cell44_plot.png")
plt.close()
print("[Plot: Top 30 Arabic Words - saved]")

# ============================================================
# CELL 45 (index 45): English Translation Analysis
# ============================================================
print("\n--- Cell 45 ---")
print("=" * 60)
print("ENGLISH TRANSLATION ANALYSIS")
print("=" * 60)
print("\nNote: The chapter JSON files contain only Arabic text fields:")
print("  - text_uthmani (Uthmani script)")
print("  - text_imlaei (Imlaei script)")
print("\nNo English translation field is present in the data.")
print("To enable English analysis, translation data would need to be")
print("added to the JSON files or loaded from a separate source.")

# ============================================================
# CELL 46 (index 46): Chapter-Level Bar Charts
# ============================================================
print("\n--- Cell 46 ---")
fig, ax = plt.subplots(figsize=(20, 6))
colors_vc = plt.cm.viridis(
    chapters_df["verse_count"] / chapters_df["verse_count"].max()
)
ax.bar(
    chapters_df["chapter_number"],
    chapters_df["verse_count"],
    color=colors_vc,
    edgecolor="none",
    width=0.8,
)
ax.set_title("Verse Count per Chapter (All 114 Surahs)")
ax.set_xlabel("Chapter Number")
ax.set_ylabel("Number of Verses")
ax.set_xticks(range(1, 115, 5))
ax.set_xlim(0.5, 114.5)
plt.tight_layout()
plt.savefig("/tmp/cell46_plot1.png")
plt.close()

fig, ax = plt.subplots(figsize=(20, 6))
colors_wc = plt.cm.magma(
    chapters_df["total_word_count"] / chapters_df["total_word_count"].max()
)
ax.bar(
    chapters_df["chapter_number"],
    chapters_df["total_word_count"],
    color=colors_wc,
    edgecolor="none",
    width=0.8,
)
ax.set_title("Total Word Count per Chapter (All 114 Surahs)")
ax.set_xlabel("Chapter Number")
ax.set_ylabel("Total Words")
ax.set_xticks(range(1, 115, 5))
ax.set_xlim(0.5, 114.5)
plt.tight_layout()
plt.savefig("/tmp/cell46_plot2.png")
plt.close()

most_words = chapters_df.loc[chapters_df["total_word_count"].idxmax()]
fewest_words = chapters_df.loc[chapters_df["total_word_count"].idxmin()]
print(f"[Plot: Verse Count per Chapter - saved]")
print(f"[Plot: Word Count per Chapter - saved]")
print(
    f'Chapter with MOST words:   Chapter {int(most_words["chapter_number"])} — {int(most_words["total_word_count"]):,} words ({int(most_words["verse_count"])} verses)'
)
print(
    f'Chapter with FEWEST words: Chapter {int(fewest_words["chapter_number"])} — {int(fewest_words["total_word_count"]):,} words ({int(fewest_words["verse_count"])} verses)'
)

# ============================================================
# CELL 47 (index 47): Verse Position Analysis
# ============================================================
print("\n--- Cell 47 ---")
position_stats = (
    verses_df[verses_df["verse_number"] <= 50]
    .groupby("verse_number")
    .agg(
        avg_word_count=("word_count_arabic", "mean"),
        median_word_count=("word_count_arabic", "median"),
        count=("word_count_arabic", "count"),
    )
    .reset_index()
)

fig, ax = plt.subplots(figsize=(16, 6))
ax.plot(
    position_stats["verse_number"],
    position_stats["avg_word_count"],
    color="steelblue",
    linewidth=2,
    marker="o",
    markersize=4,
    label="Mean",
)
ax.plot(
    position_stats["verse_number"],
    position_stats["median_word_count"],
    color="coral",
    linewidth=2,
    marker="s",
    markersize=4,
    alpha=0.7,
    label="Median",
)
ax.set_title("Average Verse Length by Verse Position Within Chapter (Positions 1-50)")
ax.set_xlabel("Verse Position (within chapter)")
ax.set_ylabel("Average Word Count")
ax.legend()
ax.set_xlim(0.5, 50.5)
ax.set_xticks(range(1, 51, 2))

ax2 = ax.twinx()
ax2.bar(
    position_stats["verse_number"],
    position_stats["count"],
    alpha=0.15,
    color="gray",
    width=0.8,
    label="# chapters with this position",
)
ax2.set_ylabel("Number of Chapters with This Verse Position", color="gray")
ax2.tick_params(axis="y", labelcolor="gray")

plt.tight_layout()
plt.savefig("/tmp/cell47_plot.png")
plt.close()
print("[Plot: Average Verse Length by Position - saved]")
print("Interpretation: This plot shows whether verses tend to get longer or shorter")
print("as chapters progress. The gray bars show how many chapters have each position")
print("(all 114 have verse 1, but fewer have verse 50+).")

# ============================================================
# CELL 48 (index 48): Summary Table
# ============================================================
print("\n--- Cell 48 ---")
pd.set_option("display.max_rows", 120)
pd.set_option("display.max_columns", 10)
pd.set_option("display.width", 120)

summary = chapters_df[
    [
        "chapter_number",
        "verse_count",
        "total_word_count",
        "avg_words_per_verse",
        "min_verse_words",
        "max_verse_words",
    ]
].copy()
summary.columns = [
    "Chapter",
    "Verses",
    "Total Words",
    "Avg Words/Verse",
    "Min Verse Words",
    "Max Verse Words",
]
summary = summary.set_index("Chapter")

print("=" * 80)
print("FULL SUMMARY TABLE — ALL 114 CHAPTERS")
print("=" * 80)
print(summary.to_string())
