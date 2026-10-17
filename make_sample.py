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
import time
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


# block tag -> (language, style). [h] is a spoken heading; [ref] is a reference shown in the
# text but never sent to ElevenLabs.
TAGS = {"ar": ("ar", None), "ur": ("ur", None), "en": ("en", None), "h": ("ur", "h"), "hen": ("en", "h"), "ref": ("ur", "ref")}


def parse_page(path):
    """Split a page file into [(tag, text), ...] using its [ar] / [ur] / [en] / [h] / [ref] tags."""
    segments, tag, lines = [], None, []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            continue
        match = re.fullmatch(r"\[(%s)\]" % "|".join(TAGS), line.strip())
        if match:
            if tag and " ".join(lines).strip():
                segments.append((tag, " ".join(lines)))
            tag, lines = match.group(1), []
        elif tag:
            lines.append(line)
    if tag and " ".join(lines).strip():
        segments.append((tag, " ".join(lines)))
    return segments


def page_title(path):
    """The page's '# title: ...' line, or a title made from the file name."""
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("# title:"):
            return line.partition(":")[2].strip()
    return Path(path).stem.replace("_", " ").title()


def synthesize(text, lang, voice_id, api_key, model, voice_settings=None):
    """Return (mp3 bytes, character alignment) for `text`."""
    body = {"text": text, "model_id": model, "language_code": lang}
    if voice_settings:
        body["voice_settings"] = voice_settings
    network_errors = 0
    while True:
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
            if "language_code" in detail and "language_code" in body:
                body.pop("language_code")
                continue
            sys.exit(f"ElevenLabs error {e.code}: {detail}")
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            # a dropped connection or timeout: wait and try again, up to 3 times
            network_errors += 1
            if network_errors > 3:
                sys.exit(f"Network error after 3 retries: {e}")
            print(f"  network error ({e}); retrying in {10 * network_errors}s")
            time.sleep(10 * network_errors)


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


def mp3_seconds(path):
    """Length of an ElevenLabs mp3_44100_128 file (constant 128 kbps)."""
    return Path(path).stat().st_size * 8 / 128_000


def spread_collapsed(words, duration):
    """ElevenLabs sometimes gives the last few words one shared timestamp. Spread them evenly over
    the rest of the audio so the highlighting keeps moving. Returns (words, number of words spread)."""
    i = len(words) - 1
    while i > 0 and words[i - 1]["s"] == words[-1]["s"]:
        i -= 1
    count = len(words) - i
    if count < 2 or duration <= words[i]["s"]:
        return words, 0
    start, step = words[i]["s"], (duration - words[i]["s"]) / count
    spread = [{**w, "s": start + k * step, "e": start + (k + 1) * step} for k, w in enumerate(words[i:])]
    return words[:i] + spread, count


