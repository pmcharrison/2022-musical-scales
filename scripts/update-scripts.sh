set -euo pipefail

. scripts/params.sh
. scripts/build.sh

docker run \
  --name dallinger \
  --rm \
  -ti \
  -u $(id -u "${USER}"):$(id -g "${USER}") \
  -v "${PWD}":/experiment \
  -v "${HOME}"/.dallingerconfig:/.dallingerconfig \
  -v "$PSYNET_DEBUG_STORAGE":/psynet-debug-storage \
  -v "$PSYNET_EXPORT_STORAGE":/psynet-exports \
  --network dallinger \
  -p 5000:5000 \
  -e FLASK_OPTIONS='-h 0.0.0.0' \
  -e REDIS_URL=redis://dallinger_redis:6379 \
  -e DATABASE_URL=postgresql://dallinger:dallinger@dallinger_postgres/dallinger \
  -e PSYNET_EDITABLE="${PSYNET_EDITABLE:-}" \
  -v "${PSYNET_LOCAL_PATH}":/PsyNet \
  "${EXPERIMENT_IMAGE}" \
  psynet update-scripts \
  | sed -e "s:/tmp/dallinger_develop/:${PWD}/:" -e "s:\"/PsyNet/":"\"${PSYNET_LOCAL_PATH}/:"
