# 📱 Android APK Build Guide
## Monkeypox AI Classifier - Native Android App

Transform your monkeypox classifier into a native Android APK that can be installed on any Android phone.

## 🚀 Quick Start Options

### Option 1: Progressive Web App (PWA) - **RECOMMENDED** ⭐
The fastest way to get a mobile app experience:

```bash
# Run the PWA deployment script
build_apk.bat  # On Windows
# OR
bash build_apk.sh  # On Linux/Mac

# Then run
deploy_pwa.bat
```

**Benefits:**
- ✅ Works immediately on any device
- ✅ Camera and gallery access
- ✅ Add to home screen like native app
- ✅ Offline capabilities
- ✅ No app store approval needed

### Option 2: Native APK Building

#### Requirements:
- **Linux/Mac** (recommended) or **WSL on Windows**
- **Python 3.8+**
- **Java JDK 8**
- **Android SDK & NDK**
- **5-10 GB free space**

#### Build Steps:

1. **Install Dependencies:**
   ```bash
   pip install buildozer cython
   pip install kivy kivymd plyer
   ```

2. **Build APK:**
   ```bash
   # Navigate to mobile_app directory
   cd mobile_app
   
   # Run build script
   bash build_apk.sh
   ```

3. **Wait (15-30 minutes):** ☕
   - First build downloads Android SDK/NDK
   - Subsequent builds are faster

4. **Install APK:**
   - Transfer `bin/monkeypoxai-*.apk` to Android device
   - Enable "Unknown Sources" in Settings
   - Install APK

### Option 3: GitHub Actions (Cloud Building) ☁️

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Add mobile app"
   git push origin main
   ```

2. **Enable GitHub Actions:**
   - Go to your repository on GitHub
   - Click "Actions" tab
   - Enable workflows

3. **Download APK:**
   - Actions will build APK automatically
   - Download from "Artifacts" section
   - Or from "Releases" page

## 📱 APK Features

### **🧠 AI Classification**
- Full ResNet18 model included in APK
- Real-time skin lesion analysis
- Confidence scoring and probabilities
- Supports JPG, PNG, WebP formats

### **📸 Camera Integration**
- Direct photo capture from camera
- Gallery/photo library access
- Auto-optimization for AI processing
- Image quality enhancement

### **🏥 Medical Guidance**
- Comprehensive emergency protocols
- Contact information for healthcare
- Step-by-step medical instructions
- Crisis support resources

### **🔒 Privacy & Security**
- All processing happens on-device
- No data sent to external servers
- Medical information stays private
- HIPAA-compliant design

### **⚡ Performance**
- Optimized for mobile devices
- Battery-efficient inference
- Fast loading and processing
- Minimal storage requirements

## 📋 APK Specifications

```
Package Name: org.healthai.monkeypoxai
App Name: Monkeypox AI Classifier
Version: 1.0
Min Android: 5.0 (API 21)
Target Android: 12.0 (API 31)
Size: ~50-100 MB (with AI model)
Permissions: Camera, Storage, Internet
Architecture: ARM64, ARMv7
```

## 🛠️ Build Configuration

The `buildozer.spec` file contains all build settings:

```ini
[app]
title = Monkeypox AI Classifier
package.name = monkeypoxai
package.domain = org.healthai
version = 1.0
requirements = python3,kivy,kivymd,torch,torchvision,pillow,numpy,plyer
android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
```

## 🚨 Troubleshooting

### **Build Fails:**
```bash
# Clean and retry
buildozer android clean
buildozer android debug -v  # Verbose output

# Check requirements
java -version  # Should be Java 8
python --version  # Should be 3.8+
```

### **APK Won't Install:**
- Enable "Unknown Sources" in Android Settings
- Check available storage space
- Try installing via ADB: `adb install app.apk`

### **Camera Doesn't Work:**
- Grant camera permissions in app settings
- Restart app after granting permissions
- Check device camera functionality

### **AI Model Missing:**
```bash
# Ensure model file exists
ls ../monkeypox_model/best_model.pth

# Copy manually if needed
cp ../../monkeypox_model/best_model.pth ../monkeypox_model/
```

## 📊 File Structure

```
mobile_app/
├── main.py                 # Main app (dual PWA/APK)
├── buildozer.spec         # APK build configuration
├── build_apk.sh          # Linux/Mac build script
├── build_apk.bat         # Windows build script
├── deploy_pwa.bat        # PWA deployment
├── screens/              # UI screens
│   ├── mobile_main_menu.py
│   └── mobile_analyze_screen.py
├── .github/workflows/    # GitHub Actions
│   └── build-apk.yml
└── bin/                  # Generated APK files
    └── monkeypoxai-*.apk
```

## 🏥 Medical Compliance

### **Regulatory Considerations:**
- App provides screening only, not diagnosis
- Clear medical disclaimers included
- Emergency contact information provided
- Privacy protection implemented

### **Distribution Options:**
- **Direct Distribution:** Share APK files directly
- **Enterprise Distribution:** Internal company deployment
- **Google Play Store:** Requires medical app approval
- **Alternative Stores:** F-Droid, Amazon Appstore

## 🔄 Updates & Maintenance

### **Updating the App:**
1. **Increment version** in `buildozer.spec`
2. **Rebuild APK** with new changes
3. **Distribute updated APK**
4. **Users install over existing app**

### **Model Updates:**
- Replace `best_model.pth` with new model
- Rebuild APK with updated AI
- Test thoroughly before distribution

## 📈 Analytics & Monitoring

### **Usage Tracking:**
- Classification accuracy metrics
- User engagement statistics
- Error reporting and crashes
- Performance monitoring

### **Medical Compliance:**
- Audit trail maintenance
- Privacy protection verification
- Regulatory compliance checking

## 🎯 Success Metrics

### **Technical:**
- ✅ APK builds successfully
- ✅ Installs on Android devices
- ✅ Camera and AI work properly
- ✅ No crashes or errors

### **Medical:**
- ✅ Clear medical disclaimers
- ✅ Emergency contacts accessible
- ✅ Privacy protection active
- ✅ Guidance protocols complete

---

## 🚀 Quick Commands

```bash
# Build APK (Linux/Mac)
bash build_apk.sh

# Build APK (Windows)
build_apk.bat

# Deploy PWA
deploy_pwa.bat

# Clean build
buildozer android clean

# Debug build with verbose output
buildozer android debug -v

# Release build (for production)
buildozer android release
```

Your monkeypox classifier is now ready for native Android deployment! 📱🧠✨

**Remember:** This app provides AI screening only - always consult healthcare professionals for medical diagnosis.
