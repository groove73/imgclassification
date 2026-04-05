import sys
import os

# Add project root to sys.path for direct script execution
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.controller.routes import router
import os

app = FastAPI(title="Human Image Classifier", version="1.0.0")

# Mount static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include API routes
app.include_router(router, prefix="/api")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Serve index.html from static
    path = os.path.join("app", "static", "index.html")
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return "<h1>Project Root</h1><p>Static files not found.</p>"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
