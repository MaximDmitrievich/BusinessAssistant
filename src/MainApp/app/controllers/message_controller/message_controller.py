import os

from aiohttp.web import Request, WebSocketResponse
from aiohttp.http import WSMsgType, WSMessage
from aiohttp_rest_api import AioHTTPRestEndpoint
from aiohttp_rest_api.responses import respond_with_json, respond_with_html
from asyncio import get_event_loop, wait, shield
from concurrent.futures import ThreadPoolExecutor
from services.recognizer_service import RecognizerService
from json import loads, dumps

class MessageController(AioHTTPRestEndpoint):
    def __init__(self, recognizer: RecognizerService):
        self.recognizer = recognizer

    async def post(self, request: Request):
        data = None
        status = 500
        if request.body_exists and request.query is not None:
            body = await request.json()
            message = body['message']
            data = await self.recognizer.recognize(message)
            if data is not None:
                status = 201
            else:
                status = 400
                data = {}
        return respond_with_json(status=status, data=data)

