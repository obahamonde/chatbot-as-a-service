import asyncio

from aiofauna import AioFauna, Response

from .apis import *
from .models import *
from .tools import *

app = AioFauna()

@app.post("/api/chatbot")
async def main(request: OpenAIEmbeddingRequest):
    user_vector = (await openai.post_embeddings(request)).data[0].embedding
    meta = (await pinecone.query(
            PineconeVectorQuery(
                vector=user_vector,
                namespace=request.namespace,
            )
        )).matches[0].metadata
    app.logger.info(meta)
    if meta is None:
        meta = {
            "text": request.input,
        }
    req = OpenAIChatCompletionRequest(role="lead-generation-machine",
        prompt=request.input,
        namespace=request.namespace,
        context=meta,
    )
    content = req.chain()
    gpt_request = OpenAIChatGptRequest().chain(content, request.input)
    response = await openai.text_completion(gpt_request)
    text = response.choices[0].message.content
    ai_vector = (
        (
            await openai.post_embeddings(
                OpenAIEmbeddingRequest(input=text, namespace=request.namespace)
            )
        )
        .data[0]
        .embedding
    )
    await pinecone.upsert(
        request.namespace,
        PineconeVector(
            values=ai_vector,
            metadata={"text": text},
        ),
    )
    await pinecone.upsert(
        request.namespace,
        PineconeVector(
            values=user_vector,
            metadata={"text": request.input},
        ),
    )
    return text

async def get_embeddings(namespace: str, tool:SiteMapTool):
    pages = await tool.run(namespace)
    requests = [
        OpenAIEmbeddingRequest(input=page.content, namespace=namespace)
        for page in pages
    ]
    responses: List[OpenAIEmbeddingResponse] = await asyncio.gather(
        *[openai.post_embeddings(request) for request in requests]
    )
    embeddings = [response.data[0].embedding for response in responses]
    vectors = [
        PineconeVector(values=vector, metadata={"text": page.content})
        for vector, page in zip(embeddings, pages)
    ]
    return vectors

@app.websocket("/api/chatbot/ingest")
async def ingest_organization_website(namespace: str, ref:str, websocket: WebSocketResponse):
    """
    Ingests a website and creates a new organization.
    """
    user = await User.get(ref)
    assert isinstance(user, User)        
    app.logger.info(user.json())
    tool = SiteMapTool(websocket)
    await tool.run(namespace)
    vectors = await get_embeddings(namespace, tool)
    await asyncio.gather(*[pinecone.upsert(namespace, vector) for vector in vectors])
    await websocket.close()
@app.post("/api/audio")
async def audio(text:str):
    polly = Polly.from_text(text)
    return Response(body=polly.get_audio(), content_type="application/octet-stream")

URL = "https://www.ransa.biz"