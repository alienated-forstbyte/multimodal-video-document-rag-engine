from fastembed import TextEmbedding
from qdrant_client import QdrantClient

COLLECTION_NAME = "multimodel-video-rag"

client = QdrantClient(path="./qdrant_db")

# 2. Load the same embedding model
model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")

def search_video(query_text: str, top_k: int = 3):
    # Convert query into a vector
    query_vector = list(model.embed([query_text]))[0].tolist()

    # Search Qdrant
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k
    )

    # Collect matched chunks
    matched_chunks = []
    for point in results.points:
        matched_chunks.append({
            "score": point.score,
            "text": point.payload["text"],
            "frame_path": point.payload["frame_path"],
            "formatted_time": point.payload["formatted_time"],
            "start_time": point.payload["start_time"],
        })
    
    return matched_chunks


if __name__ == "__main__":
    query = "music video"
    results = search_video(query, top_k=3)

    print(f"\n--- Search results for '{query}' ---")
    for r in results:
        print(f"[{r['formatted_time']}] (Score: {r['score']:.3f})")
        print(f"  Frame: {r['frame_path']}")
        print(f"  Text:  {r['text']}\n")
    client.close()