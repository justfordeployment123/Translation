"""Generate a word-synced audio sample of one book page with ElevenLabs.

Usage (settings are read from .env next to this script, or from the shell):
    ELEVENLABS_API_KEY=...     # ElevenLabs > Developers > API Keys
    ELEVENLABS_VOICE_AR=...    # voice ID used for [ar] blocks
    ELEVENLABS_VOICE_UR=...    # voice ID used for [ur] blocks
    ELEVENLABS_VOICE_ID=...    # fallback voice for any language without its own voice

    python3 make_sample.py pages/page_001.txt --dry-run   # show the cleaned text only, no API call
    python3 make_sample.py pages/page_001.txt
    python3 make_sample.py pages/page_001.txt --voice-ar ID1 --voice-ur ID2 --tag combo1

Each [ar] / [ur] block of the page file is cleaned by preprocess.py and sent to ElevenLabs as its
own request with the matching language code, so a voice never has to switch language mid-sentence.
Output goes to out/<page>[_<tag>]/: one MP3 per segment, sample.mp3 (all segments joined) and
player.html, a single self-contained file that plays the audio and highlights each word as it is spoken.
"""
import argparse
import base64
import html
import json
import os
import re
import shutil
import sys
import urllib.error
import urllib.request
from pathlib import Path

from preprocess import preprocess

API_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps?output_format=mp3_44100_128"


def load_env(path=Path(__file__).parent / ".env"):
    """Read KEY=value lines from .env into os.environ; values already set in the shell win."""
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            key, sep, value = line.partition("=")
            if sep and not key.strip().startswith("#") and value.strip():
                os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


def parse_page(path):
    """Split a page file into [(lang, text), ...] using its [ar] / [ur] / [en] tags."""
    segments, lang, lines = [], None, []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            continue
        tag = re.fullmatch(r"\[(ar|ur|en)\]", line.strip())
        if tag:
            if lang and " ".join(lines).strip():
                segments.append((lang, " ".join(lines)))
            lang, lines = tag.group(1), []
        elif lang:
            lines.append(line)
    if lang and " ".join(lines).strip():
        segments.append((lang, " ".join(lines)))
    return segments


def synthesize(text, lang, voice_id, api_key, model):
    """Return (mp3 bytes, character alignment) for `text`."""
    body = {"text": text, "model_id": model, "language_code": lang}
    for attempt in range(2):
        req = urllib.request.Request(
            API_URL.format(voice_id=voice_id),
            data=json.dumps(body).encode("utf-8"),
            headers={"xi-api-key": api_key, "Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = json.load(resp)
            return base64.b64decode(data["audio_base64"]), data["alignment"]
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")
            # some models reject language_code; retry once letting the model detect the language
            if attempt == 0 and "language_code" in detail:
                body.pop("language_code")
                continue
            sys.exit(f"ElevenLabs error {e.code}: {detail}")


def words_from_alignment(alignment):
    """Group character timings into [{"w": word, "s": start, "e": end}, ...]."""
    words, word, start, end = [], "", 0.0, 0.0
    chars = zip(alignment["characters"], alignment["character_start_times_seconds"], alignment["character_end_times_seconds"])
    for ch, s, e in chars:
        if ch.isspace():
            if word:
                words.append({"w": word, "s": start, "e": end})
                word = ""
            continue
        if not word:
            start = s
        word, end = word + ch, e
    if word:
        words.append({"w": word, "s": start, "e": end})
    return words


def data_uri(path, mime):
    return f"data:{mime};base64," + base64.b64encode(Path(path).read_bytes()).decode()


def render_player(title, segments, image_src="", nav=""):
    """Return the player page. `segments` is [{"lang", "words", "audio"}, ...], where `audio` and
    `image_src` are either relative file paths (website) or data URIs (single self-contained file)."""
    image = ""
    if image_src:
        image = f'<figure class="card"><img src="{image_src}" alt="Original page"><figcaption>Original page</figcaption></figure>'
    template = (Path(__file__).parent / "player_template.html").read_text(encoding="utf-8")
    return (
        template.replace("{{TITLE}}", html.escape(title))
        .replace("{{NAV}}", nav)
        .replace("{{IMAGE}}", image)
        .replace("{{SEGMENTS}}", json.dumps(segments, ensure_ascii=False).replace("</", "<\\/"))
    )


def main():
    load_env()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("page", help="page text file, e.g. pages/page_001.txt")
    ap.add_argument("--voice-ar", default=os.environ.get("ELEVENLABS_VOICE_AR"), help="voice ID for Arabic")
    ap.add_argument("--voice-ur", default=os.environ.get("ELEVENLABS_VOICE_UR"), help="voice ID for Urdu")
    ap.add_argument("--voice-id", default=os.environ.get("ELEVENLABS_VOICE_ID"), help="fallback voice ID")
    ap.add_argument("--model", default="eleven_v3", help="must support Urdu, e.g. eleven_v3")
    ap.add_argument("--tag", help="suffix for the output folder, to keep several voice combinations apart")
    ap.add_argument("--dry-run", action="store_true", help="print the cleaned segments and stop")
    args = ap.parse_args()

    page = Path(args.page)
    segments = [(lang, preprocess(raw, lang)) for lang, raw in parse_page(page)]
    for lang, text in segments:
        print(f"[{lang}] {text}")
    if args.dry_run:
        return

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        sys.exit("ELEVENLABS_API_KEY is missing: add it to the .env file.")
    voices = {"ar": args.voice_ar, "ur": args.voice_ur}
    missing = sorted({lang for lang, _ in segments if not (voices.get(lang) or args.voice_id)})
    if missing:
        sys.exit(f"No voice ID for: {', '.join(missing)}. Set ELEVENLABS_VOICE_AR / _UR / _ID in .env.")

    out = Path("out") / (f"{page.stem}_{args.tag}" if args.tag else page.stem)
    out.mkdir(parents=True, exist_ok=True)
    sync = {"page": page.stem, "title": page.stem.replace("_", " ").title(), "segments": []}
    for i, (lang, text) in enumerate(segments, 1):
        print(f"Generating segment {i}/{len(segments)} ({lang})...")
        mp3, alignment = synthesize(text, lang, voices.get(lang) or args.voice_id, api_key, args.model)
        name = f"seg_{i:02d}_{lang}.mp3"
        (out / name).write_bytes(mp3)
        sync["segments"].append({"lang": lang, "words": words_from_alignment(alignment), "audio": name})
    if page.with_suffix(".png").exists():
        shutil.copy(page.with_suffix(".png"), out / "page.png")
        sync["image"] = "page.png"
    # sync.json is what export_site.py turns into the website
    (out / "sync.json").write_text(json.dumps(sync, ensure_ascii=False, indent=1), encoding="utf-8")

    # MP3 frames are self-contained, so joining the files byte-for-byte plays back fine
    (out / "sample.mp3").write_bytes(b"".join((out / s["audio"]).read_bytes() for s in sync["segments"]))
    embedded = [{**s, "audio": data_uri(out / s["audio"], "audio/mpeg")} for s in sync["segments"]]
    image = data_uri(out / "page.png", "image/png") if "image" in sync else ""
    (out / "player.html").write_text(render_player(sync["title"], embedded, image), encoding="utf-8")
    print(f"Done: {out / 'sample.mp3'} and {out / 'player.html'}")


if __name__ == "__main__":
    main()
