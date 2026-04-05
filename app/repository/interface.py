from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models import FaceEmbedding, CelebrityMatch

class IEmbeddingRepository(ABC):
    @abstractmethod
    def load_embeddings(self) -> None:
        """Load all embeddings into memory or from a database."""
        pass

    @abstractmethod
    def get_all_embeddings(self) -> List[FaceEmbedding]:
        """Return all stored embeddings."""
        pass

    @abstractmethod
    def save_embedding(self, embedding: FaceEmbedding) -> None:
        """Save a single embedding."""
        pass

    @abstractmethod
    def find_nearest_match(self, query_embedding: List[float], top_k: int = 1) -> List[CelebrityMatch]:
        """Find the most similar matches based on cosine similarity."""
        pass
