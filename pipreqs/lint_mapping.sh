#!/usr/bin/bash
# ------------------------------------------------------------------------------
# Author      : Michael Wurm <wurm.michael95@gmail.com>
# Description : Formats mapping to lowercase and removes duplicate
#               entries from the mappings file.
# ------------------------------------------------------------------------------

# Script setup

SCRIPT_PATH=$(cd -- "$(dirname -- "$(readlink -f "${BASH_SOURCE[0]}" || ${BASH_SOURCE[0]})")" &>/dev/null && pwd)
cd "$SCRIPT_PATH"

set -euo pipefail

# Functions

convert_file_to_lowercase() {
    FILE_MIXED=mapping
    FILE_LOWER=mapping.new

    tr '[:upper:]' '[:lower:]' <$FILE_MIXED >$FILE_LOWER

    mv $FILE_LOWER $FILE_MIXED
    echo "Converted entire file to lowercase"
}

filter_duplicates() {
    # Loop through the original file line by line.
    # Write each line into a new file.
    # Skip lines with a duplicate mapping, i.e. abc:abc

    MAPPING_OLD="$SCRIPT_PATH/mapping"
    MAPPING_NEW="$SCRIPT_PATH/mapping.new"

    i=0
    found=0
    while IFS= read -r line; do
        ((i = i + 1))
        mapelements=($(echo "$line" | tr ':' '\n'))
        if [ "${mapelements[0]}" == "${mapelements[1]}" ]; then
            echo "Found a duplicate mapping in line #$i: '$line'"
            ((found = found + 1))
            continue
        fi
        echo "$line" >>"$MAPPING_NEW"
    done <"$MAPPING_OLD"

    echo "---"
    mv "$MAPPING_NEW" "$MAPPING_OLD"
    echo "Removed $found duplicates."
}

main() {
    convert_file_to_lowercase
    filter_duplicates
}

main
