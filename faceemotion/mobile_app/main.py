"""
Native Android APK - Monkeypox AI Classifier
Simplified version for APK building using Kivy/KivyMD
Can also run as Streamlit PWA
"""

import os
import sys
import traceback
from datetime import datetime

# Set up paths
APP_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(APP_DIR, 'model')
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

# Check if running as APK or Streamlit
RUNNING_AS_APK = False
try:
    from kivy.app import App
    from kivy.utils import platform
    if platform == 'android':
        RUNNING_AS_APK = True
except ImportError:
    pass

if RUNNING_AS_APK:
    # APK version using Kivy
    try:
        from kivy.app import App
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        from kivy.uix.label import Label
        from kivy.uix.image import Image
        from kivy.uix.popup import Popup
        from kivy.uix.filechooser import FileChooserIconView
        from kivy.clock import Clock
        from kivy.logger import Logger
        from kivy.utils import platform
        
        # Android permissions
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            from android.storage import primary_external_storage_path
            request_permissions([
                Permission.CAMERA,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.INTERNET
            ])
        
    except ImportError as e:
        print(f"Kivy import error: {e}")
else:
    # Streamlit PWA version
    import streamlit as st
    # Add the current directory to the path for imports
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(current_dir)
    
    # Import screen modules
    from screens.mobile_main_menu import show_mobile_main_menu, show_mobile_about
    from screens.mobile_analyze_screen import show_mobile_analyze_screen

# Model import
try:
    from monkeypox_model.monkeypox_configuration import MonkeypoxModel
    MODEL_AVAILABLE = True
except ImportError as e:
    MODEL_AVAILABLE = False
    if RUNNING_AS_APK:
        Logger.warning(f"MonkeypoxModel import failed: {e}")

