# Transcribing *100 Haraam Karobaar aur Tijarti Mamlaat*

Rules for typing this book's pages, on top of the general ones in [PIPELINE.md](../../PIPELINE.md) (steps 2 and 3). The finished pages `page_017.txt` to `page_038.txt` are worked examples of these rules (pages 19, 20, 29, 31 and 35 show the headings, a Bismillah, a hadith with verses inside it and numbered lists); read them first.

Every word typed here will later be paid for in ElevenLabs credits and shown on screen, so a page is finished only when it matches the scan exactly.

## The book

- Arabic original: *تحذير الكرام من مائة باب من أبواب الحرام* by Ibrahim bin Fathi bin Abd al-Muqtadir; Urdu edition by Maktaba Bait-us-Salam.
- Book pages 17–564 hold the text (PDF page = book page + 1). **One exception:** the PDF has book pages 278 and 279 in swapped order, so book page 278 is PDF page 280 (`--offset 2`) and book page 279 is PDF page 279 (`--offset 0`). Every other page number was checked against the print. The scans in `scans/` are already named by the printed page number. Pages 1–16 (cover, notices, contents) are not transcribed, and the pages after 564 are the publisher's adverts.
- 100 chapters («پہلا باب» ... «سوواں باب»), grouped in large rounds («پہلا دورہ», «دوسرا دورہ», ...), each made of smaller rounds numbered again from ① («غلہ منڈی کا دورہ», «صرافہ بازار کا دورہ», ...). Most chapters are a story: a teacher (استاد) and his student Ammar (عمار) walk through a market, see a forbidden practice, and discuss its ruling with Quran and hadith.
- The scan is clean, born-digital typesetting. Arabic is printed with full harakat.

## Reading a page

- Render the page large and read it in two overlapping halves: `python3 render_page.py 100-Haraam-Karobaar.pdf NNN --offset 1 --out <folder>`. Re-render at 300 dpi for anything small: harakat, footnotes, superscript honorifics.
- **Not transcribed:** the top line «www.KitaboSunnat.com», the page-number box and running title «100 حرام کاروبار اور تجارتی معاملات», the footer «محکم دلائل و براہین سے مزین ...», and decorative graphics.
- Read every word against the image. Never complete a sentence from memory or from what "should" be there.

## The page file

`page_NNN.txt`, where NNN is the printed page number, starts with header comments (never spoken):

```
# title: Page 37
# 100 Haraam Karobaar aur Tijarti Mamlaat, book page 37 (PDF page 38), <section or chapter>
# <any text moved to or from the next page, any correction, any uncertainty>
```

Then tagged blocks, separated by a blank line, in the order printed:

| Tag | Use |
|---|---|
| `[h]` | A heading: section, chapter, or sub-heading such as «خلاصہ» |
| `[ur]` | Urdu text: one paragraph, or one dialogue turn |
| `[ar]` | Arabic: Quran, hadith, Arabic sayings or titles |
| `[ref]` | A footnote or source reference, typed as printed (shown, not spoken) |

A page with no text at all (a picture or a blank page) gets no file; say so in your report.

## Headings

- Chapter: the small «پہلا باب» line and the large title become one heading: `پہلا باب: ناپ تول میں کمی کرنا`.
- A large round's title page: `[h] پہلا دورہ`, and its list of smaller rounds read with ordinals (page 31).
- A smaller round's title page: `[h] غلہ منڈی کا دورہ`, with the ① dropped (page 35). The rounds are not combined into one heading, because the smaller ones restart at ① in each large round.
- The calligraphic «بسم اللہ الرحمن الرحیم» above a heading is transcribed as an `[ar]` block, `{{Q 1:1}}` (page 19).
- Other printed headings and bold lead-ins standing on their own line (e.g. «خلاصہ», «فائدہ») are `[h]` as printed.

## Dialogue

Each turn is its own `[ur]` block that starts with the speaker's name as printed and a colon: `عمار: شیخ! مجھے وہ دعا یاد نہیں، وہ کونسی دعا ہے؟`. Narration between turns is an ordinary `[ur]` block. Narration that runs on inside a turn's printed paragraph («فوزی: ... دونوں نے گرم جوشی سے معانقہ کیا ...») stays in the turn's block; narration printed as its own paragraph is its own block. List items that start with a bold label take the ordinal and the label: «تیسری: مقدار کا تعین: ...». Bracketed stage directions («(عمار کی طرف دیکھتے ہوئے بولے)») stay inside the turn. A turn that opens straight with a verse or hadith keeps the name alone in its `[ur]` block (`استاد:`), then the `[ar]`; in every other case the name stays with the turn's first words (`استاد: پہلا: ...`). Short Arabic set phrases used in Urdu speech (جزاک اللہ, ان شاء اللہ, السلام علیکم ورحمۃ اللہ) stay inside the `[ur]` block in Urdu spelling, even when printed in Arabic type. When a turn contains Arabic, it is split: `[ur]` (the turn up to the Arabic, with the name), `[ar]`, then `[ur]` for the rest, without repeating the name.

