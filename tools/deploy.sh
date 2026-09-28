#!/usr/bin/env bash
# Deploy code.llmotions.com (and, with --apex, the llmotions.com pages) to the VPS.
#
#   tools/deploy.sh                    dry run: show what would change on the live site, print every step
#   tools/deploy.sh --apply            deploy code/ to code.llmotions.com
#   tools/deploy.sh --apex [--apply]   deploy the apex pages from an explicit list, never deleting
#   tools/deploy.sh --rollback [--apply]   put the .prev copy back
#
# How a deploy runs (the server is reached as the `gcp` ssh alias):
#   1. rsync to a staging folder in the deploy user's home, without sudo;
#   2. keep a copy of the live webroot as <webroot>.prev (the rollback);
#   3. sudo rsync the staging folder into the webroot, owned by www-data.
# code.llmotions.com is synced with --delete, except /downloads/ (installers go up in a separate,
# owner-confirmed step) and .DS_Store. The apex gets only index.html, cympho.html, cymphony.html
# and assets/, and nothing on the server is deleted.
#
# Before --apply the tree must be committed and `tools/build_ncode.py --check --release` must pass
# (it also ties code/install.sh to the newest release).
#
# Testing: NCODE_DEPLOY_ROOT=/some/dir makes that directory play the server (no ssh, no sudo):
# staging is <root>/home/deploy/<site>, the webroot <root>/var/www/<site>. Only in that mode
# NCODE_DEPLOY_SKIP_CHECK=1 skips the build check. NCODE_DEPLOY_HOST overrides the ssh alias.
set -euo pipefail

usage() { sed -n '2,24p' "$0" | sed 's/^# \{0,1\}//'; }

APPLY=0
APEX=0
ROLLBACK=0
while [ $# -gt 0 ]; do
  case "$1" in
    --apply) APPLY=1 ;;
    --apex) APEX=1 ;;
    --rollback) ROLLBACK=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "deploy.sh: unknown option $1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done

REPO=$(cd "$(dirname "$0")/.." && pwd)
HOST=${NCODE_DEPLOY_HOST:-gcp}
LOCAL_ROOT=${NCODE_DEPLOY_ROOT:-}

if [ "$APEX" = 1 ]; then
  SITE=llmotions.com
  SOURCES=(index.html cympho.html cymphony.html assets/)
  FILTERS=(--exclude=.DS_Store)
  PUBLISH_DELETE=()
else
  SITE=code.llmotions.com
  SOURCES=(code/)
  FILTERS=(--exclude=/downloads/ --exclude=.DS_Store)
  PUBLISH_DELETE=(--delete)
fi
STAGE=deploy/$SITE
WEB=/var/www/$SITE
PREV=/var/www/$SITE.prev

