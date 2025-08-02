"""
Common helper functions for metrics pages (OPAS, SAAS, etc.)
"""
import streamlit as st
import pandas as pd
from utils.assmnt_plan import constants
from utils.assmnt_plan.utils_assmnt import get_metrics_df, read_metrics_file


# Constants
FILE_NAME_COL = "File_Name"
FILE_NAME_CLEAN_COL = "File_Name_Clean"
ALL_LEVELS = "All Levels"
ALL_TYPES = "All Types"
ALL_HOSPITALS = "All Hospitals"
ALL_TENANTS = "All Tenants"

# Display configuration constants
MAX_DISPLAYED_ROWS = 10
COLUMN_WIDTHS = [3, 1, 1, 1]  # For file display columns
DECIMAL_PLACES = 1


def get_common_labels():
    """Get common column labels for metrics display."""
    return {
        constants.ColumnNames.FILE_NAME_URL_COL: "Feedback",
        "TenantId": "Tenant",
        "AssessmentId": "Assessment",
        "Physician_Recommendation": "IP/OBS",
        "Note_Type": "Note Type",
        "Dates_Of_Service_Count_File": "Dates of Service Count",
        "Annotated_Date_Count_File": "Annotated Date Count",
        "LLM_Date_Count_File": "AI Extracted Date Count",
        "Total_Words_File": "Total Words",
        "Notes": "Hospital",
    }


def get_opas_specific_labels():
    """Get OPAS-specific column labels."""
    base_labels = get_common_labels()
    opas_labels = {
        "BLEU_Score_File": "BLEU Score",
        "Cosine_Similarity_File": "Cosine Similarity",
        "Rouge_Score_File": "Rouge Score",
        "Meteor_Score_File": "Meteor Score",
        "Cosine_Similarity_Date": "Date Cosine Similarity",
        "Rouge_Score_Date": "Date Rouge Score",
        "Meteor_Score_Date": "Date Meteor Score",
    }
    return {**base_labels, **opas_labels}


def get_saas_specific_labels():
    """Get SAAS-specific column labels."""
    base_labels = get_common_labels()
    saas_labels = {
        "BLEU_Score_File": "Similarity %",
    }
    return {**base_labels, **saas_labels}


def handle_clinician_change():
    """Callback function when clinician selection changes"""
    # No need to set a flag, we'll use a different approach
    pass


def select_clinician():
    """Create clinician selection dropdown and handle selection."""
    clinician_list = constants.ClinicianList.get_reviewers()
    viewer_list = constants.ClinicianList.get_viewers()
    
    # Combine lists with Viewer as the first option
    all_options = viewer_list + clinician_list
    
    # Get the previous selection from session state, but don't override if already set
    # This ensures persistence across page navigations
    if "clinician_name" not in st.session_state:
        st.session_state.clinician_name = viewer_list[0] if viewer_list else ""
    
    previous_selection = st.session_state.clinician_name
    
    # If the previous selection isn't in our options (should be rare), default to first
    if previous_selection not in all_options:
        default_index = 0
    else:
        default_index = all_options.index(previous_selection)

    # Create a smaller column for the selectbox
    col1, _ = st.columns([1, 2])  # First column is smaller (25% width)
    
    with col1:
        # Create the dropdown in the smaller column
        selection = st.selectbox(
            "**Select Your Name (Required for saving feedback)**",
            all_options,
            index=default_index,
            key="clinician_selector",  # Use a different key
            help="Viewers can browse assessments. Clinicians can provide feedback."
        )
    
    # # Update the session state manually
    # if selection != st.session_state.clinician_name:
    #     st.session_state.clinician_name = selection
    #     # Force cache invalidation for the dataframe
    #     st.cache_data.clear()
    #     # Rerun the app to apply changes
    #     st.rerun()
    # Update the session state manually
    if selection != st.session_state.clinician_name:
        # Store the new selection
        st.session_state.clinician_name = selection
        
        # Instead of clearing cache and rerunning, 
        # mark that data needs to be reloaded for this user
        if "metrics_data" in st.session_state:
            del st.session_state.metrics_data
        
        # Also clear any derived data that depends on clinician selection
        if "filtered_metrics" in st.session_state:
            del st.session_state.filtered_metrics
    
    # Debug output - should now show the correct selection
    st.write(f"Current selection: {selection}")
    
    return selection


