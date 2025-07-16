# Monkeypox AI Mobile App

Transform your monkeypox classifier into a mobile application with multiple deployment options.

## 📱 Mobile App Options

### 1. Progressive Web App (PWA) - **RECOMMENDED**
The easiest way to create a mobile experience using Streamlit.

#### Features:
- ✅ **Works on all devices** (iOS, Android, Desktop)
- ✅ **Camera integration** for photo capture
- ✅ **Offline capabilities** (when cached)
- ✅ **App-like experience** (can be added to home screen)
- ✅ **Touch-optimized** interface
- ✅ **Responsive design** for all screen sizes

#### Quick Start:
```bash
# Navigate to mobile app directory
cd mobile_app

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Run the mobile-optimized app
streamlit run main.py --server.port 8502
```

#### Access:
- **Mobile Browser**: http://localhost:8502
- **Add to Home Screen**: Use browser "Add to Home Screen" option

### 2. Native Mobile App (Kivy/KivyMD)
For a truly native mobile experience.

#### Features:
- ✅ **Native performance**
- ✅ **Device integration** (camera, storage)
- ✅ **Offline functionality**
- ✅ **App store distribution** possible

#### Setup:
```bash
# Install mobile dependencies
pip install kivy kivymd plyer

# Run native app
python native_app.py
```

### 3. React Native/Expo (Future Development)
For cross-platform native apps with JavaScript.

## 🚀 Mobile PWA Features

### **📸 Camera Integration**
- Direct camera capture from mobile devices
- Gallery/photo library access
- Real-time image processing

### **🧠 AI Classification**
- Same ResNet18 model as desktop version
- Mobile-optimized inference
- Real-time confidence scoring

### **🏥 Medical Guidance**
- Emergency contact information
- Step-by-step medical protocols
- Crisis support resources

### **💾 Data Collection**
- Save classified images
- Track analysis history
- Export functionality

### **🔒 Privacy & Security**
- Local processing (no data leaves device)
- HIPAA-compliant design
- Secure image handling

## 📋 Installation Instructions

### **Option 1: PWA (Recommended)**

1. **Start the mobile app**:
   ```bash
   cd faceemotion/mobile_app
   streamlit run main.py --server.port 8502
   ```

2. **Access on mobile**:
   - Open browser on your phone
   - Navigate to: `http://your-computer-ip:8502`
   - Tap "Add to Home Screen" in browser menu

3. **Use like a native app**:
   - Icon appears on home screen
   - Full-screen experience
   - Camera and gallery access

### **Option 2: Native App Development**

1. **Install mobile development tools**:
   ```bash
   pip install kivy kivymd plyer buildozer
   ```

2. **Build for Android**:
   ```bash
   # Install buildozer
   pip install buildozer

   # Initialize buildozer
   buildozer init

   # Build APK
   buildozer android debug
   ```

3. **Build for iOS** (macOS only):
   ```bash
   # Install kivy-ios
   pip install kivy-ios

   # Build iOS app
   toolchain build python3 kivy
   ```

## 🎯 Mobile-Specific Features

### **Touch-Optimized Interface**
- Large, thumb-friendly buttons
- Swipe gestures
- Haptic feedback (native apps)

### **Camera Features**
- **Real-time capture**: Take photos directly
- **Gallery access**: Choose existing images
- **Image quality optimization**: Automatic compression

### **Offline Capabilities**
- **Model caching**: AI works without internet
- **Local storage**: Save results locally
- **Sync when online**: Upload to cloud when connected

### **Mobile Medical Features**
- **Emergency calling**: Direct dial emergency numbers
- **GPS location**: Share location with emergency services
- **Medical ID integration**: Access emergency medical info

## 📊 Performance Optimization

### **Mobile Model Optimization**
```python
# Quantize model for mobile
import torch
model_quantized = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)
```

### **Image Processing**
- Automatic image resizing
- Format optimization (WebP support)
- Memory management for mobile devices

### **Battery Optimization**
- Efficient inference
- Background processing limits
- Power-aware computing

## 🔧 Deployment Options

### **1. Self-Hosted PWA**
```bash
# Run on local network
streamlit run main.py --server.address 0.0.0.0 --server.port 8502
```

### **2. Cloud Deployment**
- **Streamlit Cloud**: Easy deployment
- **Heroku**: Scalable hosting
- **AWS/GCP**: Enterprise deployment

### **3. App Store Distribution**
- **Google Play Store**: Android apps
- **Apple App Store**: iOS apps (requires developer account)
- **Enterprise distribution**: Internal company apps

## 📱 User Guide

### **Getting Started**
1. Open the app on your mobile device
2. Grant camera permissions when prompted
3. Tap "Analyze Skin Lesion"
4. Take photo or choose from gallery
5. Wait for AI analysis
6. Follow medical guidance provided

### **Emergency Features**
- **Quick dial**: Emergency numbers pre-programmed
- **Medical info**: Critical guidance always accessible
- **Location sharing**: GPS coordinates for emergency services

### **Privacy Protection**
- All processing happens on-device
- No images sent to external servers
- Medical data stays private

## 🆘 Support & Resources

### **Technical Support**
- App crashes or errors
- Camera/gallery issues
- Performance problems

### **Medical Support**
- **Emergency**: Call 911
- **CDC Hotline**: 1-800-CDC-INFO
- **Crisis Text**: Text HOME to 741741

### **Updates**
- App updates delivered automatically (PWA)
- Model improvements pushed regularly
- Security patches applied continuously

## 📈 Analytics & Monitoring

### **Usage Analytics**
- Classification accuracy tracking
- User engagement metrics
- Performance monitoring

### **Medical Compliance**
- HIPAA compliance monitoring
- Audit trail maintenance
- Privacy protection verification

---

## 🚀 Quick Start Commands

```bash
# Start mobile PWA
cd mobile_app && streamlit run main.py --server.port 8502

# Build native Android app
buildozer android debug

# Deploy to cloud
streamlit deploy
```

Your monkeypox classifier is now ready for mobile deployment! 📱🧠✨
