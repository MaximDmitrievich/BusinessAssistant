from os import environ
from aiohttp import ClientSession
from aiohttp.web import Application, AppRunner, TCPSite
from asyncio import get_event_loop, ensure_future
from logging import INFO, getLogger
from simpletransformers.ner import NERModel

from controllers.ner_controller import NERController
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
    labels=[
        'B-ORGANIZATION', 
        'I-ORGANIZATION', 
        'B-SUBJECT',
        'I-SUBJECT',
        'B-OBJECT',
        'I-OBJECT',
        'B-CODEX',
        'I-CODEX',
        'B-NUMBER',
        'I-NUMBER',
        'B-LAWFACE',
        'I-LAWFACE',
        'B-PHYSFACE',
        'I-PHYSFACE',
        'B-REGISTRY',
        'I-REGISTRY',
        'B-SIZES',
        'I-SIZES',
        'B-DATE',
        'I-DATE',
        'B-SPARESUBJECT',
        'I-SPARESUBJECT',
        'B-CADASTRE',
        'I-CADASTRE',
        'B-ADDRESS',
        'I-ADDRESS',
        'O'
    ]

    model = NERModel(model_type='distilbert', model_name='outputs/', args=args, use_cuda=False, labels=labels)

    async def main(loop=None):
        ner_controller = NERController(model)
        
        application = Application(middlewares=[middleware.logging], logger=logger)
        application.router.add_post('/api/ner', ner_controller.post)

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