# Quran & Bible: Comparative Content Analysis

A thematic and narrative comparison of the Quran and Bible, exploring shared figures, common narratives, theological themes, and unique content in each scripture.

---

## 1. Corpus Overview

This study analyzes two foundational Abrahamic scriptures using keyword-based textual analysis across their English translations.

| Metric | Bible | Quran |
|--------|-------|-------|
| Total Verses | 31,103 | 6,236 |
| Books / Surahs | 66 books | 114 surahs |
| Primary Divisions | Old Testament (23,145 verses) + New Testament (7,958 verses) | Meccan (4,613 verses) + Medinan (1,623 verses) |

The Bible is roughly five times larger by verse count. The Quran's surahs are divided by revelation context: Meccan surahs (revealed in Mecca, generally earlier) focus on theology and the hereafter, while Medinan surahs (revealed in Medina) tend to address community law and social matters.

---

## 2. Shared Prophets & Figures

Both the Quran and Bible share many prophets and key figures. Each figure was searched using regex patterns covering name variants (English and Arabic transliteration).

### Mention Counts

| Figure | Bible (verses) | Quran (verses) |
|--------|:--------------:|:---------------:|
| Jesus / Isa | 1,209 | 37 |
| David / Dawud | 894 | 17 |
| Moses / Musa | 786 | 169 |
| Jacob / Yaqub | 347 | 24 |
| Aaron / Harun | 333 | 24 |
| Abraham / Ibrahim | 281 | 74 |
| Solomon / Sulaiman | 272 | 23 |
| Joseph / Yusuf | 228 | 47 |
| John / Yahya | 130 | 5 |
| Isaac / Ishaq | 123 | 17 |
| Lot / Lut | 97 | 48 |
| Noah / Nuh | 51 | 54 |
| Mary / Maryam | 46 | 31 |
| Ishmael / Ismail | 44 | 13 |
| Jonah / Yunus | 29 | 4 |
| Adam | 19 | 25 |

All 16 figures were found in both scriptures. The Bible's much larger corpus naturally yields higher absolute counts for most figures. Notable observations:

- **Moses / Musa** is the most frequently mentioned prophet in the Quran (169 verses), far ahead of the second-most mentioned (Abraham / Ibrahim, 74 verses).
- **Jesus / Isa** dominates the Bible count (1,209 verses), but also appears meaningfully in the Quran (37 verses).
- **Noah / Nuh** and **Adam** are among the few figures mentioned more frequently in the Quran than in the Bible in absolute terms (54 vs. 51 and 25 vs. 19, respectively).

### Where Figures Appear Most

**Bible — Top Books per Figure:**

| Figure | Top Books |
|--------|-----------|
| Adam | Genesis (8), 1 Corinthians (2), 1 Timothy (2) |
| Noah / Nuh | Genesis (35), Numbers (3), Luke (3) |
| Abraham / Ibrahim | Genesis (168), Luke (14), Romans (10) |
| Moses / Musa | Exodus (263), Numbers (216), Leviticus (80) |
| Jesus / Isa | John (259), Matthew (176), Luke (115) |
| David / Dawud | 1 Samuel (232), 2 Samuel (226), 1 Chronicles (159) |
| Solomon / Sulaiman | 1 Kings (140), 2 Chronicles (74), 1 Chronicles (24) |
| Joseph / Yusuf | Genesis (137), Numbers (12), Joshua (11) |
| Mary / Maryam | Luke (16), John (14), Matthew (8) |
| Aaron / Harun | Exodus (109), Numbers (97), Leviticus (77) |
| Jacob / Yaqub | Genesis (162), Isaiah (40), Psalms (34) |
| John / Yahya | Luke (30), Matthew (26), Mark (26) |

**Quran — Top Surahs per Figure:**

