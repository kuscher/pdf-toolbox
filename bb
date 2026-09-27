#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Dev helper for BentoBook: build, install and test the app on a Googlebook
# over adb (Wireless debugging, set up by VSCodeBook's `vscodebook android`),
# and publish releases.
#
#   ./bb app                  build, install and launch
#   ./bb install | start | stop | logs [N]
#   ./bb debug CMD            dump | reload | open PATH | crash | devtools on|off
#   ./bb cdp ...              DevTools on the app's WebView (tools/cdp.py)
#   ./bb shot [FILE] [full]   screenshot the app window (or the full screen)
#   ./bb share                copy the APK to the Googlebook's Download folder
#   ./bb incoming FILE...     hand files to the app as if shared to it (they are
#                             saved to Download/ first; debug builds of the flow)
#   ./bb live-resize [on|off|status]
#                             resize the window live instead of under a veil
#                             (Android's per-app ENABLE_FLUID_RESIZING switch)
#   ./bb smoke [CHECK...]     run the engines end to end on the device (tools/smoke.py)
#   ./bb release [--publish]  release files for the version in AndroidManifest.xml
#                             (tools/release.sh); --publish makes the GitHub release
#
# adb's server listens on a Unix socket, not tcp:5037: the Terminal forwards
# every TCP port in the VM to Android, where any app could use it.
set -euo pipefail
cd "$(dirname "$(readlink -f "$0")")"
CONF=${XDG_CONFIG_HOME:-$HOME/.config}/vscodebook
SERIAL=${ADB_SERIAL:-$(cat "$CONF/adb-serial" 2>/dev/null || echo none)}
mkdir -p "$HOME/.local/state/vscodebook"
export ADB_SERVER_SOCKET=${ADB_SERVER_SOCKET:-localfilesystem:$HOME/.local/state/vscodebook/adb.sock}
export ADB_SERIAL=$SERIAL CDP_PKG=local.bentobook CDP_SOCK=/tmp/claude-$(id -u)/bb-devtools.sock
PKG=local.bentobook
A=(adb -s "$SERIAL")

adb_up() { # connects on demand, finding Wireless debugging's port if it changed
  "${A[@]}" get-state >/dev/null 2>&1 && return
  vscodebook android connect >/dev/null || exit 1
  SERIAL=$(cat "$CONF/adb-serial"); A=(adb -s "$SERIAL"); export ADB_SERIAL=$SERIAL
}

install() {
  # Play Protect would stop an adb install to scan it; skip that, then restore.
  "${A[@]}" shell settings put global verifier_verify_adb_installs 0
  "${A[@]}" install -r build/BentoBook.apk || { "${A[@]}" shell settings put global verifier_verify_adb_installs 1; exit 1; }
  "${A[@]}" shell settings put global verifier_verify_adb_installs 1
}

share() { # MediaStore Downloads of the current Android user
  local apk=executables/BentoBook-$(sed -n 's/.*versionName="\([^"]*\)".*/\1/p' AndroidManifest.xml).apk name user tmp id
  [[ -f $apk ]] || { echo "no $apk"; exit 1; }
  name=$(basename "$apk"); user=$("${A[@]}" shell am get-current-user | tr -d '\r'); tmp=/data/local/tmp/$name
  "${A[@]}" push "$apk" "$tmp" >/dev/null
  "${A[@]}" shell content delete --user "$user" --uri content://media/external/downloads \
    --where "\"_display_name='$name'\"" >/dev/null 2>&1 || true
  "${A[@]}" shell content insert --user "$user" --uri content://media/external/downloads \
    --bind _display_name:s:"$name" --bind mime_type:s:application/vnd.android.package-archive
  id=$("${A[@]}" shell content query --user "$user" --uri content://media/external/downloads \
    --projection _id --where "\"_display_name='$name'\"" | grep -o '_id=[0-9]*' | tail -1 | cut -d= -f2)
  [[ -n $id ]] || { echo "could not create Download/$name"; exit 1; }
  "${A[@]}" shell "content write --user $user --uri content://media/external/downloads/$id < $tmp"
  "${A[@]}" shell rm -f "$tmp"
  echo "Download/$name on the Googlebook"
}

