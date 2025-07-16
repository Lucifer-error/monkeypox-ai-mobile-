"""
Analyze Screen
Image upload and classification interface
"""

import streamlit as st
from PIL import Image
import os
from datetime import datetime
import sys

# Add the parent directory to the path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from monkeypox_model.monkeypox_configuration import MonkeypoxModel
except ImportError:
    st.error("Could not import MonkeypoxModel. Please check the model configuration.")

def show_analyze_screen():
    """Display the image analysis screen"""
    st.title("🔬 Monkeypox Image Analysis")
    
    # Navigation
    if st.button("🏠 Back to Home"):
        st.session_state.page = "main"
        st.rerun()
    
    st.markdown("---")
    
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
    
    # File uploader
    st.markdown("### 📤 Upload Image")
    uploaded_file = st.file_uploader(
        "Choose a skin lesion image for analysis", 
        type=["jpg", "jpeg", "png", "webp"],
        help="Upload a clear image of the skin lesion for classification (JPG, JPEG, PNG, WebP formats supported)"
    )
    
    if uploaded_file is not None:
        try:
            # Load and display image
            image = Image.open(uploaded_file).convert("RGB")
            
            # Display image in columns for better layout
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### 📷 Uploaded Image")
                st.image(image, caption="Original Image", use_container_width=True)
            
            with col2:
                st.markdown("#### 🔍 Analysis Results")
                
                # Make prediction
                with st.spinner("🤖 Analyzing image..."):
                    try:
                        prediction_result = model.predict(image)
                        
                        predicted_class = prediction_result['predicted_class']
                        confidence = prediction_result['confidence']
                        probabilities = prediction_result['probabilities']
                        
                        # Display results
                        if predicted_class == "Monkey Pox":
                            st.error(f"⚠️ **Predicted Class**: {predicted_class}")
                            show_monkeypox_guidance(confidence)
                        else:
                            st.success(f"✅ **Predicted Class**: {predicted_class}")
                            show_other_condition_guidance()
                        
                        st.metric("Confidence Score", f"{confidence:.2%}")
                        
                        # Show probability breakdown
                        st.markdown("**Class Probabilities:**")
                        for class_name, prob in probabilities.items():
                            st.progress(prob, text=f"{class_name}: {prob:.2%}")
                        
                    except Exception as e:
                        st.error(f"Error during prediction: {e}")
                        return
            
            # User feedback section
            st.markdown("---")
            st.markdown("### 💬 Feedback & Data Collection")
            
            # User confirmation
            confirm = st.radio(
                "Is this prediction correct?", 
                ("Please select", "Yes, correct", "No, incorrect"),
                help="Your feedback helps improve the model accuracy"
            )
            
            if confirm != "Please select":
                col1, col2 = st.columns(2)
                
                with col1:
                    if confirm == "No, incorrect":
                        st.markdown("**What is the correct classification?**")
                        correct_class = st.selectbox(
                            "Select the correct class:",
                            ("Monkey Pox", "Others"),
                            help="Please provide the correct classification"
                        )
                        save_class = correct_class
                    else:
                        save_class = predicted_class
                        st.success(f"Thank you for confirming: **{predicted_class}**")
                
                with col2:
                    st.markdown("**Save to Collection**")
                    if st.button("💾 Save Image to Collection", use_container_width=True):
                        save_image_to_collection(image, save_class, confidence)
        
        except Exception as e:
            st.error(f"Error processing image: {e}")

def save_image_to_collection(image, save_class, confidence):
    """Save the analyzed image to the appropriate collection folder"""
    try:
        # Create timestamp
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Determine save directory
        base_dir = os.path.join(os.path.dirname(__file__), '..', 'collections')
        save_dir = os.path.join(base_dir, save_class)
        
        # Create directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)
        
        # Create filename with confidence score
        confidence_str = f"{confidence:.3f}".replace('.', '')
        filename = f"{save_class.replace(' ', '_')}_{now}_conf{confidence_str}.jpg"
        save_path = os.path.join(save_dir, filename)
        
        # Save image
        # Convert to RGB if needed (WebP might have RGBA channels)
        if image.mode in ('RGBA', 'LA', 'P'):
            rgb_image = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            rgb_image.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
            image = rgb_image
        
        image.save(save_path, format='JPEG', quality=95)
        
        # Show success message
        st.success(f"✅ Image saved successfully!")
        st.info(f"📁 Saved to: `{save_path}`")
        
        # Show collection stats
        show_collection_stats()
        
    except Exception as e:
        st.error(f"❌ Error saving image: {e}")

