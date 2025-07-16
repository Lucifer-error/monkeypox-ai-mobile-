"""
Native Mobile App using Kivy/KivyMD
Alternative native mobile implementation
"""

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivy.clock import Clock
from kivy.logger import Logger
import os
import sys
from datetime import datetime

# Add model path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from monkeypox_model.monkeypox_configuration import MonkeypoxModel
except ImportError:
    Logger.warning("MonkeypoxModel: Could not import model")

class MonkeypoxMobileApp(MDApp):
    """Native mobile app for Monkeypox classification"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = MDScreen()
        self.file_manager = None
        self.model = None
        self.dialog = None
        
    def build(self):
        """Build the mobile app interface"""
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Red"
        
        # Load model
        self.load_classification_model()
        
        # Create main layout
        main_layout = MDBoxLayout(
            orientation="vertical",
            padding=20,
            spacing=20
        )
        
        # App header
        header_card = MDCard(
            MDBoxLayout(
                MDLabel(
                    text="🧠 Monkeypox AI Classifier",
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1),
                    font_style="H4",
                    halign="center"
                ),
                orientation="vertical",
                padding=20
            ),
            md_bg_color=(0.8, 0.2, 0.2, 1),
            size_hint_y=None,
            height=100
        )
        
        # Action buttons
        analyze_button = MDRaisedButton(
            text="📸 ANALYZE SKIN LESION",
            size_hint_y=None,
            height=60,
            md_bg_color=(0.8, 0.2, 0.2, 1),
            on_release=self.open_camera_or_gallery
        )
        
        info_button = MDRaisedButton(
            text="ℹ️ Medical Information",
            size_hint_y=None,
            height=50,
            md_bg_color=(0.2, 0.4, 0.8, 1),
            on_release=self.show_medical_info
        )
        
        emergency_button = MDRaisedButton(
            text="🚨 Emergency Contacts",
            size_hint_y=None,
            height=50,
            md_bg_color=(0.8, 0.4, 0.2, 1),
            on_release=self.show_emergency_contacts
        )
        
        # Add to layout
        main_layout.add_widget(header_card)
        main_layout.add_widget(analyze_button)
        main_layout.add_widget(info_button)
        main_layout.add_widget(emergency_button)
        
        self.screen.add_widget(main_layout)
        return self.screen
    
    def load_classification_model(self):
        """Load the monkeypox classification model"""
        try:
            model_path = os.path.join(
                os.path.dirname(__file__), 
                '..', 
                'monkeypox_model', 
                'best_model.pth'
            )
            self.model = MonkeypoxModel()
            success = self.model.load_model(model_path)
            if not success:
                Logger.error("MonkeypoxApp: Failed to load model")
        except Exception as e:
            Logger.error(f"MonkeypoxApp: Error loading model: {e}")
    
    def open_camera_or_gallery(self, instance):
        """Open camera or file picker for image selection"""
        try:
            from plyer import camera, filechooser
            
            # Create dialog for camera/gallery choice
            self.dialog = MDDialog(
                title="Choose Image Source",
                buttons=[
                    MDRaisedButton(
                        text="📷 Camera",
                        on_release=self.take_photo
                    ),
                    MDRaisedButton(
                        text="📁 Gallery",
                        on_release=self.choose_from_gallery
                    ),
                ],
            )
            self.dialog.open()
            
        except ImportError:
            self.show_error_dialog("Camera not available on this device")
    
    def take_photo(self, instance):
        """Take photo using device camera"""
        try:
            from plyer import camera
            
            # Close dialog
            self.dialog.dismiss()
            
            # Take photo
            filename = f"monkeypox_photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            camera.take_picture(
                filename=filename,
                on_complete=self.analyze_captured_image
            )
            
        except Exception as e:
            self.show_error_dialog(f"Camera error: {str(e)}")
    
    def choose_from_gallery(self, instance):
        """Choose image from device gallery"""
        try:
            from plyer import filechooser
            
            # Close dialog
            self.dialog.dismiss()
            
            # Open file chooser
            filechooser.open_file(
                on_selection=self.analyze_selected_image,
                filters=[("Image files", "*.jpg", "*.jpeg", "*.png", "*.webp")]
            )
            
        except Exception as e:
            self.show_error_dialog(f"Gallery error: {str(e)}")
    
    def analyze_captured_image(self, filename):
        """Analyze image captured from camera"""
        if filename:
            self.perform_analysis(filename)
    
    def analyze_selected_image(self, selection):
        """Analyze image selected from gallery"""
        if selection:
            self.perform_analysis(selection[0])
    
    def perform_analysis(self, image_path):
        """Perform AI analysis on the selected image"""
        if not self.model:
            self.show_error_dialog("AI model not loaded")
            return
        
        try:
            # Show loading dialog
            self.show_loading_dialog("Analyzing image...")
            
            # Perform prediction
            def analyze():
                result = self.model.predict(image_path)
                Clock.schedule_once(lambda dt: self.show_results(result), 0)
            
            # Run analysis in background
            Clock.schedule_once(lambda dt: analyze(), 0.1)
            
        except Exception as e:
            self.show_error_dialog(f"Analysis error: {str(e)}")
    
    def show_results(self, result):
        """Display analysis results"""
        # Close loading dialog
        if self.dialog:
            self.dialog.dismiss()
        
        predicted_class = result['predicted_class']
        confidence = result['confidence']
        
        if predicted_class == "Monkey Pox":
            title = "⚠️ POTENTIAL MONKEYPOX DETECTED"
            content = f"""
