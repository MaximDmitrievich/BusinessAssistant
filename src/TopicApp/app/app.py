from os import environ
from aiohttp import ClientSession
from aiohttp.web import Application, AppRunner, TCPSite
from asyncio import get_event_loop, ensure_future
from logging import INFO, getLogger
from bertopic import BERTopic

from controllers.topic_controller import TopicController
from middlewares.exception_handler_middleware import ExceptionHandlerMiddleware

if __name__ == "__main__":
    logger = getLogger(environ['APP_NAME'])
    logger.setLevel(INFO)

    middleware = ExceptionHandlerMiddleware(logger)
    model = BERTopic.load("models")
    

    async def main(loop=None):
        ner_controller = TopicController(model)
        
        application = Application(middlewares=[middleware.logging], logger=logger)
        application.router.add_post('/api/topic', ner_controller.post)

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