## Text that runs across a page break

- A sentence that starts on one page and ends on the next is typed **whole on the page where it starts**, and left out of the next page. Both pages say so in their header (see pages 17 and 18).
- An Arabic passage, or a quoted translation (“...”), is a single unit: it goes whole on the page where it starts (see pages 37 and 38).
- The same applies inside a turn: a page can open with a nameless `[ur]` block that continues the previous page's turn.
- So at the edges of your range: read the top of the page after your last page to finish a sentence, and the bottom of the page before your first page to know whether your first page starts mid-sentence.

## Urdu text

- **Exactly as printed:** the same words, spelling (تمھارا, انھیں, لیے as printed), and punctuation (، ۔ ؟ ! :). Do not modernise, reword or "improve".
- Spacing may be normalised where the print joins words loosely: separate compound verbs and phrases (ہوجائے → ہو جائے, کرلو → کر لو, پروانہیں → پروا نہیں, زیرنظر → زیر نظر; زیرِ only when the zer is printed). Keep ہوگا / ہوگی / ہوں گے as printed.
- Quotation marks: the book's ''...'' or "..." become “...”.
- **Numbers in spoken text are written as words**: «100 روپے» → «سو روپے», «1/2» → «آدھا». Digits appear only in `[ref]` blocks. Numbered list markers (①, 1-) are read as ordinal words that agree with the items' noun: «پہلا، دوسرا» for masculine items (دورہ, نقصان), «پہلی، دوسری» for feminine ones (حکمت, بات); write them as `پہلی: ...` at the start of the item. Drop them when every item starts with its own heading or with Arabic (a hadith), since a number word cannot go in an `[ar]` block (page 49). When only some items open with Arabic, keep the ordinals for all of them, so none is skipped: an item that opens with Arabic gets its ordinal alone in an `[ur]` block (`پہلی:`) before the `[ar]` (pages 491–492).
- **Abbreviations** spelled in Urdu letters are written without punctuation between the letters, so the voice doesn't pause inside them: «اے، سی» → «اے سی».
- **Dates and amounts** are written as they are said: «14,1,2012» → «چودہ جنوری دو ہزار بارہ», «9500» → «نو ہزار پانچ سو».
- **Words ending in ى pronounced as a long a** take the dagger alif even when the print leaves it out, so the voice reads them right: فتویٰ, تقویٰ, تعالیٰ, حتیٰ, اعلیٰ, موسیٰ, عیسیٰ.
- **A missing word that reverses the meaning** (usually «نہ» in «نہ ... اور نہ ...») is added when the fix is clear from the sentence, and logged as a print typo with "Proofreader please check", because otherwise the voice reads the opposite (page 337). When the fix is not clear, type as printed and log it.
- **A numbered list printed on one line** stays one block: «پہلی: ایجابی۔ دوسری: سلبی۔» (page 438). When the print separates its items only by the circled numbers, put «،» before each ordinal after the first and log it, so the voice doesn't run the items together (pages 453, 472, 549).
- **A label standing alone on its line above a paragraph** («زندگی کی انشورنس:») is a list item with its ordinal (`پہلی: زندگی کی انشورنس: ...`), not a heading, when the labels are numbered; an unnumbered one is `[h]`.
- **Obvious print typos** are corrected and logged in the header: `# Print typo corrected: "او وہ بھی" -> "اور وہ بھی".` Only when there is no doubt.
- **Anything unclear** is typed as best read and logged: `# Proofreader please check: "..." (smudged in the scan)`.

## Honorifics

- «ﷺ» (or the printed «صلی اللہ علیہ وسلم» ligature) is typed as `ﷺ`; it is spoken in full later. If the book prints the words, type the words.
- Every other honorific is typed **in full words**, matching the person: رضی اللہ عنہ / رضی اللہ عنہا / رضی اللہ عنہما / رضی اللہ عنہم, رحمہ اللہ, علیہ السلام. Never use the small symbols ؓ ؒ ؑ: they cannot tell a man from a woman or one from two.