def show_collection_stats():
    """Display current collection statistics"""
    try:
        base_dir = os.path.join(os.path.dirname(__file__), '..', 'collections')
        
        monkey_pox_dir = os.path.join(base_dir, 'Monkey Pox')
        others_dir = os.path.join(base_dir, 'Others')
        
        monkey_pox_count = len([f for f in os.listdir(monkey_pox_dir) if f.endswith(('.jpg', '.jpeg', '.png', '.webp'))]) if os.path.exists(monkey_pox_dir) else 0
        others_count = len([f for f in os.listdir(others_dir) if f.endswith(('.jpg', '.jpeg', '.png', '.webp'))]) if os.path.exists(others_dir) else 0
        
        st.markdown("**📊 Collection Statistics:**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Monkey Pox", monkey_pox_count)
        with col2:
            st.metric("Others", others_count)
        with col3:
            st.metric("Total", monkey_pox_count + others_count)
            
    except Exception as e:
        st.warning(f"Could not load collection stats: {e}")

def show_monkeypox_guidance(confidence):
    """Display guidance and instructions when Monkeypox is detected"""
    
    # Confidence-based messaging
    if confidence > 0.8:
        confidence_level = "High"
        urgency_color = "🔴"
    elif confidence > 0.6:
        confidence_level = "Moderate"
        urgency_color = "🟡"
    else:
        confidence_level = "Low"
        urgency_color = "🟠"
    
    st.markdown(f"""
    ### {urgency_color} **POTENTIAL MONKEYPOX DETECTION**
    **Confidence Level**: {confidence_level} ({confidence:.1%})
    """)
    
    # Critical Warning
    st.error("""
    ⚠️ **IMPORTANT MEDICAL DISCLAIMER**
    This is an AI screening tool and NOT a medical diagnosis. 
    Immediate medical consultation is required for proper evaluation.
    """)
    
    # Immediate Actions
    with st.expander("🚨 **IMMEDIATE ACTIONS REQUIRED**", expanded=True):
        st.markdown("""
        ### 1. **Seek Medical Attention Immediately**
        - Contact your healthcare provider or local health department
        - Visit an urgent care center or emergency room if severe symptoms
        - Call ahead to inform them of potential monkeypox exposure
        
        ### 2. **Isolate Yourself**
        - Stay away from others, including family members
        - Use a separate room and bathroom if possible
        - Avoid physical contact with people and animals
        - Do not share clothing, bedding, or personal items
        
        ### 3. **Cover the Lesions**
        - Keep all lesions covered with clothing or bandages
        - Wash hands frequently with soap and water
        - Use alcohol-based hand sanitizer
        """)
    
    # Medical Contact Information
    with st.expander("📞 **EMERGENCY CONTACTS**"):
        st.markdown("""
        ### **When to Call Emergency Services (911)**
        - Difficulty breathing or severe respiratory symptoms
        - High fever with confusion or altered mental state
        - Severe dehydration or inability to keep fluids down
        - Signs of secondary bacterial infection
        
        ### **Healthcare Provider Information**
        - **Primary Care Doctor**: Contact within 24 hours
        - **Local Health Department**: Report suspected case
        - **CDC Monkeypox Hotline**: 1-800-CDC-INFO (1-800-232-4636)
        - **Poison Control**: 1-800-222-1222 (for treatment questions)
        """)
    
    # Detailed Medical Guidance
    with st.expander("🏥 **MEDICAL GUIDANCE & NEXT STEPS**"):
        st.markdown("""
        ### **What to Expect at Medical Evaluation**
        1. **Physical Examination**: Doctor will examine all lesions
        2. **Sample Collection**: Swab from lesions for laboratory testing
        3. **Medical History**: Questions about recent travel, contacts, exposure
        4. **Contact Tracing**: Identifying people you may have exposed
        
        ### **Possible Medical Tests**
        - **PCR Test**: Most accurate test for monkeypox confirmation
        - **Blood Tests**: To check immune system response
        - **Bacterial Culture**: If secondary infection suspected
        
        ### **Treatment Options**
        - **Antiviral Medications**: TPOXX (tecovirimat) may be prescribed
        - **Pain Management**: For lesion discomfort
        - **Symptomatic Care**: Fever reducers, hydration support
        - **Wound Care**: Proper lesion management
        """)
    
    # Prevention and Care
    with st.expander("🛡️ **PREVENTION & SELF-CARE**"):
        st.markdown("""
        ### **Prevent Spreading to Others**
        - **Isolation Period**: Until all lesions have healed completely
        - **Mask Wearing**: Use N95 or KN95 mask around others
        - **Hand Hygiene**: Wash hands after touching lesions
        - **Disinfection**: Clean surfaces with EPA-approved disinfectants
        
        ### **Self-Care During Illness**
        - **Stay Hydrated**: Drink plenty of fluids
        - **Rest**: Get adequate sleep to support immune system
        - **Nutrition**: Eat nutritious foods to maintain strength
        - **Monitor Symptoms**: Track temperature and lesion progression
        
        ### **Lesion Care**
        - Keep lesions clean and dry
        - Avoid scratching or picking at lesions
        - Use loose, breathable clothing
        - Apply cool, damp cloths for comfort
        """)
    
    # Contact Tracing
    with st.expander("👥 **CONTACT TRACING INFORMATION**"):
        st.markdown("""
        ### **People to Notify Immediately**
        - **Close Contacts**: Anyone you've had skin-to-skin contact with
        - **Household Members**: People living in your home
        - **Intimate Partners**: Sexual or romantic partners
        - **Healthcare Workers**: Who provided care without proper PPE
        
        ### **Exposure Timeline**
        - **Infectious Period**: From symptom onset until all lesions heal
        - **High-Risk Exposure**: Direct contact with lesions or body fluids
        - **Moderate Risk**: Close contact within 6 feet for >3 hours
        
        ### **Information to Provide**
        - Date and nature of contact
        - Duration of exposure
        - Whether proper precautions were taken
        """)
    
    # Resources
    with st.expander("📚 **ADDITIONAL RESOURCES**"):
        st.markdown("""
        ### **Official Health Resources**
        - **CDC Monkeypox Information**: cdc.gov/poxvirus/monkeypox
        - **WHO Monkeypox Fact Sheet**: who.int/monkeypox
        - **Local Health Department**: Search "[your city] health department"
        
        ### **Support and Information**
        - **Mental Health Support**: Crisis Text Line: Text HOME to 741741
        - **Financial Assistance**: Contact local social services
        - **Workplace Rights**: Know your rights regarding sick leave
        
        ### **Stay Updated**
        - Follow official health department updates
        - Monitor CDC guidelines for latest information
        - Sign up for local health alerts
        """)
    
    # Legal and Social Considerations
    with st.expander("⚖️ **LEGAL & SOCIAL CONSIDERATIONS**"):
        st.markdown("""
        ### **Reporting Requirements**
        - Monkeypox is a **notifiable disease** in most jurisdictions
        - Healthcare providers are required to report confirmed cases
        - Cooperation with public health investigations is important
        
        ### **Workplace Considerations**
        - Inform employer about need for isolation
        - Request work-from-home accommodations if possible
        - Know your rights under FMLA and ADA
        
        ### **Privacy Rights**
        - Medical information is protected under HIPAA
        - Contact tracing maintains confidentiality
        - You have the right to refuse certain treatments
        """)

