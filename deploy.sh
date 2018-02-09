#!/bin/sh

die() {
	echo >&2 "$@"
	exit 1
}

[ "$#" -eq 1 ] || die "Usage: $0 DEPLOY_DIRECTORY"

mkdir -p $1 || die "Failed to create deploy directory."
rsync --recursive --perms --times --group --owner --delete static/ deploy/ || die "Failed to copy static files."
./convert-index.py projects triggers template.html deploy/index.html
