import numpy as np
from collections import defaultdict
from typing import List, Tuple, Callable
from aimakerspace.ai_utils.embedding import EmbeddingModel
import asyncio


def cosine_similarity(vector_a: np.array, vector_b: np.array) -> float:
    """Computes the cosine similarity between two vectors."""
    dot_product = np.dot(vector_a, vector_b)
    norm_a = np.linalg.norm(vector_a)
    norm_b = np.linalg.norm(vector_b)
    return dot_product / (norm_a * norm_b)


def pearson_correlation(vector_a: np.array, vector_b: np.array) -> float:
    """Computes the Pearson correlation between two vectors."""
    return np.corrcoef(vector_a, vector_b)[0, 1]


class VectorDatabase:
    def __init__(self, embedding_model: EmbeddingModel = None):
        self.vectors = defaultdict(tuple)  # key: text -> value: (vector, metadata)
        self.embedding_model = embedding_model or EmbeddingModel()

    def insert(self, key: str, vector: np.array, metadata: dict = None) -> None:
        self.vectors[key] = (vector, metadata or {})

    def search(
        self,
        query_vector: np.array,
        k: int,
        distance_metric: Callable = pearson_correlation,
        metadata_filter: dict = None,
    ) -> List[Tuple[str, float, dict]]:
        scores = []
        for key, (vector, metadata) in self.vectors.items():
            # Skip if doesn't match filter
            if metadata_filter:
                if not all(metadata.get(fk) == fv for fk, fv in metadata_filter.items()):
                    continue
            scores.append((key, distance_metric(query_vector, vector), metadata))
        return sorted(scores, key=lambda x: x[1], reverse=True)[:k]

    def search_by_text(
        self,
        query_text: str,
        k: int,
        distance_metric: Callable = pearson_correlation,
        return_as_text: bool = False,
        metadata_filter: dict = None,
    ) -> List[Tuple[str, float, dict]]:
        query_vector = self.embedding_model.get_embedding(query_text)
        results = self.search(query_vector, k, distance_metric, metadata_filter)
        return [result[0] for result in results] if return_as_text else results

    def get_unique_metadata_values(self, key: str) -> List[str]:
        """Get all unique values for a metadata key across all vectors."""
        values = set()
        for _, (_, metadata) in self.vectors.items():
            if key in metadata:
                values.add(metadata[key])
        return list(values)

    def retrieve_from_key(self, key: str) -> Tuple[np.array, dict]:
        return self.vectors.get(key, None)

    async def abuild_from_list(self, list_of_text: List[str], metadata_list: List[dict] = None) -> "VectorDatabase":
        if metadata_list is None:
            metadata_list = [{} for _ in list_of_text]
        embeddings = await self.embedding_model.async_get_embeddings(list_of_text)
        for text, embedding, metadata in zip(list_of_text, embeddings, metadata_list):
            self.insert(text, np.array(embedding), metadata)
        return self


if __name__ == "__main__":
    list_of_text = [
        "I like to eat broccoli and bananas.",
        "I ate a banana and spinach smoothie for breakfast.",
        "Chinchillas and kittens are cute.",
        "My sister adopted a kitten yesterday.",
        "Look at this cute hamster munching on a piece of broccoli.",
    ]

    vector_db = VectorDatabase()
    vector_db = asyncio.run(vector_db.abuild_from_list(list_of_text))
    k = 2

    searched_vector = vector_db.search_by_text("I think fruit is awesome!", k=k)
    print(f"Closest {k} vector(s):", searched_vector)

    retrieved_vector = vector_db.retrieve_from_key(
        "I like to eat broccoli and bananas."
    )
    print("Retrieved vector:", retrieved_vector)

    relevant_texts = vector_db.search_by_text(
        "I think fruit is awesome!", k=k, return_as_text=True
    )
    print(f"Closest {k} text(s):", relevant_texts)
