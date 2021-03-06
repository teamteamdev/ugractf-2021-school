#!/usr/bin/env python3
import hmac
import json
import sys


PREFIX = "ugra_etot_paren_byl_iz_teh_"
SECRET1 = b"ri8rjgrjv9efjdfltifegidvlergkykd9f3otkfgjeofuwrtalrttrye4r"
SALT1_SIZE = 16
SECRET2 = b"omgkekomgkeklolaoaoaoaogoodkfas38"
SALT2_SIZE = 16


def get_user_tokens():
    user_id = sys.argv[1]

    token = hmac.new(SECRET1, str(user_id).encode(), "sha256").hexdigest()[:SALT1_SIZE]
    flag = PREFIX + hmac.new(SECRET2, token.encode(), "sha256").hexdigest()[:SALT2_SIZE]

    return token, flag


def generate():
    if len(sys.argv) < 3:
        print("Usage: generate.py user_id target_dir", file=sys.stderr)
        sys.exit(1)

    token, flag = get_user_tokens()

    json.dump({
        "flags": [flag],
        "substitutions": {},
        "urls": [f"https://urtracing.{{hostname}}/{token}/"]
    }, sys.stdout)


if __name__ == "__main__":
    generate()
