# backend\math_agent\llm\kb_loader.py
from core.config import settings
from qdrant_client import QdrantClient , AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams
from google import genai
from google.genai import types
from typing import List
import numpy as np
import asyncio
import uuid 
from qdrant_client.models import PointStruct

# sync qdrant client for initialization check
sync_qdrant_client = QdrantClient(url=settings.QDRANT_URL)

# Async qdrant client

gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)

# Check if collection exists (sync check)
collection_exists = sync_qdrant_client.collection_exists(settings.QDRANT_COLLECTION_NAME)

if collection_exists:
    print(f"Collection '{settings.QDRANT_COLLECTION_NAME}' exists.")
else:
    print(f"Collection '{settings.QDRANT_COLLECTION_NAME}' does not exist.")
    sync_qdrant_client.create_collection(
        collection_name=settings.QDRANT_COLLECTION_NAME,  # Use settings instead of hardcoded name
        vectors_config=VectorParams(
            size=settings.VECTOR_DIMENSIONS, 
            distance=Distance.COSINE
        )
    )


async def normalize_embedding(embedding_values):
    """Normalize embedding values to unit length."""
    embedding_array = np.array(embedding_values)
    norm = np.linalg.norm(embedding_array)
    if norm == 0:
        return embedding_array
    return (embedding_array / norm).tolist()

async def get_embedding(question):
    
    result = await gemini_client.aio.models.embed_content(
        model="gemini-embedding-001",
        contents=question,
        config=types.EmbedContentConfig(
            output_dimensionality=settings.VECTOR_DIMENSIONS,
            task_type="RETRIEVAL_DOCUMENT"
                                        )
    )
    # Normalize for 768 dimensions
    embedding_values = result.embeddings[0].values

    return await normalize_embedding(embedding_values)

async def upload_to_qdrant(questions: List[dict]):
    
    qdrant_client = AsyncQdrantClient(url=settings.QDRANT_URL)
    try:
        vectors = []
        for idx, item in enumerate(questions):
            embedding = await get_embedding(item['question'])
            vector = {
                "id": idx,
                "vector": embedding,
                "payload": {
                    "question": item['question'],
                    "answer": item['answer']
                }
            }
            vectors.append(vector)
        
        print(f"Uploading {len(vectors)} vectors to Qdrant...")

        await qdrant_client.upsert(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            wait=True,
            points=vectors
        )
        print(f"Uploaded {len(vectors)} vectors to Qdrant collection '{settings.QDRANT_COLLECTION_NAME}'.")
    finally:
        # Always close the client asynchronously
        await qdrant_client.close()

async def add_to_knowledge_base(question: str, answer: str):
    """
    Adds a single, human-approved question and answer pair to Qdrant.
    This is the core of the "self-learning" feedback loop.
    """
    qdrant_client = AsyncQdrantClient(url=settings.QDRANT_URL)
    try:
        # 1. Get the embedding for the question
        embedding = await get_embedding(question)
        
        # 2. Create a unique ID for this new entry
        point_id = str(uuid.uuid4().hex)
        
        # 3. Create the point structure
        point = PointStruct(
            id=point_id,
            vector=embedding,
            payload={
                "question": question,
                "answer": answer
            }
        )
        
        # 4. Upsert the new point into the collection
        await qdrant_client.upsert(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            wait=True,
            points=[point]  # Upsert expects a list of points
        )
        
        print(f"[Self-Learning] Added new QA to Knowledge Base. ID: {point_id}")

    except Exception as e:
        print(f"[Self-Learning] Error adding to KB: {e}")
    finally:
        # Always close the client
        await qdrant_client.close()

async def search_knowledge_base(query: str, top_k: int = 5):
 
   
    qdrant_client = AsyncQdrantClient(url=settings.QDRANT_URL)
    try:
        query_embedding = await get_embedding(query)
        
        search_result = await qdrant_client.query_points(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            query=query_embedding,
            limit=top_k,
            with_payload=True,
            score_threshold=0.8
        )
        
        results = []
        for point in search_result.points:
            results.append({
                "question": point.payload['question'],
                "answer": point.payload['answer'],
                "score": point.score
            })
        
        return results
    finally:
        # Always close the client asynchronously
        await qdrant_client.close()

if __name__ == '__main__':
    sample_questions = [
    {
        "question": "Alexis is applying for a new job and bought a new set of business clothes to wear to the interview. She went to a department store with a budget of $200 and spent $30 on a button-up shirt, $46 on suit pants, $38 on a suit coat, $11 on socks, and $18 on a belt. She also purchased a pair of shoes, but lost the receipt for them. She has $16 left from her budget. How much did Alexis pay for the shoes?",
        "answer": "Let S be the amount Alexis paid for the shoes.\nShe spent S + 30 + 46 + 38 + 11 + 18 = S + <<+30+46+38+11+18=143>>143.\nShe used all but $16 of her budget, so S + 143 = 200 - 16 = 184.\nThus, Alexis paid S = 184 - 143 = $<<184-143=41>>41 for the shoes.\n#### 41"
    },{
        "question": "Tina makes $18.00 an hour.  If she works more than 8 hours per shift, she is eligible for overtime, which is paid by your hourly wage + 1/2 your hourly wage.  If she works 10 hours every day for 5 days, how much money does she make?",
        "answer": "She works 8 hours a day for $18 per hour so she makes 8*18 = $<<8*18=144.00>>144.00 per 8-hour shift\nShe works 10 hours a day and anything over 8 hours is eligible for overtime, so she gets 10-8 = <<10-8=2>>2 hours of overtime\nOvertime is calculated as time and a half so and she makes $18/hour so her overtime pay is 18*.5 = $<<18*.5=9.00>>9.00\nHer overtime pay is 18+9 = $<<18+9=27.00>>27.00\nHer base pay is $144.00 per 8-hour shift and she works 5 days and makes 5 * $144 = $<<144*5=720.00>>720.00\nHer overtime pay is $27.00 per hour and she works 2 hours of overtime per day and makes 27*2 = $<<27*2=54.00>>54.00 in overtime pay\n2 hours of overtime pay for 5 days means she makes 54*5 = $270.00\nIn 5 days her base pay is $720.00 and she makes $270.00 in overtime pay so she makes $720 + $270 = $<<720+270=990.00>>990.00\n#### 990"
    },{
        "question": "A deep-sea monster rises from the waters once every hundred years to feast on a ship and sate its hunger. Over three hundred years, it has consumed 847 people. Ships have been built larger over time, so each new ship has twice as many people as the last ship. How many people were on the ship the monster ate in the first hundred years?",
        "answer": "Let S be the number of people on the first hundred years\u2019 ship.\nThe second hundred years\u2019 ship had twice as many as the first, so it had 2S people.\nThe third hundred years\u2019 ship had twice as many as the second, so it had 2 * 2S = <<2*2=4>>4S people.\nAll the ships had S + 2S + 4S = 7S = 847 people.\nThus, the ship that the monster ate in the first hundred years had S = 847 / 7 = <<847/7=121>>121 people on it.\n#### 121"
    }
    ]
    import asyncio
    asyncio.run(upload_to_qdrant(sample_questions))
    # results = asyncio.run(search_knowledge_base("How much does Tina make if she works 12 hours a day for 4 days?", top_k=3))
    # for res in results:
    #     print(f"Question: {res['question']}\nAnswer: {res['answer']}\nScore: {res['score']}\n")