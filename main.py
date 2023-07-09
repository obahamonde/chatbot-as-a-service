from aiofauna import *
from aiohttp import web
from aiohttp.worker import GunicornWebWorker
from dotenv import load_dotenv

load_dotenv()
from src import app
from src.apis import *
from src.models import *
from src.tools import *

"""
class GunicornAiohttpWorker(GunicornWebWorker):
    def make_handler(self:Type, app:web.Application=app, *args, **kwargs):
        return app.make_handler(*args, **kwargs)

    async def close(self):
        if self.servers is not None:
            servers = self.servers
            self.servers = None
            for server in servers: # type: ignore
                server.close()
            for server in servers: # type: ignore
                await server.wait_closed()
        await super().close() # type: ignore
"""
        
from aiohttp import web

web.run_app(app, port=8080, host="0.0.0.0")
