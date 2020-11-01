from os import environ
from aiohttp import ClientSession
from aiohttp.web import Application, AppRunner, TCPSite
from asyncio import get_event_loop, ensure_future
from logging import INFO, getLogger

from services.intent_service import IntentService
from services.ner_service import NERService
from services.topic_service import TopicService
from controllers.recognize_controller import ResolverController
from middlewares.exception_handler_middleware import ExceptionHandlerMiddleware

if __name__ == "__main__":
    logger = getLogger(environ['APP_NAME'])
    logger.setLevel(INFO)

    middleware = ExceptionHandlerMiddleware(logger)
    intents = IntentService(None, "http://{}:{}/api/intent".format(environ["INTENT_HOST"], environ["INTENT_PORT"]))
    ner = NERService(None, "http://{}:{}/api/ner".format(environ["NER_HOST"], environ["NER_PORT"]))
    topic = TopicService(None, "http://{}:{}/api/topic".format(environ["TOPIC_HOST"], environ["TOPIC_PORT"]))
    
    async def main(loop=None):
        recognize_controller = ResolverController(intents, ner, topic)
        
        application = Application(middlewares=[middleware.logging], logger=logger)
        application.router.add_post('/api/recognize', recognize_controller.post)

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