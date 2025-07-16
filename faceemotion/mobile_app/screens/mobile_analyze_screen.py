"""
Mobile Analyze Screen
Mobile-optimized image upload and classification interface
"""

import streamlit as st
from PIL import Image
import os
from datetime import datetime
import sys

# Add the parent directories to the path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from monkeypox_model.monkeypox_configuration import MonkeypoxModel
except ImportError:
    st.error("Could not import MonkeypoxModel. Please check the model configuration.")

def show_mobile_analyze_screen():
    """Display the mobile-optimized image analysis screen"""
    
    # Navigation
    if st.button("🏠 Back to Home", key="back_analyze"):
        st.session_state.page = "main"
        st.rerun()
    
    st.markdown("""
    <div class="pwa-header">
        <h1>🔬 AI Analysis</h1>
        <p>Upload skin lesion image for classification</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize model
    @st.cache_resource
    def load_model():
        """Load the monkeypox model"""
        try:
            model_path = os.path.join(
                os.path.dirname(__file__), 
                '..', '..', 
                'monkeypox_model', 
                'best_model.pth'
            )
            model = MonkeypoxModel()
            success = model.load_model(model_path)
            if success:
                return model
            else:
                return None
        except Exception as e:
            st.error(f"Error loading model: {e}")
            return None
    
    model = load_model()
    
    if model is None:
        st.error("❌ Failed to load the classification model. Please check the model file.")
        return
    
    # Mobile-optimized file uploader
    st.markdown("### 📱 Upload Image")
    
    # Camera option for mobile
    camera_photo = st.camera_input("📸 Take Photo with Camera")
    
    # File upload option
    uploaded_file = st.file_uploader(
        "📁 Or Choose from Gallery", 
        type=["jpg", "jpeg", "png", "webp"],
        help="Upload a clear image of the skin lesion"
    )
    
    # Process either camera or uploaded image
    image_source = camera_photo if camera_photo is not None else uploaded_file
    
    if image_source is not None:
        try:
            # Load and display image
            image = Image.open(image_source).convert("RGB")
            
            # Mobile-optimized image display
            st.markdown("#### 📷 Your Image")
            st.image(image, caption="Uploaded Image", use_container_width=True)
            
            # Analysis section
            st.markdown("#### 🤖 AI Analysis")
            
            # Make prediction
            with st.spinner("🔄 Analyzing image..."):
                try:
                    prediction_result = model.predict(image)
                    
                    predicted_class = prediction_result['predicted_class']
                    confidence = prediction_result['confidence']
                    probabilities = prediction_result['probabilities']
                    
                    # Mobile-optimized results display
                    if predicted_class == "Monkey Pox":
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #ff6b6b, #ff8787); 
                                    color: white; padding: 20px; border-radius: 15px; 
                                    text-align: center; margin: 10px 0;">
                            <h2>⚠️ POTENTIAL MONKEYPOX</h2>
                            <h3>Confidence: {confidence:.1%}</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        show_mobile_monkeypox_guidance(confidence)
                    else:
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #51cf66, #69db7c); 
                                    color: white; padding: 20px; border-radius: 15px; 
                                    text-align: center; margin: 10px 0;">
                            <h2>✅ NON-MONKEYPOX</h2>
                            <h3>Confidence: {confidence:.1%}</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        show_mobile_other_guidance()
                    
                    # Show probability breakdown
                    st.markdown("**📊 Detailed Probabilities:**")
                    for class_name, prob in probabilities.items():
                        st.progress(prob, text=f"{class_name}: {prob:.1%}")
                    
                except Exception as e:
                    st.error(f"Error during prediction: {e}")
                    return
            
            # Mobile feedback section
            st.markdown("---")
            st.markdown("### 💬 Feedback")
            
            # Simplified feedback for mobile
            feedback = st.radio(
                "Is this prediction accurate?", 
                ["Select an option", "✅ Yes, correct", "❌ No, incorrect"],
                help="Your feedback helps improve accuracy"
            )
            
            if feedback != "Select an option":
                if feedback == "❌ No, incorrect":
                    correct_class = st.selectbox(
                        "What is the correct classification?",
                        ("Monkey Pox", "Others"),
                        help="Please provide the correct classification"
                    )
                    save_class = correct_class
                    st.info(f"Thank you! Corrected to: **{correct_class}**")
                else:
                    save_class = predicted_class
                    st.success(f"Thank you for confirming: **{predicted_class}**")
                
                # Save button
                if st.button("💾 Save to Collection", key="save_mobile", use_container_width=True):
                    save_mobile_image(image, save_class, confidence)
        
        except Exception as e:
            st.error(f"Error processing image: {e}")

def show_mobile_monkeypox_guidance(confidence):
    """Display mobile-optimized guidance when Monkeypox is detected"""
    
    # Critical actions for mobile
    st.error("""
    🚨 **CRITICAL: SEEK MEDICAL ATTENTION IMMEDIATELY**
    This is NOT a diagnosis. Professional evaluation required.
    """)
    
    # Confidence level
    if confidence > 0.8:
        confidence_msg = "🔴 HIGH confidence - Urgent medical consultation needed"
    elif confidence > 0.6:
        confidence_msg = "🟡 MODERATE confidence - Medical evaluation recommended"
    else:
        confidence_msg = "🟠 LOW confidence - Consider medical consultation"
    
    st.warning(confidence_msg)
    
    # Emergency actions
    with st.expander("🚨 IMMEDIATE ACTIONS", expanded=True):
        st.markdown("""
        ### RIGHT NOW:
        1. **📞 Call your doctor** or health department
        2. **🏠 Isolate yourself** from others
        3. **🧤 Cover all lesions** with clothing/bandages
        4. **🧼 Wash hands frequently**
        
        ### ☎️ EMERGENCY CONTACTS:
        - **911** for severe symptoms
        - **1-800-CDC-INFO** for guidance
        - **Local Health Department**
        """)
    
    with st.expander("🏥 Medical Evaluation", expanded=False):
        st.markdown("""
        **What to expect:**
        - Physical examination of lesions
        - Sample collection for lab testing
        - Questions about exposure/travel
        - Contact tracing discussion
        
        **Bring to appointment:**
        - List of recent contacts
        - Travel history
        - This app screenshot
        """)
    
    with st.expander("🛡️ Prevent Spreading", expanded=False):
        st.markdown("""
        **Isolation rules:**
        - Stay away from others until healed
        - Use separate room/bathroom
        - Don't share items
        - Wear mask around others
        
        **Clean frequently:**
        - Hands with soap/sanitizer
        - Surfaces with disinfectant
        - Clothing/bedding separately
        """)

def show_mobile_other_guidance():
    """Display mobile-optimized guidance for non-monkeypox results"""
    
    st.success("""
    ✅ **Good News**: AI suggests this is likely NOT monkeypox.
    However, still consult a healthcare provider if concerned.
    """)
    
    with st.expander("🩺 General Skin Care", expanded=False):
        st.markdown("""
        **Still see a doctor if:**
        - Lesions are painful or spreading
        - You have fever or feel unwell
        - Recent travel to affected areas
        - Known exposure to monkeypox
        
        **General care:**
        - Keep area clean and dry
        - Avoid scratching
        - Monitor for changes
        """)

def save_mobile_image(image, save_class, confidence):
    """Save the analyzed image from mobile interface"""
    try:
        # Create timestamp
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Determine save directory
        base_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'app', 'collections')
        save_dir = os.path.join(base_dir, save_class)
        
        # Create directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)
        
        # Create filename with confidence score
        confidence_str = f"{confidence:.3f}".replace('.', '')
        filename = f"mobile_{save_class.replace(' ', '_')}_{now}_conf{confidence_str}.jpg"
        save_path = os.path.join(save_dir, filename)
        
        # Convert and save image for mobile
        if image.mode in ('RGBA', 'LA', 'P'):
            rgb_image = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            rgb_image.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
            image = rgb_image
        
        image.save(save_path, format='JPEG', quality=95)
        
        # Mobile-optimized success message
        st.success("✅ Image saved!")
        st.info(f"📁 Saved as: `{filename}`")
        
        # Show updated stats
        show_mobile_collection_stats()
        
    except Exception as e:
        st.error(f"❌ Error saving: {e}")

def show_mobile_collection_stats():
    """Display mobile-optimized collection statistics"""
    try:
        base_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'app', 'collections')
        
        monkey_pox_dir = os.path.join(base_dir, 'Monkey Pox')
        others_dir = os.path.join(base_dir, 'Others')
        
        monkey_pox_count = len([f for f in os.listdir(monkey_pox_dir) 
                               if f.endswith(('.jpg', '.jpeg', '.png', '.webp'))]) if os.path.exists(monkey_pox_dir) else 0
        others_count = len([f for f in os.listdir(others_dir) 
                           if f.endswith(('.jpg', '.jpeg', '.png', '.webp'))]) if os.path.exists(others_dir) else 0
        
        st.markdown("**📊 Your Collection:**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Monkeypox", monkey_pox_count)
        with col2:
            st.metric("Others", others_count)
        with col3:
            st.metric("Total", monkey_pox_count + others_count)
            
    except Exception as e:
        st.warning("Collection stats unavailable")