| Figure | Top Surahs |
|--------|------------|
| Adam | Al-A'raaf (7), Al-Baqara (5), Taa-Haa (5) |
| Noah / Nuh | Hud (14), Nooh (5), Al-A'raaf (3) |
| Abraham / Ibrahim | Al-Baqara (12), Aal-i-Imraan (7), Al-Ankaboot (6) |
| Moses / Musa | Taa-Haa (24), Al-A'raaf (23), Al-Qasas (22) |
| Jesus / Isa | Al-Maaida (9), Aal-i-Imraan (6), An-Nisaa (5) |
| David / Dawud | Saad (6), Al-Anbiyaa (2), An-Naml (2) |
| Solomon / Sulaiman | An-Naml (13), Al-Anbiyaa (3), Saba (2) |
| Joseph / Yusuf | Yusuf (45), Al-An'aam (1), Ghafir (1) |
| Mary / Maryam | Al-Maaida (9), Aal-i-Imraan (6), An-Nisaa (3) |
| Aaron / Harun | Taa-Haa (5), Al-A'raaf (4), Maryam (2) |
| Lot / Lut | Hud (7), Al-Hijr (6), Al-Anbiyaa (4) |
| Isaac / Ishaq | Al-Baqara (3), Yusuf (2), Al-Ankaboot (2) |
| Ishmael / Ismail | Al-Baqara (5), Aal-i-Imraan (1), An-Nisaa (1) |
| Jacob / Yaqub | Yusuf (11), Al-Baqara (4), Maryam (2) |

The Bible concentrates figure narratives in dedicated books (e.g., Joseph's story in Genesis, David's in 1–2 Samuel), while the Quran distributes references across multiple surahs, with notable concentrations such as Joseph/Yusuf in Surah Yusuf (45 of 47 mentions).

---

## 3. Shared Narratives

Both scriptures contain overlapping narratives. Verses related to each narrative were identified using keyword sets covering key terms for each story.

### Verse Counts by Narrative

| Narrative | Bible (verses) | Quran (verses) |
|-----------|:--------------:|:---------------:|
| Creation | 57 | 71 |
| The Flood (Noah) | 238 | 66 |
| Abraham's Trial | 15 | 1 |
| Exodus / Moses & Pharaoh | 409 | 101 |
| David & Goliath | 6 | 3 |
| Jonah & the Whale | 29 | 5 |
| Mary & Jesus' Birth | 57 | 7 |

The Exodus / Pharaoh narrative is the most extensively covered in both texts. The Creation narrative is one of the few where the Quran contains more matching verses than the Bible (71 vs. 57), reflecting its frequent reminders of God's creative power dispersed across many surahs.

### Sample Verses Side by Side

#### Creation

> **Bible** — *Genesis:* "In the beginning, God created the heavens and the earth."
>
> **Quran** — *Al-Baqara:* "Verily, in the creation of the heavens and of the earth, and the succession of night and day: and in the ships that speed through the sea with what is useful to man: and in the waters which God sends down from the sky…"

#### The Flood (Noah)

> **Bible** — *Genesis:* "In the same day Noah, and Shem, Ham, and Japheth—the sons of Noah—and Noah's wife and the three wives of his sons with them, entered into the ship—"
>
> **Quran** — *Nooh:* "[And after a time, Noah] said: 'O my Sustainer! Verily, I have been calling unto my people night and day…'"

#### Abraham's Trial

> **Bible** — *Numbers:* "…and for the sacrifice of peace offerings, two head of cattle, five rams, five male goats, and five male lambs a year old."
>
> **Quran** — *As-Saaffaat:* "And [one day,] when [the child] had become old enough to share in his [father's] endeavours, the latter said: 'O my dear son! I have seen in a dream that I should sacrifice thee: consider, then, what would be thy view!'"

#### Exodus / Moses & Pharaoh

> **Bible** — *Exodus:* "When Pharaoh had let the people go, God didn't lead them by the way of the land of the Philistines, although that was near…"
>
> **Quran** — *Ad-Dukhaan:* "AND, INDEED, [long] before their time did We try Pharaoh's people [in the same way]: for there came unto them a noble apostle…"

#### David & Goliath

> **Bible** — *1 Samuel:* "A champion out of the camp of the Philistines named Goliath, of Gath, whose height was six cubits and a span went out."
>
> **Quran** — *Al-Baqara:* "And when they came face to face with Goliath and his forces, they prayed: 'O our Sustainer! Shower us with patience in adversity, and make firm our steps, and succour us against the people who deny the truth.'"

