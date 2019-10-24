#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

>&2 echo "Cmdline: cmd_wrapper.sh $@"

while test $# -gt 0
do
    # shellcheck disable=SC1090
    case "$1" in
      use-source ) >&2 echo "Source script: $2"; source "$2"; shift 2;;
      * ) break;;
    esac
done

if [ $# -lt 1 ]; then
    echo "Command arg is missing. Usage: cmd_wrapper.sh [use-source SOURCE_FILE]* {CMD} [CMD_ARGS]*"
    exit 1
fi

exec "$@"

