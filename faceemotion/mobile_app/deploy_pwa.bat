@echo off
echo 🚀 Deploying Monkeypox AI as Progressive Web App (PWA)...
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.8+ first.
    pause
    exit /b 1
)

:: Navigate to mobile app directory
cd /d "%~dp0"

echo 📦 Installing required packages...
pip install streamlit kivy kivymd plyer torch torchvision pillow

echo 🌐 Starting PWA server...
echo.
echo 📱 PWA Features:
echo   ✅ Add to Home Screen
echo   ✅ Camera Access
echo   ✅ Offline Capabilities
echo   ✅ Push Notifications
echo   ✅ Full-Screen Mode
echo.
echo 🏥 Medical AI Features:
echo   ✅ Monkeypox Classification
echo   ✅ Medical Guidance
echo   ✅ Emergency Protocols
echo   ✅ Privacy Protection
echo.
echo 🌍 Access URLs:
echo   📱 Mobile PWA: http://localhost:8502
echo   💻 Desktop:   http://localhost:8501
echo.
echo 📱 To install on mobile:
echo   1. Open http://localhost:8502 on your phone
echo   2. Tap 'Add to Home Screen'
echo   3. App icon will appear like native app
echo.
echo 🔄 Starting servers...

:: Start both desktop and mobile versions
start "Desktop App" cmd /k "echo Desktop App (localhost:8501) && cd .. && streamlit run app/main.py --server.port=8501"
timeout 3 >nul

start "Mobile PWA" cmd /k "echo Mobile PWA (localhost:8502) && python main.py"
timeout 3 >nul

echo.
echo ✅ PWA deployed successfully!
echo.
echo 📱 Mobile Users:
echo   1. Connect phone to same WiFi
echo   2. Find your computer's IP address: ipconfig
echo   3. Use http://[IP]:8502 on phone
echo   4. Add to home screen for app-like experience
echo.
echo 💻 Desktop Users:
echo   Use http://localhost:8501
echo.
echo 🛑 Press Ctrl+C in any window to stop servers
echo.
pause
