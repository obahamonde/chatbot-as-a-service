import aiohttp.web
from aiofauna import *
from aiohttp.worker import GunicornWebWorker
from dotenv import load_dotenv

load_dotenv()
from src import app
from src.apis import *
from src.models import *
from src.tools import *


class GunicornAiohttpWorker(GunicornWebWorker):
    def make_handler(self, app, *args, **kwargs):
        return app.make_handler(*args, **kwargs)

    async def close(self):
        if self.servers is not None:
            servers = self.servers
            self.servers = None
            for server in servers:
                server.close()
            for server in servers:
                await server.wait_closed()
        await super().close()

   
   