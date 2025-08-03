# components/sidebar_info.py
import streamlit as st
from config.settings import app_config as AppConfig

def render_sidebar_info(storage_config):
    st.markdown("### 📊 Dashboard Info")
    st.write(f"**Storage Account:** {storage_config['storage_account_name']}")
    st.write(f"**Container:** {storage_config['container_name']}")
    st.write(f"**Data File:** {storage_config['blob_name']}")
    st.write(f"**Environment:** {AppConfig.get_environment()}")
