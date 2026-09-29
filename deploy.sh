#!/usr/bin/env bash
# Upload the static site (site/) to your server over SSH.
# Usage: ./deploy.sh user@your-server.com:/var/www/html/audio
# Only site/ is uploaded: no scripts, no .env, no API key.
set -euo pipefail

target="${1:?Usage: ./deploy.sh user@your-server.com:/path/on/server}"
cd "$(dirname "$0")"

if [ ! -f site/index.html ]; then
  echo "site/ not found. Run first: python3 export_site.py out/<recording folder>"
  exit 1
fi

rsync -avz --exclude ".generated-by-export-site" site/ "$target/"
echo "Deployed to $target"
