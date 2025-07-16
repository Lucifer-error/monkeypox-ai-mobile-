@echo off
echo.
echo 🔍 APK BUILD READINESS CHECK
echo ============================
echo.

:: Check if we're in the right directory
if not exist "faceemotion" (
    echo ❌ Error: Run this from the PRACTICE-main directory
    echo    Should contain faceemotion folder
    pause
    exit /b 1
)

echo ✅ Project Structure Check:
if exist "faceemotion\mobile_app\main.py" (
    echo    ✅ Mobile app exists
) else (
    echo    ❌ Mobile app missing
)

if exist "faceemotion\mobile_app\buildozer.spec" (
    echo    ✅ APK build config exists
) else (
    echo    ❌ APK build config missing
)

if exist "faceemotion\monkeypox_model\best_model.pth" (
    echo    ✅ AI model exists
) else (
    echo    ❌ AI model missing
)

if exist "faceemotion\mobile_app\.github\workflows\build-apk-enhanced.yml" (
    echo    ✅ GitHub Actions workflow exists
) else (
    echo    ❌ GitHub Actions workflow missing
)

echo.
echo 🧠 AI Model Check:
python -c "import torch; print('✅ PyTorch available')" 2>nul || echo "⚠️  PyTorch not found"

echo.
echo 📱 Mobile Dependencies:
python -c "import streamlit; print('✅ Streamlit available')" 2>nul || echo "⚠️  Streamlit not found"

echo.
echo 🔗 Git Status:
git status --porcelain >nul 2>&1
if %errorlevel% equ 0 (
    echo    ✅ Git repository initialized
    
    git remote -v | findstr origin >nul
    if %errorlevel% equ 0 (
        echo    ✅ GitHub remote configured
    ) else (
        echo    ⚠️  GitHub remote not set (run GITHUB_SETUP.bat)
    )
) else (
    echo    ❌ Not a git repository
)

echo.
echo 📊 READINESS SUMMARY:
echo =====================

set all_good=1

if not exist "faceemotion\mobile_app\main.py" set all_good=0
if not exist "faceemotion\mobile_app\buildozer.spec" set all_good=0
if not exist "faceemotion\monkeypox_model\best_model.pth" set all_good=0

if %all_good% equ 1 (
    echo ✅ ALL SYSTEMS READY FOR APK BUILD!
    echo.
    echo 🚀 NEXT STEPS:
    echo    1. Run GITHUB_SETUP.bat to push to GitHub
    echo    2. GitHub Actions will build APK automatically
    echo    3. Download APK from Actions artifacts
    echo    4. Install on Android device
    echo.
    echo 🎯 ESTIMATED TIME:
    echo    • GitHub setup: 2 minutes
    echo    • APK build: 15-20 minutes
    echo    • Total: ~20 minutes
) else (
    echo ❌ SOME COMPONENTS MISSING
    echo    Please ensure all required files exist
)

echo.
pause
