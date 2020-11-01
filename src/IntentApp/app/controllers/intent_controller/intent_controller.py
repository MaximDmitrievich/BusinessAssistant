import os

from aiohttp.web import Request, WebSocketResponse
from asyncio import sleep, Lock
from simpletransformers.classification import ClassificationModel
from aiohttp.http import WSMsgType, WSMessage
from aiohttp_rest_api import AioHTTPRestEndpoint
from aiohttp_rest_api.responses import respond_with_json, respond_with_html
from asyncio import get_event_loop, wait, shield
from concurrent.futures import ThreadPoolExecutor
from json import loads, dumps

class IntentController(AioHTTPRestEndpoint):
    def __init__(self, model: ClassificationModel):
        self.model = model
        self.raw_pred = [
            '110-АПК',
            '176-АПК',
            '170-АПК',
            '310-ГК',
            '11-ГК',
            '181-АПК',
            '123-АПК',
            '29-АПК',
            '64-АПК',
            '75-АПК',
            '200-АПК',
            '4-АПК',
            '180-АПК',
            '156-АПК',
            '309-ГК',
            '71-АПК',
            '198-АПК',
            '167-АПК',
            '8-ГК',
            '65-АПК',
            '12-ГК',
            '171-АПК',
            '68-АПК',
            '201-АПК'
        ]

    async def post(self, request: Request):
        data = None
        status = 500
        if request.body_exists and request.query is not None:
            body = await request.json()
            text = body['text']
            predictions, raw_outputs = self.model.predict([text])
            for pred in range(len(predictions)):
                if predictions[pred]:
                    data = [self.raw_pred[pred]]
            if data is not None:
                status = 201
            else:
                status = 400
                data = {}
        return respond_with_json(status=status, data=data)

