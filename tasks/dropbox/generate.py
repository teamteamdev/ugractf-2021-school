import hmac
import sys
import json

PREFIX = 'ugra_dvoinoi_ris_etot_gospodin'
TOKEN_SECRET = b'zRo5A4KVHQCmKyXu'
TOKEN_SALT_SIZE = 16
FLAG_SECRET = b'2RG64fXAGfLZQSDK'
FLAG_SALT_SIZE = 12


def get_user_tokens():
    user_id = sys.argv[1]

    token = hmac.new(TOKEN_SECRET, str(user_id).encode(), 'sha256').hexdigest()[:TOKEN_SALT_SIZE]
    flag = PREFIX + hmac.new(FLAG_SECRET, token.encode(), 'sha256').hexdigest()[:FLAG_SALT_SIZE]

    return token, flag


def generate():
    if len(sys.argv) < 3:
        print('Usage: generate.py user_id target_dir', file=sys.stderr)
        sys.exit(1)

    token, flag = get_user_tokens()

    json.dump({
        'flags': [flag],
        'substitutions': {},
        'urls': [f'https://dropbox.{{hostname}}/{token}/']
    }, sys.stdout)


if __name__ == '__main__':
    generate()