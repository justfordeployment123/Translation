# Transcribing *Salaf-e-Saliheen ke Aqaid o Nazariyat*

Rules for typing this book's pages, on top of the general ones in [PIPELINE.md](../../PIPELINE.md) (steps 2 and 3). The rules were worked out and tested over 535 pages of the previous book, *100 Haraam Karobaar*; **page numbers in parentheses in the general sections below ("page 37", "pages 48, 56") are worked examples in `books/haraam-karobaar/`**, which is fully proofread. This book's own worked examples are `page_060.txt` and `page_061.txt` here.

Every word typed here will later be paid for in ElevenLabs credits and shown on screen, so a page is finished only when it matches the scan exactly.

## The book

- *سلف صالحین کے عقائد و نظریات*, the Urdu edition (Darussalam) of *الوجيز في عقيدة السلف الصالح*: the creed of the early generations (Ahl as-Sunnah wal-Jama'ah), set out with Quran and hadith.
- **PDF page = book page − 3** (book page 10 is PDF page 7), checked for every page. The PDF holds book pages 5–196 only: pages 5–9 are the contents and are not transcribed, the text runs from page 10 (عرضِ ناشر) to page 196, and the book's later pages (from the ninth principle on) are not in this PDF. Page 196's last sentence may run on to page 197, which we don't have: type what page 196 prints and log it.
- Structure: عرضِ ناشر (10), پیش لفظ (13), مقدمہ (26), «ضروری تعریفیں» (definitions, 31), then the principles: «پہلا اصول» (60) ... «آٹھواں اصول» (188), each with sub-headings (printed with ◇ or in bold).
- **The pages are phone photos of the printed book**, not a digital scan: the page is slightly curved, the photo often shows the edge of the facing page, and sometimes a finger at the bottom. Arabic is printed with full harakat.

## Reading a page

- Render the page large and read it in two overlapping halves: `python3 render_page.py Salaf-Saliheen-ke-Aqaid.pdf NNN --offset -3 --out <folder>`. For the finest detail (harakat, footnotes), extract the photo itself, `pdfimages -f N -l N -j Salaf-Saliheen-ke-Aqaid.pdf <folder>/x` with N = NNN − 3, and zoom into it; the photos are 144 dpi, so rendering above about 300 dpi only enlarges them.
- **Not transcribed:** the running title in the coloured tab at the top of the page («پہلا اصول», «فہرست», ...), the page number at the bottom, decorative graphics, and anything from the facing page visible at the photo's edge.
- **Text hidden or cut off** by a finger, the curve of the page or the photo's edge is restored only when certain from the visible part and the context, and logged: `# Text restored where a finger covers the line: "..."`; if not certain, `# Proofreader please check: ...`.
- Read every word against the image. Never complete a sentence from memory or from what "should" be there.

## The page file

`page_NNN.txt`, where NNN is the printed page number, starts with header comments (never spoken):

```
# title: Page 60
# Salaf-e-Saliheen ke Aqaid o Nazariyat, book page 60 (PDF page 57), پہلا اصول: ایمان اور ارکانِ ایمان
# <any text moved to or from the next page, any correction, any uncertainty>
```

Then tagged blocks, separated by a blank line, in the order printed:

| Tag | Use |
|---|---|
| `[h]` | A heading: section, principle, or sub-heading |
| `[ur]` | Urdu text: one paragraph |
| `[ar]` | Arabic: Quran, hadith, Arabic sayings or titles |
| `[ref]` | A source reference: a footnote or inline reference that only cites (shown, not spoken) |
| `[fn]` | An explanatory footnote: prose that explains, defines or adds to the text (shown, not spoken for now; translated in the English edition) |

A page with no text at all (a picture or a blank page) gets no file; say so in your report.

## Headings

- A principle: the running tab «پہلا اصول» and the large title on its first page become one heading: `پہلا اصول: ایمان اور ارکانِ ایمان`.
- The front sections are headed as printed: `عرضِ ناشر`, `پیش لفظ`, `مقدمہ`, `ضروری تعریفیں`.
- Sub-headings (a line marked ◇, or a bold line standing on its own) are `[h]` as printed, without the ◇. A bold lead-in that runs on in the same line as its paragraph (`ایمان باللہ (اللہ پر ایمان لانا): ...`) stays inside the `[ur]` block.

## Text that runs across a page break

- A sentence that starts on one page and ends on the next is typed **whole on the page where it starts**, and left out of the next page. Both pages say so in their header (see pages 17 and 18).
- An Arabic passage, or a quoted translation (“...”), is a single unit: it goes whole on the page where it starts (see pages 37 and 38).
- The same applies inside a turn: a page can open with a nameless `[ur]` block that continues the previous page's turn.
- So at the edges of your range: read the top of the page after your last page to finish a sentence, and the bottom of the page before your first page to know whether your first page starts mid-sentence.

## Urdu text

- **Exactly as printed:** the same words, spelling (تمھارا, انھیں, لیے as printed), and punctuation (، ۔ ؟ ! :). Do not modernise, reword or "improve".
- Spacing may be normalised where the print joins words loosely: separate compound verbs and phrases (ہوجائے → ہو جائے, کرلو → کر لو, پروانہیں → پروا نہیں, زیرنظر → زیر نظر; زیرِ only when the zer is printed). Keep ہوگا / ہوگی / ہوں گے as printed.
- Quotation marks: the book's ''...'' or "..." become “...”.
- **Numbers in spoken text are written as words**: «100 روپے» → «سو روپے», «1/2» → «آدھا». Digits appear only in `[ref]` blocks. A number printed both as a word and in digits («تہتر (73)») keeps only the word, logged (page 48 of this book). Numbered list markers (①, 1-) are read as ordinal words that agree with the items' noun: «پہلا، دوسرا» for masculine items (دورہ, نقصان), «پہلی، دوسری» for feminine ones (حکمت, بات); write them as `پہلی: ...` at the start of the item. Drop them when every item starts with its own heading or with Arabic (a hadith), since a number word cannot go in an `[ar]` block (page 49). When only some items open with Arabic, keep the ordinals for all of them, so none is skipped: an item that opens with Arabic gets its ordinal alone in an `[ur]` block (`پہلی:`) before the `[ar]` (pages 491–492).
- **Abbreviations** spelled in Urdu letters are written without punctuation between the letters, so the voice doesn't pause inside them: «اے، سی» → «اے سی».
- **Dates and amounts** are written as they are said: «14,1,2012» → «چودہ جنوری دو ہزار بارہ», «9500» → «نو ہزار پانچ سو».
- **Words ending in ى pronounced as a long a** take the dagger alif even when the print leaves it out, so the voice reads them right: فتویٰ, تقویٰ, تعالیٰ, حتیٰ, اعلیٰ, موسیٰ, عیسیٰ.
- **A missing word that reverses the meaning** (usually «نہ» in «نہ ... اور نہ ...») is added when the fix is clear from the sentence, and logged as a print typo with "Proofreader please check", because otherwise the voice reads the opposite (page 337). When the fix is not clear, type as printed and log it. The single-«نہ» idiom between two short items with no comma («دوستی رکھے نہ دشمنی», «کھایا نہ پیا») is correct Urdu, heard as "neither ... nor", and stays as printed; the first «نہ» is added only where a comma splits the pair and the first half reads affirmative («وہ رسول کی تصدیق کرے، نہ تکذیب», page 146 of this book).
- **A numbered list printed on one line** stays one block: «پہلی: ایجابی۔ دوسری: سلبی۔» (page 438). When the print separates its items only by the circled numbers, put «،» before each ordinal after the first and log it, so the voice doesn't run the items together (pages 453, 472, 549).
- **A label standing alone on its line above a paragraph** («زندگی کی انشورنس:») is a list item with its ordinal (`پہلی: زندگی کی انشورنس: ...`), not a heading, when the labels are numbered; an unnumbered one is `[h]`.
- **Obvious print typos** are corrected and logged in the header: `# Print typo corrected: "او وہ بھی" -> "اور وہ بھی".` Only when there is no doubt.
- **Anything unclear** is typed as best read and logged: `# Proofreader please check: "..." (smudged in the scan)`.

## Honorifics

- «ﷺ» (or the printed «صلی اللہ علیہ وسلم» ligature) is typed as `ﷺ`; it is spoken in full later. If the book prints the words, type the words.
- Every other honorific is typed **in full words**, matching the person: رضی اللہ عنہ / رضی اللہ عنہا / رضی اللہ عنہما / رضی اللہ عنہم, رحمہ اللہ, علیہ السلام. Never use the small symbols ؓ ؒ ؑ: they cannot tell a man from a woman or one from two.

## Footnotes and references

**A verse's reference follows the block that carries its marker.** In this book the marker of a verse's reference is printed after the verse's Urdu translation. When the Arabic starts at the foot of a page (and is kept whole there) but its translation is printed on the next page, the reference stays on the next page, after the translation (page 160 of this book), not after the Arabic. It moves back with the verse only when the block with the marker is itself kept on the earlier page.

**This book has many long explanatory footnotes** (on miracles, karamat, the kinds of nifaq, ...). Those go in `[fn]` blocks, not `[ref]`, because the English edition translates them (a `[ref]` is copied into it unchanged) and because they may be voiced later:
- A footnote with any explanatory prose is `[fn]`, one block per printed paragraph, typed as printed. One that gives a source and then explains («طٰهٰ 5:20، امام اسحاق بن راہویہ رحمہ اللہ نے ... فرمایا ...») is `[fn]` as a whole. One that only cites («جامع الترمذي، الإيمان، حديث: 2641.», «یونس 64-62:10.») stays `[ref]`.
- It goes straight after the block that carries its marker, like any footnote. When it runs on to the next page or pages (the print opens the continuation with «»»», not typed), each part stays on the page where it is printed, in `[fn]` blocks after that page's own blocks; a sentence crossing the page break goes whole on the page where it starts. The continuation is in the footnote's type, below the rule, even when it fills the page (page 172 of this book).
- A signature under a section (the publisher's on page 12, the foreword writer's on 25, the author's on 30: name, title, place, date) is also `[fn]`: shown, not spoken, and translated in the English edition.
- A Quran verse quoted inside it is filled on its own line inside the `[fn]` block (`# quran ...` comment, then the filled line), with its printed translation on the next line (page 95 of this book).

The footnote text goes in a `[ref]` block straight after the block that carries its marker (①), typed as printed, numbers included, without the marker. Several footnotes for one block become several `[ref]` blocks. A footnote or inline reference printed on the next page, for a verse or hadith that is kept whole on this page, moves with it (pages 173, 265, 349). An inline reference such as «[البقرة: 208]» is a `[ref]` after the verse. Keep Arabic letters as printed in references (للحاكم, not للحاکم) and type the digits in the order they appear on the page, left to right («[491/5]», «[المطففين: 6,1]»), so the app shows them as printed. Write a number group without spaces inside it («[المطففين:3- 1]» → «[المطففين:3-1]»), or the app may reverse it. The one exception is digits joined by an underscore («[البقرة: 278_279]»): the app shows those reversed, so type them right to left («279_278») to make it look like the print.

## Quran

Never typed by hand. Write a placeholder alone on its line in an `[ar]` block, one ayah per `[ar]` block. A verse quoted inside a hadith splits the hadith into several `[ar]` blocks, each verse followed by its printed reference (page 20):

```
{{Q 2:208 from يَا أَيُّهَا الَّذِينَ to مُبِينٌ}}
```

- `from` = **the first 2–3 words the book prints**, `to` = **the last 2–3 words the book prints**, both typed in the plain Tanzil spelling (يَا أَيُّهَا, not Uthmani يٰٓاَيُّهَا). The fill then confirms the book's reference and copies exactly the part the book quotes. Never use a `from` that skips the book's first words (that drops them).
- If the reference is missing, or a phrase is not found, search: `python3 find_source.py "<words>" --quran`. If the book's reference is wrong, use the right ayah, keep the printed `[ref]`, and log it: `# Proofreader please check: the book cites [البقرة: 200]; the words are 2:201.`
- Run `python3 fill_quran.py books/salaf-aqaid/page_NNN.txt`; it must say "OK, identical to the official text".

## Hadith

This book's footnotes give the collection, its book and the hadith number («صحیح مسلم، الایمان، حدیث: 8»). Bukhari's numbers usually match the sources; Muslim's printed numbers are the standard (Abd al-Baqi) ones, which the hadith-api numbers differently, so always confirm the report by its text with `find_source.py`, and keep the book's number in the `[ref]`.

The Prophet's words are never typed by hand when they are in the official collections.

1. Search by a distinctive phrase from the print: `python3 find_source.py "<4–6 words>"` (Bukhari, Muslim, Abu Dawud, Tirmidhi, Nasa'i, Ibn Majah, Malik). The book's footnotes give volume/page, not hadith numbers, so search by text even when a collection is named.
2. Write the placeholder, with `from` = the first printed words of the quoted part and `to` = the last ones: `{{H tirmidhi:3428 from مَنْ دَخَلَ to فَقَالَ}}`. Narrator lead-ins the book prints in Arabic («عَنْ أَبِي هُرَيْرَةَ ...») are typed by hand before the placeholder, on the same line.
3. **When the book's wording matches the source, but only in parts** (excerpts may be joined only from reports of the same hadith, never a word taken from an unrelated one; a different Companion's report of the same Prophetic words counts as the same hadith, and a join that uses one is logged with "Proofreader please check" naming both reports) (a narration joined from two reports, or a vowel slip in the source), build it from several excerpts so the result reads exactly as the book prints, and explain it in the header. Page 37 is the example: Tirmidhi 3428 has «لاَ شَرِيكُ لَهُ» (a slip) and lacks the book's ending, so the text is joined from 3428 and 3429.
4. **When the wording differs and no excerpt reproduces it**: fill the official text and log the difference with "Proofreader please check".
5. **When the hadith is not in these collections, or the book prints the wording of a source outside them** (for example it cites Tirmidhi but prints as-Silsilah as-Sahihah's wording, which is the one its translation follows) (al-Mustadrak, Musnad Ahmad, al-Bayhaqi, at-Tabarani, ...): type it **exactly as printed, with the printed harakat**, give the last word before each pause its stopping form (waqf: final vowel → sukun, «ـةٍ» → «ـةْ», «ـًا» → «ـَا»; `python3 -c "from fill_quran import waqf; print(waqf('دَرَجَةٍ'))"`), and log it: `# Hadith typed from the print (not in the hadith-api collections): المستدرك للحاكم.` An obvious vowel slip in the print («نُبِتَ» for «نَبَتَ») is corrected, because it would be read aloud, and logged with "Proofreader please check" (page 19).
6. Run `python3 fill_hadith.py books/salaf-aqaid/page_NNN.txt`; it must say "OK, identical to the source text".
7. Search with `#n` when a phrase occurs more than once in the hadith (`to الْجَنَّةِ#2`), and add ` flat` only where the source's own punctuation would pause mid-phrase.
8. Pauses inside a hadith follow the book's commas, «؟» and «!» (split into excerpts there when the source has no pause); the colon after «قَالَ» / «قُلْنَا» is not a pause, but a colon that introduces a list or an explanation («ثَلَاثٌ ... وَجَدَ حَلَاوَةَ الْإِيمَانِ: أَنْ يَكُونَ ...») is (page 161 of this book).
9. When the book starts its quote without the source's joined «وَ» or «فَ» («الْإِثْمُ» where the source has «وَالإِثْمُ», «مَنْ» for «فَمَنْ»), start the `from` phrase with `~`: `{{H muslim:6516 from ~الإِثْمُ#2 to النَّاسُ}}`. It matches the word with or without the joined conjunction and leaves the conjunction out.
10. When joined excerpts meet mid-phrase (no pause in the book between them), end the first one with ` cont` so its last word keeps its vowel and the voice runs on: `{{H ibnmajah:12 from مَا to اللَّهِ cont}} {{H ibnmajah:12 from مِثْلُ to اللَّهُ}}`. Without it every excerpt ends in a stop.
11. The narrative words between the Prophet's words («قَالَ», «قَالُوا», «قُلْنَا») follow the source too. When the book's differ («قَالَ: وَمَنْ هِيَ» where Tirmidhi has «قَالُوا وَمَنْ هِيَ»), keep the source's and log it as a print slip; never borrow a single word from elsewhere in the report just to reproduce the print (page 43 of this book).

Arabic typed from the print must be read in the original photo, zoomed in: in this font the sukun and the damma look almost the same. The photos are 144 dpi, so rendering higher only enlarges them; extract the photo itself, `pdfimages -f N -l N -j Salaf-Saliheen-ke-Aqaid.pdf <folder>/x` (N = book page − 3), and zoom into it: a damma has a filled round head, a sukun is a thin open curl.

## Arabic poetry

One verse (both halves, joined by «، », whether printed side by side or stacked on two lines) per `[ar]` block, typed as printed with its harakat, the rhyme vowel kept, and no waqf (pages 32, 159, 211).

## Arabic inside an Urdu sentence

- **Words of the Quran or of a hadith quoted to be recited and explained** are `[ar]`, however short, so they are recited in Arabic (page 42: «وَإِذَا كَالُوهُمْ» explained word by word; page 121: «يَدًا بِيَدٍ» then its translation). The sentence is split around them, even when that leaves a short `[ur]` fragment after the verse (page 81 of this book: «... اس آیت:», then 20:5 in `[ar]`, then «کے متعلق سوال کیا ...»).
- **An Arabic term used as part of an Urdu sentence** (the name of a transaction, a word being defined, a set phrase, or a hadith's own word used as a name, such as «طِينَةُ الْخَبَالِ سے مراد») stays inside that sentence's `[ur]` block. The test: if an Urdu word (سے، کا، کی، ہے، کہتے ہیں) attaches to the Arabic within the sentence, it is a term in the sentence. It is typed as printed with its harakat, its last word in the stopping form, so the sentence is read in one flow and never leaves fragments such as «ہے۔» on their own (pages 48, 56, 138, 194).

## Other Arabic

A Companion's or a scholar's own saying quoted on its own (not the Prophet's words) is typed from the print as other Arabic, even when a collection records it; only the Prophet's words are filled. Narration that is part of a hadith report (the Companion's «قَالَتْ: فَجَعَلْنَا مِنْهُ ...» inside it) is filled together with that hadith. Quranic words used as an everyday phrase (إنا لله وإنا إليه راجعون on hearing of a death, بسم اللہ, ان شاء اللہ) are set phrases: inside an Urdu sentence they stay in the `[ur]` block in Urdu spelling.

Arabic that is neither Quran nor hadith (sayings, duas from other sources, book titles, Arabic terms quoted on their own) is typed exactly as printed, harakat included, with waqf on the last word before each pause. Use Arabic letters in `[ar]` (ي ك ه ة), not the Urdu ones (ی ک ہ). Dagger-alif spellings are typed in the standard form («اللّٰهُ» → «اللَّهُ», «حَتّٰى» → «حَتَّى»); a sukun printed on a long vowel («حَكَمُوْا») is kept.

## Checks before a page is done

```bash
python3 fill_quran.py  books/salaf-aqaid/page_NNN.txt   # if it has {{Q ...}}
python3 fill_hadith.py books/salaf-aqaid/page_NNN.txt   # if it has {{H ...}}
python3 check_pages.py books/salaf-aqaid/page_NNN.txt  # must report 0 problems
```

Then read the page file once more against the image, word by word.

Never start a header comment line with `# hadith ` or `# quran `, even when a note wraps onto a new line: those prefixes mark filled lines, and the checks will try to rebuild the line below. Start such lines with other words (`# The hadith ...`).

Never run Unicode normalisation (NFC/NFD) or other bulk rewrites over a page's Arabic: it changes the filled Quran and hadith text. If a fill check fails after an edit, re-run `fill_quran.py` / `fill_hadith.py` on the page.
