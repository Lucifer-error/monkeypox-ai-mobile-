@echo off
REM APK Build Script for Windows - Monkeypox AI Classifier
REM This script builds an Android APK using Buildozer on Windows

echo 🚀 Building Monkeypox AI Classifier APK...
echo ============================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python first.
    pause
    exit /b 1
)

REM Install required dependencies
echo 📦 Installing build dependencies...
pip install buildozer Cython

REM Note about Android development on Windows
echo ⚠️  NOTE: Building APKs on Windows requires additional setup:
echo 1. Install Windows Subsystem for Linux (WSL)
echo 2. Or use a Linux virtual machine
echo 3. Or use GitHub Actions for cloud building
echo.

REM For Windows users, provide alternative instructions
echo 🔄 Alternative APK Building Options:
echo.
echo OPTION 1 - Use WSL (Recommended):
echo 1. Install WSL: wsl --install
echo 2. Open WSL terminal
echo 3. Navigate to this directory
echo 4. Run: bash build_apk.sh
echo.
echo OPTION 2 - GitHub Actions (Cloud Build):
echo 1. Push code to GitHub repository
echo 2. Use GitHub Actions workflow for APK building
echo 3. Download built APK from Actions artifacts
echo.
echo OPTION 3 - Online Build Services:
echo 1. Use Buildozer online services
echo 2. Use Kivy Garden build services
echo 3. Use cloud-based Android build platforms
echo.

REM Create a simple batch file for PWA deployment instead
echo 🌐 Creating PWA deployment script instead...

REM Create PWA deployment batch file
echo @echo off > deploy_pwa.bat
echo echo 🌐 Deploying Monkeypox AI as Progressive Web App... >> deploy_pwa.bat
echo echo ============================================ >> deploy_pwa.bat
echo. >> deploy_pwa.bat
echo REM Start the mobile-optimized Streamlit app >> deploy_pwa.bat
echo echo 📱 Starting mobile-optimized web app... >> deploy_pwa.bat
echo python -m streamlit run main.py --server.port 8502 --server.address 0.0.0.0 >> deploy_pwa.bat
echo. >> deploy_pwa.bat
echo echo ✅ Mobile web app is running! >> deploy_pwa.bat
echo echo 📱 Access from mobile: http://your-ip:8502 >> deploy_pwa.bat
echo echo 🏠 Add to home screen for app-like experience >> deploy_pwa.bat
echo pause >> deploy_pwa.bat

echo ✅ Created deploy_pwa.bat for Progressive Web App deployment

REM Show QR code instructions
echo.
echo 📱 MOBILE ACCESS INSTRUCTIONS:
echo.
echo 1. Run deploy_pwa.bat to start the web app
echo 2. Find your computer's IP address (ipconfig)
echo 3. Open mobile browser: http://your-ip:8502
echo 4. Tap "Add to Home Screen" in browser menu
echo 5. Use like a native app!
echo.
echo 🎯 This creates a PWA that works like a native app:
echo ✅ Camera access
echo ✅ Offline capable
echo ✅ App icon on home screen
echo ✅ Full-screen experience
echo ✅ Push notifications (future)
echo.

echo 🏥 Important: This app contains AI for medical screening only.
echo ⚠️  Always consult healthcare professionals for medical diagnosis.
echo.
pause
