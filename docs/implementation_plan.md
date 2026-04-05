# Implementation Plan: Human Image Classifier

## 1. Project Background

This project aims to build a human image classifier using machine learning (CNN-based) and serve it as a recommendation service via FastAPI.

## 2. Technical Stack

- **ML**: Python, PyTorch (or FaceNet/InsightFace), OpenCV, NumPy, Scikit-learn
- **Frontend**: HTML5, Vanilla CSS, Vanilla JavaScript
- **Backend**: FastAPI, Pydantic, Pillow, Uvicorn
- **Architecture**: Clean Architecture (Controller, Service, Repository, Domain)

## 3. Detailed Steps

### Step 1: Project Skeleton

- `app/domain`: Logic and Entities (FaceEmbedding, Celebrity)
- `app/service`: Application Logic (FaceSearchService, RecommendationService)
- `app/repository`: Data Access Layer (EmbeddingStore)
- `app/controller`: API Routes (FastAPI endpoints)
- `app/main.py`: Application entry point
- `app/static`: Frontend files (HTML, CSS, JS)
- `docs/`: Documentation (Todo, Plan, Architecture, Walkthrough)

### Step 2: ML Model Selection & Training

- We will use **FaceNet** or **InsightFace** (pre-trained ResNet/CNN models) for extracting high-dimensional embeddings from human faces.
- **Reference Data**: Download/load PubFig celebrities (or a smaller pre-curated subset if PubFig is too large/unavailable) and generate their face embeddings.
- **Similarity**: Use Cosine Similarity or Euclidean distance to find the closest match to a newly uploaded image.

### Step 3: API Design

- `POST /upload`: Receiver image file/base64, process via ML, return recommendation.
- `GET /health`: Health check.
- `GET /`: Serve frontend page.

### Step 4: Frontend Development

- Responsive design for uploading images.
- Camera support via `MediaDevices.getUserMedia()`.
- Result display with similarity percentage and recommended name/image.

### Step 5: Integration & Verification

- Test image processing pipeline (Upload → Preprocess → Embedding → Search → Result).
- Performance optimization (caching embeddings).

## 4. Risks & Mitigations

- **Data Size**: Downloading all of PubFig might be time-consuming. We'll start with a small, high-quality subset.
- **Face Detection**: Handling non-human images or low-quality images. We'll add basic face detection checks before extraction.
- **Performance**: Generating embeddings on-the-fly for a large database. We'll precalculate and store the reference embeddings.
