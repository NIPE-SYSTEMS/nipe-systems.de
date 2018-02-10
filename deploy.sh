#!/bin/sh

die() {
	echo >&2 "$@"
	exit 1
}

[ "$#" -eq 1 ] || die "Usage: $0 DEPLOY_DIRECTORY"

echo "Creating deploy directory ..."
mkdir -p $1 || die "Failed to create deploy directory."

echo "Copy files into deploy directory ..."
rsync --recursive --perms --times --group --owner --delete static/ $1/ || die "Failed to copy static files."

echo "Generating index file ..."
./convert-index.py projects triggers template_index.html $1/index.html

echo "Generating text files ..."
find projects -name text | while read f; do
	./convert-texts.sh "$f" template_text.html "$1/$(cat "$(dirname "$f")/id").html"
done
