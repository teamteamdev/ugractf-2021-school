#!/usr/bin/env nix-shell
#!nix-shell -i sh -p python3 python38Packages.pyyaml openssl

exec ./generate.py "$@"
