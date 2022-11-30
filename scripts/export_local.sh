set -euo pipefail

. params.sh

docker exec \
  dallinger \
  psynet export --local \
  | sed -e "s:/tmp/dallinger_develop/:${PWD}/:" -e "s:\"/PsyNet/":"\"${PSYNET_LOCAL_PATH}/:"
