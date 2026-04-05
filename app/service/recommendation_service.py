import onnxruntime as ort
import cv2
import numpy as np
from PIL import Image
import io
import os
from typing import List, Optional
from app.domain.models import CelebrityMatch
from app.repository.interface import IEmbeddingRepository

class RecommendationService:
    def __init__(self, repository: IEmbeddingRepository):
        self.repository = repository
        
        # Load ONNX model for embeddings (assume model is in app/models/facenet.onnx)
        # If model doesn't exist, will raise error or can be lazily loaded
        model_path = os.path.join(os.getcwd(), "app", "models", "facenet.onnx")
        if not os.path.exists(model_path):
            print(f"Warning: ONNX model not found at {model_path}. Please place facenet.onnx there.")
            self.session = None
        else:
            self.session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
        
        # OpenCV Face Detector (Lighter than MTCNN)
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        # Pre-load repository
        self.repository.load_embeddings()

    def find_similar_human(self, image_data: bytes) -> List[CelebrityMatch]:
        if self.session is None:
            print("ONNX session not initialized.")
            return []
            
        try:
            # Load image with OpenCV
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Detect face
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            if len(faces) == 0:
                return []
            
            # Pick the largest face
            (x, y, w, h) = sorted(faces, key=lambda f: f[2]*f[3], reverse=True)[0]
            face_img = img[y:y+h, x:x+w]
            
            # Preprocess for FaceNet (160x160, normalize)
            face_img = cv2.resize(face_img, (160, 160))
            face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
            face_img = (face_img.astype(np.float32) - 127.5) / 128.0
            face_img = np.transpose(face_img, (2, 0, 1)) # HWC to CHW
            face_img = np.expand_dims(face_img, axis=0) # Add batch dim
            
            # Extract embedding using ONNX
            inputs = {self.session.get_inputs()[0].name: face_img}
            embedding = self.session.run(None, inputs)[0][0]
            
            # Search nearest match in repository
            matches = self.repository.find_nearest_match(embedding, top_k=3)
            return matches
            
        except Exception as e:
            print(f"Error finding similar human (ONNX): {e}")
            return []