if [ -n "$LOCAL_ROOT" ]; then
  case "$LOCAL_ROOT" in /*) ;; *) echo "deploy.sh: NCODE_DEPLOY_ROOT must be an absolute path" >&2; exit 2 ;; esac
  STAGE_DEST=$LOCAL_ROOT/home/$STAGE
  WEB_DEST=$LOCAL_ROOT$WEB
  PREV_DEST=$LOCAL_ROOT$PREV
  MODE="local test root $LOCAL_ROOT"
else
  STAGE_DEST=$HOST:$STAGE
  WEB_DEST=$HOST:$WEB
  MODE="server $HOST"
fi

say() { printf '%s\n' "$*"; }
show() { printf '  $'; printf ' %q' "$@"; printf '\n'; }
run() { show "$@"; "$@"; }
# rsync from the repo root, so the apex's relative include list keeps its paths
sync_from_repo() { (cd "$REPO" && run rsync "$@"); }

if [ "$APEX" = 1 ]; then
  SRC=(-R "${SOURCES[@]}")
else
  SRC=("${SOURCES[@]}")
fi

say "deploy $SITE to $MODE ($([ "$APPLY" = 1 ] && echo apply || echo dry run))"

# ---- rollback ------------------------------------------------------------------------------
if [ "$ROLLBACK" = 1 ]; then
  if [ -n "$LOCAL_ROOT" ]; then
    [ -d "$PREV_DEST" ] || { say "no $PREV_DEST to roll back to"; exit 1; }
    if [ "$APPLY" = 1 ]; then
      run rsync -a ${PUBLISH_DELETE[@]+"${PUBLISH_DELETE[@]}"} "${FILTERS[@]}" "$PREV_DEST/" "$WEB_DEST/"
    else
      run rsync -n -ai ${PUBLISH_DELETE[@]+"${PUBLISH_DELETE[@]}"} "${FILTERS[@]}" "$PREV_DEST/" "$WEB_DEST/"
    fi
  else
    CMD="sudo -n rsync -a ${PUBLISH_DELETE[*]:-} ${FILTERS[*]} --chown=www-data:www-data $PREV/ $WEB/"
    [ "$APPLY" = 1 ] || CMD="rsync -n -ai ${PUBLISH_DELETE[*]:-} ${FILTERS[*]} $PREV/ $WEB/"
    run ssh "$HOST" "$CMD"
  fi
  [ "$APPLY" = 1 ] || say "dry run only; add --apply to roll back"
  exit 0
fi

# ---- pre-flight ----------------------------------------------------------------------------
DIRTY=$(git -C "$REPO" status --porcelain -- "${SOURCES[@]}" tools/ content/ 2>/dev/null || true)
if [ -n "$DIRTY" ]; then
  say "the tree has uncommitted changes under the deployed paths:"
  printf '%s\n' "$DIRTY" | sed 's/^/    /'
  if [ "$APPLY" = 1 ]; then say "refusing to deploy: commit first"; exit 1; fi
fi
if [ "$APEX" = 0 ]; then
  if [ -n "$LOCAL_ROOT" ] && [ "${NCODE_DEPLOY_SKIP_CHECK:-0}" = 1 ]; then
    say "build check skipped (local test root)"
  elif ! python3 "$REPO/tools/build_ncode.py" --check --release; then
    if [ "$APPLY" = 1 ]; then say "refusing to deploy: tools/build_ncode.py --check --release failed"; exit 1; fi
    say "(the build check fails; --apply would refuse)"
  fi
fi
for f in "${SOURCES[@]}"; do
  [ -e "$REPO/$f" ] || { say "missing $f"; exit 1; }
done

# ---- dry run: what would change on the live site ------------------------------------------
if [ "$APPLY" = 0 ]; then
  say "changes against the live webroot (read-only rsync -n):"
  if [ -n "$LOCAL_ROOT" ] && [ ! -d "$WEB_DEST" ]; then
    say "  (no webroot yet: every file is new)"
  else
    sync_from_repo -n -ai ${PUBLISH_DELETE[@]+"${PUBLISH_DELETE[@]}"} "${FILTERS[@]}" "${SRC[@]}" "$WEB_DEST/"
  fi
  say "steps --apply would run:"
  show rsync -a --delete "${FILTERS[@]}" "${SRC[@]}" "$STAGE_DEST/"
  if [ -n "$LOCAL_ROOT" ]; then
    show rsync -a --delete "${FILTERS[@]}" "$WEB_DEST/" "$PREV_DEST/"
    show rsync -a ${PUBLISH_DELETE[@]+"${PUBLISH_DELETE[@]}"} "${FILTERS[@]}" "$LOCAL_ROOT/home/$STAGE/" "$WEB_DEST/"
  else
    show ssh "$HOST" "sudo -n rsync -a --delete ${FILTERS[*]} $WEB/ $PREV/"
    show ssh "$HOST" "sudo -n rsync -a ${PUBLISH_DELETE[*]:-} ${FILTERS[*]} --chown=www-data:www-data ~/$STAGE/ $WEB/"
  fi
  say "dry run only; add --apply to deploy"
  exit 0
fi

# ---- apply ---------------------------------------------------------------------------------
if [ -n "$LOCAL_ROOT" ]; then
  mkdir -p "$STAGE_DEST" "$WEB_DEST"
  sync_from_repo -a --delete "${FILTERS[@]}" "${SRC[@]}" "$STAGE_DEST/"
  run rsync -a --delete "${FILTERS[@]}" "$WEB_DEST/" "$PREV_DEST/"
  run rsync -a ${PUBLISH_DELETE[@]+"${PUBLISH_DELETE[@]}"} "${FILTERS[@]}" "$STAGE_DEST/" "$WEB_DEST/"
  say "(local test root: no sudo and no --chown)"
else
  run ssh "$HOST" "mkdir -p ~/$STAGE"
  sync_from_repo -a --delete "${FILTERS[@]}" "${SRC[@]}" "$STAGE_DEST/"
  REMOTE="set -eu
sudo -n install -d -o www-data -g www-data -m 755 $WEB
sudo -n rsync -a --delete ${FILTERS[*]} $WEB/ $PREV/
sudo -n rsync -a ${PUBLISH_DELETE[*]:-} ${FILTERS[*]} --chown=www-data:www-data \$HOME/$STAGE/ $WEB/"
  run ssh "$HOST" "$REMOTE"
fi
BACK="tools/deploy.sh --rollback --apply"
[ "$APEX" = 1 ] && BACK="tools/deploy.sh --apex --rollback --apply"
say "deployed $SITE; the previous webroot is kept at $PREV ($BACK puts it back)"
