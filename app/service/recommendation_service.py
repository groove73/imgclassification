import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
import io
import numpy as np
from typing import List, Optional
from app.domain.models import CelebrityMatch
from app.repository.interface import IEmbeddingRepository

class RecommendationService:
    def __init__(self, repository: IEmbeddingRepository):
        self.repository = repository
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        
        # Initialize models (using lazy loading or caching)
        self.mtcnn = MTCNN(image_size=160, margin=0, device=self.device)
        self.resnet = InceptionResnetV1(pretrained='vggface2').eval().to(self.device)
        
        # Pre-load repository
        self.repository.load_embeddings()

    def find_similar_human(self, image_data: bytes) -> List[CelebrityMatch]:
        try:
            # Load and convert image
            img = Image.open(io.BytesIO(image_data)).convert('RGB')
            
            # Detect face
            face = self.mtcnn(img)
            if face is None:
                return []
            
            # Extract embedding
            face = face.unsqueeze(0).to(self.device)
            embedding = self.resnet(face).detach().cpu().numpy()[0]
            
            # Search nearest match in repository
            matches = self.repository.find_nearest_match(embedding, top_k=3)
            return matches
            
        except Exception as e:
            print(f"Error finding similar human: {e}")
            return []
