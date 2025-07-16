import streamlit as st
from PIL import Image
import torch
import torch.nn as nn
from torchvision import models, transforms
import os
from datetime import datetime

# 🛠️ Set Streamlit page config
st.set_page_config(page_title="Monkeypox Classifier", layout="centered")

# ✅ Class names
class_names = ['Monkey Pox', 'Others']

# 🔁 Preprocessing function
def preprocess_image(image):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])
    return transform(image).unsqueeze(0)

# 🎯 Load the model
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
model = models.resnet18(pretrained=False)
model.fc = nn.Linear(model.fc.in_features, 2)
model.load_state_dict(torch.load("best_model.pth", map_location=device))
model = model.to(device)
model.eval()

# 🚀 Streamlit UI
st.title("🧠 Monkeypox Skin Lesion Classifier")

uploaded_file = st.file_uploader("Upload a skin lesion image", type=["jpg", "jpeg", "png", "webp"])
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Prediction
    input_tensor = preprocess_image(image).to(device)
    with torch.no_grad():
        outputs = model(input_tensor)
        _, predicted = torch.max(outputs, 1)
        predicted_class = class_names[predicted.item()]

    st.markdown(f"### 🔍 Predicted: `{predicted_class}`")

    # User Confirmation
    confirm = st.radio("Is the prediction correct?", ("Yes", "No"))

    if confirm == "Yes":
        now = datetime.now().strftime("%Y%m%d_%H%M%S")

        # If prediction was Monkey Pox, ask for subclass
        if predicted_class == "Monkey Pox":
            subclass = st.selectbox("Please confirm the actual class:", ("Monkey Pox", "Others"))
            save_class = subclass
        else:
            save_class = predicted_class

        # Save image to collections folder
        if st.button("📁 Save Image"):
            save_dir = os.path.join("faceemotion", "app", "collections", save_class)
            os.makedirs(save_dir, exist_ok=True)
            filename = f"{save_class.replace(' ', '_')}_{now}.jpg"
            save_path = os.path.join(save_dir, filename)
            image.save(save_path)
            st.success(f"✅ Image saved to `{save_path}`")