"""
Mobile Main Menu Screen
Mobile-optimized landing page for the Monkeypox Classifier Application
"""

import streamlit as st

def show_mobile_main_menu():
    """Display the mobile-optimized main menu screen"""
    
    # PWA-style header
    st.markdown("""
    <div class="pwa-header">
        <h1>🧠 Monkeypox AI</h1>
        <p>AI-Powered Skin Lesion Classifier</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Critical medical disclaimer for mobile
    st.error("""
    🚨 **MEDICAL ALERT**: This AI tool is for screening only. 
    NOT a medical diagnosis. Always consult healthcare professionals.
    """)
    
    # Quick stats or welcome message
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 20px; border-radius: 15px; 
                text-align: center; margin: 20px 0;">
        <h3>🔬 Advanced AI Classification</h3>
        <p>ResNet18 Neural Network • Real-time Analysis</p>
        <p>Supports JPG, PNG, WebP formats</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main action buttons - mobile optimized
    st.markdown("### 📱 Quick Actions")
    
    # Primary action - analyze image
    if st.button("📸 ANALYZE SKIN LESION", key="analyze_main"):
        st.session_state.page = "analyze"
        st.rerun()
    
    # Secondary actions in columns for mobile
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("ℹ️ About", key="about_main"):
            st.session_state.page = "about"
            st.rerun()
    
    with col2:
        if st.button("📊 Stats", key="stats_main"):
            show_quick_stats()
    
    # Quick instructions for mobile users
    st.markdown("---")
    st.markdown("### 📖 Quick Guide")
    
    with st.expander("🚀 How to Use", expanded=False):
        st.markdown("""
        1. **Tap 'Analyze Skin Lesion'** 📸
        2. **Upload photo** from camera or gallery 📱
        3. **Get AI analysis** in seconds ⚡
        4. **Follow medical guidance** 🏥
        5. **Save results** for records 💾
        """)
    
    with st.expander("⚠️ When to Seek Medical Care", expanded=False):
        st.markdown("""
        **Seek immediate medical attention if:**
        - New or changing skin lesions 🔍
        - Fever with skin symptoms 🌡️
        - Recent travel to affected areas ✈️
        - Known exposure to monkeypox 👥
        - Any concerning symptoms 🚨
        """)
    
    # Emergency contacts for mobile
    st.markdown("---")
    st.markdown("### 🆘 Emergency Resources")
    
    emergency_col1, emergency_col2 = st.columns(2)
    
    with emergency_col1:
        st.markdown("""
        **🚨 Emergency: 911**
        
        **🏥 CDC Hotline:**
        1-800-CDC-INFO
        """)
    
    with emergency_col2:
        st.markdown("""
        **🩺 Health Dept:**
        Search local services
        
        **💭 Crisis Support:**
        Text HOME to 741741
        """)

def show_mobile_about():
    """Display mobile-optimized about information"""
    
    # Navigation
    if st.button("🏠 Back to Home", key="back_about"):
        st.session_state.page = "main"
        st.rerun()
    
    st.markdown("""
    <div class="pwa-header">
        <h1>ℹ️ About Monkeypox AI</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎯 Purpose")
    st.info("""
    This mobile app provides AI-powered preliminary screening for monkeypox 
    skin lesions using advanced deep learning technology.
    """)
    
    with st.expander("🤖 AI Technology", expanded=False):
        st.markdown("""
        - **Model**: ResNet18 Convolutional Neural Network
        - **Training**: Curated medical image dataset
        - **Accuracy**: Optimized for medical screening
        - **Speed**: Real-time mobile processing
        """)
    
    with st.expander("🚨 Medical Guidance Features", expanded=False):
        st.markdown("""
        - **Emergency protocols** and contact information
        - **Isolation guidelines** to prevent transmission  
        - **Medical evaluation** process guidance
        - **Contact tracing** instructions
        - **Self-care** recommendations
        - **Legal and workplace** considerations
        """)
    
    with st.expander("📱 Mobile Features", expanded=False):
        st.markdown("""
        - **Touch-optimized** interface
        - **Camera integration** for photo capture
        - **Offline-capable** PWA design
        - **Responsive** layout for all screen sizes
        - **Fast processing** on mobile devices
        """)
    
    st.error("""
    ⚠️ **IMPORTANT DISCLAIMER**
    
    This app is for educational and preliminary screening only. 
    It does NOT provide medical diagnosis. Always consult qualified 
    healthcare professionals for medical advice and treatment.
    """)

def show_quick_stats():
    """Show quick statistics in a mobile-friendly format"""
    
    st.markdown("### 📊 Quick Stats")
    
    try:
        # Try to get collection stats
        import os
        base_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'app', 'collections')
        
        monkey_pox_dir = os.path.join(base_dir, 'Monkey Pox')
        others_dir = os.path.join(base_dir, 'Others')
        
        monkey_pox_count = len([f for f in os.listdir(monkey_pox_dir) 
                               if f.endswith(('.jpg', '.jpeg', '.png', '.webp'))]) if os.path.exists(monkey_pox_dir) else 0
        others_count = len([f for f in os.listdir(others_dir) 
                           if f.endswith(('.jpg', '.jpeg', '.png', '.webp'))]) if os.path.exists(others_dir) else 0
        
        # Mobile-optimized metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-container">
                <h3>{monkey_pox_count}</h3>
                <p>Monkeypox</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-container">
                <h3>{others_count}</h3>
                <p>Others</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-container">
                <h3>{monkey_pox_count + others_count}</h3>
                <p>Total</p>
            </div>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        st.info("Collection statistics will be available after analyzing images.")