#### Jonah & the Whale

> **Bible** — *Jonah:* "God said to Jonah, 'Is it right for you to be angry about the vine?' He said, 'I am right to be angry, even to death.'"
>
> **Quran** — *As-Saaffaat:* "[And they cast him into the sea,] whereupon the great fish swallowed him, for he had been blameworthy."

#### Mary & Jesus' Birth

> **Bible** — *Genesis:* "Rachel died, and was buried on the way to Ephrath (also called Bethlehem)."
>
> **Quran** — *Aal-i-Imraan:* "Lo! The angels said: 'O Mary! Behold, God sends thee the glad tiding, through a word from Him, [of a son] who shall become known as the Christ Jesus, son of Mary, of great honour…'"

---

## 4. Core Theological Themes

Both scriptures were analyzed for seven major theological themes using keyword-based detection.

### Theme Counts and Proportions

| Theme | Bible (verses) | Bible (%) | Quran (verses) | Quran (%) |
|-------|:--------------:|:---------:|:---------------:|:---------:|
| Monotheism | 137 | 0.44% | 113 | 1.81% |
| Afterlife / Judgment | 172 | 0.55% | 421 | 6.75% |
| Mercy / Forgiveness | 381 | 1.22% | 460 | 7.38% |
| Prayer / Worship | 688 | 2.21% | 463 | 7.42% |
| Sin / Repentance | 2,269 | 7.30% | 851 | 13.65% |
| Charity / Justice | 998 | 3.21% | 324 | 5.20% |
| Faith / Belief | 627 | 2.02% | 847 | 13.58% |

**Key findings from the thematic comparison:**

- **Sin / Repentance** is the most prominent theme in both texts by absolute count (Bible: 2,269; Quran: 851), and by proportion of total verses (Bible: 7.30%; Quran: 13.65%).
- The **Quran dedicates proportionally far more space** to every theme analyzed. The Afterlife/Judgment theme occupies 6.75% of Quran verses vs. only 0.55% of Bible verses — a 12× proportional difference.
- **Faith / Belief** is proportionally the second-largest theme in the Quran (13.58%) but only 2.02% in the Bible, reflecting the Quran's recurring emphasis on belief as a central obligation.
- **Prayer / Worship** accounts for 7.42% of the Quran vs. 2.21% of the Bible, consistent with the Quran's detailed prescriptions for worship.
- **Mercy / Forgiveness** is proportionally prominent in the Quran (7.38%), where nearly every surah invokes God's mercy ("In the name of God, the Most Gracious, the Most Merciful").

### Thematic Distribution Across Text Sections

**Bible — Theme Distribution by Book Group (% of verses):**

| Book Group | Monotheism | Afterlife | Mercy | Prayer | Sin | Charity | Faith |
|------------|:----------:|:---------:|:-----:|:------:|:---:|:-------:|:-----:|
| Pentateuch | 0.15 | 0.24 | 0.63 | 0.63 | 5.88 | 1.18 | 0.34 |
| Historical | 0.23 | 0.07 | 0.47 | 1.81 | 5.10 | 0.73 | 0.34 |
| Wisdom/Poetry | 0.13 | 0.27 | 1.04 | 3.85 | 11.66 | 7.82 | 1.13 |
| Major Prophets | 1.24 | 0.81 | 0.97 | 2.12 | 9.30 | 3.90 | 0.54 |
| Minor Prophets | 1.33 | 0.10 | 1.52 | 1.52 | 10.19 | 3.71 | 0.48 |
| Gospels | 0.03 | 1.32 | 1.48 | 2.30 | 4.50 | 2.65 | 4.21 |
| Acts & Epistles | 0.82 | 1.30 | 3.81 | 3.10 | 7.97 | 4.79 | 8.74 |
| Revelation | 1.24 | 0.99 | 0.50 | 6.44 | 4.46 | 2.72 | 2.72 |