if RUNNING_AS_APK:
    # Kivy APK Application Class
    class MonkeypoxAPK(App):
        """Native Android APK for Monkeypox Classification"""
        
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.model = None
            self.current_image_path = None
            self.result_popup = None
            
        def build(self):
            """Build the mobile app interface"""
            self.title = "Monkeypox AI Classifier"
            
            # Load AI model
            if MODEL_AVAILABLE:
                self.load_model()
            
            # Main layout
            main_layout = BoxLayout(
                orientation='vertical',
                padding=20,
                spacing=15
            )
            
            # App header
            header = Label(
                text='🧠 Monkeypox AI Classifier',
                size_hint_y=None,
                height=80,
                font_size='24sp',
                color=(0.8, 0.2, 0.2, 1)
            )
            
            # Medical disclaimer
            disclaimer = Label(
                text='⚠️ MEDICAL DISCLAIMER:\nThis AI tool is for screening only.\nNOT a medical diagnosis.\nAlways consult healthcare professionals.',
                size_hint_y=None,
                height=120,
                font_size='14sp',
                color=(1, 0.5, 0, 1),
                text_size=(None, None),
                halign='center'
            )
            
            # Action buttons
            camera_button = Button(
                text='📷 Take Photo',
                size_hint_y=None,
                height=60,
                font_size='18sp',
                background_color=(0.2, 0.6, 0.8, 1)
            )
            camera_button.bind(on_press=self.take_photo)
            
            gallery_button = Button(
                text='📁 Choose from Gallery',
                size_hint_y=None,
                height=60,
                font_size='18sp',
                background_color=(0.4, 0.7, 0.4, 1)
            )
            gallery_button.bind(on_press=self.choose_from_gallery)
            
            info_button = Button(
                text='ℹ️ Medical Information',
                size_hint_y=None,
                height=50,
                font_size='16sp',
                background_color=(0.6, 0.4, 0.8, 1)
            )
            info_button.bind(on_press=self.show_medical_info)
            
            emergency_button = Button(
                text='🚨 Emergency Contacts',
                size_hint_y=None,
                height=50,
                font_size='16sp',
                background_color=(0.8, 0.4, 0.2, 1)
            )
            emergency_button.bind(on_press=self.show_emergency_contacts)
            
            # Status label
            self.status_label = Label(
                text='Ready for image analysis',
                size_hint_y=None,
                height=40,
                font_size='14sp'
            )
            
            # Add widgets to layout
            main_layout.add_widget(header)
            main_layout.add_widget(disclaimer)
            main_layout.add_widget(camera_button)
            main_layout.add_widget(gallery_button)
            main_layout.add_widget(info_button)
            main_layout.add_widget(emergency_button)
            main_layout.add_widget(self.status_label)
            
            return main_layout
        
        def load_model(self):
            """Load the AI classification model"""
            try:
                model_path = os.path.join(
                    os.path.dirname(__file__), 
                    '..', 
                    'monkeypox_model', 
                    'best_model.pth'
                )
                
                if os.path.exists(model_path):
                    self.model = MonkeypoxModel()
                    success = self.model.load_model(model_path)
                    if success:
                        self.status_label.text = "AI Model loaded successfully"
                        Logger.info("MonkeypoxAPK: Model loaded successfully")
                    else:
                        self.status_label.text = "Failed to load AI model"
                        Logger.error("MonkeypoxAPK: Failed to load model")
                else:
                    self.status_label.text = "Model file not found"
                    Logger.error(f"MonkeypoxAPK: Model file not found at {model_path}")
                    
            except Exception as e:
                self.status_label.text = f"Model loading error: {str(e)}"
                Logger.error(f"MonkeypoxAPK: Model loading error: {e}")
        
        def take_photo(self, instance):
            """Take photo using device camera"""
            try:
                if platform == 'android':
                    from plyer import camera
                    
                    # Generate filename
                    filename = f"monkeypox_photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                    filepath = os.path.join(primary_external_storage_path(), filename)
                    
                    # Take photo
                    camera.take_picture(
                        filename=filepath,
                        on_complete=self.photo_taken
                    )
                    
                    self.status_label.text = "Taking photo..."
                    
                else:
                    self.show_popup("Camera Not Available", "Camera functionality is only available on Android devices.")
                    
            except Exception as e:
                self.show_popup("Camera Error", f"Failed to access camera: {str(e)}")
        
        def photo_taken(self, filename):
            """Handle photo taken from camera"""
            if filename and os.path.exists(filename):
                self.current_image_path = filename
                self.status_label.text = f"Photo captured: {os.path.basename(filename)}"
                Clock.schedule_once(lambda dt: self.analyze_image(), 0.5)
            else:
                self.show_popup("Photo Error", "Failed to capture photo. Please try again.")
        
        def choose_from_gallery(self, instance):
            """Choose image from device gallery"""
            try:
                # Create file chooser popup
                content = BoxLayout(orientation='vertical')
                
                if platform == 'android':
                    # On Android, use external storage path
                    start_path = primary_external_storage_path()
                else:
                    start_path = os.path.expanduser('~')
                
                filechooser = FileChooserIconView(
                    path=start_path,
                    filters=['*.jpg', '*.jpeg', '*.png', '*.webp']
                )
                
                button_layout = BoxLayout(
                    size_hint_y=None,
                    height=50,
                    spacing=10
                )
                
                select_button = Button(text='Select')
                cancel_button = Button(text='Cancel')
                
                def select_image(btn):
                    if filechooser.selection:
                        self.current_image_path = filechooser.selection[0]
                        self.status_label.text = f"Selected: {os.path.basename(self.current_image_path)}"
                        popup.dismiss()
                        Clock.schedule_once(lambda dt: self.analyze_image(), 0.5)
                    else:
                        self.show_popup("Selection Error", "Please select an image file.")
                
                def cancel_selection(btn):
                    popup.dismiss()
                
                select_button.bind(on_press=select_image)
                cancel_button.bind(on_press=cancel_selection)
                
                button_layout.add_widget(select_button)
                button_layout.add_widget(cancel_button)
                
                content.add_widget(filechooser)
                content.add_widget(button_layout)
                
                popup = Popup(
                    title='Choose Image',
                    content=content,
                    size_hint=(0.9, 0.9)
                )
                popup.open()
                
            except Exception as e:
                self.show_popup("Gallery Error", f"Failed to access gallery: {str(e)}")
        
        def analyze_image(self):
            """Analyze the selected image using AI"""
            if not self.current_image_path:
                self.show_popup("No Image", "Please select an image first.")
                return
            
            if not self.model:
                self.show_popup("Model Error", "AI model not available. Please check installation.")
                return
            
            try:
                self.status_label.text = "Analyzing image..."
                
                # Perform AI analysis
                result = self.model.predict(self.current_image_path)
                
                predicted_class = result['predicted_class']
                confidence = result['confidence']
                
                # Show results
                self.show_analysis_results(predicted_class, confidence)
                
            except Exception as e:
                self.show_popup("Analysis Error", f"Failed to analyze image: {str(e)}")
                Logger.error(f"MonkeypoxAPK: Analysis error: {e}")
                Logger.error(f"MonkeypoxAPK: Traceback: {traceback.format_exc()}")
        
        def show_analysis_results(self, predicted_class, confidence):
            """Display analysis results"""
            if predicted_class == "Monkey Pox":
                title = "⚠️ POTENTIAL MONKEYPOX DETECTED"
                message = f"""Confidence: {confidence:.1%}

🚨 SEEK IMMEDIATE MEDICAL ATTENTION

This is NOT a medical diagnosis.
Professional evaluation required.

IMMEDIATE ACTIONS:
• Contact healthcare provider NOW
• Isolate from others immediately
• Cover all lesions with clothing
• Wash hands frequently

EMERGENCY: Call local emergency number
CDC Hotline: 1-800-CDC-INFO"""
                
            else:
                title = "✅ NON-MONKEYPOX CLASSIFICATION"
                message = f"""Confidence: {confidence:.1%}

Good news! AI suggests this is likely NOT monkeypox.

However, still consult a healthcare provider if:
• You have concerns about the lesion
• Symptoms persist or worsen
• Recent travel to affected areas

Remember: This is screening only, not diagnosis."""
            
            self.show_popup(title, message, auto_dismiss=False)
            self.status_label.text = f"Analysis complete: {predicted_class}"
        
        def show_medical_info(self, instance):
            """Show medical information"""
            message = """🏥 MEDICAL GUIDANCE

This app provides AI screening only - NOT a medical diagnosis.

WHEN TO SEEK MEDICAL CARE:
• New or changing skin lesions
• Fever with skin symptoms  
• Recent travel to affected areas
• Known exposure to monkeypox

Always consult qualified healthcare professionals."""
            
            self.show_popup("Medical Information", message, auto_dismiss=False)
        
        def show_emergency_contacts(self, instance):
            """Show emergency contact information"""
            message = """🆘 EMERGENCY CONTACTS

🚨 IMMEDIATE EMERGENCY:
Call your local emergency services

🏥 HEALTH AUTHORITIES:
• CDC Monkeypox Hotline: 1-800-CDC-INFO
• Local Health Department

💭 CRISIS SUPPORT:
• Crisis Text Line: Text HOME to 741741

🔗 OFFICIAL RESOURCES:
• CDC: cdc.gov/poxvirus/monkeypox
• WHO: who.int/monkeypox"""
            
            self.show_popup("Emergency Contacts", message, auto_dismiss=False)
        
        def show_popup(self, title, message, auto_dismiss=True):
            """Show popup dialog"""
            content = BoxLayout(orientation='vertical', padding=10, spacing=10)
            
            label = Label(
                text=message,
                text_size=(400, None),
                halign='left',
                valign='top'
            )
            
            button_layout = BoxLayout(
                size_hint_y=None,
                height=50,
                spacing=10
            )
            
            close_button = Button(text='Close')
            
            def close_popup(btn):
                popup.dismiss()
            
            close_button.bind(on_press=close_popup)
            button_layout.add_widget(close_button)
            
            content.add_widget(label)
            content.add_widget(button_layout)
            
            popup = Popup(
                title=title,
                content=content,
                size_hint=(0.9, 0.8),
                auto_dismiss=auto_dismiss
            )
            popup.open()

