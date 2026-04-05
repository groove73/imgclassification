# Walkthrough: Human Image Classifier

## Introduction

The Human Image Classifier is a machine learning-based recommendation system that finds the most similar celebrity to a user-provided image. It uses a state-of-the-art CNN model (FaceNet) for facial embedding extraction and cosine similarity for matching, served through a FastAPI backend with a minimalist and premium glassmorphism frontend.

## Key Features

- **Face Recognition**: Uses FaceNet (InceptionResnetV1) pre-trained on VGGFace2 for high-quality facial feature extraction.
- **Real-time Camera**: Support for capturing images directly from the browser's camera.
- **Drag & Drop**: Seamless image uploading experience.
- **Similarity Search**: Calculates cosine similarity against a database of 10+ celebrities (Audrey Tautou, Barack Obama, etc.).
- **Clean Architecture**: Decoupled domain, service, and repository layers for better maintainability.

## How to Run

1. **Virtual Environment & Dependencies**:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install fastapi uvicorn python-multipart numpy opencv-python-headless pillow pydantic facenet-pytorch torch torchvision
   ```

2. **Generate Database**:

   Run the `setup_dataset.py` script to download a small celebrity dataset and generate embeddings.

   ```bash
   python3 setup_dataset.py
   ```

3. **Start Application**:

   Run the following command from the root directory of the project:

   ```bash
   source .venv/bin/activate
   python3 -m app.main
   ```

   > [!TIP]
   > If you encounter `ModuleNotFoundError: No module named 'app'`, ensure you are in the project root directory and the `python3 -m` flag is used. This allows Python to correctly resolve the `app` package.

   Access the web interface at `http://localhost:8000`.

## Technical Implementation Details

### Model Pipeline

1. **MTCNN**: Detects and crops the face from the provided image, resizing it to 160x160.
2. **InceptionResnetV1 (FaceNet)**: Converts the face image into a 512-dimension embedding vector.
3. **Cosine Similarity**: Comparing the 512D query vector with the pre-calculated database vectors:
   $\text{sim} = \frac{A \cdot B}{\|A\|\|B\|}$

### Project Structure (Clean Architecture)

- **Domain**: Pure data models (`app/domain/models.py`).
- **Service**: Business logic (`app/service/recommendation_service.py`).
- **Repository**: Data access/storage (`app/repository/numpy_repository.py`).
- **Controller**: Web API routes (`app/controller/routes.py`).

## Future Enhancements

- Support for larger datasets using FAISS (Facebook AI Similarity Search) for faster vector indexing.
- Enhanced facial attribute analysis (age, gender estimation).
- Multi-face detection and recommendation.
