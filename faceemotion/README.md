# Monkeypox Skin Lesion Classifier

A deep learning application for classifying skin lesions as Monkeypox or other conditions using ResNet18 architecture.

## 🏗️ Project Structure

```
faceemotion/
├── monkeypox_model/          # Model configuration and utilities
│   ├── __init__.py
│   ├── best_model.pth        # Trained model weights
│   └── monkeypox_configuration.py  # Model class and configuration
├── app/                      # Main application
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── screens/             # UI screens
│   │   ├── __init__.py
│   │   ├── main_menu.py     # Landing page and navigation
│   │   └── analyze_screen.py # Image analysis interface
│   └── collections/         # Saved classified images
│       ├── Monkey Pox/      # Monkeypox classified images
│       └── Others/          # Other conditions classified images
├── assets/                  # Static assets (icons, fonts, etc.)
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project**
   ```bash
   cd faceemotion
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the Streamlit application**
   ```bash
   cd app
   streamlit run main.py
   ```

2. **Open your browser** to the URL shown in the terminal (usually `http://localhost:8501`)

## 📱 Features

### 🔬 Image Analysis
- Upload skin lesion images (JPG, JPEG, PNG, WebP)
- Real-time AI classification using ResNet18
- Confidence scores and probability breakdown
- User feedback collection

### 💾 Data Collection
- Save classified images to organized folders
- Build training datasets for model improvement
- Track collection statistics

### 🎯 Model Information
- **Architecture**: ResNet18 Convolutional Neural Network
- **Classes**: Monkeypox, Others
- **Input Size**: 224×224 pixels
- **Performance**: Optimized for medical image classification

## 🛠️ Technical Details

### Model Configuration
The `MonkeypoxModel` class in `monkeypox_model/monkeypox_configuration.py` handles:
- Model loading and initialization
- Image preprocessing
- Prediction with confidence scores
- Device management (CPU/CUDA/MPS)

### Application Structure
- **main.py**: Entry point with page routing and styling
- **main_menu.py**: Landing page with navigation and information
- **analyze_screen.py**: Image upload and classification interface

## ⚠️ Important Disclaimer

**This tool is for educational and research purposes only.** It should not be used as a substitute for professional medical diagnosis. Always consult with qualified healthcare professionals for medical advice.

## 🔧 Development

### Adding New Features
1. Create new screen modules in `app/screens/`
2. Add routing logic in `app/main.py`
3. Update navigation in `main_menu.py`

### Model Updates
1. Replace `best_model.pth` with new trained weights
2. Update configuration in `monkeypox_configuration.py` if needed
3. Test with sample images

## 📊 Usage Analytics

The application tracks:
- Classification accuracy feedback
- Image collection growth
- User interaction patterns

## 🤝 Contributing

1. Follow the existing code structure
2. Add comprehensive docstrings
3. Test new features thoroughly
4. Update documentation as needed

## 📄 License

This project is for educational and research purposes. Please ensure compliance with relevant medical AI regulations in your jurisdiction.
