#!/usr/bin/env nix-shell
#!nix-shell -i sh -p python3 openssl openssl-chacha

exec ./generate.py "$@"
