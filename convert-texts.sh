#!/bin/bash

die() {
	echo >&2 "$@"
	exit 1
}

[ "$#" -eq 3 ] || die "Usage: $0 INPUT_FILE TEMPLATE_FILE OUTPUT_FILE"
INPUT_FILE=$1
TEMPLATE_FILE=$2
OUTPUT_FILE=$3

echo "Generating $OUTPUT_FILE ..."

LINE=$(grep -n {{text}} template_text.html | cut -d : -f1)
cp "$TEMPLATE_FILE" "$OUTPUT_FILE"
head -n $(echo $LINE - 1 | bc -l) "$TEMPLATE_FILE" > "$OUTPUT_FILE"
markdown "$INPUT_FILE" >> "$OUTPUT_FILE"
tail -n +$(echo $LINE + 1 | bc -l) "$TEMPLATE_FILE" >> "$OUTPUT_FILE"
