import os
import requests
import numpy as np
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
import io

# Setup models
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

mtcnn = MTCNN(image_size=160, margin=0, device=device)
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)

def get_embedding(img_bytes):
    try:
        img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
        # Detect and crop face
        face = mtcnn(img)
        if face is not None:
            # Generate embedding
            face = face.unsqueeze(0).to(device)
            embedding = resnet(face).detach().cpu().numpy()
            return embedding[0]
    except Exception as e:
        print(f"Error processing image: {e}")
    return None

def setup_data():
    source_url = "http://www.cs.columbia.edu/CAVE/databases/pubfig/download/dev_urls.txt"
    response = requests.get(source_url)
    lines = response.text.split('\n')
    
    celebrities = {}
    # Skip comments
    data_lines = [l for l in lines if l and not l.startswith('#')]
    
    # Let's pick a few distinct names
    all_embeddings = []
    all_names = []
    
    processed_names = set()
    needed_celebs = 10
    
    for line in data_lines:
        if len(processed_names) >= needed_celebs:
            break
            
        parts = line.split('\t')
        if len(parts) < 3:
            continue
            
        name = parts[0]
        img_url = parts[2]
        
        if name in processed_names:
            continue
            
        print(f"Trying to download {name} from {img_url}...")
        try:
            img_res = requests.get(img_url, timeout=5)
            if img_res.status_code == 200:
                emb = get_embedding(img_res.content)
                if emb is not None:
                    all_embeddings.append(emb)
                    all_names.append(name)
                    processed_names.add(name)
                    print(f"Successfully processed {name}")
                else:
                    print(f"No face found in {name} image")
            else:
                print(f"Failed to download {name} image, status: {img_res.status_code}")
        except Exception as e:
            print(f"Error downloading {name}: {e}")

    if all_embeddings:
        # Save embeddings and names
        np.savez('app/repository/celebrities.npz', 
                embeddings=np.array(all_embeddings), 
                names=np.array(all_names))
        print(f"Saved {len(all_names)} celebrity embeddings.")
    else:
        print("No embeddings were generated.")

if __name__ == "__main__":
    setup_data()
