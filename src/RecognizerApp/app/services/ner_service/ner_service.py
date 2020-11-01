from aiohttp import ClientSession
from aiohttp.client_reqrep import ClientResponse
from json import dumps


class NERService:
    def __init__(self, client_session: ClientSession, url):
        self.client_session = client_session
        self.url = url

    async def detect(self, text):
        headers= {'content-type': 'application/json'}
        if self.client_session is None:
            async with ClientSession() as session:
                response: ClientResponse = await session.post(url=self.url, json={ "text": str(text) }, headers=headers)
        else:
            response: ClientResponse = await self.client_session.post(url=self.url, json={ "text": str(text) }, headers=headers)
        return response.json()