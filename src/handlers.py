import asyncio

from aiofauna import AioFauna, Response

from .apis import *
from .tools import *

app = AioFauna()

@app.post("/chatbot")
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

async def get_embeddings(namespace: str):
    pages = await sitemap_tool.run(namespace)
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

async def ingest_data(namespace: str):
    vectors = await get_embeddings(namespace)
    data = await asyncio.gather(
        *[pinecone.upsert(namespace, vector) for vector in vectors]
    )
    return data

@app.get("/chatbot/ingest")
async def ingest(namespace: str):
    return await ingest_data(namespace)

@app.post("/audio")
async def audio(text:str):
    polly = Polly.from_text(text)
    return Response(body=polly.get_audio(), content_type="application/octet-stream")

