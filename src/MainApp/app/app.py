from os import environ
from aiohttp import ClientSession
from aiohttp.web import Application, AppRunner, TCPSite
from asyncio import get_event_loop, ensure_future
from logging import INFO, getLogger
from pymongo.mongo_client import MongoClient
from services.recognizer_service.recognizer_service import RecognizerService

from controllers.message_controller.message_controller import MessageController
from controllers.search_controller.search_controller import SearchController
from services.db_provider import DBProvider
from middlewares.exception_handler_middleware import ExceptionHandlerMiddleware

if __name__ == "__main__":
    logger = getLogger(environ['APP_NAME'])
    logger.setLevel(INFO)

    middleware = ExceptionHandlerMiddleware(logger)
    db = DBProvider(MongoClient('0.0.0.0', 5002))
    recognizer = RecognizerService(None, "http://{}:{}/api/recognize".format(environ["RECOGNIZER_HOST"], environ["RECOGNIZER_PORT"]))

    async def main(loop=None):
        message_controller = MessageController(recognizer)
        search_controller = SearchController(db)
        
        application = Application(middlewares=[middleware.logging], logger=logger)
        application.router.add_post('/api/messages', message_controller.post)
        application.router.add_get('/api/search', search_controller.search)

        runner = AppRunner(application)
        await runner.setup()
        site = TCPSite(runner, environ['APP_HOST'], int(environ['APP_PORT']))
        await site.start()

    loop = get_event_loop()
    try:
        ensure_future(main(loop=loop), loop=loop)
        loop.run_forever()
    except RuntimeError as exc:
        logger.exception(exc)
        raise(exc)
    finally:
        loop.run_unitl_complete(main(loop=loop))
        loop.close()