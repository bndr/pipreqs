#!/usr/bin/bash
# ------------------------------------------------------------------------------
# Author : Michael Wurm <wurm.michael95@gmail.com>
# ------------------------------------------------------------------------------

SCRIPT_PATH=$(cd -- "$(dirname -- "$(readlink -f "${BASH_SOURCE[0]}" || ${BASH_SOURCE[0]})")" &>/dev/null && pwd)

set -euo pipefail

MAPPING_OLD="$SCRIPT_PATH"/mapping
MAPPING_NEW="$SCRIPT_PATH"/mapping.new

while IFS= read -r line; do
    mapelements=($(echo "$line" | tr ':' '\n'))
    if [ "${mapelements[0]}" == "${mapelements[1]}" ]; then
        echo "Found a duplicate mapping in line: '$line'"
        continue
    fi
    echo "$line" >>"$MAPPING_NEW"
done <"$MAPPING_OLD"

mv "$MAPPING_NEW" "$MAPPING_OLD"
