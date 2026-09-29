# Urdu / Arabic Book Audio

Turns book pages (Quranic Arabic + Urdu translation) into ElevenLabs audio with a word-synced reading page.

## Setup

```bash
cp .env.example .env   # then add your ElevenLabs API key and voice IDs
```

## Make a recording

```bash
python3 make_sample.py pages/page_001.txt --dry-run      # preview the cleaned text (no API call)
python3 make_sample.py pages/page_001.txt --tag axee      # creates out/page_001_axee/
```

Before any text reaches ElevenLabs, `preprocess.py` replaces honorific symbols (ﷺ, ؑ, ؓ, ...) with the full words and removes footnote markers and Quranic pause signs. Run the tests with `python3 -m unittest test_preprocess`.

## Deploy the frontend

```bash
python3 export_site.py out/page_001_axee                 # builds site/ and site.zip
./deploy.sh user@your-server.com:/var/www/html/audio     # or upload site.zip and extract it
```

`site/` is static HTML + MP3 + PNG, so the server needs no Python and no API key.

To find voices, run `python3 find_voices.py ur` or `python3 find_voices.py ar`.
