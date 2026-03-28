import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import re
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Configure matplotlib for Arabic text support
matplotlib.rcParams['figure.dpi'] = 100
matplotlib.rcParams['figure.figsize'] = (12, 6)
sns.set_style('whitegrid')
sns.set_palette('viridis')

print('Libraries loaded successfully.')

# Quranic stop/pause marks to strip from text before word counting
QURANIC_MARKS = re.compile(r'[\u06D6-\u06DC\u06DD-\u06DE\u06DF-\u06E8\u06EA-\u06ED۞ۖۗۘۙۚۛۜ]')

with open('full_quran.md', 'r', encoding='utf-8') as f:
    content = f.read()

rows = []
current_chapter = None

for line in content.split('\n'):
    line = line.strip()
    # Detect chapter headers
    chapter_match = re.match(r'^## Chapter (\d+)', line)
    if chapter_match:
        current_chapter = int(chapter_match.group(1))
        continue
    # Detect verse lines: **chapter:verse** text
    verse_match = re.match(r'^\*\*(\d+):(\d+)\*\*\s*(.*)', line)
    if verse_match and current_chapter is not None:
        ch = int(verse_match.group(1))
        verse_num = int(verse_match.group(2))
        text = verse_match.group(3).strip()
        # Remove ornamental markers
        text_clean = QURANIC_MARKS.sub('', text).strip()
        # Remove standalone pause marks that became empty tokens
        words = [w for w in text_clean.split() if w.strip()]
        word_count = len(words)
        char_count = len(text_clean.replace(' ', ''))
        rows.append({
            'chapter': ch,
            'verse_number': verse_num,
            'text': text_clean,
            'word_count': word_count,
            'char_count': char_count
        })

df = pd.DataFrame(rows)
print(f'Total verses parsed: {len(df)}')
print(f'Total chapters: {df["chapter"].nunique()}')
print(f'Total words: {df["word_count"].sum():,}')
print(f'Total characters (no spaces): {df["char_count"].sum():,}')
print()
df.head(10)

chapter_stats = df.groupby('chapter').agg(
    verse_count=('verse_number', 'count'),
    total_words=('word_count', 'sum'),
    total_chars=('char_count', 'sum'),
    avg_verse_words=('word_count', 'mean'),
    avg_verse_chars=('char_count', 'mean'),
    max_verse_words=('word_count', 'max'),
    min_verse_words=('word_count', 'min')
).reset_index()

fig, ax = plt.subplots(figsize=(14, 5))
ax.bar(chapter_stats['chapter'], chapter_stats['verse_count'], color=sns.color_palette('viridis', len(chapter_stats)), width=0.8)
ax.set_xlabel('Chapter Number', fontsize=12)
ax.set_ylabel('Number of Verses', fontsize=12)
ax.set_title('Number of Verses per Chapter', fontsize=14, fontweight='bold')
ax.set_xlim(0, 115)
plt.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(14, 5))
colors = plt.cm.plasma(chapter_stats['total_words'] / chapter_stats['total_words'].max())
ax.bar(chapter_stats['chapter'], chapter_stats['total_words'], color=colors, width=0.8)
ax.set_xlabel('Chapter Number', fontsize=12)
ax.set_ylabel('Total Words', fontsize=12)
ax.set_title('Total Words per Chapter', fontsize=14, fontweight='bold')
ax.set_xlim(0, 115)
plt.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(chapter_stats['chapter'], chapter_stats['avg_verse_words'], color='teal', linewidth=1.5, marker='o', markersize=3)
ax.fill_between(chapter_stats['chapter'], chapter_stats['avg_verse_words'], alpha=0.2, color='teal')
ax.set_xlabel('Chapter Number', fontsize=12)
ax.set_ylabel('Average Words per Verse', fontsize=12)
ax.set_title('Average Verse Length (Words) per Chapter', fontsize=14, fontweight='bold')
ax.set_xlim(1, 114)
plt.tight_layout()
plt.show()

top10_longest = chapter_stats.nlargest(10, 'total_words')[['chapter', 'verse_count', 'total_words']]
top10_shortest = chapter_stats.nsmallest(10, 'total_words')[['chapter', 'verse_count', 'total_words']]

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].barh(top10_longest['chapter'].astype(str), top10_longest['total_words'], color=sns.color_palette('Reds_r', 10))
axes[0].set_xlabel('Total Words')
axes[0].set_title('Top 10 Longest Chapters', fontweight='bold')
axes[0].invert_yaxis()
for i, v in enumerate(top10_longest['total_words']):
    axes[0].text(v + 20, i, str(v), va='center', fontsize=9)

