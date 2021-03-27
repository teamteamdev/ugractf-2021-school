#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hmac
import os
import io
import pathlib
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, send_file

ROOT_FOLDER = 'fake'
APP_PATH = 'opt/dropbox/app/storage'
PREFIX = 'ugra_plus_twenty_social_points_'
FLAG_SECRET = b'2RG64fXAGfLZQSDK'
FLAG_SALT_SIZE = 12

app = Flask(__name__)


def generate_flag(token):
    return PREFIX + hmac.new(FLAG_SECRET, token.encode(), 'sha256').hexdigest()[:FLAG_SALT_SIZE]


def fix_char(c):
    if not (97 <= ord(c) <= 122):
        return chr(ord(c) + 32)
    return c


def fix_extension(filename):
    extension_index = filename.rfind('.')
    if extension_index == -1 or extension_index == len(filename):
        return filename
    extension = filename[extension_index + 1:]
    filename_without_extension = filename[:extension_index + 1] if extension_index > 0 else ''
    extension = ''.join([fix_char(c) for c in extension])
    return filename_without_extension + extension


@app.route('/<token>/')
def index(token):
    return render_template('index.html', token=token)


@app.route('/<token>/upload', methods=['POST'])
def upload(token):
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', info='Документ не указан. Вы укажите.', token=token)
    filename = secure_filename(file.filename)
    filename = fix_extension(filename)
    if os.path.exists(os.path.join(ROOT_FOLDER, APP_PATH, filename)):
        return render_template('index.html', info='Документ с имя %s существует. Не расстраивайте товарищ Xi Зиньпин!' % filename, token=token)
    file.save(os.path.join(ROOT_FOLDER, APP_PATH, filename))
    link = request.url_root + token + '/getfile?filename=' + filename
    return render_template('upload.html', link=link, token=token)


@app.route('/<token>/getfile')
def getfile(token):
    filename = request.args.get('filename', '')
    if filename == '':
        return 'Документ не обнаружен.'

    filename = fix_extension(filename)
    path = pathlib.PurePath('/', APP_PATH)

    for item in pathlib.PurePath(filename).parts:
        if item == '..':
            path = path.parent
        else:
            path = path / item

    path = ROOT_FOLDER + str(path)

    try:
        f = open(path, 'rb')
        content = f.read().replace(b'!!!{{{flag}}}!!!', generate_flag(token).encode())
        return send_file(filename_or_fp=io.BytesIO(content), as_attachment=True, attachment_filename=filename)
    except FileNotFoundError:
        return 'Документ с имя %s не обнаружен.' % filename
    except IsADirectoryError:
        return "IsADirectoryError: [Errno 21] Is a directory: '%s'" % filename


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)