## Footnotes and references

The footnote text goes in a `[ref]` block straight after the block that carries its marker (①), typed as printed, numbers included, without the marker. Several footnotes for one block become several `[ref]` blocks. A footnote or inline reference printed on the next page, for a verse or hadith that is kept whole on this page, moves with it (pages 173, 265, 349). An inline reference such as «[البقرة: 208]» is a `[ref]` after the verse. Keep Arabic letters as printed in references (للحاكم, not للحاکم) and type the digits in the order they appear on the page, left to right («[491/5]», «[المطففين: 6,1]»), so the app shows them as printed. Write a number group without spaces inside it («[المطففين:3- 1]» → «[المطففين:3-1]»), or the app may reverse it. The one exception is digits joined by an underscore («[البقرة: 278_279]»): the app shows those reversed, so type them right to left («279_278») to make it look like the print.

## Quran

Never typed by hand. Write a placeholder alone on its line in an `[ar]` block, one ayah per `[ar]` block. A verse quoted inside a hadith splits the hadith into several `[ar]` blocks, each verse followed by its printed reference (page 20):

```
{{Q 2:208 from يَا أَيُّهَا الَّذِينَ to مُبِينٌ}}
```

- `from` = **the first 2–3 words the book prints**, `to` = **the last 2–3 words the book prints**, both typed in the plain Tanzil spelling (يَا أَيُّهَا, not Uthmani يٰٓاَيُّهَا). The fill then confirms the book's reference and copies exactly the part the book quotes. Never use a `from` that skips the book's first words (that drops them).
- If the reference is missing, or a phrase is not found, search: `python3 find_source.py "<words>" --quran`. If the book's reference is wrong, use the right ayah, keep the printed `[ref]`, and log it: `# Proofreader please check: the book cites [البقرة: 200]; the words are 2:201.`
- Run `python3 fill_quran.py books/haraam-karobaar/page_NNN.txt`; it must say "OK, identical to the official text".

## Hadith

The Prophet's words are never typed by hand when they are in the official collections.

