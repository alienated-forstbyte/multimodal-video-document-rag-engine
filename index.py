from fastembed import TextEmbedding
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import json

COLLECTION_NAME = "multimodel-video-rag"

model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
client = QdrantClient(path="./qdrant_db")

with open("metadata.json","r",encoding="utf-8") as f:
    chunks = json.load(f)

texts = [chunk['text'] for chunk in chunks]

embeddings = list(model.embed(texts))

vector_size = len(embeddings[0])

if client.collection_exists(COLLECTION_NAME):
    client.delete_collection(COLLECTION_NAME)
client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
)

points = []

for chunk, embedding in zip(chunks,embeddings):
    chunk['embedding'] = embedding.tolist()
    payload ={
        "chunk_id": chunk["chunk_id"],
        "start_time": chunk["start_time"],
        "end_time": chunk["end_time"],
        "formatted_time": chunk["formatted_time"],
        "text": chunk["text"],
        "frame_path": chunk["frame_path"]
    }

    points.append(
        PointStruct(id=chunk["chunk_id"],vector=embedding.tolist(),payload=payload)
    )

client.upsert(COLLECTION_NAME,points=points)
client.close()