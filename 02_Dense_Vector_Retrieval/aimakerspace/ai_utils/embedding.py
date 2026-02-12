from typing import List
import asyncio
from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    def __init__(self, embeddings_model_name: str = "all-MiniLM-L6-v2", batch_size: int = 1024):
        self.model = SentenceTransformer(embeddings_model_name)
        self.embeddings_model_name = embeddings_model_name
        self.batch_size = batch_size

    async def async_get_embeddings(self, list_of_text: List[str]) -> List[List[float]]:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.get_embeddings, list_of_text)

    async def async_get_embedding(self, text: str) -> List[float]:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.get_embedding, text)

    def get_embeddings(self, list_of_text: List[str]) -> List[List[float]]:
        embeddings = self.model.encode(list_of_text, batch_size=self.batch_size)
        return embeddings.tolist()

    def get_embedding(self, text: str) -> List[float]:
        embedding = self.model.encode(text)
        return embedding.tolist()


if __name__ == "__main__":
    embedding_model = EmbeddingModel()
    print(asyncio.run(embedding_model.async_get_embedding("Hello, world!")))
    print(
        asyncio.run(
            embedding_model.async_get_embeddings(["Hello, world!", "Goodbye, world!"])
        )
    )