1. Search by a distinctive phrase from the print: `python3 find_source.py "<4–6 words>"` (Bukhari, Muslim, Abu Dawud, Tirmidhi, Nasa'i, Ibn Majah, Malik). The book's footnotes give volume/page, not hadith numbers, so search by text even when a collection is named.
2. Write the placeholder, with `from` = the first printed words of the quoted part and `to` = the last ones: `{{H tirmidhi:3428 from مَنْ دَخَلَ to فَقَالَ}}`. Narrator lead-ins the book prints in Arabic («عَنْ أَبِي هُرَيْرَةَ ...») are typed by hand before the placeholder, on the same line.
3. **When the book's wording matches the source, but only in parts** (excerpts may be joined only from reports of the same hadith, never a word taken from an unrelated one; a different Companion's report of the same Prophetic words counts as the same hadith, and a join that uses one is logged with "Proofreader please check" naming both reports) (a narration joined from two reports, or a vowel slip in the source), build it from several excerpts so the result reads exactly as the book prints, and explain it in the header. Page 37 is the example: Tirmidhi 3428 has «لاَ شَرِيكُ لَهُ» (a slip) and lacks the book's ending, so the text is joined from 3428 and 3429.
4. **When the wording differs and no excerpt reproduces it**: fill the official text and log the difference with "Proofreader please check".
5. **When the hadith is not in these collections, or the book prints the wording of a source outside them** (for example it cites Tirmidhi but prints as-Silsilah as-Sahihah's wording, which is the one its translation follows) (al-Mustadrak, Musnad Ahmad, al-Bayhaqi, at-Tabarani, ...): type it **exactly as printed, with the printed harakat**, give the last word before each pause its stopping form (waqf: final vowel → sukun, «ـةٍ» → «ـةْ», «ـًا» → «ـَا»; `python3 -c "from fill_quran import waqf; print(waqf('دَرَجَةٍ'))"`), and log it: `# Hadith typed from the print (not in the hadith-api collections): المستدرك للحاكم.` An obvious vowel slip in the print («نُبِتَ» for «نَبَتَ») is corrected, because it would be read aloud, and logged with "Proofreader please check" (page 19).
6. Run `python3 fill_hadith.py books/haraam-karobaar/page_NNN.txt`; it must say "OK, identical to the source text".
7. Search with `#n` when a phrase occurs more than once in the hadith (`to الْجَنَّةِ#2`), and add ` flat` only where the source's own punctuation would pause mid-phrase.
8. Pauses inside a hadith follow the book's commas, «؟» and «!» (split into excerpts there when the source has no pause); the colon after «قَالَ» / «قُلْنَا» is not a pause.
9. When the book starts its quote without the source's joined «وَ» or «فَ» («الْإِثْمُ» where the source has «وَالإِثْمُ», «مَنْ» for «فَمَنْ»), start the `from` phrase with `~`: `{{H muslim:6516 from ~الإِثْمُ#2 to النَّاسُ}}`. It matches the word with or without the joined conjunction and leaves the conjunction out.
10. When joined excerpts meet mid-phrase (no pause in the book between them), end the first one with ` cont` so its last word keeps its vowel and the voice runs on: `{{H ibnmajah:12 from مَا to اللَّهِ cont}} {{H ibnmajah:12 from مِثْلُ to اللَّهُ}}`. Without it every excerpt ends in a stop.

Arabic typed from the print must be read at 300–400 dpi: in this font the sukun and the damma look almost the same. The PDF pages are 300 dpi black-and-white images, so rendering higher only enlarges them; for the clearest view extract the page itself, `pdfimages -f N -l N -png 100-Haraam-Karobaar.pdf <folder>/x` (N = PDF page), and zoom into it: a damma has a filled round head, a sukun is a thin open curl.

## Arabic poetry

One verse (both halves, joined by «، », whether printed side by side or stacked on two lines) per `[ar]` block, typed as printed with its harakat, the rhyme vowel kept, and no waqf (pages 32, 159, 211).

## Arabic inside an Urdu sentence

- **Words of the Quran or of a hadith quoted to be recited and explained** are `[ar]`, however short, so they are recited in Arabic (page 42: «وَإِذَا كَالُوهُمْ» explained word by word; page 121: «يَدًا بِيَدٍ» then its translation). The sentence is split around them.
- **An Arabic term used as part of an Urdu sentence** (the name of a transaction, a word being defined, a set phrase, or a hadith's own word used as a name, such as «طِينَةُ الْخَبَالِ سے مراد») stays inside that sentence's `[ur]` block. The test: if an Urdu word (سے، کا، کی، ہے، کہتے ہیں) attaches to the Arabic within the sentence, it is a term in the sentence. It is typed as printed with its harakat, its last word in the stopping form, so the sentence is read in one flow and never leaves fragments such as «ہے۔» on their own (pages 48, 56, 138, 194).

## Other Arabic

A Companion's or a scholar's own saying quoted on its own (not the Prophet's words) is typed from the print as other Arabic, even when a collection records it; only the Prophet's words are filled. Narration that is part of a hadith report (the Companion's «قَالَتْ: فَجَعَلْنَا مِنْهُ ...» inside it) is filled together with that hadith. Quranic words used as an everyday phrase (إنا لله وإنا إليه راجعون on hearing of a death, بسم اللہ, ان شاء اللہ) are set phrases: inside an Urdu sentence they stay in the `[ur]` block in Urdu spelling.

Arabic that is neither Quran nor hadith (sayings, duas from other sources, book titles, Arabic terms quoted on their own) is typed exactly as printed, harakat included, with waqf on the last word before each pause. Use Arabic letters in `[ar]` (ي ك ه ة), not the Urdu ones (ی ک ہ). Dagger-alif spellings are typed in the standard form («اللّٰهُ» → «اللَّهُ», «حَتّٰى» → «حَتَّى»); a sukun printed on a long vowel («حَكَمُوْا») is kept.

## Checks before a page is done

```bash
python3 fill_quran.py  books/haraam-karobaar/page_NNN.txt   # if it has {{Q ...}}
python3 fill_hadith.py books/haraam-karobaar/page_NNN.txt   # if it has {{H ...}}
python3 check_pages.py books/haraam-karobaar/page_NNN.txt  # must report 0 problems
```

Then read the page file once more against the image, word by word.

Never start a header comment line with `# hadith ` or `# quran `, even when a note wraps onto a new line: those prefixes mark filled lines, and the checks will try to rebuild the line below. Start such lines with other words (`# The hadith ...`).

Never run Unicode normalisation (NFC/NFD) or other bulk rewrites over a page's Arabic: it changes the filled Quran and hadith text. If a fill check fails after an edit, re-run `fill_quran.py` / `fill_hadith.py` on the page.
