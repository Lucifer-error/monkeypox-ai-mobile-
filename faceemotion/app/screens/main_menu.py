"""
Main Menu Screen
Landing page for the Monkeypox Classifier Application
"""

import streamlit as st

def show_main_menu():
    """Display the main menu screen"""
    st.title("🧠 Monkeypox Skin Lesion Classifier")
    
    # Welcome message
    st.markdown("""
    ### Welcome to the Monkeypox Classification System
    
    This application uses advanced deep learning to analyze skin lesion images 
    and classify them as either Monkeypox or Other skin conditions.
    
    ⚠️ **Important**: This tool provides preliminary screening and medical guidance 
    but is NOT a replacement for professional medical diagnosis.
    """)
    
    # Medical Disclaimer - Make it prominent
    st.error("""
    🏥 **MEDICAL DISCLAIMER**: This AI tool is for educational and screening purposes only. 
    Always consult qualified healthcare professionals for medical diagnosis and treatment. 
    If Monkeypox is detected, seek immediate medical attention and follow isolation protocols.
    """)
    
    # Features overview
    st.markdown("### 🚀 Features")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🔍 AI-Powered Analysis**
        - ResNet18 deep learning model
        - High accuracy classification
        - Real-time predictions
        """)
    
    with col2:
        st.markdown("""
        **💾 Data Collection**
        - Save classified images
        - Build training datasets
        - Improve model performance
        """)
    
    # Navigation buttons
    st.markdown("### 📋 Navigation")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔬 Analyze Image", use_container_width=True):
            st.session_state.page = "analyze"
            st.rerun()
    
    with col2:
        if st.button("📁 View Collections", use_container_width=True):
            st.session_state.page = "collections"
            st.rerun()
    
    with col3:
        if st.button("ℹ️ About", use_container_width=True):
            st.session_state.page = "about"
            st.rerun()
    
    # Model information
    st.markdown("---")
    st.markdown("### 🔧 Model Information")
    st.info("""
    **Model**: ResNet18 Architecture  
    **Classes**: Monkeypox, Others  
    **Input Size**: 224x224 pixels  
    **Performance**: Optimized for medical image classification
    """)
    
    # Instructions
    st.markdown("### 📖 How to Use")
    st.markdown("""
    1. **Click 'Analyze Image'** to start classifying skin lesions
    2. **Upload an image** (JPG, JPEG, PNG, WebP formats supported)
    3. **Review the prediction** and provide feedback
    4. **Save images** to build your collection for future training
    """)

def show_about():
    """Display about information"""
    st.title("ℹ️ About Monkeypox Classifier")
    
    st.markdown("""
    ### ⚠️ Important Disclaimer
    **This tool is for educational and research purposes only.** 
    It should not be used as a substitute for professional medical diagnosis. 
    Always consult with qualified healthcare professionals for medical advice.
    
    ### 🚨 If Monkeypox is Detected
    The application provides comprehensive medical guidance including:
    - **Immediate action steps** for patient safety
    - **Emergency contact information** and when to call 911
    - **Isolation protocols** to prevent transmission
    - **Medical evaluation process** and what to expect
    - **Contact tracing guidance** for public health
    - **Self-care instructions** during illness
    - **Legal and workplace considerations**
    
    ### 🔬 Technical Details
    - **Architecture**: ResNet18 Convolutional Neural Network
    - **Training Data**: Curated dataset of skin lesion images
    - **Preprocessing**: Image normalization and resizing
    - **Output**: Binary classification with confidence scores
    - **Medical Integration**: Evidence-based guidance protocols
    
    ### 🛠️ Development
    Built with:
    - **PyTorch**: Deep learning framework
    - **Streamlit**: Web application framework
    - **PIL**: Image processing
    - **ResNet18**: Pre-trained CNN architecture
    - **Medical Guidelines**: CDC and WHO protocols
    """)
    
    if st.button("🏠 Back to Home"):
        st.session_state.page = "main"
        st.rerun()

def show_collections():
    """Display collections management"""
    st.title("📁 Image Collections")
    
    st.markdown("""
    ### Saved Classifications
    View and manage your saved image classifications.
    """)
    
    # TODO: Add functionality to browse saved images
    st.info("Collections management feature coming soon!")
    
    if st.button("🏠 Back to Home"):
        st.session_state.page = "main"
        st.rerun()