Notable patterns: Wisdom/Poetry books (Psalms, Proverbs, etc.) have the highest concentration of Sin/Repentance content (11.66%). The Acts & Epistles section leads in Faith/Belief (8.74%) and Mercy/Forgiveness (3.81%). Revelation has the highest Prayer/Worship density (6.44%).

**Quran — Theme Distribution by Surah Group (% of verses):**

| Surah Group | Monotheism | Afterlife | Mercy | Prayer | Sin | Charity | Faith |
|-------------|:----------:|:---------:|:-----:|:------:|:---:|:-------:|:-----:|
| Surahs 1–10 | 2.78 | 6.92 | 9.91 | 10.12 | 20.77 | 7.67 | 24.71 |
| Surahs 11–20 | 1.78 | 7.52 | 9.41 | 8.42 | 13.56 | 4.65 | 8.81 |
| Surahs 21–40 | 2.25 | 6.74 | 6.92 | 8.47 | 11.99 | 5.07 | 12.39 |
| Surahs 41–60 | 0.85 | 6.88 | 7.20 | 4.44 | 11.96 | 4.13 | 12.38 |
| Surahs 61–80 | 0.78 | 7.06 | 4.08 | 3.77 | 9.26 | 3.14 | 6.75 |
| Surahs 81–100 | 0.28 | 4.20 | 1.12 | 1.96 | 5.60 | 4.20 | 5.04 |
| Surahs 101–114 | 1.27 | 1.27 | 1.27 | 11.39 | 10.13 | 2.53 | 1.27 |

The earliest and longest surahs (1–10, which include Al-Baqara and Aal-i-Imraan) are the most thematically dense: 24.71% of their verses relate to Faith/Belief and 20.77% to Sin/Repentance. Afterlife/Judgment maintains a steady 6–7% across most groups. The shorter, later surahs (81–100) show lower thematic density overall, as many are brief eschatological passages.

---

## 5. Unique Content

Concepts and themes that are distinctive to each scripture were identified through targeted keyword searches.

### Bible-Distinctive Concepts

| Concept | Verse Count |
|---------|:-----------:|
| Crucifixion / Resurrection | 305 |
| Covenant | 291 |
| Trinity / Holy Spirit | 95 |
| Grace (Theological) | 91 |
| Original Sin / Fall | 5 |

The Bible's distinctive theological content centers on the **crucifixion and resurrection** of Jesus (305 verses) and the concept of **covenant** between God and His people (291 verses). The **Trinity / Holy Spirit** appears in 95 verses, primarily in the New Testament. **Grace** as a theological concept tied to God/Lord/Christ appears in 91 verses. The explicit concept of **Original Sin** is rare even in the Bible (5 verses), though its theological influence is much broader.

### Quran-Distinctive Concepts

| Concept | Verse Count |
|---------|:-----------:|
| God-consciousness (Taqwa) | 60 |
| Community (Ummah) | 59 |
| Self-Surrender / Islam | 30 |
| Invisible Beings (Jinn) | 26 |
| Consultation (Shura) | 4 |

The Quran's distinctive content includes **God-consciousness (taqwa)** — the concept of pious awareness of God (60 verses) — and a strong emphasis on the believing **community (ummah)** as a collective (59 verses). **Self-surrender (Islam/submission)** as a named religious concept appears in 30 verses. **Jinn** (invisible beings) are unique to the Quran with 26 mentions, including an entire surah (Al-Jinn) dedicated to them. **Consultation (shura)** as a governance principle appears in 4 verses.

---

## 6. Cross-References — Quran References to Biblical Content

The Quran frequently references Biblical figures and scriptures explicitly. A search for direct references to earlier Abrahamic texts and people yielded the following:

| Reference Category | Quran Verses |
|--------------------|:------------:|
| Children of Israel | 49 |
| Followers of Earlier Revelation | 33 |
| Torah | 19 |
| Gospel | 14 |
| Psalms / Zabur | 0 |

A total of **115 Quran verses** explicitly reference Biblical content, positioning the Quran within the Abrahamic tradition and engaging directly with the earlier scriptures.

### Sample Cross-Reference Verses