def show_other_condition_guidance():
    """Display guidance when other skin condition is detected"""
    
    st.markdown("""
    ### ✅ **Non-Monkeypox Classification**
    The AI analysis suggests this lesion is likely **not monkeypox**.
    """)
    
    with st.expander("🩺 **GENERAL SKIN HEALTH GUIDANCE**"):
        st.markdown("""
        ### **Still Consult a Healthcare Provider If:**
        - Lesions are painful, itchy, or spreading
        - You have fever or other systemic symptoms
        - The condition doesn't improve within a few days
        - You're concerned about the appearance
        
        ### **General Skin Care**
        - Keep the area clean and dry
        - Avoid scratching or picking
        - Use gentle, fragrance-free products
        - Protect from sun exposure
        
        ### **Monitor for Changes**
        - Size, color, or texture changes
        - Development of new lesions
        - Signs of infection (pus, increased redness, warmth)
        """)
    
    with st.expander("📞 **When to Seek Medical Care**"):
        st.markdown("""
        ### **See a Healthcare Provider If:**
        - Lesions persist longer than 2 weeks
        - Signs of bacterial infection develop
        - You have compromised immune system
        - Recent travel to monkeypox-affected areas
        - Known exposure to monkeypox cases
        
        ### **Emergency Care If:**
        - Severe pain or rapid spreading
        - High fever with skin lesions
        - Signs of systemic illness
        """)
