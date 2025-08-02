import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Load environment variables first
load_dotenv(override=True)

# Import and initialize Pydantic-based configuration
from config.settings import app_config as AppConfig
from utils.blobaccess import BlobAccessUtil
from utils.logging_config import configure_logging

# Configure logging at the start of the application
configure_logging()

# Get Azure Storage configuration from Pydantic settings
storage_config = AppConfig.get_azure_storage_config()

# Initialize global blob utility instance
blob_util = BlobAccessUtil(
    storage_config["connection_string"], 
    storage_config["container_name"]
)

# Make configuration available globally
st.session_state.app_config = AppConfig
st.session_state.blob_util = blob_util

# Set default environment to the current detected environment
if "environment" not in st.session_state:
    st.session_state.environment = AppConfig.get_environment()

# Application configuration
st.set_page_config(
    page_title="Clinical Documentation AI Tools", 
    page_icon="🏥", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for shared data
if "selected_file" not in st.session_state:
    st.session_state.selected_file = None

if "selected_note" not in st.session_state:
    st.session_state.selected_note = None

if "clinician_name" not in st.session_state:
    st.session_state.clinician_name = None

if "confidence_level" not in st.session_state:
    st.session_state.confidence_level = None

if "tenant_assessment" not in st.session_state:
    st.session_state.tenant_assessment = None

# Make configuration and utilities available globally
if "app_config" not in st.session_state:
    st.session_state.app_config = AppConfig

if "blob_util" not in st.session_state:
    st.session_state.blob_util = blob_util

# Define page functions
def home_page():
    """Main landing page."""
    # Inject custom CSS for improved appearance
    st.markdown(
        """
        <style>
        /* Main background and card styling */
        .stApp {
            background-color: #f7f9fa;
        }
        
        /* Title styling */
        .st-emotion-cache-10trblm {
            font-size: 2.5rem;
            font-weight: 700;
            color: #2a3f5f;
            margin-bottom: 0.5em;
        }
        
        /* Markdown text styling */
        .stMarkdown p {
            font-size: 1.1rem;
            color: #444;
        }
        
        /* Button styling */
        .stButton > button {
            background-color: #1976d2;
            color: white;
            border-radius: 6px;
            padding: 0.5em 1.5em;
            font-size: 1.1rem;
            border: none;
            transition: background 0.2s;
        }
        .stButton > button:hover {
            background-color: #1565c0;
        }
        
        /* Divider styling */
        .st-emotion-cache-1avcm0n {
            border-top: 2px solid #e0e0e0;
            margin: 2em 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    st.title("Clinical Documentation AI Tools")

    # Environment switcher (for administrators and developers)
    with st.expander("⚙️ Environment Settings", expanded=False):
        st.write("These settings control where feedback data is stored")
        
        # Environment selection
        col1, col2 = st.columns([1, 3])
        with col1:
            selected_env = st.radio(
                "Select Environment:",
                options=["development", "production"],
                index=0 if st.session_state.environment == "development" else 1,
                key="env_selector"
            )
        with col2:
            st.info(
                f"**Current Environment: {selected_env.upper()}**\n\n"
                f"Feedback will be stored in {'development' if selected_env == 'development' else 'production'} "
                f"paths. This affects where user feedback is saved."
            )
        
        # Update session state if environment changed
        if selected_env != st.session_state.environment:
            st.session_state.environment = selected_env
            st.success(f"Environment switched to {selected_env.upper()}. Feedback will now be stored in {selected_env} paths.")

    # st.markdown("""
    # Welcome to the Clinical Documentation AI Tools suite.

    # - **Assessment Extraction**: Extract and review clinical assessment metrics from notes.
    # - **Summarization**: Summarize clinical notes for quick review.

    # Use the sidebar navigation to access the tools.
    # """)
    st.markdown("""

    Welcome to the Clinical Documentation AI Tools suite.

    - **Assessment Extraction**: Extract and review clinical assessment metrics from notes.
    
    ### Quick Start
    - [View Assessment Overview](assessment_overview) - Get started with assessment extraction
    - [Browse Saas File List](assessment_metrics_saas) - View all available clinical notes and metrics
    - [Browse OPAS File List](assessment_metrics_opas) - View all available clinical notes and metrics
                
   
    Use the sidebar navigation to access the tools.
    """)

    st.divider()
    st.markdown("**Clinical Documentation AI Tools** - Powering clinical documentation analysis")

def assessment_overview():
    """Assessment extraction overview page."""
    from pages.assessment.overview import render_overview_page
    render_overview_page()

def assessment_metrics_saas():
    """Assessment extraction metrics page."""
    from pages.assessment.metrics_saas import render_metrics_page
    render_metrics_page()

def assessment_metrics_opas():
    """Assessment extraction metrics page."""
    from pages.assessment.metrics_opas import render_metrics_page
    render_metrics_page()    

def assessment_feedback():
    """Assessment extraction feedback page."""
    from pages.assessment.assessment_viewer import render_feedback_page
    render_feedback_page()

def summary_overview():
    """Summarization overview page."""
    from pages.summarization.overview import render_summary_overview_page
    render_summary_overview_page()

def summary_list():
    """Summarization note list page."""
    from pages.summarization.note_list import render_summary_list_page
    render_summary_list_page()

def summary_detail():
    """Summarization note detail page."""
    from pages.summarization.note_detail import render_summary_detail_page
    render_summary_detail_page()

from utils.user import select_clinician

# Show the dropdown in sidebar
with st.sidebar:
    clinician_name = select_clinician()

# Define pages using st.Page
home = st.Page(home_page, title="Home", icon="🏠")

# Always show Overview
assessment_pages = [
    st.Page(assessment_overview, title="Overview", icon="📊"),
]

# ⬅️ Conditionally add the rest only if a user is selected
if clinician_name:
    assessment_pages += [
        st.Page(assessment_metrics_saas, title="Saas Metrics List", icon="📁"),
        st.Page(assessment_metrics_opas, title="OPAS File List", icon="📈"),
        st.Page(assessment_feedback, title="Note", icon="💬"),
    ]

# Summarization pages stay as-is
summarization_pages = [
    st.Page(summary_overview, title="Dashboard", icon="📋"),
    st.Page(summary_list, title="Summarized Notes", icon="📝"),
    st.Page(summary_detail, title="Note Detail", icon="🔍"),
]

# Create navigation structure
pg = st.navigation({
    "Clinical AI Tools": [home],
    "Assessment Extraction": assessment_pages,
    "Summarization": summarization_pages
})

# Run selected page
pg.run()
