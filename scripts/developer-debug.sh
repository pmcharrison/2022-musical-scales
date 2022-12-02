# Ensures that the script stops on errors
set -euo pipefail

. scripts/params.sh

export PSYNET_EDITABLE=1

if [ ! -d "$PSYNET_LOCAL_PATH"/psynet/trial ]; then
  printf '%s\n' "Couldn't find a PsyNet repository at $PSYNET_LOCAL_PATH. Consider downloading a PsyNet repository and/or updating params.sh." >&2  # write error message to stderr
  exit 1
fi

. scripts/debug.sh
