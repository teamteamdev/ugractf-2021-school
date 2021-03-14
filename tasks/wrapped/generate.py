#!/usr/bin/env python3

import base64
import hmac
import json
import os
import random
import subprocess
import sys
import yaml

PREFIX = "ugra_seal_it_file_it_batch_it_mark_it_"
SECRET = b"oophooweeha1eevoh3hei9Ziequa5alooghaish4naen"
SALT_SIZE = 14


def get_flag():
    user_id = sys.argv[1]
    return PREFIX + hmac.new(SECRET, str(user_id).encode(), "sha256").hexdigest()[:SALT_SIZE]


def generate():
    if len(sys.argv) < 3:
        print("Usage: generate.py user_id target_dir", file=sys.stderr)
        sys.exit(1)

    random.seed(hmac.new(SECRET, str(sys.argv[1]).encode(), "sha256").digest())

    flag = get_flag()

    k = f"{random.getrandbits(256):064x}"
    s = f"{random.getrandbits(128):032x}"
    iv = f"{random.getrandbits(128):032x}"

    cipher = subprocess.check_output(f"echo -n '{flag}' | openssl enc -e -chacha20 -K {k} -S {s} -iv {iv}",
                                     shell=True)
    data = yaml.safe_load(open(os.path.join("private", "template.yaml")).read()
                          .replace("+++K+++", base64.b64encode(bytes.fromhex(k)).decode())
                          .replace("+++S+++", base64.b64encode(bytes.fromhex(s)).decode())
                          .replace("+++IV+++", base64.b64encode(bytes.fromhex(iv)).decode())
                          .replace("+++CIPHER+++", base64.b64encode(cipher).decode()))
    json.dump(data, open(os.path.join(sys.argv[2], "wrapped.json"), "w"), indent=4)

    json.dump({"flags": [flag], "substitutions": {}, "urls": []}, sys.stdout)


if __name__ == "__main__":
    generate()
