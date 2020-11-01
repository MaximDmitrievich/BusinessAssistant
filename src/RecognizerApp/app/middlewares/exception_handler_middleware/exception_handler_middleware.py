from aiohttp.web_exceptions import HTTPException
from aiohttp.web import Request, Response, middleware
from aiohttp_rest_api.responses import respond_with_json
from sys import exc_info
import json
from time import time
from logging import Logger, INFO, ERROR



class ExceptionHandlerMiddleware:
    def __init__(self, logger: Logger):
        self.logger = logger

    @middleware
    async def logging(self, request: Request, handler) -> Response:
        start = time()
        try:
            response: Response = await handler(request)
            self.logger.info("Request finished in {:.2f}ms {} {}".format((time() - start) * 100, response.status, response.content_type))
            return response
        except HTTPException as exc:
            self.logger.exception(exc.body)
            return respond_with_json(data=exc, status=exc.status)
        except Exception as exc:
            self.logger.error(exc, exc_info=True)
            raise(exc)