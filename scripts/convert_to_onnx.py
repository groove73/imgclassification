import torch
from facenet_pytorch import InceptionResnetV1
import os

def convert():
    # 1. Initialize the model
    print("Loading FaceNet (InceptionResnetV1) model...")
    model = InceptionResnetV1(pretrained='vggface2').eval()

    # 2. Define dummy input
    dummy_input = torch.randn(1, 3, 160, 160)

    # 3. Define the path
    model_dir = os.path.join(os.getcwd(), "app", "models")
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    
    onnx_path = os.path.join(model_dir, "facenet.onnx")

    # 4. Export to ONNX
    print(f"Exporting to {onnx_path}...")
    torch.onnx.export(
        model,
        dummy_input,
        onnx_path,
        export_params=True,
        opset_version=11,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}}
    )
    print("Conversion complete!")

if __name__ == "__main__":
    convert()
