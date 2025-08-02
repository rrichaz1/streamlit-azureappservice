# utils/user.py
import streamlit as st
import constants

def select_clinician():
    clinician_list = constants.ClinicianList.get_reviewers()
    viewer_list = constants.ClinicianList.get_viewers()
    all_options = viewer_list + clinician_list

    # Load from query params if not already set
    query_params = st.experimental_get_query_params()
    if "clinician_name" in query_params and not st.session_state.get("clinician_name"):
        st.session_state.clinician_name = query_params["clinician_name"][0]

    if "clinician_name" not in st.session_state or st.session_state.clinician_name not in all_options:
        st.session_state.clinician_name = viewer_list[0] if viewer_list else ""

    selection = st.selectbox(
        "**Select Your Name (Required for feedback and filtering)**",
        all_options,
        index=all_options.index(st.session_state.clinician_name),
        key="clinician_selector"
    )

    if selection != st.session_state.clinician_name:
        st.session_state.clinician_name = selection
        for key in ["metrics_data", "filtered_metrics"]:
            st.session_state.pop(key, None)

    return selection




# utils/user.py
def get_clinician_name():
    query_params = st.experimental_get_query_params()
    if "clinician_name" in query_params and not st.session_state.get("clinician_name"):
        st.session_state.clinician_name = query_params["clinician_name"][0]

    return st.session_state.get("clinician_name")

