#!/bin/sh
# Downloads the raw sources into sources/ and rebuilds data/candidates.tsv.
# Then: rate data/batches2/*.txt (AI-assisted, see README) and run `python3 scripts/build.py`.
set -eu
cd "$(dirname "$0")/.."
mkdir -p sources
curl -sL https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/pl/pl_full.txt -o sources/pl_full.txt
ODM=$(curl -sL https://sjp.pl/sl/odmiany/ | grep -oE 'sjp-odm-[0-9]+\.zip' | head -1)
curl -sL "https://sjp.pl/sl/odmiany/$ODM" -o sources/odm.zip
unzip -oq sources/odm.zip -d sources
python3 scripts/candidates.py sources/odm.txt sources/pl_full.txt data/candidates.tsv
