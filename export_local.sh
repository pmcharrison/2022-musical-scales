# Ensures that the script stops on errors
set -euo pipefail

. params.sh

#printf "\n"
#echo "Please enter a name for your exported dataset:"
#read -r DATASET_NAME

# Note: any changes to this command should be propagated to terminal.sh
docker exec \
  dallinger \
  psynet export --local \
  | sed -e "s:/tmp/dallinger_develop/:${PWD}/:" -e "s:\"/PsyNet/":"\"${PSYNET_LOCAL_PATH}/:"
