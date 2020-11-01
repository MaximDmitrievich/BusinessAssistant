import os

from aiohttp.web import Request, WebSocketResponse
from aiohttp.http import WSMsgType, WSMessage
from aiohttp_rest_api import AioHTTPRestEndpoint
from aiohttp_rest_api.responses import respond_with_json, respond_with_html
from asyncio import get_event_loop, wait, shield
from concurrent.futures import ThreadPoolExecutor
from services.db_provider import DBProvider
from json import loads, dumps

class SearchController(AioHTTPRestEndpoint):
    def __init__(self, db_provider: DBProvider):
        self.db_provider = db_provider

    async def search(self, request: Request):
        result = []
        if request.query is not None:
            query = request.query['q']
            return respond_with_json(status=200, data=self.db_provider.search(query))
