#!/usr/bin/env bash
set -euo pipefail

source_dir="${1:-notebooks/src}"
output_dir="${2:-notebooks}"

mkdir -p "${output_dir}"

shopt -s nullglob
sources=("${source_dir}"/*.py)

if [[ ${#sources[@]} -eq 0 ]]; then
  echo "No notebook sources found in ${source_dir}."
  exit 0
fi

for source in "${sources[@]}"; do
  stem="$(basename "${source}" .py)"
  uv run --group docs python -m jupytext --to ipynb "${source}" --output "${output_dir}/${stem}.ipynb"
done
