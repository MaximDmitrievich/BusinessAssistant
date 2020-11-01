import os

from aiohttp.web import Request, Response
from asyncio import sleep, Lock
from simpletransformers.ner import NERModel
from aiohttp_rest_api import AioHTTPRestEndpoint
from aiohttp_rest_api.responses import respond_with_json, respond_with_html
from asyncio import get_event_loop, wait, shield
from concurrent.futures import ThreadPoolExecutor
from json import loads, dumps

class NERController(AioHTTPRestEndpoint):
    def __init__(self, model: NERModel):
        self.model = model

    async def post(self, request: Request):
        data = None
        status = 500
        if request.body_exists and request.query is not None:
            body = await request.json()
            text = body['text']
            data = self.model.predict([text])[0][0]
            if data is not None:
                status = 201
            else:
                status = 400
                data = {}
        return respond_with_json(status=status, data=data)

