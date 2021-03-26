#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=unused-variable

import aiohttp_session
import cryptography
from aiohttp_session import setup, get_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import asyncio

import aiohttp.web as web
from aiohttp.web import middleware
import aiohttp_jinja2 as jinja2
import urllib.parse
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

from functools import wraps

from s21 import air

BASE_DIR = os.path.dirname(__file__)
STATE_DIR = sys.argv[1] if len(sys.argv) >= 2 else BASE_DIR

COOKIE_SECRET = "EsYFdGSAN3tzzEy6wceEFFEUTVmHURYrvuXq5Am2CoM="

PREFIX = "ugra_booking_numbers_are_sequential_yet_ticket_prices_are_exponential_"
SECRET1 = b"entangled-defraud-shortcut-livable-repent"
SALT1_SIZE = 16
SECRET2 = b"clump-renovator-purge-data-sleek-whiff"
SALT2_SIZE = 16


def get_flag(token):
    return PREFIX + hmac.new(SECRET2, token.encode(), "sha256").hexdigest()[:SALT2_SIZE]


def raise_price(function):
    @wraps(function)
    async def wrapper(request):
        session = await get_session(request)
        session['hits'] = session.get('hits', 0) + 1
        return await function(request)
    return wrapper


def build_app():
    @middleware
    async def error_middleware(request, handler):
        try:
            response = await handler(request)
            
            if response.status == 404:
                return jinja2.render_template(f'404.html', request, {})
            return response
        except web.HTTPException as ex:
            if ex.status == 404:
                return jinja2.render_template(f'404.html', request, {})
            else:
                raise
    
    app = web.Application(middlewares=[error_middleware])
    routes = web.RouteTableDef()

    @routes.get('/favicon.ico')
    async def go_to_hell(request):
        raise web.HTTPNotFound()
    
    @routes.get('/')
    async def index_page(request):
        session = await get_session(request)
        return jinja2.render_template('index.html', request, {
            "flights": air.flights
        })
    
    @routes.get(r'/{page:(miles|corruption|cities|feedback)}')
    async def static_page(request):
        page = request.match_info['page']
        return jinja2.render_template(f'{page}.html', request, {})

    @routes.post('/place-an-order')
    @raise_price
    async def send_form(request):
        data = await request.post()        
        form = air.parse_search_form(data)
        notice = None

        # imitate the real thing as good as possible
        #await asyncio.sleep(random.randint(1, 7))

        if form:
            origin, destination, date = form
            destination = destination.split(' · ')[0]
            origin = origin.split(' · ')[0]
            
            session = await get_session(request)
            hits = session['hits']

            session['number'] = session['date'] = session['city'] = None

            if destination != air.flights[0][0]:
                notice = "<b>Невозможный пункт назначения</b> Мы автоматически исправили его на возможный"
            
            flights = air.build_search_results(origin, date, hits)
            return jinja2.render_template(f'form/1.html', request, {
                "flights": flights,
                "hm": air.flights[0]
            })
        else:
            raise web.HTTPNotFound()

    @routes.get('/place-an-order')
    @raise_price
    async def send_static_form(request):
        step = request.query.get('step')
        session = await get_session(request)
        hits = session['hits']
        # 1: flight selection
        # 2: class selection
        # 3: personal details
        # 4: contact information
        # 5: seat
        # 6: sandwich
        # 7: confirm booking
        try:
            step = int(step)
        except:
            return jinja2.render_template(f'404.html', request, {})
        if not step or step < 2 or step > 7:
            return jinja2.render_template(f'404.html', request, {})
        else:
            if step == 2:
                session['number'] = request.query.get('number')
                session['date'] = request.query.get('date')
                session['city'] = request.query.get('from')

            data = air.parse_cookies(session)
            if not data:
                return web.HTTPSeeOther('/')
            number, date, city = data['number'], data['date'], data['city']
                
            flights = air.build_search_results(city, date, hits)
            try:
                the_flight = list(filter(lambda x: str(x[5]) == number, flights))[0]
            except:
                return web.HTTPSeeOther('/')
            return jinja2.render_template(f'form/{step}.html', request, {
                "flight": the_flight
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
        tmp = os.environ['TMPDIR']
        web.run_app(app, path=os.path.join(tmp, 'airlines.sock'))


if __name__ == '__main__':
    start()
