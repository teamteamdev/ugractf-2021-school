#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=unused-variable

import aiohttp_session
import cryptography
from aiohttp_session import setup, get_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import asyncio

import aiohttp.web as web
import aiohttp_jinja2 as jinja2
import asyncio
import base64
import random
import math
import hmac
import json
import os
import io
import sys
from jinja2 import FileSystemLoader
import base64
import time

BASE_DIR = os.path.dirname(__file__)
STATE_DIR = sys.argv[1] if len(sys.argv) >= 2 else BASE_DIR

PREFIX = "ugra_i_is_to_ro_as_ro_is_to_ha_"
SECRET1 = b"foo-bar-baz-employment-statistics-department-tools-python"
SALT1_SIZE = 16
SECRET2 = b"eEEEeeHlaStikBlinseventydegrees13percentandAflyIngSaucer"
SALT2_SIZE = 16
COOKIE_SECRET = "6EsYFdGSAN3VtRzzEywceWEFEUTmHUYrvuXq5Am2CoM="

ALPHABET = "いろはにほへとちりぬるをわかよたれそつねならむうゐのおくやまけふこえてあさきゆめみしゑひもせす"


def get_flag(token):
    return PREFIX + hmac.new(SECRET2, token.encode(), 'sha256').hexdigest()[:SALT2_SIZE]


def get_tries(session):
    tries_count = session.get('tries_count')
    if tries_count is None:
        session['tries_count'] = 0
    return tries_count


def get_poem(poems, token):
    random.seed(token)
    return '\n'.join(random.choices(poems, k=3)).strip()


def atbash(text):
    m = len(ALPHABET)
    ciphertext = ""
    for c in text:
        if c in ALPHABET:
            c = (ALPHABET[::-1])[ALPHABET.index(c)]
        ciphertext += c
    return ciphertext


def build_app():
    app = web.Application()
    routes = web.RouteTableDef()

    with open('poems.txt', 'r') as poems_file:
        poems = poems_file.read().split('\n')[:-1]
        print(poems)

    @routes.post('/{token}')
    @routes.get('/{token}')
    async def index_page(request):
        session = await get_session(request)
        tries_count = get_tries(session)
        token = request.match_info['token']

        poem = get_poem(poems, token)
        ciphertext = atbash(poem)

        if request.method == 'POST':
            data = await request.post()
            answer = data.get('answer', 'no_answer!!!').replace('\r', '')
            msg = flag = False
            mascot = "angry"

            if answer == poem:
                flag = get_flag(token)
                mascot = "happy"
            elif answer == 'no_answer!!!' or answer == "":
                mascot = "angry"
                msg = "Your answer is malformed. Please seek help. P.S. YOU MADE MATITYAHU-KUN ANGRY."
            else:
                mascot = "sad"
                msg = "Your answer is incorrect. May the patience and wisdom overcome your inpatience..."            
            return jinja2.render_template(f'index.html', request, {
                "ciphertext": ciphertext,
                "mascot": mascot,
                "msg": msg,
                "flag": flag
            })
        else:
            return jinja2.render_template(f'index.html', request, {
                "ciphertext": ciphertext,
                "mascot": "happy"
            })
            
    routes.static('/static', 'static')

    aiohttp_session.setup(app, EncryptedCookieStorage(base64.b64decode(COOKIE_SECRET)))
    app.add_routes(routes)
    jinja2.setup(
        app,
        loader=FileSystemLoader(os.path.join(BASE_DIR, 'templates'))
    )
    return app


def start():
    app = build_app()

    loop = asyncio.get_event_loop()

    if os.environ.get('DEBUG') == 'F':
        web.run_app(app, host='0.0.0.0', port=31337)
    else:
        web.run_app(app, path=os.path.join(STATE_DIR, 'japcipher.sock'))


if __name__ == '__main__':
    start()
