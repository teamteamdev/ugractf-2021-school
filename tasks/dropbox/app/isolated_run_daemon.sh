#!/usr/bin/env bash

STATE_DIR=$1 exec gunicorn -b "unix:$TMPDIR/dropbox.sock" "server:make_app()"