axes[1].barh(top10_shortest['chapter'].astype(str), top10_shortest['total_words'], color=sns.color_palette('Blues_r', 10))
axes[1].set_xlabel('Total Words')
axes[1].set_title('Top 10 Shortest Chapters', fontweight='bold')
axes[1].invert_yaxis()
for i, v in enumerate(top10_shortest['total_words']):
    axes[1].text(v + 1, i, str(v), va='center', fontsize=9)

plt.tight_layout()
plt.show()

print('\nTop 10 Longest Chapters:')
print(top10_longest.to_string(index=False))
print('\nTop 10 Shortest Chapters:')
print(top10_shortest.to_string(index=False))

df['verse_ref'] = df['chapter'].astype(str) + ':' + df['verse_number'].astype(str)

top10_long_verses = df.nlargest(10, 'word_count')[['verse_ref', 'word_count', 'char_count']]
top10_short_verses = df.nsmallest(10, 'word_count')[['verse_ref', 'word_count', 'char_count']]

print('Top 10 Longest Verses (by word count):')
print(top10_long_verses.to_string(index=False))
print('\nTop 10 Shortest Verses (by word count):')
print(top10_short_verses.to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].barh(top10_long_verses['verse_ref'], top10_long_verses['word_count'], color='coral')
axes[0].set_xlabel('Word Count')
axes[0].set_title('Top 10 Longest Verses', fontweight='bold')
axes[0].invert_yaxis()

axes[1].barh(top10_short_verses['verse_ref'], top10_short_verses['word_count'], color='skyblue')
axes[1].set_xlabel('Word Count')
axes[1].set_title('Top 10 Shortest Verses', fontweight='bold')
axes[1].invert_yaxis()

plt.tight_layout()
plt.show()

all_words = []
for text in df['text']:
    words = text.split()
    all_words.extend(words)

word_counts = Counter(all_words)
top50 = word_counts.most_common(50)

words_list, counts_list = zip(*top50)

