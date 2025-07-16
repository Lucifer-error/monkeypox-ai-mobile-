"""
Monkeypox Model Configuration
Contains model configuration, preprocessing, and loading utilities.
"""

import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import os

class MonkeypoxConfig:
    """Configuration class for Monkeypox model"""
    
    # Model parameters
    MODEL_NAME = "resnet18"
    NUM_CLASSES = 2
    CLASS_NAMES = ['Monkey Pox', 'Others']
    IMAGE_SIZE = (224, 224)
    
    # Model path
    MODEL_PATH = "best_model.pth"
    
    # Device configuration
    @staticmethod
    def get_device():
        """Get the best available device for model inference"""
        if torch.backends.mps.is_available():
            return torch.device("mps")
        elif torch.cuda.is_available():
            return torch.device("cuda")
        else:
            return torch.device("cpu")

class MonkeypoxModel:
    """Monkeypox classification model wrapper"""
    
    def __init__(self, model_path=None):
        self.config = MonkeypoxConfig()
        self.device = self.config.get_device()
        self.model = None
        self.transform = self._get_transform()
        
        if model_path:
            self.load_model(model_path)
    
    def _get_transform(self):
        """Get image preprocessing transform"""
        return transforms.Compose([
            transforms.Resize(self.config.IMAGE_SIZE),
            transforms.ToTensor(),
        ])
    
    def load_model(self, model_path):
        """Load the trained model"""
        try:
            # Initialize model architecture
            self.model = models.resnet18(pretrained=False)
            self.model.fc = nn.Linear(self.model.fc.in_features, self.config.NUM_CLASSES)
            
            # Load trained weights
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            self.model = self.model.to(self.device)
            self.model.eval()
            
            print(f"Model loaded successfully from {model_path}")
            return True
            
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def preprocess_image(self, image):
        """Preprocess image for model input"""
        if isinstance(image, str):
            # If image is a file path
            image = Image.open(image).convert("RGB")
        elif not isinstance(image, Image.Image):
            raise ValueError("Image must be PIL Image or file path")
        
        # Ensure image is in RGB format (handle WebP RGBA or other formats)
        if image.mode != 'RGB':
            if image.mode in ('RGBA', 'LA', 'P'):
                # Create white background for transparent images
                rgb_image = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                # Paste with alpha channel as mask if available
                rgb_image.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
                image = rgb_image
            else:
                image = image.convert('RGB')
        
        # Apply transforms and add batch dimension
        return self.transform(image).unsqueeze(0)
    
    def predict(self, image):
        """Make prediction on input image"""
        if self.model is None:
            raise ValueError("Model not loaded. Call load_model() first.")
        
        # Preprocess image
        input_tensor = self.preprocess_image(image).to(self.device)
        
        # Make prediction
        with torch.no_grad():
            outputs = self.model(input_tensor)
            probabilities = torch.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
            
            predicted_class = self.config.CLASS_NAMES[predicted.item()]
            confidence_score = confidence.item()
            
            return {
                'predicted_class': predicted_class,
                'confidence': confidence_score,
                'probabilities': {
                    class_name: prob.item() 
                    for class_name, prob in zip(self.config.CLASS_NAMES, probabilities[0])
                }
            }