else:
    # Streamlit PWA version
    def main():
        """Main mobile application function"""
        
        # Set page configuration for mobile
        st.set_page_config(
            page_title="Monkeypox Classifier",
            page_icon="🧠",
            layout="centered",
            initial_sidebar_state="collapsed",
            menu_items={
                'Get Help': 'https://cdc.gov/poxvirus/monkeypox',
                'Report a bug': None,
                'About': "Monkeypox AI Classifier - Mobile Version"
            }
        )
        
        # Initialize session state
        if 'page' not in st.session_state:
            st.session_state.page = "main"
        
        # Mobile-optimized CSS
        st.markdown("""
        <style>
        /* Mobile-first responsive design */
        .main {
            padding: 0.5rem !important;
            max-width: 100% !important;
        }
        
        /* Mobile-friendly buttons */
        .stButton > button {
            width: 100%;
            height: 60px;
            background: linear-gradient(45deg, #ff6b6b, #ff8787);
            color: white;
            border: none;
            border-radius: 15px;
            font-size: 18px;
            font-weight: bold;
            margin: 10px 0;
            box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background: linear-gradient(45deg, #ff5252, #ff6b6b);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
        }
        
        /* Mobile-optimized file uploader */
        .uploadedFile {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 10px;
            margin: 10px 0;
        }
        
        /* Touch-friendly radio buttons */
        .stRadio > div {
            flex-direction: column;
        }
        
        .stRadio > div > label {
            padding: 15px;
            margin: 5px 0;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            background-color: #f8f9fa;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .stRadio > div > label:hover {
            border-color: #ff6b6b;
            background-color: #fff5f5;
        }
        
        /* Mobile-optimized metrics */
        .metric-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin: 10px 0;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        /* PWA-style header */
        .pwa-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 0 0 20px 20px;
            text-align: center;
            margin: -1rem -1rem 20px -1rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        /* Responsive columns for mobile */
        @media (max-width: 768px) {
            .row-widget.stColumns {
                flex-direction: column;
            }
            
            .stColumns > div {
                width: 100% !important;
                margin-bottom: 20px;
            }
        }
        </style>
        """, unsafe_allow_html=True)
        
        # PWA manifest
        st.markdown("""
        <link rel="manifest" href="data:application/json;base64,ewogICJuYW1lIjogIk1vbmtleXBveCBDbGFzc2lmaWVyIiwKICAic2hvcnRfbmFtZSI6ICJNb25rZXlwb3ggQUkiLAogICJkZXNjcmlwdGlvbiI6ICJBSSBwb3dlcmVkIG1vbmtleXBveCBza2luIGxlc2lvbiBjbGFzc2lmaWVyIiwKICAic3RhcnRfdXJsIjogIi8iLAogICJkaXNwbGF5IjogInN0YW5kYWxvbmUiLAogICJiYWNrZ3JvdW5kX2NvbG9yIjogIiNmZmZmZmYiLAogICJ0aGVtZV9jb2xvciI6ICIjZmY2YjZiIiwKICAiaWNvbnMiOiBbCiAgICB7CiAgICAgICJzcmMiOiAiZGF0YTppbWFnZS9zdmcreG1sO2Jhc2U2NCxQSE4yWnlCNGJXeHVjejBpYUhSMGNEb3ZMM2QzZHk1M00zUXViM0puTHpJd01EQXZjM1puSWlCM2FXUjBhRDBpTWpRaUlHaGxhV2RvZEQwaU1qUWlJSFpwWlhkQ2IzZzlJakFnTUNBeU5DQXlOQ0krUEhCaGRHZ2daRDBpVFRFeUlERXlZemt1TlRNdE5DNDJNVEU0TGpNNUxUZ3VPVEJhVFRFeUlERXdZamt1TlRNdE5DNDBOVEU0TGpNNUxUZ3VNRE5hSWlCbWFXeHNQU0lqWm1ZMlltWmlJaTgrUEM5emRtYysiLAogICAgICAic2l6ZXMiOiAiMjR4MjQiLAogICAgICAidHlwZSI6ICJpbWFnZS9zdmcreG1sIgogICAgfQogIF0KfQ==">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="apple-mobile-web-app-title" content="Monkeypox AI">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        """, unsafe_allow_html=True)
        
        # Page routing
        if st.session_state.page == "main":
            show_mobile_main_menu()
        elif st.session_state.page == "analyze":
            show_mobile_analyze_screen()
        elif st.session_state.page == "about":
            show_mobile_about()
        else:
            # Default to main menu if unknown page
            st.session_state.page = "main"
            show_mobile_main_menu()

