#!/bin/sh
cd "$(dirname "$0")"
NOTES_PATH="$(readlink _post-links/notes.md)"
NOTES_BASENAME="$(basename "$NOTES_PATH")"
NOTES_REAL_PATH="$(realpath _post-links/notes.md)"
NOTES_DIR="$(dirname "$NOTES_PATH")"
NOTES_REAL_DIR="$(dirname "$NOTES_REAL_PATH")"
NOTES_NEW_BASENAME="$(printf "%s" "$NOTES_BASENAME" | sed "s/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]/$(date +%Y-%m-%d)/")"
NOTES_NEW_REAL_PATH="${NOTES_REAL_DIR}/${NOTES_NEW_BASENAME}"
NOTES_NEW_LINK_VALUE="${NOTES_DIR}/${NOTES_NEW_BASENAME}"
if [ -f "$NOTES_NEW_REAL_PATH" ]; then
	printf 'New path already exists. Would you like to overwrite the existing post '\''%s'\'' with the contents of '\''%s'\''? [y/N] ' "$NOTES_NEW_BASENAME" "$NOTES_BASENAME"
	read yesno
	yesno="$(printf "%s" "$yesno" | tr '[:upper:]' '[:lower:]')"
	if [ "$yesno" = "y" ] || [ "$yesno" = "yes" ]; then
		echo "Overwriting file..."
	else
		echo "Skipped writing file."
		exit 1
	fi
fi
mv -v "$NOTES_REAL_PATH" "$NOTES_NEW_REAL_PATH"
ln -sf "$NOTES_NEW_REAL_PATH" _post-links/notes.md

