import asyncio

from aiofauna import AioFauna, Response

from .apis import *
from .models import *
from .tools import *

app = AioFauna()

@app.post("/api/chatbot")
async def main(text:str,namespace:str="default"):
    gpt = ChatGPT(namespace=namespace)
    return await gpt.question(text)
    

async def get_embeddings(namespace: str, tool:SiteMapTool):
    pages = await tool.run(namespace)
    gpt = ChatGPT(namespace=namespace)
    await asyncio.gather(*[gpt.insert(["\n".join([page.title,page.url,page.content])]) for page in pages])

@app.websocket("/api/chatbot/ingest")
async def ingest_organization_website(namespace: str, ref:str, websocket: WebSocketResponse):
    """
    Ingests a website and creates a new organization.
    """
    user = await User.get(ref)
    assert isinstance(user, User)        
    app.logger.info(user.json())
    tool = SiteMapTool(websocket)
    await get_embeddings(namespace, tool)    

@app.post("/api/audio")
async def audio(text:str):
    polly = Polly.from_text(text)
    return Response(body=polly.get_audio(), content_type="application/octet-stream")