**Followers of Earlier Revelation (33 verses):**

> *Al-Bayyina 1:* "IT IS NOT [conceivable] that such as are bent on denying the truth — [be they] from among the followers of earlier revelation or from among those who ascribe divinity to aught beside God — should ever have changed their ways…"
>
> *An-Nisaa 159:* "Yet there is not one of the followers of earlier revelation who does not, at the moment of his death, grasp the truth about Jesus; and on the Day of Resurrection he [himself] shall bear witness…"

**Torah (19 verses):**

> *Aal-i-Imraan 3:* "Step by step has He bestowed upon thee from on high this divine writ, setting forth the truth which confirms whatever there still remains [of earlier revelations]: for it is He who bestowed from on high the Torah and the Gospel…"
>
> *Al-Maaida 43:* "But how is it that they ask thee for judgment seeing that they have the Torah, containing God's injunctions — and thereafter turn away [from thy judgment]?"

**Gospel (14 verses):**

> *At-Tawba 111:* "BEHOLD, God has bought of the believers their lives and their possessions, promising them paradise in return, [and so] they fight in God's cause, and slay, and are slain: a promise which is binding on Him in the Torah, and the Gospel, and the Quran."

**Children of Israel (49 verses):**

> *Al-Maaida 70:* "INDEED, We accepted a solemn pledge from the children of Israel, and We sent apostles unto them; [but] every time an apostle came unto them with anything that was not to their liking, [some of them] they called liars and some they would slay."
>
> *As-Saff 6:* "And [this happened, too,] when Jesus, the son of Mary, said: 'O children of Israel! Behold, I am an apostle of God unto you, [sent] to confirm the truth of whatever there still remains of the Torah…'"

---

## 7. Summary Dashboard

| Aspect | Bible | Quran |
|--------|-------|-------|
| Total Verses | 31,103 | 6,236 |
| Books / Surahs | 66 books | 114 surahs |
| Divisions | OT (23,145v) + NT (7,958v) | Meccan (4,613v) + Medinan (1,623v) |
| Top 3 Themes | Sin / Repentance, Charity / Justice, Prayer / Worship | Sin / Repentance, Faith / Belief, Prayer / Worship |
| Top 3 Shared Figures | Jesus / Isa, David / Dawud, Moses / Musa | Moses / Musa, Abraham / Ibrahim, Noah / Nuh |
| Distinctive Concepts | Trinity / Holy Spirit, Crucifixion / Resurrection, Original Sin / Fall, Grace, Covenant | Invisible Beings (Jinn), Self-Surrender / Islam, God-consciousness (Taqwa), Community (Ummah), Consultation (Shura) |
| Cross-References to Other | N/A (predecessor text) | 115 verses referencing Biblical content |
| Revelation Style | Multiple authors over ~1,500 years | Revealed over ~23 years to Prophet Muhammad |

---

## Key Findings

1. **Shared Heritage**: Both scriptures share a large cast of prophets and figures, with Moses/Musa and Abraham/Ibrahim among the most frequently mentioned in both texts. All 16 searched figures were found in both scriptures (16/16).

2. **Narrative Overlap**: The Creation story, Noah's flood, Moses & Pharaoh, and Mary & Jesus' birth appear in both texts, though with different emphases and details. The Bible tends to provide extended sequential narratives in dedicated books, while the Quran revisits these stories across multiple surahs for different rhetorical purposes.

3. **Theological Convergence**: Sin/Repentance is the dominant theme in both scriptures. Monotheism, mercy/forgiveness, and faith/belief are central themes in both, though the Quran devotes proportionally much more space to each (often 3–12× the Bible's percentage).

4. **Distinctive Content**: The Bible's emphasis on covenant (291 verses), crucifixion/resurrection (305 verses), and grace contrasts with the Quran's focus on submission/self-surrender, God-consciousness (taqwa), and jinn.

5. **Intertextual References**: The Quran explicitly references the Torah, Gospel, and Children of Israel in 115 verses, positioning itself within the Abrahamic tradition and engaging with earlier scriptures as part of a continuous revelatory arc.
