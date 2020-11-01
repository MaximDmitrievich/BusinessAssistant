import os

from aiohttp.web import Request, WebSocketResponse
from aiohttp.http import WSMsgType, WSMessage
from aiohttp_rest_api import AioHTTPRestEndpoint
from aiohttp_rest_api.responses import respond_with_json, respond_with_html
from asyncio import get_event_loop, wait, shield
from concurrent.futures import ThreadPoolExecutor
from services.intent_service import IntentService
from services.ner_service import NERService
from services.topic_service import TopicService
from json import loads, dumps

class ResolverController(AioHTTPRestEndpoint):
    def __init__(self, intent: IntentService, ner: NERService, topic: TopicService):
        self.intent = intent
        self.ner = ner
        self.topic = topic

    async def post(self, request: Request):
        data = None
        status = 500
        if request.body_exists and request.query is not None:
            body = await request.json()
            text = body['text']
            data = {"Entities": None, "Intents": None, "Topic": None}
            intent = await self.intent.detect(text)
            data["Intents"] = intent
            ner = await self.ner.detect(text)
            data["Entities"] = ner
            #topic = await self.topic.detect(text)
            #data["Topic"] = topic
            if data is not None:
                status = 201
            else:
                status = 400
                data = {}
        return respond_with_json(status=status, data=data)