def render_player(title, segments, pages, downloads=()):
    """Return the player page, which shows one book page at a time and turns pages with the audio.

    segments:  [{"lang", "words", "audio", "page"}, ...]; "page" is an index into `pages` (default 0).
    pages:     [{"title", "image"}, ...]; "image" is the scanned page, or "" when there is none.
    downloads: [(label, href), ...] MP3 files offered in a download menu.
    Every src is either a relative file path (website) or a data URI (single self-contained file).
    """
    links = "".join(
        f'<a href="{href}" download="{Path(href).name}">{html.escape(label)}</a>' for label, href in downloads
    )
    button = f'<details class="dl"><summary class="button">⬇ MP3</summary><div class="menu">{links}</div></details>' if links else ""
    as_json = lambda data: json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    template = (Path(__file__).parent / "player_template.html").read_text(encoding="utf-8")
    return (
        template.replace("{{TITLE}}", html.escape(title))
        .replace("{{DOWNLOAD}}", button)
        .replace("{{PAGES}}", as_json(pages))
        .replace("{{SEGMENTS}}", as_json(segments))
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
    ap.add_argument("--speed", type=float, help="speaking speed, e.g. 0.9 for slower (default: the voice's own)")
    ap.add_argument("--stability", type=float, help="0 to 1; higher is steadier and more even (default 0.5)")
    ap.add_argument("--dry-run", action="store_true", help="print the cleaned segments and stop")
    args = ap.parse_args()

    page = Path(args.page)
    segments = []
    for tag, raw in parse_page(page):
        lang, style = TAGS[tag]
        text = " ".join(raw.split()) if style == "ref" else preprocess(raw, lang)
        segments.append({"tag": tag, "lang": lang, "style": style, "text": text})
    for s in segments:
        print(f"[{s['tag']}] {s['text']}")
    spoken = [s for s in segments if s["style"] != "ref"]
    print(f"{sum(len(s['text']) for s in spoken)} characters in {len(spoken)} requests will be sent to ElevenLabs")
    if args.dry_run:
        return

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        sys.exit("ELEVENLABS_API_KEY is missing: add it to the .env file.")
    voices = {"ar": args.voice_ar, "ur": args.voice_ur}
    missing = sorted({s["lang"] for s in spoken if not (voices.get(s["lang"]) or args.voice_id)})
    if missing:
        sys.exit(f"No voice ID for: {', '.join(missing)}. Set ELEVENLABS_VOICE_AR / _UR / _ID in .env.")

    out = Path("out") / (f"{page.stem}_{args.tag}" if args.tag else page.stem)
    out.mkdir(parents=True, exist_ok=True)
    settings = {k: v for k, v in (("speed", args.speed), ("stability", args.stability)) if v is not None}
    # every segment recorded so far, by its cache key, so identical text is never paid for twice
    recorded = {}
    for f in Path("out").glob("*/seg_*.json"):
        try:
            k = json.loads(f.read_text(encoding="utf-8"))["key"]
        except (ValueError, KeyError):
            continue
        if f.with_suffix(".mp3").exists():
            recorded.setdefault(json.dumps(k, ensure_ascii=False, sort_keys=True), f)
    sync = {"page": page.stem, "title": page_title(page), "segments": []}
    for s in segments:
        style = {"style": s["style"]} if s["style"] else {}
        if s["style"] == "ref":
            sync["segments"].append({"lang": s["lang"], "text": s["text"], **style})
            continue
        i = sum(1 for x in sync["segments"] if "audio" in x) + 1
        voice = voices.get(s["lang"]) or args.voice_id
        name = f"seg_{i:02d}_{s['lang']}.mp3"
        # each finished segment is cached, so a re-run after an error never pays for it twice
        cache = out / name.replace(".mp3", ".json")
        key = {"text": s["text"], "voice": voice, "model": args.model, **({"settings": settings} if settings else {})}
        cached = json.loads(cache.read_text(encoding="utf-8")) if cache.exists() and (out / name).exists() else {}
        elsewhere = recorded.get(json.dumps(key, ensure_ascii=False, sort_keys=True))
        if cached.get("key") == key:
            print(f"Segment {i}/{len(spoken)} ({s['lang']}) already generated, reusing it")
            words = cached["words"]
        elif elsewhere:  # the same text was already recorded for another page or edition
            print(f"Segment {i}/{len(spoken)} ({s['lang']}) already recorded in {elsewhere.parent.name}, reusing it")
            shutil.copy(elsewhere.with_suffix(".mp3"), out / name)
            shutil.copy(elsewhere, cache)
            words = json.loads(cache.read_text(encoding="utf-8"))["words"]
        else:
            print(f"Generating segment {i}/{len(spoken)} ({s['lang']})...")
            mp3, alignment = synthesize(s["text"], s["lang"], voice, api_key, args.model, settings)
            words = words_from_alignment(alignment)
            (out / name).write_bytes(mp3)
            cache.write_text(json.dumps({"key": key, "words": words}, ensure_ascii=False), encoding="utf-8")
        words, spread = spread_collapsed(words, mp3_seconds(out / name))
        if spread:
            print(f"  note: the last {spread} words had no separate timings; listen to {out / name} to check them")
        sync["segments"].append({"lang": s["lang"], "words": words, "audio": name, **style})
    scan = next((p for p in (page.with_suffix(".png"), page.parent.parent / (page.stem + ".png")) if p.exists()), None)
    if scan:
        shutil.copy(scan, out / "page.png")
        sync["image"] = "page.png"
    # sync.json is what export_site.py turns into the website
    (out / "sync.json").write_text(json.dumps(sync, ensure_ascii=False, indent=1), encoding="utf-8")

    # MP3 frames are self-contained, so joining the files byte-for-byte plays back fine
    voiced = [s for s in sync["segments"] if "audio" in s]
    (out / "sample.mp3").write_bytes(b"".join((out / s["audio"]).read_bytes() for s in voiced))
    embedded = [{**s, "audio": data_uri(out / s["audio"], "audio/mpeg")} if "audio" in s else s for s in sync["segments"]]
    image = data_uri(out / "page.png", "image/png") if "image" in sync else ""
    pages = [{"title": sync["title"], "image": image}]
    (out / "player.html").write_text(render_player(sync["title"], embedded, pages), encoding="utf-8")
    print(f"Done: {out / 'sample.mp3'} and {out / 'player.html'}")


if __name__ == "__main__":
    main()
