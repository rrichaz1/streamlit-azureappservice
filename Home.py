"""
Main Portal/Router for Multi-App Streamlit Deployment
This serves as the entry point for users to select between different applications.
"""

import streamlit as st
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from config import AppConfig

def main():
    st.set_page_config(
        page_title="Document Management Portal",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Get app configuration
    app_config = AppConfig.get_app_config()
    
    st.title("🏠 Document Management Portal")
    st.markdown("---")
    
    st.markdown("""
    ### Welcome to the Document Management System
    
    Choose from the applications below to get started:
    """)
    
    # Create two columns for the app selection
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 📋 App 1: Assessment/Plan Extractor
        Extract and analyze assessment plans from documents with AI-powered processing.
        """)
        
        if st.button("🚀 Launch Assessment Extractor", type="primary", use_container_width=True):
            st.session_state['selected_app'] = 'app1'
            st.switch_page("pages/App1_Documents.py")
    
    with col2:
        st.markdown("""
        #### 📄 App 2: Document Summarizer
        Automatically generate intelligent summaries from uploaded documents.
        """)
        
        if st.button("📊 Launch Document Summarizer", type="primary", use_container_width=True):
            st.session_state['selected_app'] = 'app2'
            st.switch_page("pages/App2_Documents.py")
    
    # Sidebar information
    with st.sidebar:
        st.header("ℹ️ Portal Information")
        st.write(f"**Environment:** {AppConfig.get_environment()}")
        st.write("**Version:** 1.0.0")
        
        st.markdown("---")
        st.markdown("### 🔧 Current Features")
        st.markdown("""
        - Multi-application architecture
        - Document management workflows
        - User feedback collection
        - Azure cloud integration
        """)
        
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <small>Powered by Streamlit • Deployed on Azure App Service</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