# Main execution
def main():
    """Main application function - handles both APK and PWA modes"""
    
    if RUNNING_AS_APK:
        # Run as native Android APK
        try:
            app = MonkeypoxAPK()
            app.run()
        except Exception as e:
            print(f"APK startup error: {e}")
            print(f"Traceback: {traceback.format_exc()}")
    else:
        # Run as Streamlit PWA
        # Set page configuration for mobile
        st.set_page_config(
            page_title="Monkeypox Classifier",
            page_icon="🧠",
            layout="centered",
            initial_sidebar_state="collapsed",
            menu_items={
                'Get Help': 'https://cdc.gov/poxvirus/monkeypox',
                'Report a bug': None,
                'About': "Monkeypox AI Classifier - Mobile Version"
            }
        )
        
        # Initialize session state
        if 'page' not in st.session_state:
            st.session_state.page = "main"
        
        # Mobile-optimized CSS
        st.markdown("""
        <style>
        /* Mobile-first responsive design */
        .main {
            padding: 0.5rem !important;
            max-width: 100% !important;
        }
        
        /* Mobile-friendly buttons */
        .stButton > button {
            width: 100%;
            height: 60px;
            background: linear-gradient(45deg, #ff6b6b, #ff8787);
            color: white;
            border: none;
            border-radius: 15px;
            font-size: 18px;
            font-weight: bold;
            margin: 10px 0;
            box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background: linear-gradient(45deg, #ff5252, #ff6b6b);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
        }
        
        /* Mobile-optimized file uploader */
        .uploadedFile {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 10px;
            margin: 10px 0;
        }
        
        /* Touch-friendly radio buttons */
        .stRadio > div {
            flex-direction: column;
        }
        
        .stRadio > div > label {
            padding: 15px;
            margin: 5px 0;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            background-color: #f8f9fa;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .stRadio > div > label:hover {
            border-color: #ff6b6b;
            background-color: #fff5f5;
        }
        
        /* Mobile-optimized metrics */
        .metric-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin: 10px 0;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        /* PWA-style header */
        .pwa-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 0 0 20px 20px;
            text-align: center;
            margin: -1rem -1rem 20px -1rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        /* Responsive columns for mobile */
        @media (max-width: 768px) {
            .row-widget.stColumns {
                flex-direction: column;
            }
            
            .stColumns > div {
                width: 100% !important;
                margin-bottom: 20px;
            }
        }
        </style>
        """, unsafe_allow_html=True)
        
        # PWA manifest
        st.markdown("""
        <link rel="manifest" href="data:application/json;base64,ewogICJuYW1lIjogIk1vbmtleXBveCBDbGFzc2lmaWVyIiwKICAic2hvcnRfbmFtZSI6ICJNb25rZXlwb3ggQUkiLAogICJkZXNjcmlwdGlvbiI6ICJBSSBwb3dlcmVkIG1vbmtleXBveCBza2luIGxlc2lvbiBjbGFzc2lmaWVyIiwKICAic3RhcnRfdXJsIjogIi8iLAogICJkaXNwbGF5IjogInN0YW5kYWxvbmUiLAogICJiYWNrZ3JvdW5kX2NvbG9yIjogIiNmZmZmZmYiLAogICJ0aGVtZV9jb2xvciI6ICIjZmY2YjZiIiwKICAiaWNvbnMiOiBbCiAgICB7CiAgICAgICJzcmMiOiAiZGF0YTppbWFnZS9zdmcreG1sO2Jhc2U2NCxQSE4yWnlCNGJXeHVjejBpYUhSMGNEb3ZMM2QzZHk1M00zUXViM0puTHpJd01EQXZjM1puSWlCM2FXUjBhRDBpTWpRaUlHaGxhV2RvZEQwaU1qUWlJSFpwWlhkQ2IzZzlJakFnTUNBeU5DQXlOQ0krUEhCaGRHZ2daRDBpVFRFeUlERXlZemt1TlRNdE5DNDJNVEU0TGpNNUxUZ3VPVEJhVFRFeUlERXdZamt1TlRNdE5DNDBOVEU0TGpNNUxUZ3VNRE5hSWlCbWFXeHNQU0lqWm1ZMlltWmlJaTgrUEM5emRtYysiLAogICAgICAic2l6ZXMiOiAiMjR4MjQiLAogICAgICAidHlwZSI6ICJpbWFnZS9zdmcreG1sIgogICAgfQogIF0KfQ==">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="apple-mobile-web-app-title" content="Monkeypox AI">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        """, unsafe_allow_html=True)
        
        # Page routing
        if st.session_state.page == "main":
            show_mobile_main_menu()
        elif st.session_state.page == "analyze":
            show_mobile_analyze_screen()
        elif st.session_state.page == "about":
            show_mobile_about()
        else:
            # Default to main menu if unknown page
            st.session_state.page = "main"
            show_mobile_main_menu()

if __name__ == "__main__":
    main()
