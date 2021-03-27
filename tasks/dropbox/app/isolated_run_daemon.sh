#!/usr/bin/env bash

exec gunicorn -b "unix:$1/dropbox.sock" "server:make_app()"
