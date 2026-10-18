# Book Audio Pipeline

How a scanned Islamic book becomes the Noor Library app: Urdu and English audio read by ElevenLabs, with the text shown on screen, each word highlighted as it is spoken, and pages turning by themselves.

The first book is *Zindagi Aur Waqt* (book pages 13 to 178). Every step below was used to produce it.

```
 Zindagi-Aur-Waqat.pdf
        │
        ▼
 1. Scan pages to images ........................ pdftoppm
        │
        ▼
 2. Transcribe each page by hand ................ books/<book>/page_NNN.txt
        │
        ▼
 3. Fill Quran and hadith from official sources . fill_quran.py, fill_hadith.py
        │
        ▼
 4. Write the English edition ................... en_src/ → build_english.py → en/
        │
        ▼
 5. Clean the text for speech ................... preprocess.py (runs inside step 6)
        │
        ▼
 6. Dry run, then record with ElevenLabs ........ make_sample.py → out/page_NNN_<tag>/
        │
        ▼
 7. Build the app ............................... build_app.py → site/
        │
        ▼
 8. Test in a phone-sized browser ............... headless Chrome
        │
        ▼
 9. Deploy and save ............................. gh-pages branch → GitHub Pages; code → main
```

---

## Setup (once)

| What | Where |
|---|---|
| ElevenLabs API key | `.env` → `ELEVENLABS_API_KEY=...` |
| Voice | `.env` → `ELEVENLABS_VOICE_ID=JBFqnCBsd6RMkjVDRZzb` (George, used for Arabic, Urdu and English) |
| Tools | Python 3, `pdftoppm` (poppler), Google Chrome for testing |

`.env` is in `.gitignore`. It must never be committed, copied into `site/`, or shared.

---

## Step 1: Turn the PDF pages into images

The PDF is a scan; its built-in OCR text is unusable, so every page is read from the image.

```bash
# PDF page = book page + 2
pdftoppm -f 132 -l 132 -r 110 -png -singlefile Zindagi-Aur-Waqat.pdf books/zindagi-aur-waqt/page_130
```

- **Output:** `books/zindagi-aur-waqt/page_NNN.png`, one per book page. The app shows this as the "Original page" button.
- For reading the text, a page is also rendered at 220–500 dpi and cropped into halves, so small words, harakat and anything cut off at the scan's edge can be read clearly.

## Step 2: Transcribe each page

Each book page becomes one text file, `books/zindagi-aur-waqt/page_NNN.txt`. The text is typed exactly as printed and divided into tagged blocks:

