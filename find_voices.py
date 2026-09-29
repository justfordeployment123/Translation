"""Search the ElevenLabs Voice Library and add voices to your account.

Usage (reads ELEVENLABS_API_KEY from .env):
    python3 find_voices.py ar                      # Arabic voices
    python3 find_voices.py ur --gender male        # male Urdu voices
    python3 find_voices.py ur --search axee        # search by name / description
    python3 find_voices.py --add OWNER_ID VOICE_ID "Name"   # add a library voice to My Voices
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

from make_sample import load_env

API = "https://api.elevenlabs.io/v1"


def call(method, path, api_key, body=None):
    req = urllib.request.Request(
        API + path,
        method=method,
        data=json.dumps(body).encode("utf-8") if body is not None else None,
        headers={"xi-api-key": api_key, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        sys.exit(f"ElevenLabs error {e.code}: {e.read().decode('utf-8', 'replace')}")


def main():
    load_env()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("language", nargs="?", help="language code, e.g. ar or ur")
    ap.add_argument("--search", help="text to search in names and descriptions")
    ap.add_argument("--gender", choices=["male", "female"])
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--add", nargs=3, metavar=("OWNER_ID", "VOICE_ID", "NAME"), help="add a library voice to My Voices")
    args = ap.parse_args()

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        sys.exit("ELEVENLABS_API_KEY is missing: add it to the .env file.")

    if args.add:
        owner_id, voice_id, name = args.add
        result = call("POST", f"/voices/add/{owner_id}/{voice_id}", api_key, {"new_name": name})
        print(f"Added '{name}'. Voice ID to use: {result.get('voice_id', voice_id)}")
        return

    params = {"page_size": min(args.limit, 100)}
    for key in ("language", "search", "gender"):
        if getattr(args, key):
            params[key] = getattr(args, key)
    voices = call("GET", "/shared-voices?" + urllib.parse.urlencode(params), api_key).get("voices", [])
    if not voices:
        print("No voices found.")
    for v in voices:
        print(f"{v.get('name')}  |  {v.get('gender')}, {v.get('age')}, accent: {v.get('accent')}")
        print(f"    voice_id: {v.get('voice_id')}   owner_id: {v.get('public_owner_id')}")
        if v.get("description"):
            print(f"    {v['description'][:140]}")
        if v.get("preview_url"):
            print(f"    preview: {v['preview_url']}")


if __name__ == "__main__":
    main()
