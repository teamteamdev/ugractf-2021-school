#!/usr/bin/env nix-shell
#!nix-shell -i sh shell.nix

exec "$TMPDIR/isolate" ./isolated_run_daemon.sh "$@"
