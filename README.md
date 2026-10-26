# Noor Library: Islamic Books as Synced Audio

This project turns scanned Islamic books (Quranic Arabic with Urdu text) into an installable reading app. ElevenLabs reads every page aloud, each word is highlighted as it is spoken, and pages turn by themselves.

**Live app:** https://justfordeployment123.github.io/Translation/

| Book | Pages | Editions |
|---|---|---|
| *Zindagi Aur Waqt* (Life and Time) | 13–178 | Urdu and English |
| *Shab o Roz ke Masnoon Amaal* (Sunnahs of Day and Night) | 17–170 | Urdu |
| *100 Haraam Karobaar aur Tijarti Mamlaat* (100 Forbidden Trades and Business Dealings) | 17–564 | Urdu and English text finished and proofread; audio not yet recorded |
| *Salaf-e-Saliheen ke Aqaid o Nazariyat* (The Beliefs and Doctrines of the Righteous Predecessors) | 10–196 | Urdu and English text finished and proofread; audio not yet recorded (the source PDF stops at page 196) |

The full step-by-step process, with every rule and command, is in **[PIPELINE.md](PIPELINE.md)**. This page is the overview.

## How it works

```
scanned PDF → page images → hand transcription → Quran/hadith filled from official sources
            → English edition (optional) → text cleaned for speech → ElevenLabs recording
            → app build → phone-size test → GitHub Pages
```

1. **Transcribe.** Each book page becomes `books/<book>/page_NNN.txt`, typed from the scan and split into tagged blocks: `[ar]` Arabic, `[ur]` Urdu, `[h]` heading, `[ref]` source reference and `[fn]` explanatory footnote (both shown, not spoken), and `[en]` / `[hen]` / `[fen]` for English.
2. **Fill Quran and hadith.** The Quran and the Prophet's words are never typed by hand. A placeholder such as `{{Q 2:132}}` or `{{H bukhari:614 from ... to ...}}` is filled from official sources (Tanzil text for the Quran, the hadith-api collections for hadith), and `--check` confirms the text is identical to the source.
3. **English edition.** Only the English is written, one block per Urdu block. Quran translations are Sahih International. `build_english.py` merges the English with the Urdu page's Arabic and references, and stops if the blocks don't line up.
4. **Clean for speech.** `preprocess.py` spells out honorific symbols (ﷺ → «صلی اللہ علیہ وسلم»), removes footnote markers and pause signs, and fixes Arabic/Urdu letter forms so each language is pronounced correctly.
5. **Record.** `make_sample.py` sends each block to ElevenLabs (`eleven_v3`, one language per request) and turns the returned character timings into word timings. Finished segments are cached, so nothing is paid for twice.
6. **Build.** `build_app.py` assembles every book into `site/`: one static HTML app with the text, audio, scans, contents and chapter downloads.

## Requirements

- Python 3 (standard library only; Pillow is needed only to regenerate the app icons)
- An ElevenLabs API key with text-to-speech access (only for recording)
- `pdftoppm` (poppler) to turn PDF pages into images
- macOS `afconvert` to make the smaller chapter downloads (optional; without it they stay MP3)

## Quick start

```bash
cp .env.example .env                       # add ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID
python3 -m unittest test_preprocess        # text-cleaning tests

python3 fill_quran.py  --check books/shab-o-roz/*.txt     # Quran text matches the source
python3 fill_hadith.py --check books/shab-o-roz/*.txt     # hadith text matches the source

python3 make_sample.py books/shab-o-roz/page_031.txt --dry-run   # show what would be spoken; no API call
python3 make_sample.py books/shab-o-roz/page_031.txt --tag sr    # record it into out/page_031_sr/

python3 build_app.py                       # build site/, site.zip and site_chapters/
```

Each book has its own recording tag (`george` and `en` for *Zindagi Aur Waqt*, `sr` for *Shab o Roz*), set in the `BOOKS` list in `build_app.py`.

## Project files

| Path | Role |
|---|---|
| `books/zindagi-aur-waqt/` | Urdu pages; `en_src/` English source, `en/` built English pages |
| `books/shab-o-roz/` | Urdu pages of the second book |
| `books/haraam-karobaar/`, `books/salaf-aqaid/` | Urdu pages, English (`en_src/`, `en/`), the book's rules (`TRANSCRIBING.md`, `ENGLISH.md`) and review list (`REVIEW.md`) |
| `preview_book.py`, `preview_template.html` | A local text preview of a book (scan, Urdu, English, notes), before any recording |
| `preprocess.py`, `test_preprocess.py` | Text cleaning for speech, with tests |
| `render_page.py` | Renders a scanned page large, in two halves, for transcribing |
| `fill_quran.py`, `fill_hadith.py` | Fill and check Quran and hadith text from official sources |
| `find_source.py` | Finds a hadith's number (or an ayah) from a few printed words |
| `check_pages.py` | Reports text that would be read wrongly, before any credits are spent |
| `build_english.py` | Builds English page files from `en_src/` |
| `make_sample.py` | Records a page with ElevenLabs and makes word timings |
| `build_app.py`, `app_template.html`, `app_assets/` | Builds the app (installable, works offline for played pages) |
| `find_voices.py` | Lists ElevenLabs voices for a language |
| `export_site.py`, `player_template.html`, `website_template.html`, `deploy.sh`, `pages/` | Earlier single-page player and website, kept for reference |

## Not included in the repository

The API key (`.env`), recordings (`out/`), the built site, chapter audio, page scans and the source PDFs are kept out of git. They can be recreated from the files here by following [PIPELINE.md](PIPELINE.md); recording needs ElevenLabs credits (about 1,000–1,200 per page per language).
