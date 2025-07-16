@echo off
echo.
echo 🚀 GITHUB APK BUILD SETUP
echo =========================
echo.

echo ⚠️  BEFORE RUNNING THIS SCRIPT:
echo    1. Create GitHub repository at: https://github.com/new
echo    2. Name: monkeypox-ai-mobile
echo    3. Make it PUBLIC (for free GitHub Actions)
echo    4. DO NOT initialize with README
echo.

set /p username="Enter your GitHub username: "
if "%username%"=="" (
    echo ❌ Username cannot be empty!
    pause
    exit /b 1
)

echo.
echo 🔗 Setting up GitHub remote...
git remote add origin https://github.com/%username%/monkeypox-ai-mobile.git

echo 🌿 Setting up main branch...
git branch -M main

echo 📤 Pushing to GitHub...
echo    This will trigger automatic APK building!
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ✅ SUCCESS! Your code is now on GitHub!
    echo.
    echo 🏗️ APK BUILD STATUS:
    echo    • GitHub Actions will auto-trigger
    echo    • Build time: ~15-20 minutes
    echo    • Linux environment with proper tools
    echo.
    echo 📥 TO DOWNLOAD APK:
    echo    1. Go to: https://github.com/%username%/monkeypox-ai-mobile
    echo    2. Click "Actions" tab
    echo    3. Click latest workflow run
    echo    4. Download "Monkeypox-AI-APK" artifact
    echo    5. Extract and install APK on Android
    echo.
    echo 🎉 Your native Android APK will be ready soon!
    start https://github.com/%username%/monkeypox-ai-mobile/actions
) else (
    echo.
    echo ❌ Push failed! Common solutions:
    echo    • Make sure repository exists on GitHub
    echo    • Check repository name is correct
    echo    • Ensure repository is public
    echo    • Try again with correct username
)

echo.
pause
