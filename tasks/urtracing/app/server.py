#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import aiohttp
import aiohttp.web as web
import hmac
import os
import json
import sys
import random
from datetime import datetime
from dataclasses import dataclass
import math
import threading

BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE_DIR, 'static')

PREFIX = "ugra_etot_paren_byl_iz_teh_"
SECRET1 = b"ri8rjgrjv9efjdfltifegidvlergkykd9f3otkfgjeofuwrtalrttrye4r"
SALT1_SIZE = 16
SECRET2 = b"omgkekomgkeklolaoaoaoaogoodkfas38"
SALT2_SIZE = 16

CPS = 20

with open('poems.txt', 'r') as file:
    poems = file.read().split('*\n')


@dataclass
class gameState():
    token: str
    session_id: int
    text: str
    status: str = 'continue'
    mistakes: int = 0
    cursor: int = 0
    start_time: float = 0
    last_good: float = 0
    last_mistake: float = 0
    avg: float = 0
    accuracy: float = 0
    opponent_cursor: int = 0
    prize: str = ''


def getText():
    return random.choice(poems)


def get_flag(token):
    return PREFIX + hmac.new(
        SECRET2, token.encode(),
        'sha256').hexdigest()[:SALT2_SIZE]


def mimicOpponent(duration, entropy):
    return int(CPS * duration + 1.7 * math.sin(duration + 0.2 * entropy))


def updateState(s, msg=None):
    now = datetime.now().timestamp()
    if msg:
        try:
            inp = chr(int(msg.data))
            if inp == '\r':
                inp = '\n'
        except ValueError:
            s.mistakes += 1
            s.last_mistake = now
            return s
    else:
        inp = ''

    duration = max(
        s.last_good - s.start_time,
        s.last_mistake - s.start_time,
    )
    s.opponent_cursor = mimicOpponent(
        now - s.start_time,
        ord(s.token[-1])
    )
    ai_won = s.opponent_cursor >= len(s.text)
    if ai_won:
        s.status = 'finish'

    if s.text[s.cursor] == inp:
        s.cursor += 1
        s.last_good = now

        you_won = s.cursor >= len(s.text)
        if you_won:
            s.prize = get_flag(s.token)
            s.status = 'finish'
    elif msg:
        s.mistakes += 1
        s.last_mistake = now

    if s.cursor > 0:
        s.avg = s.cursor / duration
        s.accuracy = s.cursor / (s.mistakes + s.cursor)

    return s


async def pingState(state, ws):
    while True:
        state = updateState(state)
        await ws.send_str(json.dumps(vars(state)))
        await asyncio.sleep(0.25)


def build_app():
    app = web.Application()
    routes = web.RouteTableDef()

    @routes.get('/{token}/')
    async def main(request):
        return web.FileResponse(os.path.join(STATIC_DIR, 'index.html'))

    @routes.get('/{token}/ws')
    async def websocket_handler(request):
        token = request.match_info['token']
        ws = web.WebSocketResponse(heartbeat=5)
        await ws.prepare(request)

        state = gameState(
            token=token,
            session_id=id(ws),
            text=getText(),
            start_time=datetime.now().timestamp()
        )
        await ws.send_str(json.dumps(vars(state)))

        t = threading.Thread(target=asyncio.run, args=(pingState(state, ws),))
        t.start()

        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                state = updateState(state, msg)
                await ws.send_str(json.dumps(vars(state)))
            elif msg.type == aiohttp.WSMsgType.ERROR:
                t.stop()
                return ws
        t.stop()

    routes.static('/static', STATIC_DIR)

    app.add_routes(routes)
    return app


def start():
    app = build_app()

    if os.environ.get('DEBUG') == 'F':
        web.run_app(app, host='0.0.0.0', port=31337)
    else:
        tmp = os.environ.get('TMP_DIR')
        web.run_app(app, path=os.path.join(tmp, 'urtracing.sock'))


if __name__ == '__main__':
    start()
