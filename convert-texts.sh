#!/bin/bash

die() {
	echo >&2 "$@"
	exit 1
}

[ "$#" -eq 3 ] || die "Usage: $0 INPUT_FILE TEMPLATE_FILE OUTPUT_FILE"
INPUT_FILE=$1
TEMPLATE_FILE=$2
OUTPUT_FILE=$3
PROJECT=$(basename "$(dirname "$INPUT_FILE")")

echo "Generating $OUTPUT_FILE ($PROJECT)..."

LINE=$(grep -n {{text}} template_text.html | cut -d : -f1)
cp "$TEMPLATE_FILE" "$OUTPUT_FILE"
head -n $(echo $LINE - 1 | bc -l) "$TEMPLATE_FILE" > "$OUTPUT_FILE"
pandoc --from gfm+tex_math_dollars --to html --highlight-style tango "$INPUT_FILE" >> "$OUTPUT_FILE"
tail -n +$(echo $LINE + 1 | bc -l) "$TEMPLATE_FILE" >> "$OUTPUT_FILE"
sed -i "s|<title>NIPE-SYSTEMS</title>|<title>NIPE-SYSTEMS - $(basename "$(dirname "$INPUT_FILE")")</title>|g" "$OUTPUT_FILE"
