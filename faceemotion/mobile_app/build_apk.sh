#!/bin/bash
# APK Build Script for Monkeypox AI Classifier
# This script builds an Android APK using Buildozer

echo "🚀 Building Monkeypox AI Classifier APK..."
echo "============================================"

# Check if buildozer is installed
if ! command -v buildozer &> /dev/null; then
    echo "❌ Buildozer not found. Installing..."
    pip install buildozer
fi

# Check if Cython is installed (required for buildozer)
if ! python -c "import Cython" &> /dev/null; then
    echo "❌ Cython not found. Installing..."
    pip install Cython
fi

# Install required dependencies for APK building
echo "📦 Installing build dependencies..."
pip install kivy kivymd plyer python-for-android

# Copy model file to the build directory
echo "📋 Copying model files..."
mkdir -p ../monkeypox_model
cp ../../monkeypox_model/*.py ../monkeypox_model/
cp ../../monkeypox_model/*.pth ../monkeypox_model/ 2>/dev/null || echo "⚠️  Model file (best_model.pth) not found - app will run without AI"

# Initialize buildozer if not already done
if [ ! -f "buildozer.spec" ]; then
    echo "🔧 Initializing buildozer..."
    buildozer init
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
buildozer android clean

# Build the APK
echo "🔨 Building APK (this may take 15-30 minutes)..."
echo "☕ Time for coffee! This is a long process..."

# Build debug APK
buildozer android debug

# Check if build was successful
if [ -f "bin/*.apk" ]; then
    echo "✅ APK built successfully!"
    echo "📱 APK Location: $(pwd)/bin/"
    echo ""
    echo "📋 Installation Instructions:"
    echo "1. Transfer the APK file to your Android device"
    echo "2. Enable 'Unknown Sources' in Android Settings > Security"
    echo "3. Tap the APK file to install"
    echo "4. Grant camera and storage permissions when prompted"
    echo ""
    echo "🎉 Your Monkeypox AI Classifier is ready for mobile!"
    
    # List the generated APK files
    echo "📄 Generated APK files:"
    ls -la bin/*.apk
else
    echo "❌ APK build failed. Check the output above for errors."
    echo ""
    echo "🔧 Common solutions:"
    echo "1. Install Android SDK and NDK"
    echo "2. Install Java JDK 8"
    echo "3. Run: buildozer android debug -v for verbose output"
    echo "4. Check buildozer.spec configuration"
fi

echo ""
echo "🏥 Important: This APK contains AI for medical screening only."
echo "⚠️  Always consult healthcare professionals for medical diagnosis."