Confidence: {confidence:.1%}

🚨 SEEK IMMEDIATE MEDICAL ATTENTION

This is NOT a medical diagnosis.
Professional evaluation required.

Immediate actions:
• Contact healthcare provider
• Isolate from others
• Cover lesions
• Wash hands frequently

Emergency: Call 911 if severe symptoms
CDC Hotline: 1-800-CDC-INFO
"""
            button_color = (0.8, 0.2, 0.2, 1)
        else:
            title = "✅ NON-MONKEYPOX CLASSIFICATION"
            content = f"""
Confidence: {confidence:.1%}

Good news! AI suggests this is likely 
NOT monkeypox.

However, still consult a healthcare 
provider if you have concerns.

Monitor for:
• Changes in lesion appearance
• Fever or other symptoms
• Spreading of lesions
"""
            button_color = (0.2, 0.6, 0.2, 1)
        
        # Show results dialog
        self.dialog = MDDialog(
            title=title,
            text=content,
            buttons=[
                MDRaisedButton(
                    text="Save Result",
                    md_bg_color=button_color,
                    on_release=self.save_result
                ),
                MDRaisedButton(
                    text="New Analysis",
                    on_release=self.close_result_dialog
                ),
            ],
        )
        self.dialog.open()
    
    def show_medical_info(self, instance):
        """Show medical information and guidance"""
        content = """
🏥 MEDICAL GUIDANCE

This app provides AI screening only.
NOT a medical diagnosis.

When to seek medical care:
• New or changing skin lesions
• Fever with skin symptoms
• Recent travel to affected areas
• Known exposure to monkeypox

Emergency symptoms:
• Difficulty breathing
• High fever with confusion
• Severe dehydration
• Signs of infection

Always consult healthcare professionals
for proper medical evaluation.
"""
        
        self.dialog = MDDialog(
            title="Medical Information",
            text=content,
            buttons=[
                MDRaisedButton(
                    text="Close",
                    on_release=self.close_dialog
                ),
            ],
        )
        self.dialog.open()
    
    def show_emergency_contacts(self, instance):
        """Show emergency contact information"""
        content = """
🆘 EMERGENCY CONTACTS

🚨 Emergency Services: 911
(For severe, life-threatening symptoms)

🏥 CDC Monkeypox Hotline:
1-800-CDC-INFO (1-800-232-4636)

🩺 Local Health Department:
Search "[your city] health department"

💭 Crisis Text Line:
Text HOME to 741741

🔗 Official Resources:
• cdc.gov/poxvirus/monkeypox
• who.int/monkeypox

⚖️ Poison Control:
1-800-222-1222
"""
        
        self.dialog = MDDialog(
            title="Emergency Contacts",
            text=content,
            buttons=[
                MDRaisedButton(
                    text="Close",
                    on_release=self.close_dialog
                ),
            ],
        )
        self.dialog.open()
    
    def show_loading_dialog(self, message):
        """Show loading dialog"""
        self.dialog = MDDialog(
            title="Processing...",
            text=message,
        )
        self.dialog.open()
    
    def show_error_dialog(self, error_message):
        """Show error dialog"""
        self.dialog = MDDialog(
            title="Error",
            text=error_message,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=self.close_dialog
                ),
            ],
        )
        self.dialog.open()
    
    def close_dialog(self, instance):
        """Close current dialog"""
        if self.dialog:
            self.dialog.dismiss()
    
    def close_result_dialog(self, instance):
        """Close result dialog and return to main screen"""
        if self.dialog:
            self.dialog.dismiss()
    
    def save_result(self, instance):
        """Save analysis result"""
        # TODO: Implement result saving
        self.close_dialog(instance)

if __name__ == "__main__":
    MonkeypoxMobileApp().run()
