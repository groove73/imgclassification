import numpy as np
import os
from typing import List
from app.repository.interface import IEmbeddingRepository
from app.domain.models import FaceEmbedding, CelebrityMatch

class NumpyEmbeddingRepository(IEmbeddingRepository):
    def __init__(self, file_path: str = 'app/repository/celebrities.npz'):
        self.file_path = file_path
        self.embeddings: List[FaceEmbedding] = []
        self._raw_embeddings: np.ndarray = None
        self._names: np.ndarray = None

    def load_embeddings(self) -> None:
        if os.path.exists(self.file_path):
            data = np.load(self.file_path)
            self._raw_embeddings = data['embeddings']
            self._names = data['names']
            print(f"Loaded {len(self._names)} embeddings from {self.file_path}")
        else:
            print(f"Warning: {self.file_path} not found.")

    def get_all_embeddings(self) -> List[FaceEmbedding]:
        if self._raw_embeddings is None:
            return []
        
        return [
            FaceEmbedding(name=name, embedding=emb.tolist())
            for name, emb in zip(self._names, self._raw_embeddings)
        ]

    def save_embedding(self, embedding: FaceEmbedding) -> None:
        # In a real repository, this would save to a DB or append to file
        pass

    def find_nearest_match(self, query_embedding: np.ndarray, top_k: int = 1) -> List[CelebrityMatch]:
        if self._raw_embeddings is None or len(self._raw_embeddings) == 0:
            return []

        # Cosine Similarity: dot(a, b) / (norm(a) * norm(b))
        # Since Facenet embeddings are normalized, we can just use dot product (or use scikit-learn)
        # Assuming embeddings from FaceNet-Pytorch are already normalized or close to it.
        # Let's use robust cosine similarity
        similarities = []
        for i, ref_emb in enumerate(self._raw_embeddings):
            dot = np.dot(query_embedding, ref_emb)
            norm_q = np.linalg.norm(query_embedding)
            norm_r = np.linalg.norm(ref_emb)
            similarity = dot / (norm_q * norm_r)
            similarities.append(similarity)

        # Get top K indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        matches = [
            CelebrityMatch(
                name=self._names[idx],
                similarity=float(similarities[idx]),
                image_url=None # We don't store URLs yet
            )
            for idx in top_indices
        ]
        return matches
