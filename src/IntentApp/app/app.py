from os import environ
from aiohttp import ClientSession
from aiohttp.web import Application, AppRunner, TCPSite
from asyncio import get_event_loop, ensure_future
from logging import INFO, getLogger
from simpletransformers.classification import ClassificationModel

from controllers.intent_controller import IntentController
from middlewares.exception_handler_middleware import ExceptionHandlerMiddleware

if __name__ == "__main__":
    logger = getLogger(environ['APP_NAME'])
    logger.setLevel(INFO)

    middleware = ExceptionHandlerMiddleware(logger)
    args = {
        "do_lower_case": True,
        "silent": True,
        "reprocess_input_data": True
        }
    
    model = ClassificationModel(model_type='bert', model_name='./outputs', args=args, use_cuda=False, num_labels=24)

    async def main(loop=None):
        intent_controller = IntentController(model)
        
        application = Application(middlewares=[middleware.logging], logger=logger)
        application.router.add_post('/api/intent', intent_controller.post)

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