if test -f Dockertag; then
  export EXPERIMENT_IMAGE=$(cat Dockertag)
else
  export EXPERIMENT_IMAGE=psynet-experiment
fi

export DOCKER_BUILDKIT=1
export PSYNET_LOCAL_PATH="${HOME}"/PsyNet
export PSYNET_DEBUG_STORAGE="${HOME}"/psynet-debug-storage
export PSYNET_EXPORT_STORAGE="${HOME}"/psynet-exports
