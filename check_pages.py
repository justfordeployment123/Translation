"""Check page files for text that would be read wrongly, before any credits are spent on them.

It cleans each spoken block exactly as make_sample.py does, then reports what should not be there:
placeholders that were never filled, digits, Latin letters in Urdu or Arabic, symbols the voice would
read or skip, Urdu letters in Arabic (and the reverse), empty or very long blocks, and unknown tags.

Usage:
    python3 check_pages.py books/haraam-karobaar/page_*.txt
"""
import re
import sys
from pathlib import Path

from make_sample import TAGS, parse_page
from preprocess import preprocess

CHECKS = [
    ("unfilled placeholder", lambda t, lang: "{{" in t or "}}" in t),
    ("digits (write numbers as words)", lambda t, lang: lang != "en" and re.search(r"[0-9٠-٩۰-۹]", t)),
    ("Latin letters", lambda t, lang: lang != "en" and re.search(r"[A-Za-z]", t)),
    ("symbol the voice would read or skip", lambda t, lang: re.search(r"[ﷺؑؓؒؔـ①-⑳«»\[\]*#\"]", t) or (lang != "en" and re.search("[‘’']", t))),
    ("Urdu letters in Arabic", lambda t, lang: lang == "ar" and re.search(r"[کہیۓےگچپژڈٹڑںھ]", t)),
    ("Arabic letters in Urdu", lambda t, lang: lang == "ur" and re.search(r"[كيى]", t)),
    ("empty block", lambda t, lang: not t.strip()),
    ("very long block (over 4,500 characters)", lambda t, lang: len(t) > 4500),
]


def check(path):
    """[(block number, tag, problem, text)] for one page file."""
    problems = []
    try:
        blocks = parse_page(path)
    except Exception as e:  # an unknown tag or text outside a block
        return [(0, "-", f"cannot be read: {e}", "")]
    for i, (tag, raw) in enumerate(blocks, 1):
        if tag not in TAGS:
            problems.append((i, tag, "unknown tag", raw))
            continue
        lang, style = TAGS[tag]
        if style == "ref":
            continue
        text = preprocess(raw, lang)
        problems += [(i, tag, name, text) for name, test in CHECKS if test(text, lang)]
    return problems


def main():
    paths = [Path(p) for p in sys.argv[1:]]
    if not paths:
        sys.exit(__doc__)
    total = 0
    for path in paths:
        for i, tag, problem, text in check(path):
            total += 1
            print(f"{path.name} block {i} [{tag}]: {problem} | {text[:100]}")
    print(f"{len(paths)} page(s), {total} problem(s)")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
