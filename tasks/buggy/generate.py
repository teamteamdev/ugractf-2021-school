#!/usr/bin/env python3

import hmac
import json
import hashlib
import os
import sys
import shutil

PREFIX = "ugra_smaller_is_better_"
SECRET = b"||43.plain.REACH.bread.88||"

PREFIX_SIZE = 24
XOR_VALUE = 37
XOR_MODIFY_VALUE = 71
CRYPTO_ROUNDS = 13
CRYPTO_ALGO = "SHA1"

SUFFIX_SIZE = 2 * hashlib.new(CRYPTO_ALGO).digest_size
SALT_SIZE = PREFIX_SIZE + SUFFIX_SIZE - len(PREFIX)

def encode_flag(flag):
    prefix = flag[:PREFIX_SIZE]
    suffix = flag[PREFIX_SIZE:]
    if len(suffix) != SUFFIX_SIZE:
        raise RuntimeError(f"Flag is of invalid size: {len(suffix)}")

    xor_value = XOR_VALUE

    encoded_prefix = bytearray()
    for c in prefix:
        encoded_prefix.append(ord(c) ^ xor_value)
        xor_value = (xor_value + XOR_MODIFY_VALUE) % 256
    encoded_prefix.append(ord('%') ^ xor_value)

    encoded_suffix = bytearray()
    for c in suffix:
        encoded_suffix.append(ord(c) ^ xor_value)
        xor_value = (xor_value + XOR_MODIFY_VALUE) % 256
    encoded_suffix.append(ord('%') ^ xor_value)

    return (bytes(encoded_prefix), bytes(encoded_suffix))

def replace_placeholder(data, placeholder, prefix):
    prefix_placeholder = placeholder + b"_" * (len(prefix) - 1 - len(placeholder)) + b"\0"
    new_data = data.replace(prefix_placeholder, prefix)
    if data == new_data:
        raise RuntimeError(f"Couldn't replace {prefix_placeholder}") 
    return new_data


def get_flag():
    user_id = sys.argv[1]
    return PREFIX + hmac.new(SECRET, str(user_id).encode(), "sha256").hexdigest()[:SALT_SIZE]


def generate():
    if len(sys.argv) < 3:
        print("Usage: generate.py user_id target_dir", file=sys.stderr)
        sys.exit(1)
    target_dir = sys.argv[2]

    flag = get_flag()
    prefix, suffix = encode_flag(flag)

    data = open(os.path.join("private", "get_flag"), "rb").read()
    data = replace_placeholder(data, b"PREFIX", prefix)
    data = replace_placeholder(data, b"SUFFIX", suffix)
    with open(os.path.join(target_dir, "get_flag"), "wb") as out:
        out.write(data)

    decoded_suffix = flag[PREFIX_SIZE:PREFIX_SIZE + SUFFIX_SIZE]
    for i in range(CRYPTO_ROUNDS):
        m = hashlib.new(CRYPTO_ALGO)
        m.update(decoded_suffix.encode("utf-8"))
        decoded_suffix = m.hexdigest()

    new_flag = flag[:PREFIX_SIZE] + decoded_suffix

    json.dump({
        "flags": [new_flag],
        "substitutions": {},
        "urls": []
    }, sys.stdout)


if __name__ == "__main__":
    generate()