fig, ax = plt.subplots(figsize=(12, 10))
ax.barh(range(len(words_list)), counts_list, color=sns.color_palette('viridis', len(words_list)))
ax.set_yticks(range(len(words_list)))
ax.set_yticklabels(words_list, fontsize=10)
ax.invert_yaxis()
ax.set_xlabel('Frequency', fontsize=12)
ax.set_title('Top 50 Most Frequent Words in the Quran', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

# Common Arabic particles/stop words to filter out
stop_words = {
    'وَ', 'فِى', 'مِن', 'عَلَىٰ', 'إِلَىٰ', 'لَا', 'مَا', 'هُمْ', 'وَلَا',
    'ٱلَّذِينَ', 'فِيهَا', 'لَهُمْ', 'وَمَا', 'إِنَّ', 'كَانُوا۟', 'ٱلَّذِى',
    'بِهِ', 'قَالَ', 'ثُمَّ', 'وَلَهُمْ', 'إِلَّا', 'عَلَيْهِمْ',
    'وَإِذَا', 'فَلَا', 'أَنَّ', 'هُوَ', 'كُلِّ', 'بِمَا', 'لَكُمْ',
    'أَن', 'قُلْ', 'كَانَ', 'ذَٰلِكَ', 'بِهِۦ', 'وَهُوَ', 'فَإِنَّ',
    'لَّهُمْ', 'وَمَنْ', 'وَإِن', 'أَوْ', 'فِيهِ', 'بَعْدِ', 'قَبْلِ',
    'إِذَا', 'هُمُ', 'وَقَالَ', 'وَلَقَدْ', 'إِنَّهُ', 'قَدْ',
    'لَمْ', 'بِهِمْ', 'وَكَانَ', 'وَلَوْ', 'حَتَّىٰ', 'كُلَّ',
    'إِنَّا', 'وَعَلَىٰ'
}

# Also filter single-char and two-char words (mostly particles)
filtered = {w: c for w, c in word_counts.items()
            if w not in stop_words and len(w) > 3}

top40_meaningful = Counter(filtered).most_common(40)
words_m, counts_m = zip(*top40_meaningful)

fig, ax = plt.subplots(figsize=(12, 9))
ax.barh(range(len(words_m)), counts_m, color=sns.color_palette('magma', len(words_m)))
ax.set_yticks(range(len(words_m)))
ax.set_yticklabels(words_m, fontsize=10)
ax.invert_yaxis()
ax.set_xlabel('Frequency', fontsize=12)
ax.set_title('Top 40 Meaningful Words (Particles Filtered)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

try:
    from wordcloud import WordCloud
    import arabic_reshaper
    from bidi.algorithm import get_display

    full_text = ' '.join(df['text'])
    reshaped_text = arabic_reshaper.reshape(full_text)
    bidi_text = get_display(reshaped_text)

    wc = WordCloud(
        width=1200, height=600,
        background_color='white',
        max_words=200,
        colormap='viridis',
        font_path=None
    ).generate(bidi_text)

    fig, ax = plt.subplots(figsize=(14, 7))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    ax.set_title('Word Cloud of the Quran', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()
except ImportError as e:
    print(f'Word cloud skipped — missing package: {e}')
    print('Install with: pip install wordcloud arabic-reshaper python-bidi')

    # Fallback: simple text-based visualization
    full_text = ' '.join(df['text'])
    try:
        wc = WordCloud(
            width=1200, height=600,
            background_color='white',
            max_words=200,
            colormap='viridis'
        ).generate(full_text)
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.imshow(wc, interpolation='bilinear')
        ax.axis('off')
        ax.set_title('Word Cloud of the Quran (raw, no reshaping)', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
    except Exception:
        print('WordCloud package not available. Skipping word cloud.')

def strip_tashkeel(text):
    """Remove Arabic diacritical marks (tashkeel) and non-letter marks."""
    # Unicode ranges for Arabic diacritics
    tashkeel_pattern = re.compile(r'[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06DC\u06DF-\u06E8\u06EA-\u06ED\u08D3-\u08E1\u08E3-\u08FF\uFE70-\uFE7F]')
    # Also remove tatweel, special marks
    text = tashkeel_pattern.sub('', text)
    text = text.replace('\u0640', '')  # tatweel
    return text

def extract_arabic_letters(text):
    """Extract only Arabic base letters."""
    # Arabic letter range: U+0621 to U+064A
    # Plus some extended: alef variants, etc.
    arabic_letters = re.findall(r'[\u0621-\u064A\u0671-\u06D3]', text)
    return arabic_letters

full_text = ' '.join(df['text'])
clean_text = strip_tashkeel(full_text)
letters = extract_arabic_letters(clean_text)

letter_counts = Counter(letters)
letter_freq = pd.DataFrame(letter_counts.most_common(), columns=['letter', 'count'])

print(f'Total Arabic letters (no diacritics): {len(letters):,}')
print(f'Unique letters: {len(letter_counts)}')
print()

fig, ax = plt.subplots(figsize=(14, 6))
colors = plt.cm.coolwarm(letter_freq['count'] / letter_freq['count'].max())
ax.bar(letter_freq['letter'], letter_freq['count'], color=colors)
ax.set_xlabel('Arabic Letter', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('Arabic Letter Frequency Distribution (Diacritics Stripped)', fontsize=14, fontweight='bold')
plt.xticks(fontsize=13)
plt.tight_layout()
plt.show()

print('\nTop 10 most frequent letters:')
for _, row in letter_freq.head(10).iterrows():
    print(f"  {row['letter']}: {row['count']:,}")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(df['word_count'], bins=50, color='teal', edgecolor='white', alpha=0.8)
axes[0].set_xlabel('Word Count per Verse', fontsize=12)
axes[0].set_ylabel('Number of Verses', fontsize=12)
axes[0].set_title('Distribution of Verse Lengths (Words)', fontsize=13, fontweight='bold')
axes[0].axvline(df['word_count'].mean(), color='red', linestyle='--', label=f"Mean: {df['word_count'].mean():.1f}")
axes[0].axvline(df['word_count'].median(), color='orange', linestyle='--', label=f"Median: {df['word_count'].median():.1f}")
axes[0].legend()

axes[1].hist(df['char_count'], bins=50, color='coral', edgecolor='white', alpha=0.8)
axes[1].set_xlabel('Character Count per Verse', fontsize=12)
axes[1].set_ylabel('Number of Verses', fontsize=12)
axes[1].set_title('Distribution of Verse Lengths (Characters)', fontsize=13, fontweight='bold')
axes[1].axvline(df['char_count'].mean(), color='red', linestyle='--', label=f"Mean: {df['char_count'].mean():.1f}")
axes[1].axvline(df['char_count'].median(), color='orange', linestyle='--', label=f"Median: {df['char_count'].median():.1f}")
axes[1].legend()

plt.tight_layout()
plt.show()

print(f"Word count stats: mean={df['word_count'].mean():.1f}, median={df['word_count'].median():.0f}, "
      f"std={df['word_count'].std():.1f}, min={df['word_count'].min()}, max={df['word_count'].max()}")

def chapter_group(ch):
    if ch <= 38:
        return 'Chapters 1-38 (Early/Long)'
    elif ch <= 76:
        return 'Chapters 39-76 (Middle)'
    else:
        return 'Chapters 77-114 (Late/Short)'

df['chapter_group'] = df['chapter'].apply(chapter_group)

fig, ax = plt.subplots(figsize=(12, 6))
group_order = ['Chapters 1-38 (Early/Long)', 'Chapters 39-76 (Middle)', 'Chapters 77-114 (Late/Short)']
sns.boxplot(data=df, x='chapter_group', y='word_count', order=group_order, palette='Set2', ax=ax)
ax.set_xlabel('Chapter Group', fontsize=12)
ax.set_ylabel('Words per Verse', fontsize=12)
ax.set_title('Verse Length Distribution by Chapter Group', fontsize=14, fontweight='bold')

for i, grp in enumerate(group_order):
    subset = df[df['chapter_group'] == grp]['word_count']
    ax.text(i, subset.max() + 2, f'n={len(subset)}\nμ={subset.mean():.1f}', ha='center', fontsize=9)

plt.tight_layout()
plt.show()

# Known Muqatta'at patterns (isolated/disconnected letters)
# These appear as the first verse of certain chapters
muqattaat_chapters = []

for ch in df['chapter'].unique():
    first_verse = df[df['chapter'] == ch].iloc[0]
    text = first_verse['text'].strip()
    # Muqatta'at verses are typically very short (1-5 letters, no spaces or 1-2 words)
    # and consist of Arabic letters with elongation marks
    # Check if the verse is very short and contains typical muqattaat characters
    clean = strip_tashkeel(text).replace(' ', '')
    # Muqattaat are typically 1-5 base letters, sometimes with spaces between
    if len(clean) <= 5 and first_verse['word_count'] <= 3:
        # Additional check: mostly Arabic letters
        arabic_only = re.sub(r'[^\u0621-\u064A\u0671-\u06D3]', '', clean)
        if len(arabic_only) >= 1 and len(arabic_only) <= 5:
            muqattaat_chapters.append({
                'chapter': ch,
                'muqattaat': text,
                'letters_clean': arabic_only
            })

muq_df = pd.DataFrame(muqattaat_chapters)
print(f'Chapters beginning with Huruf Muqattaat: {len(muq_df)}\n')
for _, row in muq_df.iterrows():
    print(f"  Chapter {row['chapter']:>3}: {row['muqattaat']}  (base letters: {row['letters_clean']})")

fig, ax = plt.subplots(figsize=(14, 5))
ax.scatter(chapter_stats['chapter'], chapter_stats['verse_count'],
           c=chapter_stats['verse_count'], cmap='viridis', s=40, alpha=0.8, edgecolors='k', linewidths=0.3)
ax.plot(chapter_stats['chapter'], chapter_stats['verse_count'], color='gray', alpha=0.3, linewidth=0.8)
ax.set_xlabel('Chapter Number', fontsize=12)
ax.set_ylabel('Number of Verses', fontsize=12)
ax.set_title('Verse Count Progression Across Chapters', fontsize=14, fontweight='bold')

# Annotate the largest chapters
for _, row in chapter_stats.nlargest(5, 'verse_count').iterrows():
    ax.annotate(f"Ch {int(row['chapter'])}", (row['chapter'], row['verse_count']),
                textcoords='offset points', xytext=(5, 5), fontsize=8)

ax.set_xlim(0, 115)
plt.tight_layout()
plt.show()

from itertools import islice

def get_ngrams(text_series, n):
    """Extract n-grams from a series of text."""
    ngram_counts = Counter()
    for text in text_series:
        words = text.split()
        for i in range(len(words) - n + 1):
            ngram = ' '.join(words[i:i+n])
            ngram_counts[ngram] += 1
    return ngram_counts

bigrams = get_ngrams(df['text'], 2)
trigrams = get_ngrams(df['text'], 3)

top20_bi = bigrams.most_common(20)
top20_tri = trigrams.most_common(20)

fig, axes = plt.subplots(1, 2, figsize=(16, 8))

# Bigrams
bi_words, bi_counts = zip(*top20_bi)
axes[0].barh(range(len(bi_words)), bi_counts, color=sns.color_palette('viridis', len(bi_words)))
axes[0].set_yticks(range(len(bi_words)))
axes[0].set_yticklabels(bi_words, fontsize=9)
axes[0].invert_yaxis()
axes[0].set_xlabel('Frequency')
axes[0].set_title('Top 20 Bigrams', fontsize=13, fontweight='bold')

# Trigrams
tri_words, tri_counts = zip(*top20_tri)
axes[1].barh(range(len(tri_words)), tri_counts, color=sns.color_palette('magma', len(tri_words)))
axes[1].set_yticks(range(len(tri_words)))
axes[1].set_yticklabels(tri_words, fontsize=9)
axes[1].invert_yaxis()
axes[1].set_xlabel('Frequency')
axes[1].set_title('Top 20 Trigrams', fontsize=13, fontweight='bold')

plt.tight_layout()
plt.show()

def strip_tashkeel_for_search(text):
    """Strip diacritics for fuzzy root-level matching."""
    pattern = re.compile(r'[\u064B-\u065F\u0610-\u061A\u0670\u06D6-\u06DC\u06DF-\u06E8\u06EA-\u06ED]')
    return pattern.sub('', text)

# Key terms — use stripped text for more robust matching
full_text_raw = ' '.join(df['text'])
full_text_stripped = strip_tashkeel_for_search(full_text_raw)

key_terms = {
    'Allah (الله)': r'\bٱلله|\bلله|\bبٱلله|\bوٱلله',
    'Rabb (رب)': r'رب',
    'Yawm (يوم)': r'يوم',
    'Jannah (جنة)': r'جن[ةـ]|جنت',
    'Nar (نار)': r'ٱلنار|نار',
    'Rahmah (رحمة)': r'رحم|رحيم|ٱلرحمـن|ٱلرحمن',
    'Adhab (عذاب)': r'عذاب',
    'Iman (إيمان)': r'ءامن|يؤمن|مؤمن|ٱلمؤمن'
}

# Count per chapter using stripped text
term_chapter_data = {}
for term_name, pattern in key_terms.items():
    counts_per_chapter = []
    for ch in range(1, 115):
        ch_text = ' '.join(df[df['chapter'] == ch]['text'])
        ch_stripped = strip_tashkeel_for_search(ch_text)
        count = len(re.findall(pattern, ch_stripped))
        counts_per_chapter.append(count)
    term_chapter_data[term_name] = counts_per_chapter

term_df = pd.DataFrame(term_chapter_data, index=range(1, 115))
term_df.index.name = 'Chapter'

# Heatmap
fig, ax = plt.subplots(figsize=(14, 10))
sns.heatmap(term_df.T, cmap='YlOrRd', ax=ax, cbar_kws={'label': 'Occurrences'},
            xticklabels=5, yticklabels=True)
ax.set_xlabel('Chapter Number', fontsize=12)
ax.set_ylabel('Key Term', fontsize=12)
ax.set_title('Key Theological Terms Frequency Across Chapters (Heatmap)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

# Grouped bar chart: total mentions per term
total_per_term = term_df.sum().sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(total_per_term.index, total_per_term.values, color=sns.color_palette('Set2', len(total_per_term)))
ax.set_xlabel('Total Occurrences Across All Chapters', fontsize=12)
ax.set_title('Total Frequency of Key Theological Terms', fontsize=14, fontweight='bold')
for i, v in enumerate(total_per_term.values):
    ax.text(v + 10, i, str(v), va='center', fontsize=10)
plt.tight_layout()
plt.show()

print('=== Quran Analysis Summary ===')
print(f'Total chapters: {df["chapter"].nunique()}')
print(f'Total verses: {len(df):,}')
print(f'Total words: {df["word_count"].sum():,}')
print(f'Total characters: {df["char_count"].sum():,}')
print(f'Average words per verse: {df["word_count"].mean():.1f}')
print(f'Longest chapter: Ch {chapter_stats.loc[chapter_stats["total_words"].idxmax(), "chapter"]} ({chapter_stats["total_words"].max():,} words)')
print(f'Shortest chapter: Ch {chapter_stats.loc[chapter_stats["total_words"].idxmin(), "chapter"]} ({chapter_stats["total_words"].min()} words)')
print(f'Chapters with Muqattaat: {len(muq_df)}')
print('Analysis complete.')

# Cell 1: Imports & Setup
import json
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re

# Plot style and defaults
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (14, 6)
plt.rcParams['figure.dpi'] = 100
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

print('All imports loaded successfully.')

# Cell 2: Load All 114 Chapters
chapters_dir = '/Users/sbaio/quran_parsing/chapters/'

all_chapters = []
all_verses = []

for i in range(1, 115):
    filepath = os.path.join(chapters_dir, f'chapter_{i}.json')
    with open(filepath, 'r', encoding='utf-8') as f:
        chapter_data = json.load(f)
    all_chapters.append(chapter_data)
    for verse in chapter_data['verses']:
        verse['chapter_number'] = chapter_data['chapter']
        all_verses.append(verse)

print(f'Loaded {len(all_chapters)} chapters with {len(all_verses)} total verses.')
print(f'\nSample verse structure (Chapter 1, Verse 1):')
for key, value in all_verses[0].items():
    print(f'  {key}: {repr(value)}')

# Cell 3: Build DataFrames

# --- Verses DataFrame ---
verses_records = []
for v in all_verses:
    text_ar = v['text_uthmani']
    word_count_arabic = len(text_ar.split())
    verses_records.append({
        'chapter_number': v['chapter_number'],
        'verse_number': v['verse_number'],
        'verse_key': v['verse_key'],
        'text_uthmani': text_ar,
        'text_imlaei': v['text_imlaei'],
        'word_count_arabic': word_count_arabic,
        'juz_number': v['juz_number'],
        'hizb_number': v['hizb_number'],
        'page_number': v['page_number'],
        'ruku_number': v['ruku_number'],
    })

verses_df = pd.DataFrame(verses_records)

# --- Chapters DataFrame ---
chapters_agg = verses_df.groupby('chapter_number').agg(
    verse_count=('verse_number', 'count'),
    total_word_count=('word_count_arabic', 'sum'),
    avg_words_per_verse=('word_count_arabic', 'mean'),
    min_verse_words=('word_count_arabic', 'min'),
    max_verse_words=('word_count_arabic', 'max'),
).reset_index()

chapters_df = chapters_agg.copy()
chapters_df['avg_words_per_verse'] = chapters_df['avg_words_per_verse'].round(2)

print(f'verses_df shape: {verses_df.shape}')
print(f'chapters_df shape: {chapters_df.shape}')
print(f'\nverses_df columns: {list(verses_df.columns)}')
print(f'chapters_df columns: {list(chapters_df.columns)}')
print(f'\nverses_df head:')
verses_df.head()

# Cell 4: Basic Statistics
print('=' * 60)
print('BASIC QURAN STATISTICS')
print('=' * 60)
print(f'Total chapters (surahs): {len(chapters_df)}')
print(f'Total verses (ayahs):    {len(verses_df)}')
print(f'\nVerses per chapter:')
print(f'  Average: {chapters_df["verse_count"].mean():.1f}')
print(f'  Min:     {chapters_df["verse_count"].min()} (Chapter {chapters_df.loc[chapters_df["verse_count"].idxmin(), "chapter_number"]})')
print(f'  Max:     {chapters_df["verse_count"].max()} (Chapter {chapters_df.loc[chapters_df["verse_count"].idxmax(), "chapter_number"]})')
print(f'  Median:  {chapters_df["verse_count"].median():.0f}')

print(f'\n{"─" * 60}')
print('TOP 10 LONGEST CHAPTERS (by verse count):')
print('─' * 60)
top10_longest = chapters_df.nlargest(10, 'verse_count')[['chapter_number', 'verse_count', 'total_word_count']]
for _, row in top10_longest.iterrows():
    print(f'  Chapter {int(row["chapter_number"]):>3}: {int(row["verse_count"]):>4} verses, {int(row["total_word_count"]):>5} words')

print(f'\n{"─" * 60}')
print('TOP 10 SHORTEST CHAPTERS (by verse count):')
print('─' * 60)
top10_shortest = chapters_df.nsmallest(10, 'verse_count')[['chapter_number', 'verse_count', 'total_word_count']]
for _, row in top10_shortest.iterrows():
    print(f'  Chapter {int(row["chapter_number"]):>3}: {int(row["verse_count"]):>4} verses, {int(row["total_word_count"]):>5} words')

# Cell 5: Distribution of Chapter Lengths
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Histogram
axes[0].hist(chapters_df['verse_count'], bins=30, color='steelblue', edgecolor='white', alpha=0.85)
axes[0].set_title('Distribution of Verses per Chapter')
axes[0].set_xlabel('Number of Verses')
axes[0].set_ylabel('Number of Chapters')
axes[0].axvline(chapters_df['verse_count'].mean(), color='red', linestyle='--', linewidth=1.5, label=f'Mean: {chapters_df["verse_count"].mean():.1f}')
axes[0].axvline(chapters_df['verse_count'].median(), color='orange', linestyle='--', linewidth=1.5, label=f'Median: {chapters_df["verse_count"].median():.0f}')
axes[0].legend()

# Box plot
axes[1].boxplot(chapters_df['verse_count'], vert=True, patch_artist=True,
                boxprops=dict(facecolor='steelblue', alpha=0.7))
axes[1].set_title('Box Plot of Verses per Chapter')
axes[1].set_ylabel('Number of Verses')
axes[1].set_xticklabels(['All Chapters'])

plt.tight_layout()
plt.show()

# Cell 6: Arabic Text Analysis
print('=' * 60)
print('ARABIC TEXT ANALYSIS')
print('=' * 60)

total_words = verses_df['word_count_arabic'].sum()
print(f'Total Arabic word count: {total_words:,}')
print(f'Average words per verse: {verses_df["word_count_arabic"].mean():.2f}')
print(f'Average words per chapter: {chapters_df["total_word_count"].mean():.1f}')
print(f'Median words per verse: {verses_df["word_count_arabic"].median():.0f}')

# Longest verse
longest_idx = verses_df['word_count_arabic'].idxmax()
longest = verses_df.loc[longest_idx]
print(f'\n{"─" * 60}')
print(f'LONGEST VERSE ({longest["word_count_arabic"]} words) — {longest["verse_key"]}:')
print(f'  {longest["text_uthmani"][:200]}...' if len(longest['text_uthmani']) > 200 else f'  {longest["text_uthmani"]}')

# Shortest verse
shortest_idx = verses_df['word_count_arabic'].idxmin()
shortest = verses_df.loc[shortest_idx]
print(f'\nSHORTEST VERSE ({shortest["word_count_arabic"]} words) — {shortest["verse_key"]}:')
print(f'  {shortest["text_uthmani"]}')

# Distribution of verse lengths
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

axes[0].hist(verses_df['word_count_arabic'], bins=50, color='teal', edgecolor='white', alpha=0.85)
axes[0].set_title('Distribution of Verse Lengths (Arabic Word Count)')
axes[0].set_xlabel('Words per Verse')
axes[0].set_ylabel('Number of Verses')
axes[0].axvline(verses_df['word_count_arabic'].mean(), color='red', linestyle='--', label=f'Mean: {verses_df["word_count_arabic"].mean():.1f}')
axes[0].legend()

# CDF
sorted_wc = sorted(verses_df['word_count_arabic'])
cdf = [i / len(sorted_wc) for i in range(1, len(sorted_wc) + 1)]
axes[1].plot(sorted_wc, cdf, color='teal', linewidth=2)
axes[1].set_title('Cumulative Distribution of Verse Lengths')
axes[1].set_xlabel('Words per Verse')
axes[1].set_ylabel('Cumulative Proportion')
axes[1].axhline(0.5, color='gray', linestyle=':', alpha=0.5)
axes[1].axhline(0.9, color='gray', linestyle=':', alpha=0.5)

plt.tight_layout()
plt.show()

# Cell 7: Arabic Word Frequency — Top 30
all_arabic_words = []
for text in verses_df['text_uthmani']:
    words = text.split()
    all_arabic_words.extend(words)

arabic_word_counts = Counter(all_arabic_words)
top30_arabic = arabic_word_counts.most_common(30)

print(f'Total Arabic words: {len(all_arabic_words):,}')
print(f'Unique Arabic words: {len(arabic_word_counts):,}')
print(f'\nTop 30 most common Arabic words:')
for i, (word, count) in enumerate(top30_arabic, 1):
    print(f'  {i:>2}. {word:>30}  — {count:>5} occurrences')

# Bar chart
words_list = [w for w, c in top30_arabic]
counts_list = [c for w, c in top30_arabic]

fig, ax = plt.subplots(figsize=(14, 10))
ax.barh(range(len(words_list)), counts_list, color='darkcyan', edgecolor='white')
ax.set_yticks(range(len(words_list)))
ax.set_yticklabels(words_list, fontsize=14)
ax.invert_yaxis()
ax.set_xlabel('Frequency')
ax.set_title('Top 30 Most Common Arabic Words in the Quran (Uthmani Script)')
for i, count in enumerate(counts_list):
    ax.text(count + 20, i, str(count), va='center', fontsize=10)
plt.tight_layout()
plt.show()

# Cell 8: English Translation Analysis
# The JSON data does not contain English translations — only Arabic text
# (text_uthmani and text_imlaei fields).
# This cell is included for completeness but notes the absence of English data.

print('=' * 60)
print('ENGLISH TRANSLATION ANALYSIS')
print('=' * 60)
print('\nNote: The chapter JSON files contain only Arabic text fields:')
print('  - text_uthmani (Uthmani script)')
print('  - text_imlaei (Imlaei script)')
print('\nNo English translation field is present in the data.')
print('To enable English analysis, translation data would need to be')
print('added to the JSON files or loaded from a separate source.')

# Cell 9: Chapter-Level Bar Charts

# Verse count per chapter
fig, ax = plt.subplots(figsize=(20, 6))
colors = plt.cm.viridis(chapters_df['verse_count'] / chapters_df['verse_count'].max())
ax.bar(chapters_df['chapter_number'], chapters_df['verse_count'], color=colors, edgecolor='none', width=0.8)
ax.set_title('Verse Count per Chapter (All 114 Surahs)')
ax.set_xlabel('Chapter Number')
ax.set_ylabel('Number of Verses')
ax.set_xticks(range(1, 115, 5))
ax.set_xlim(0.5, 114.5)
plt.tight_layout()
plt.show()

# Word count per chapter
fig, ax = plt.subplots(figsize=(20, 6))
colors = plt.cm.magma(chapters_df['total_word_count'] / chapters_df['total_word_count'].max())
ax.bar(chapters_df['chapter_number'], chapters_df['total_word_count'], color=colors, edgecolor='none', width=0.8)
ax.set_title('Total Word Count per Chapter (All 114 Surahs)')
ax.set_xlabel('Chapter Number')
ax.set_ylabel('Total Words')
ax.set_xticks(range(1, 115, 5))
ax.set_xlim(0.5, 114.5)
plt.tight_layout()
plt.show()

# Identify chapters with most/fewest words
most_words = chapters_df.loc[chapters_df['total_word_count'].idxmax()]
fewest_words = chapters_df.loc[chapters_df['total_word_count'].idxmin()]
print(f'Chapter with MOST words:   Chapter {int(most_words["chapter_number"])} — {int(most_words["total_word_count"]):,} words ({int(most_words["verse_count"])} verses)')
print(f'Chapter with FEWEST words: Chapter {int(fewest_words["chapter_number"])} — {int(fewest_words["total_word_count"]):,} words ({int(fewest_words["verse_count"])} verses)')

# Cell 10: Verse Position Analysis
# Average verse length by position within a chapter (first 50 positions)

position_stats = verses_df[verses_df['verse_number'] <= 50].groupby('verse_number').agg(
    avg_word_count=('word_count_arabic', 'mean'),
    median_word_count=('word_count_arabic', 'median'),
    count=('word_count_arabic', 'count'),
).reset_index()

fig, ax = plt.subplots(figsize=(16, 6))
ax.plot(position_stats['verse_number'], position_stats['avg_word_count'],
        color='steelblue', linewidth=2, marker='o', markersize=4, label='Mean')
ax.plot(position_stats['verse_number'], position_stats['median_word_count'],
        color='coral', linewidth=2, marker='s', markersize=4, alpha=0.7, label='Median')
ax.set_title('Average Verse Length by Verse Position Within Chapter (Positions 1–50)')
ax.set_xlabel('Verse Position (within chapter)')
ax.set_ylabel('Average Word Count')
ax.legend()
ax.set_xlim(0.5, 50.5)
ax.set_xticks(range(1, 51, 2))

# Annotate with chapter count
ax2 = ax.twinx()
ax2.bar(position_stats['verse_number'], position_stats['count'],
        alpha=0.15, color='gray', width=0.8, label='# chapters with this position')
ax2.set_ylabel('Number of Chapters with This Verse Position', color='gray')
ax2.tick_params(axis='y', labelcolor='gray')

plt.tight_layout()
plt.show()

print('Interpretation: This plot shows whether verses tend to get longer or shorter')
print('as chapters progress. The gray bars show how many chapters have each position')
print('(all 114 have verse 1, but fewer have verse 50+).')

# Cell 11: Summary Table — All 114 Chapters
pd.set_option('display.max_rows', 120)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 120)

summary = chapters_df[['chapter_number', 'verse_count', 'total_word_count',
                        'avg_words_per_verse', 'min_verse_words', 'max_verse_words']].copy()
summary.columns = ['Chapter', 'Verses', 'Total Words', 'Avg Words/Verse', 'Min Verse Words', 'Max Verse Words']
summary = summary.set_index('Chapter')

print('=' * 80)
print('FULL SUMMARY TABLE — ALL 114 CHAPTERS')
print('=' * 80)
summary