| Tag | Meaning | Spoken? |
|---|---|---|
| `[ar]` | Arabic: Quran, hadith, sayings, poetry | Yes, in Arabic |
| `[ur]` | Urdu text or translation | Yes, in Urdu |
| `[h]` | Urdu heading (chapter, section, person's name) | Yes, with a longer pause |
| `[ref]` | Source reference, e.g. «صحیح البخاری، رقم الحدیث: ۶۴۱۲» | No, shown only |
| `[en]` / `[hen]` | English text / heading (English edition only) | Yes, in English |

Rules followed on every page:

- **Header comments** (`# ...` lines) record the book and PDF page number, and any text moved to or from the next page. When the scan is unclear, the reading chosen is marked with **"Proofreader please check"**. Comments are never spoken.
- **Text that runs across a page break** goes in the page where it starts or ends as a whole, so no sentence or verse is split between two recordings.
- **Arabic harakat** are typed as printed. Poetry keeps its rhyme vowels, and prose takes a sukun at each stop (waqf), as a reader would say it.
- **Numbers** are written as words in spoken text (e.g. «دو سو چورانوے ہجری»). Digits appear only in `[ref]` blocks.
- **Numbered lists** (①, ②) are read as words («پہلا نقصان», «دوسرا نقصان»), or the numbers are dropped when each item has its own heading.
- **Honorific symbols** (ﷺ, ؓ, ؒ) may be typed as symbols; step 5 turns them into full words. Where ؓ refers to a woman or to more than one person, the full words are typed instead (رضی اللہ عنہا / عنہما).
- **Chapter headings** start with «باب ...» (English: «Chapter ...»). The app builds its table of contents and chapter downloads from them.

## Step 3: Fill Quran and hadith from official sources

The Arabic of the Quran and the Prophet's words is never retyped by hand. A placeholder is written instead, and a script fills it in:

```
[ar]
{{Q 2:132 from فَلَا تَمُوتُنَّ}}                      ← a verse, or part of it
عَنْ سَلْمَانَ {{H tirmidhi:2139 from قَالَ to الْبِرُّ}}  ← the narrator typed, the hadith filled in
```

```bash
python3 fill_quran.py  books/zindagi-aur-waqt/page_178.txt   # fill, then check
python3 fill_hadith.py books/zindagi-aur-waqt/page_177.txt
python3 fill_quran.py  --check books/zindagi-aur-waqt/*.txt  # recheck the whole book
python3 fill_hadith.py --check books/zindagi-aur-waqt/*.txt
```

- **Quran:** text from api.alquran.cloud (Tanzil, full harakat). The only change is the stopping form of the last word.
- **Hadith:** text from the hadith-api collections (Bukhari, Muslim, Abu Dawud, Tirmidhi, Nasa'i, Ibn Majah), cached in `cache/hadith/`. The salawat is written in full, and the stopping form is applied at each pause.
- `from` / `to` select just the part the book quotes. Matching uses letters only, so differences in harakat don't matter.
- Each filled line keeps its placeholder in a `# quran ...` / `# hadith ...` comment, so `--check` can rebuild it later and confirm it is **identical to the official text**.
- **Hadith numbering:** the hadith-api numbers Sahih Muslim differently from the printed book (e.g. Muslim 2553 is 6516 there). Search the source by text, and keep the book's number in the `[ref]`.
- **When the book's wording differs from the official text,** the official wording is read and the difference is noted with "Proofreader please check".

## Step 4: Write the English edition

The English edition follows the Urdu page exactly, so the two languages always show the same book page.

1. **`books/zindagi-aur-waqt/en_src/page_NNN.txt`**: only the English, with one `[en]` for every `[ur]` and one `[hen]` for every `[h]` of the Urdu page, in the same order. A page with no Urdu blocks gets an empty file.
2. **Quran translations** are never our own wording:
   - For a whole verse, write `{{QEN 23:51}}` (several verses: `{{QEN 102:1 102:2}}`), and Sahih International is filled in.
   - For a partial quotation, the matching part of the Sahih International text is copied word for word.
3. **Build:**
   ```bash
   python3 build_english.py 63-178
   ```
   This interleaves the English with the Urdu page's `[ar]` and `[ref]` blocks, copied unchanged, and writes `books/zindagi-aur-waqt/en/page_NNN.txt`. It stops with an error if the number or order of blocks doesn't match the Urdu page.

## Step 5: Clean the text for speech (automatic)

`preprocess.py` runs on every block just before it is sent to ElevenLabs:

- Honorific symbols become spoken words in the block's language (ﷺ → «صلی اللہ علیہ وسلم» / «صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ» / "Sallallahu Alayhi Wasallam").
- Footnote markers, Quranic pause signs, ornate brackets, decorative quotes and tatweel are removed.
- **Urdu blocks:** Arabic-keyboard letters are changed to Urdu ones (ك → ک, ي → ی).
- **Arabic blocks:** Urdu-keyboard letters are changed to Arabic ones (ک → ك, ہ → ه, final ی → ي/ى). Otherwise the voice reads the Arabic with an Urdu accent.

Tests: `python3 -m unittest test_preprocess`

## Step 6: Dry run, then record

**Always dry-run first.** It prints the exact cleaned text that would be spoken and the character count, without calling the API.

```bash
python3 make_sample.py books/zindagi-aur-waqt/page_150.txt --dry-run
python3 make_sample.py books/zindagi-aur-waqt/page_150.txt --tag george        # Urdu edition
python3 make_sample.py books/zindagi-aur-waqt/en/page_150.txt --tag en         # English edition
```

What happens:

1. Each spoken block is sent as its own request to ElevenLabs `/v1/text-to-speech/{voice}/with-timestamps`, with model `eleven_v3` and `language_code` set to `ar`, `ur` or `en`. One language per request, so the voice never switches language mid-sentence.
2. ElevenLabs returns the MP3 and the start time of every character. These are grouped into word timings for the highlighting. When the last few words share one timestamp, they are spread evenly to the end of the audio.
3. **Output:** `out/page_NNN_<tag>/` with `seg_NN_<lang>.mp3` and `.json` per block, plus `sync.json` (all segments and word timings), `sample.mp3` and a single-page `player.html`.

Rules for spending credits:

- **A segment is never paid for twice.** Each finished segment is cached under a key of text + voice + model + settings. A re-run after an error reuses what was already made.
- **Identical text is reused across pages and editions.** The English edition's Arabic blocks reuse the Urdu edition's recordings. So record the Urdu edition of a page first, then the English.
- **The dry-run count includes everything,** even blocks that will be reused, so the real cost is lower.
- **If the credits run out,** the run stops with "ElevenLabs error 401 ... quota". Re-run the same pages after recharging; finished segments are kept.
- **Pace:** `eleven_v3` ignores the speed setting, so the app plays at 0.9× (pitch kept) and adds pauses between blocks.

## Step 7: Build the app

```bash
python3 build_app.py --pages 13-178
```

`build_app.py` reads `out/page_NNN_george` (Urdu) and `out/page_NNN_en` (English) and produces `site/` and `site.zip`:

| Output | Contents |
|---|---|
| `index.html` | The app (from `app_template.html`), with all book data embedded |
| `audio/ur/`, `audio/en/` | One MP3 per spoken block, named by page |
| `images/` | The page scans |
| `chapters/` | One audio file per chapter and language, for download: 48 kbps mono AAC (`.m4a`, made with macOS `afconvert`), or MP3 where that tool isn't available |
| `manifest.webmanifest`, `icons/`, `sw.js` | Lets the app be installed on a phone and work offline for pages already played |

The table of contents comes from the `[h]` headings that start with «باب / مقدمہ / تمہید» (English: Chapter / Introduction / Preface). Book details, author, blurb, and the 14 "Coming soon" shelf places are set at the top of `build_app.py`.

**In the app:**

- One book page is shown at a time, in RTL Urdu or LTR English, with the current word highlighted.
- Pages turn by themselves when their audio ends.
- Pauses between blocks: 650 ms (normal), 900 ms (Arabic), 1,100 ms (heading), 1,600 ms (page turn), all divided by the speed.
- The player has Play/Pause, Restart, previous/next page, Contents and speed. Tapping any word plays from there.
- The reading position is saved as the book page number. Switching language keeps the same page; if the other edition doesn't have that page yet, a message says which pages it covers.

`build_app.py` deletes and rebuilds `site/`. Any local test server serving `site/` must be restarted after a build.

## Step 8: Test before going live

The app is tested at phone size (390×844) in headless Chrome, served by a static server that supports HTTP Range requests (needed for seeking in audio). The test checks:

- Playback turns pages in order, with the visible page always matching the audio (0 mismatches).
- Seeking, the Contents sheet, speed, text size, and the Urdu/English switch all work.
- The installable-app manifest loads.
- There are no JavaScript errors.

Screenshots of every screen are reviewed in both languages.

## Step 9: Deploy and save

**Live site:** https://justfordeployment123.github.io/Translation/ (GitHub Pages, served from the `gh-pages` branch).

```bash
# in a separate clone of the repository, on branch gh-pages
git rm -rq . && cp -R "<project>/site/." . && touch .nojekyll
grep -rl "sk_" . --exclude-dir=.git      # must find nothing: no API key in the site
git add -A && git commit -m "Update site" && git push origin HEAD:gh-pages
gh api repos/justfordeployment123/Translation/pages/builds/latest --jq .status   # wait for "built"
```

Then commit the source to `main` (`git push origin main`). These stay out of git, as listed in `.gitignore`:

- `.env`
- `out/`
- `site/` and `site.zip`
- `cache/`
- `download/`
- the page images
- the PDF

The site is plain HTML, MP3 and PNG, so it can also be uploaded to any web host (`site.zip`) with no server code and no API key.

---

## Adding the next book

1. Make a folder `books/<book-id>/`, and render its scans (step 1).
2. Transcribe the pages (step 2), filling Quran and hadith (step 3).
3. Optionally write the English edition (step 4).
4. Dry run, then record (step 6).
5. Add the book's details to `build_app.py` in place of one "Coming soon" place, then build, test and deploy (steps 7–9).

## Files at a glance

| File | Role |
|---|---|
| `preprocess.py` | Text cleaning for speech (step 5) |
| `fill_quran.py`, `fill_hadith.py` | Official Quran and hadith text, with checks (step 3) |
| `build_english.py` | Builds English page files (step 4) |
| `make_sample.py` | Records a page with ElevenLabs and makes word timings (step 6) |
| `build_app.py`, `app_template.html`, `app_assets/` | Builds the app (step 7) |
| `books/zindagi-aur-waqt/` | Urdu pages, `en_src/` English source, `en/` built English pages |
| `out/` | Recordings, one folder per page and edition (not in git) |
| `find_voices.py` | Lists ElevenLabs voices for a language |
| `export_site.py`, `player_template.html`, `website_template.html` | Earlier single-player and website versions, kept for reference |
