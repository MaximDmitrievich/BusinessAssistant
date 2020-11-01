from aiohttp import ClientSession, ClientResponse
from json import dumps

class RecognizerService:
    def __init__(self, client_session: ClientSession, url):
        self.client_session = client_session
        self.url = url

    async def recognize(self, text):
        headers= {'content-type': 'application/json'}
        if self.client_session is None:
            async with ClientSession() as session:
                response: ClientResponse  = await session.post(url=self.url, json={ "query": str(text) }, headers=headers)
        else:
            response: ClientResponse  = await self.client_session.post(url=self.url, json={ "query": str(text) }, headers=headers)
        return await response.json()