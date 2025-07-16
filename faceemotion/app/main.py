"""
Main Application Entry Point
Monkeypox Skin Lesion Classifier
"""

import streamlit as st
import os
import sys

# Add the current directory to the path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import screen modules
from screens.main_menu import show_main_menu, show_about, show_collections
from screens.analyze_screen import show_analyze_screen

def main():
    """Main application function"""
    
    # Set page configuration
    st.set_page_config(
        page_title="Monkeypox Classifier",
        page_icon="🧠",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = "main"
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stButton > button {
        width: 100%;
        background-color: #ff6b6b;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #ff5252;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Page routing
    if st.session_state.page == "main":
        show_main_menu()
    elif st.session_state.page == "analyze":
        show_analyze_screen()
    elif st.session_state.page == "about":
        show_about()
    elif st.session_state.page == "collections":
        show_collections()
    else:
        # Default to main menu if unknown page
        st.session_state.page = "main"
        show_main_menu()

if __name__ == "__main__":
    main()
