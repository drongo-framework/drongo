import base64
import hashlib

from .status_codes import HttpStatusCodes


class InvalidWebsocketConnection(Exception):
    pass


def _get_accept_key(env):
    magic_string = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    key = env.get('HTTP_SEC_WEBSOCKET_KEY')
    sha1 = hashlib.sha1((key + magic_string).encode('ascii')).digest()
    return base64.b64encode(sha1).decode()


def check_request_headers(ctx):
    if 'Upgrade' not in ctx.request.env.get('HTTP_CONNECTION', ''):
        raise InvalidWebsocketConnection('Connection header is invalid')

    if 'websocket' not in ctx.request.env.get('HTTP_UPGRADE', ''):
        raise InvalidWebsocketConnection('Upgrade header is invalid')

    if 'HTTP_SEC_WEBSOCKET_KEY' not in ctx.request.env:
        raise InvalidWebsocketConnection('Sec-WebSocket-Key header is missing')


def set_response(ctx):
    key = _get_accept_key(ctx.request.env)
    ctx.response.set_header(key='Upgrade', value='websocket')
    ctx.response.set_header(key='Connection', value='Upgrade')
    ctx.response.set_header(key='Sec-WebSocket-Accept', value=key)
    ctx.response.set_status(status_code=HttpStatusCodes.HTTP_101)
