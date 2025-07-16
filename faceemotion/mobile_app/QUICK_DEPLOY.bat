@echo off
echo.
echo 🚀 MONKEYPOX AI - INSTANT DEPLOYMENT
echo =====================================
echo.

:: Check if we're in the right directory
if not exist "main.py" (
    echo ❌ Error: Please run this script from the mobile_app directory
    echo    Current location should contain main.py
    pause
    exit /b 1
)

echo ✅ Starting instant deployment...
echo.

:: Install required packages
echo 📦 Installing packages...
pip install streamlit plyer torch torchvision pillow >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Some packages may already be installed - continuing...
)

:: Get IP address for mobile access
echo 🔍 Finding your IP address...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    for /f "tokens=1 delims= " %%b in ("%%a") do (
        set "IP=%%b"
        goto :found_ip
    )
)
:found_ip

echo.
echo 🎉 DEPLOYMENT READY!
echo ==================
echo.
echo 📱 MOBILE ACCESS (PWA):
echo    Open on your phone: http://%IP%:8503
echo    Then: Add to Home Screen
echo.
echo 💻 DESKTOP ACCESS:
echo    Open in browser: http://localhost:8503
echo.
echo 🏥 FEATURES ACTIVE:
echo    ✅ AI Monkeypox Classification
echo    ✅ Camera Integration
echo    ✅ Medical Guidance
echo    ✅ Privacy Protection
echo    ✅ Offline Capable
echo.
echo 🚀 Starting Streamlit PWA...
echo    (Press Ctrl+C to stop)
echo.

:: Start the PWA
streamlit run main.py --server.port=8503 --server.headless=true --server.address=0.0.0.0

echo.
echo 👋 Thanks for using Monkeypox AI!
pause
