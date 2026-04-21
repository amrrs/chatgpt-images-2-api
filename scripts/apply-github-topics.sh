#!/usr/bin/env bash
# Apply the GitHub repository topics listed in .github/topics.txt
# to the current repo via the `gh` CLI.
#
# Prerequisites:
#   - gh CLI installed and authenticated (https://cli.github.com/)
#   - Run from inside the repo, with `origin` pointing at the GitHub repo.
#
# Usage:
#   bash scripts/apply-github-topics.sh
#   bash scripts/apply-github-topics.sh your-org/your-repo   # explicit target

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOPICS_FILE="$ROOT_DIR/.github/topics.txt"

if [[ ! -f "$TOPICS_FILE" ]]; then
  echo "error: $TOPICS_FILE not found" >&2
  exit 1
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "error: gh CLI not installed. See https://cli.github.com/" >&2
  exit 1
fi

REPO_ARG="${1:-}"

topics=()
while IFS= read -r line; do
  line="${line%%#*}"                      # strip comments
  line="$(echo "$line" | tr -d '[:space:]')"
  [[ -z "$line" ]] && continue
  topics+=("$line")
done < "$TOPICS_FILE"

if (( ${#topics[@]} == 0 )); then
  echo "error: no topics found in $TOPICS_FILE" >&2
  exit 1
fi

if (( ${#topics[@]} > 20 )); then
  echo "warning: GitHub allows at most 20 topics; found ${#topics[@]}. Truncating." >&2
  topics=("${topics[@]:0:20}")
fi

echo "Applying ${#topics[@]} topics:"
printf '  - %s\n' "${topics[@]}"

args=()
for t in "${topics[@]}"; do
  args+=(--add-topic "$t")
done

if [[ -n "$REPO_ARG" ]]; then
  gh repo edit "$REPO_ARG" "${args[@]}"
else
  gh repo edit "${args[@]}"
fi

echo "Done."
