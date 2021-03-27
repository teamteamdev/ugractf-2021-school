#!/usr/bin/python3

import hashlib
import hmac
import os, sys

PREFIX = "ugra_agents_of_a_feather_duck_together_"
SECRET2 = b"raeF2Ko9eTohF"
SALT2_SIZE = 12
SECRET3 = b"Iey9ooxepheev"

def verify_code(code):
    h, sig = code[:40], code[40:]
    signature = hmac.new(SECRET3, h.encode(), "sha256").hexdigest()
    return all(i in "0123456789abcdef" for i in code) and sig == signature

token, secret = input('Your secret? ').strip().split('o')

if verify_code(secret):
    print(PREFIX + hmac.new(SECRET2, token.encode(), 'sha256').hexdigest()[:SALT2_SIZE])
else:
    print('Not true.')