def create_filters(df, use_hospital_filter=True):
    """Create filter controls and return selected values.
    
    Args:
        df: DataFrame to create filters for
        use_hospital_filter: If True, use hospital filter (Notes column), 
                           if False, use tenant filter (TenantId column)
    """
    st.subheader("Filter Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Filter by accuracy level
        selected_accuracy = st.selectbox(
            "Filter by similarity level",
            constants.Accuracy.get_all_levels() 
        )
    
    with col2:
        # Filter by note type
        note_type_list = sorted(df["Note_Type"].unique().tolist())
        note_type_list = [ALL_TYPES] + note_type_list
        selected_note_type = st.selectbox("Filter by Note Type", note_type_list)
    
    with col3:
        if use_hospital_filter:
            # Filter by hospital
            hospitals_list = sorted(df["Notes"].dropna().unique().astype(str).tolist())
            # Remove 'null' values if they exist
            hospitals_list = [h for h in hospitals_list if h.lower() != 'null']
            hospitals = [ALL_HOSPITALS] + hospitals_list
            selected_third_filter = st.selectbox("Filter by Hospital", hospitals)
        else:
            # Filter by tenant
            tenants_list = sorted(df["TenantId"].unique().astype(str).tolist())
            tenants = [ALL_TENANTS] + tenants_list
            selected_third_filter = st.selectbox("Filter by Tenant", tenants)
    
    return selected_accuracy, selected_note_type, selected_third_filter


def apply_filters(df, selected_accuracy, selected_note_type, selected_third_filter, use_hospital_filter=True):
    """Apply filters to the dataframe.
    
    Args:
        df: DataFrame to filter
        selected_accuracy: Selected accuracy level
        selected_note_type: Selected note type
        selected_third_filter: Selected hospital or tenant (depending on use_hospital_filter)
        use_hospital_filter: If True, filter by hospital (Notes column), 
                           if False, filter by tenant (TenantId column)
    """
    filtered_df = df.copy()
    
    if selected_accuracy != ALL_LEVELS:
        filtered_df = filtered_df[filtered_df["Accuracy"] == selected_accuracy]
    
    if selected_note_type != ALL_TYPES and "Note_Type" in df.columns:
        filtered_df = filtered_df[filtered_df["Note_Type"] == selected_note_type]
    
    if use_hospital_filter:
        if selected_third_filter != ALL_HOSPITALS and "Notes" in df.columns:
            filtered_df = filtered_df[filtered_df["Notes"].astype(str) == selected_third_filter]
    else:
        if selected_third_filter != ALL_TENANTS and "TenantId" in df.columns:
            filtered_df = filtered_df[filtered_df["TenantId"].astype(str) == selected_third_filter]
    
    return filtered_df


def get_display_columns():
    """Get the columns to display."""
    base_columns = [constants.ColumnNames.FILE_NAME_URL_COL]
    
    # Filter only existing columns
    display_columns = base_columns + list(constants.MetricsColumns.DISPLAY_COLUMNS)
    return display_columns


def create_column_config(labels, percent_columns=None):
    """Create column configuration for dataframe display."""
    if percent_columns is None:
        percent_columns = constants.MetricsColumns.PERCENT_COLUMNS
    
    column_config = {}
    column_order = labels.keys()  # Use labels keys for column order

    for col in column_order:
        # Pick a user-friendly label (fallback to raw name)
        nice_label = labels.get(col, col)

        if col == constants.ColumnNames.FILE_NAME_URL_COL:
            # Clickable link to your feedback page
            column_config[col] = st.column_config.LinkColumn(
                label=nice_label,
                width="small",
                display_text="Open Feedback"  # Display text for the link
            )

        elif col in percent_columns:
            # BLEU percent columns for SAAS
            column_config[col] = st.column_config.NumberColumn(
                label=nice_label,
                format=f"%.{DECIMAL_PLACES}f%%",
                width="small",
            )

        elif col in constants.MetricsColumns.NUMBER_COLUMNS:
            # Any other number columns
            column_config[col] = st.column_config.NumberColumn(
                label=nice_label,
                width="small"
            )

        else:
            # Everything else as plain text
            column_config[col] = st.column_config.TextColumn(
                label=nice_label,
                width="auto",
            )

    return column_config


def get_bleu_score_display(row):
    """Get formatted BLEU score for display."""
    if "BLEU_Score_File_Percent" in row:
        return f"{row['BLEU_Score_File_Percent']:.{DECIMAL_PLACES}f}%" if pd.notna(row['BLEU_Score_File_Percent']) else "N/A"
    return "N/A"


def render_metrics_summary(filtered_df, use_hospital_filter=True):
    """Render summary statistics for the filtered metrics.
    
    Args:
        filtered_df: DataFrame with applied filters
        use_hospital_filter: If True, show hospital count, if False, show tenant count
    """
    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
        return
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", len(filtered_df))
    
    with col2:
        if use_hospital_filter:
            if "Notes" in filtered_df.columns:
                unique_hospitals = filtered_df["Notes"].dropna().nunique()
                st.metric("Unique Hospitals", unique_hospitals)
        else:
            if "TenantId" in filtered_df.columns:
                unique_tenants = filtered_df["TenantId"].nunique()
                st.metric("Unique Tenants", unique_tenants)
    
    with col3:
        if "Note_Type" in filtered_df.columns:
            unique_note_types = filtered_df["Note_Type"].nunique()
            st.metric("Note Types", unique_note_types)
    
    with col4:
        if "BLEU_Score_File" in filtered_df.columns:
            avg_bleu = filtered_df["BLEU_Score_File"].mean()
            if pd.notna(avg_bleu):
                st.metric("Avg BLEU Score", f"{avg_bleu:.2f}")


# def load_and_prepare_data(source, version_key="current", clinician_name=None):
#     """Load and prepare metrics data for a specific source.
    
#     Args:
#         source (str or InputSource): The input source (OPAS/SAAS).
#         version_key (str, optional): The version key to use. Defaults to "current".
#         clinician_name (str, optional): The clinician name for feedback links. Defaults to None.
        
#     Returns:
#         pd.DataFrame: The prepared metrics dataframe.
#     """
#     from config.settings import InputSource
    
#     # Convert string source to InputSource enum if needed
#     if isinstance(source, str):
#         source = InputSource(source.lower())
    
#     # Get viewer list for passing to prepare_dataframe
#     viewer_list = constants.ClinicianList.get_viewers()
    
#     # Load metrics data using the factory method
#     df = get_metrics_df(clinician_name, viewer_list, source, version_key)
    
#     if df.empty:
#         st.error(f"Failed to load {source.value.upper()} metrics data. Please check the metrics file path.")
#         return None
    
#     return df

def load_and_prepare_data(source, version_key="current", clinician_name=None):
    """Load and prepare metrics data for a specific source using session state."""
    from config.settings import InputSource
    
    # Create cache key based on source, version, and clinician
    cache_key = f"metrics_data_{source}_{version_key}"
    
    # Check if we already have this data in session state
    if cache_key not in st.session_state:
        # Convert string source to InputSource enum if needed
        if isinstance(source, str):
            source = InputSource(source.lower())
        
        # Get viewer list for passing to prepare_dataframe
        viewer_list = constants.ClinicianList.get_viewers()
        
        # Load metrics data using the factory method
        df = get_metrics_df(clinician_name, viewer_list, source, version_key)
        
        if df.empty:
            st.error(f"Failed to load {source.value.upper()} metrics data. Please check the metrics file path.")
            return None
            
        # Store in session state for this user
        st.session_state[cache_key] = df
    
    # Return data from session state
    return st.session_state[cache_key]

def render_metrics_table(filtered_df, labels, percent_columns=None):
    """Render the metrics table with proper formatting."""
    # Get display columns and create dataframe
    display_columns = get_display_columns()
    
    # Filter display columns to only include those that exist in the dataframe
    existing_display_columns = [col for col in display_columns if col in filtered_df.columns]
    
    display_df = filtered_df[existing_display_columns].copy()
    display_df = display_df.where(pd.notnull(display_df), "")
    
    # Create column configuration and display dataframe
    column_config = create_column_config(labels, percent_columns)
    
    st.dataframe(
        display_df,
        use_container_width=True,
        column_config=column_config
    )



# Set up module logger
logger = logging.getLogger(__name__)

# Constants
FILE_NAME_COL = "File_Name"
FILE_NAME_CLEAN_COL = "File_Name_Clean"
ALL_LEVELS = "All Levels"
ALL_TYPES = "All Types"
ALL_TENANTS = "All Tenants"

# Display configuration constants
MAX_DISPLAYED_ROWS = 10
COLUMN_WIDTHS = [3, 1, 1, 1]  # For file display columns
DECIMAL_PLACES = 1


LABELS = {  
        constants.ColumnNames.FILE_NAME_URL_COL:             "Feedback",  
        "TenantId":                        "Tenant",  
        "AssessmentId":                    "Assessment",  
        "Physician_Recommendation":      "IP/OBS",  
        "Note_Type":                      "Note Type",  
        "Dates_Of_Service_Count_File":        "Dates of Service Count",  
        "Annotated_Date_Count_File":     "Annotated Date Count",  
        "LLM_Date_Count_File":  "AI Extracted Date Count",  
        "Total_Words_File": "Total Words",
        # if you want to show BLEU percent columns, label them too:  
        "BLEU_Score_File":       "Similarity %",  
        "Notes":       "Notes",  
    }  
  


def handle_clinician_change():
    """Callback function when clinician selection changes"""
    # No need to set a flag, we'll use a different approach
    pass

def select_clinician():
    """Create clinician selection dropdown and handle selection."""
    clinician_list = constants.ClinicianList.get_reviewers()
    viewer_list = constants.ClinicianList.get_viewers()
    
    # Combine lists with Viewer as the first option
    all_options = viewer_list + clinician_list
    
    # Get the previous selection from session state, but don't override if already set
    # This ensures persistence across page navigations
    if "clinician_name" not in st.session_state:
        st.session_state.clinician_name = viewer_list[0] if viewer_list else ""
    
    previous_selection = st.session_state.clinician_name
    # print(f"Previous clinician selection: {previous_selection}")
    # print(f"Available options: {all_options}")
    
    # If the previous selection isn't in our options (should be rare), default to first
    if previous_selection not in all_options:
        default_index = 0
    else:
        default_index = all_options.index(previous_selection)

     # Create a smaller column for the selectbox
    col1, _ = st.columns([1, 2])  # First column is smaller (25% width)
    
    with col1:
        # Create the dropdown in the smaller column
        selection = st.selectbox(
            "**Select Your Name (Required for saving feedback) **",
            all_options,
            index=default_index,
            key="clinician_selector",  # Use a different key
            help="Viewers can browse assessments. Clinicians can provide feedback."
  
        )
    
    # Update the session state manually
    if selection != st.session_state.clinician_name:
        st.session_state.clinician_name = selection
        # Force cache invalidation for the dataframe
        st.cache_data.clear()
        # Rerun the app to apply changes
        st.rerun()
    
    # Debug output - should now show the correct selection
    st.write(f"Current selection: {selection}")
    
    return selection

def create_filters(df):
    """Create filter controls and return selected values."""
    st.subheader("Filter Metrics")
    
    # Clinician selection is moved to a separate function
    
    col1, col2, col3 = st.columns(3)

    
    with col1:
        # Filter by accuracy level
        selected_accuracy = st.selectbox(
            "Filter by similarity level",
            constants.Accuracy.get_all_levels() 
        )
    
    with col2:
        # Filter by note type
        note_type_list = sorted(df["Note_Type"].unique().tolist())
        print("Note Type column check ", note_type_list)
        note_type_list = [ALL_TYPES] + note_type_list
        selected_note_type = st.selectbox("Filter by Note Type", note_type_list)
    
    with col3:
        # Filter by tenant
        tenants_list = sorted(df["TenantId"].unique().astype(str).tolist())
        print("Tenant column check ", tenants_list)
        tenants = [ALL_TENANTS] + tenants_list
        selected_tenant = st.selectbox("Filter by Tenant", tenants)
    
    return selected_accuracy, selected_note_type, selected_tenant

def apply_filters(df, selected_accuracy, selected_note_type, selected_tenant):
    """Apply filters to the dataframe."""
    filtered_df = df.copy()
    
    if selected_accuracy != ALL_LEVELS:
        filtered_df = filtered_df[filtered_df["Accuracy"] == selected_accuracy]
    
    if selected_note_type != ALL_TYPES and "Note_Type" in df.columns:
        filtered_df = filtered_df[filtered_df["Note_Type"] == selected_note_type]
    
    if selected_tenant != ALL_TENANTS and "TenantId" in df.columns:
        filtered_df = filtered_df[filtered_df["TenantId"].astype(str) == selected_tenant]
    
    return filtered_df
  

def get_display_columns():
    """Get the columns to display ."""
    base_columns = [constants.ColumnNames.FILE_NAME_URL_COL]
    
    # Filter only existing columns
    display_columns = base_columns + list(constants.MetricsColumns.DISPLAY_COLUMNS)
    return display_columns

def create_column_config():

    # Add number column configs for existing columns


    column_config = {}  
    column_order = LABELS.keys()  # Use LABELS keys for column order

    for col in column_order:  
        # pick a user-friendly label (fallback to raw name)  
        nice_label = LABELS.get(col, col)  

        if col == constants.ColumnNames.FILE_NAME_URL_COL:  
            # clickable link to your feedback page  
            column_config[col] = st.column_config.LinkColumn(  
                label=nice_label,      
                width="small",
                display_text = "Open Feedback"  # Display text for the link
            )  
  
        elif col in constants.MetricsColumns.PERCENT_COLUMNS:  
            # BLEU percent columns  
            column_config[col] = st.column_config.NumberColumn(  
                label=nice_label,  
                format=f"%.{DECIMAL_PLACES}f%%",  
                width="small",  
            )  
  
        elif col in constants.MetricsColumns.NUMBER_COLUMNS:  
            # any other number columns you declared  
            column_config[col] = st.column_config.NumberColumn(  
                label=nice_label,  
                width="small"  
            )  
  
        else:  
            # everything else as plain text  
            column_config[col] = st.column_config.TextColumn(  
                label=nice_label,  
                width="auto",  
            )  
  
    return column_config  


def get_bleu_score_display(row):
    """Get formatted BLEU score for display."""
    if "BLEU_Score_File_Percent" in row:
        return f"{row['BLEU_Score_File_Percent']:.{DECIMAL_PLACES}f}%" if pd.notna(row['BLEU_Score_File_Percent']) else "N/A"
    return "N/A"


def render_metrics_page():
    """Render the metrics list page with detailed metrics and filtering options."""
    st.header("Detailed Assessment Metrics")
    
    # Add clinician selection at the top of the page
    clinician_name = select_clinician()
    
    # Load metrics data - with source parameter
    from config.settings import InputSource
    source = st.session_state.get("selected_source", None)  # Get source from session state if available
    df = read_metrics_file(source=source)
    
    if df.empty:
        source_msg = f" for {source.value}" if source else ""
        st.error(f"Failed to load metrics data{source_msg}. Please check the metrics file path.")
        return
    
    # Get viewer list for passing to prepare_dataframe
    viewer_list = constants.ClinicianList.get_viewers()
    
    # Prepare dataframe with clinician parameter in links - pass clinician_name explicitly
    df = prepare_dataframe(df, clinician_name, viewer_list)
    if df is None:
        return
    
    # Create filters
    selected_accuracy, selected_note_type, selected_tenant = create_filters(df)
    # print("Selected filters:", selected_accuracy, selected_note_type, selected_tenant)
    
    # Apply filters
    filtered_df = apply_filters(df, selected_accuracy, selected_note_type, selected_tenant)
    
    # Sort the dataframe by TenantId and AssessmentId
    if "TenantId" in filtered_df.columns and "AssessmentId" in filtered_df.columns:
        filtered_df = filtered_df.sort_values(by=["TenantId", "AssessmentId"])
    
    # Display filtered metrics
    st.subheader(f"Assessment Metrics ({len(filtered_df)} records)")
    
    # Get display columns and create dataframe
    display_columns = get_display_columns()
    display_df = filtered_df[display_columns].copy()
    display_df = display_df.where(pd.notnull(display_df), "")
    
    # Create column configuration and display dataframe
    column_config = create_column_config()
    st.dataframe(
        display_df,
        use_container_width=True,
        column_config=column_config
    )    
