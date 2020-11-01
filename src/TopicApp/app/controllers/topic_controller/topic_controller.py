import os

from aiohttp.web import Request, Response
from asyncio import sleep, Lock
from bertopic import BERTopic
from aiohttp_rest_api import AioHTTPRestEndpoint
from aiohttp_rest_api.responses import respond_with_json, respond_with_html
from asyncio import get_event_loop, wait, shield
from concurrent.futures import ThreadPoolExecutor
from json import loads, dumps
from stop_words import get_stop_words
import re
from natasha import (
    NewsEmbedding,   
    NewsNERTagger,
)

emb = NewsEmbedding()
ner_tagger = NewsNERTagger(emb)
stop_words = get_stop_words('ru')

def clearing(line):
    markup = ner_tagger(line)
    for_remove = []
    for span in markup.spans:
        for_remove.append(line[span.start:span.stop])
    for remove in for_remove:
        line =  line.replace(remove, '')
    line = line.lower()
    line =' '.join(re.sub("(@[A-Za-zА-Яа-я]+)|([^A-Za-zА-Яа-я \\t])|(\\w+:\\/\\/\\S+)"," ",line).split())
    line = line.split(' ')
    line = [x for x in line if x not in stop_words]
    return ' '.join(line)

class TopicController(AioHTTPRestEndpoint):
    def __init__(self, model: BERTopic):
        self.model = model

    async def post(self, request: Request):
        data = None
        status = 500
        if request.body_exists and request.query is not None:
            body = await request.json()
            text = body['text']
            trans = []
            try:
                for line in text.split('.'):
                    trans.append(clearing(line+'.'))
                index_topic = self.model.transform(trans)
            data = index_topic
            if data is not None:
                status = 201
            else:
                status = 400
                data = {}
        return respond_with_json(status=status, data=data)

