from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
from app.domain.models import CelebrityMatch
from app.service.recommendation_service import RecommendationService
from app.repository.numpy_repository import NumpyEmbeddingRepository

router = APIRouter()

# Dependency injection for RecommendationService
# A simple singleton pattern or dependency manager.
# For simplicity, we can initialize it once.
_repo = NumpyEmbeddingRepository()
_service = RecommendationService(_repo)

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.post("/upload", response_model=List[CelebrityMatch])
async def upload_image(file: UploadFile = File(...)):
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    # Process purely in memory - no storage to disk
    content = await file.read()
    results = _service.find_similar_human(content)
    
    if not results:
        raise HTTPException(status_code=404, detail="No face detected or no matches found.")
    
    return results
