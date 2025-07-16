# 🪟 Windows APK Building Setup
## Native Android APK for Monkeypox AI Classifier

Since APK building traditionally requires Linux, here are **3 proven methods** for Windows users:

## 🎯 **Method 1: GitHub Actions (RECOMMENDED)** ⭐

### **Why GitHub Actions?**
- ✅ **Zero local setup** - Cloud builds everything
- ✅ **Linux environment** - Proper build tools
- ✅ **Automatic builds** - Push code, get APK
- ✅ **Free for public repos** - No cost
- ✅ **Professional CI/CD** - Industry standard

### **Setup Steps:**

1. **Initialize Git Repository:**
```bash
cd c:\Users\cse\Desktop\monkey_pox\PRACTICE-main
git init
git add .
git commit -m "Initial monkeypox AI mobile app"
```

2. **Create GitHub Repository:**
- Go to [GitHub.com](https://github.com)
- Click "New Repository"
- Name: `monkeypox-ai-mobile`
- Make it **Public** (for free Actions)

3. **Push to GitHub:**
```bash
git remote add origin https://github.com/YOUR_USERNAME/monkeypox-ai-mobile.git
git branch -M main
git push -u origin main
```

4. **Enable GitHub Actions:**
- Repository → "Actions" tab
- Enable workflows
- Actions will auto-trigger on push

5. **Download APK:**
- Actions → Latest workflow run
- Download "Monkeypox-AI-APK" artifact
- Extract `monkeypoxai-*.apk`

---

## 🐧 **Method 2: WSL (Windows Subsystem for Linux)**

### **Setup WSL:**
```powershell
# Run as Administrator
wsl --install
# Restart computer
```

### **Install Dependencies in WSL:**
```bash
# In WSL terminal
sudo apt update
sudo apt install python3 python3-pip openjdk-8-jdk git zip unzip

# Install buildozer
pip3 install buildozer cython
pip3 install kivy kivymd plyer torch torchvision pillow
```

### **Build APK:**
```bash
cd /mnt/c/Users/cse/Desktop/monkey_pox/PRACTICE-main/faceemotion/mobile_app
buildozer android debug
```

---

## ☁️ **Method 3: Cloud Development (Alternative)**

### **Google Colab:**
- Upload project to Google Drive
- Use Colab with GPU for faster builds
- Download APK directly

### **Gitpod/Codespaces:**
- Cloud Linux environment
- Full buildozer support
- Browser-based development

---

## 🚀 **Let's Start with GitHub Actions!**

I'll help you set up the GitHub repository and automated APK building right now!