start() { "${A[@]}" shell am start --user current -n $PKG/.MainActivity >/dev/null; }

debug() {
  local cmd=$1; shift || true
  local args=(--es cmd "$cmd")
  case $cmd in
    devtools) args+=(--ez on "$([[ ${1:-on} == on ]] && echo true || echo false)") ;;
    open) args+=(--es path "${1:?path, e.g. /merge-pdf}") ;;
  esac
  "${A[@]}" shell am broadcast -a local.bentobook.DEBUG -p $PKG "${args[@]}" >/dev/null
  if [[ $cmd == dump ]]; then
    sleep 1
    "${A[@]}" logcat -d -s BentoBook:I | grep -E "state |page ready|isolation" | tail -4
  fi
}

case ${1:-} in
  app) ./build.sh && adb_up && install && start ;;
  install) adb_up; install ;;
  start) adb_up; start ;;
  stop) adb_up; "${A[@]}" shell am force-stop --user current $PKG ;;
  logs) adb_up; "${A[@]}" logcat -d -s BentoBook:* chromium:* cr_*:* | tail -"${2:-60}" ;;
  share) adb_up; share ;;
  incoming)
    adb_up; shift; append=false
    for f in "$@"; do
      "${A[@]}" shell am broadcast -a local.bentobook.DEBUG -p $PKG --es cmd incoming \
        --es name "'$(basename "$f")'" --es b64 "$(base64 -w0 "$f")" --ez append $append >/dev/null
      append=true
    done ;;
  debug) shift; adb_up; debug "$@" ;;
  live-resize)
    # Desktop windowing shows a veil (icon on a plain colour) while a window is
    # resized, unless compat change ENABLE_FLUID_RESIZING is on for the app;
    # Google sets it for its own apps. It is @Overridable, so the shell may set
    # it on a release build too. It survives app updates; the platform saves
    # overrides in /data/misc/appcompat, so reboots should keep it as well.
    # SystemUI picks veil or live when it decorates a window, so it applies to
    # windows opened afterwards.
    adb_up
    case ${2:-on} in
      on) "${A[@]}" shell am compat enable ENABLE_FLUID_RESIZING $PKG ;;
      off) "${A[@]}" shell am compat reset ENABLE_FLUID_RESIZING $PKG ;;
      status)
        "${A[@]}" shell dumpsys platform_compat | grep 'name=ENABLE_FLUID_RESIZING;' |
          grep -q "[{ ]$PKG=true" && echo on || echo off ;;
      *) echo "usage: ./bb live-resize [on|off|status]" >&2; exit 2 ;;
    esac ;;
  cdp) shift; adb_up; python3 tools/cdp.py "$@" ;;
  smoke) shift; adb_up; python3 tools/smoke.py "$@" ;;
  release) shift; tools/release.sh "$@" ;;
  shot)
    adb_up
    out=${2:-/tmp/claude-$(id -u)/bb-shot.png}
    "${A[@]}" exec-out screencap -p > "$out.full.png"
    if [[ ${3:-} == full ]]; then
      mv "$out.full.png" "$out"
    else
      # The app's largest window: tooltips and menus are windows too.
      read -r x1 y1 x2 y2 < <("${A[@]}" shell dumpsys window windows |
        awk -v pkg="$PKG" '/Window #/ { inpkg = index($0, pkg) > 0 } inpkg && /frame=\[/ { print }' |
        grep -o 'frame=\[[0-9-]*,[0-9-]*\]\[[0-9]*,[0-9]*\]' | tr -c '0-9\n-' ' ' |
        awk '{ a = ($3 - $1) * ($4 - $2); if (a > best) { best = a; line = $1 " " $2 " " $3 " " $4 } } END { print line }')
      python3 tools/crop.py "$out.full.png" "$out" "$x1" "$y1" "$((x2 - x1))" "$((y2 - y1))"
      rm -f "$out.full.png"
    fi
    echo "$out" ;;
  *) sed -n '3,20p' "$0"; exit 1 ;;
esac
