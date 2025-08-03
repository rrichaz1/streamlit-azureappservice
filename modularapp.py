import streamlit as st
from utils.state import sync_param_to_state
from utils.user import select_clinician
from components.sidebar_info import render_sidebar_info
from config.settings import app_config as AppConfig
from utils.blobaccess import BlobAccessUtil
from utils.logging_config import configure_logging

import os
import sys
from dotenv import load_dotenv

# Set up paths and environment
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
load_dotenv(override=True)

# Configure logging
configure_logging()

# Set Streamlit page config
st.set_page_config(
    page_title="Clinical Documentation AI Tools",
    page_icon="\U0001F3E5",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom sidebar CSS
st.markdown("""
<style>
section[data-testid="stSidebar"] > div {
    padding-top: 2rem;
    padding-left: 1rem;
    padding-right: 1rem;
}
div[data-baseweb="select"] {
    font-size: 0.95rem;
}
.st-emotion-cache-1kyxreq p {
    font-weight: 600;
    font-size: 0.95rem;
}
.css-1d391kg {
    width: 300px;
}
</style>
""", unsafe_allow_html=True)

# Load configuration and initialize shared utilities
storage_config = AppConfig.get_azure_storage_config()
blob_util = BlobAccessUtil(storage_config["connection_string"], storage_config["container_name"])

# Set shared session state
st.session_state.setdefault("app_config", AppConfig)
st.session_state.setdefault("blob_util", blob_util)
st.session_state.setdefault("environment", AppConfig.get_environment())

# Sync clinician_name from query param
sync_param_to_state("clinician_name", rerun=True)

# Sidebar: User selection + environment info
with st.sidebar:
    clinician_name = select_clinician()
    render_sidebar_info(storage_config)

# Define pages
from pages.assessment.overview import render_overview_page
from pages.assessment.metrics_saas import render_metrics_page as render_saas
from pages.assessment.metrics_opas import render_metrics_page as render_opas
from pages.assessment.assessment_viewer import render_feedback_page
from pages.summarization.overview import render_summary_overview_page
from pages.summarization.note_list import render_summary_list_page
from pages.summarization.note_detail import render_summary_detail_page

home = st.Page(lambda: st.title("Clinical Documentation AI Tools"), title="Home", icon="\U0001F3E0")

assessment_pages = [
    st.Page(render_overview_page, title="Overview", icon="\U0001F4CA")
]

if clinician_name:
    assessment_pages += [
        st.Page(render_saas, title="Saas Metrics List", icon="\U0001F4C1"),
        st.Page(render_opas, title="OPAS File List", icon="\U0001F4C8"),
        st.Page(render_feedback_page, title="Note", icon="\U0001F4AC")
    ]

summarization_pages = [
    st.Page(render_summary_overview_page, title="Dashboard", icon="\U0001F4CB"),
    st.Page(render_summary_list_page, title="Summarized Notes", icon="\U0001F4DD"),
    st.Page(render_summary_detail_page, title="Note Detail", icon="\U0001F50D")
]

# Navigation
pg = st.navigation({
    "Clinical AI Tools": [home],
    "Assessment Extraction": assessment_pages,
    "Summarization": summarization_pages
})
pg.run()
