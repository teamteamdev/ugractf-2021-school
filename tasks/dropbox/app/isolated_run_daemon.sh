#!/usr/bin/env bash

exec gunicorn -b "unix:$TMPDIR/dropbox.sock" "server:make_app()"
