"""
App 1: Assessment/Plan Extractor - Document Detail View with Feedback
"""

import streamlit as st
import sys
import os
import json
from datetime import datetime

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from mock_data import generate_app1_documents, get_document_by_id

def main():
    st.set_page_config(
        page_title="Assessment/Plan Extractor - Document Detail",
        page_icon="📋",
        layout="wide"
    )
    
    # Initialize session state for app1
    if 'app1_documents' not in st.session_state:
        st.session_state.app1_documents = generate_app1_documents()
    
    # Check if document ID is in session state
    if 'selected_doc_id' not in st.session_state:
        st.error("No document selected. Please go back to the document list.")
        if st.button("🔙 Back to Document List"):
            st.switch_page("pages/App1_Documents.py")
        return
    
    # Load the selected document
    documents_df = st.session_state.app1_documents
    selected_doc = get_document_by_id(documents_df, st.session_state.selected_doc_id)
    
    if selected_doc is None:
        st.error("Document not found.")
        if st.button("🔙 Back to Document List"):
            st.switch_page("pages/App1_Documents.py")
        return
    
    st.title("📋 Assessment/Plan Extractor")
    st.markdown("### Document Detail View")
    
    # Navigation buttons
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🔙 Back to Document List", type="secondary"):
            st.switch_page("pages/App1_Documents.py")
    
    st.markdown("---")
    
    # Document information
    st.markdown(f"## {selected_doc['name']}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"**Category:** {selected_doc['category']}")
        st.markdown(f"**Processed:** {selected_doc['date_processed'].strftime('%Y-%m-%d %H:%M')}")
        
        # Highlighted summary
        st.markdown("### 📝 AI-Generated Summary")
        st.info(selected_doc['summary'])
        
    with col2:
        st.markdown("### 📊 Processing Metrics")
        metrics = selected_doc['metrics']
        st.metric("Accuracy", f"{metrics['accuracy']}%")
        st.metric("Confidence", f"{metrics['confidence']}%")
        st.metric("Processing Time", f"{metrics['processing_time']}s")
    
    # Processed Information
    st.markdown("### 🔍 Extracted Information")
    processed_info = selected_doc['processed_info']
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Assessment:**")
        st.write(processed_info['assessment'])
        
        st.markdown("**Treatment Plan:**")
        st.write(processed_info['plan'])
        
    with col2:
        st.markdown("**Key Findings:**")
        for finding in processed_info['key_findings']:
            st.write(f"• {finding}")
    
    # Full content in expandable section
    with st.expander("📄 View Full Document Content"):
        st.write(selected_doc['full_content'])
    
    st.markdown("---")
    
    # User Feedback Section
    st.markdown("### 💬 Provide Feedback")
    st.markdown("Help us improve our AI analysis by providing your feedback on this document processing.")
    
    # Feedback form
    with st.form("feedback_form"):
        st.markdown("#### Rate the Analysis Quality")
        
        # Radio button for summary helpfulness
        summary_helpful = st.radio(
            "Was the summary helpful and accurate?",
            options=["Yes", "No", "Partially"],
            index=None,
            help="Please evaluate if the AI-generated summary accurately captures the key information."
        )
        
        # Slider for accuracy rating
        accuracy_rating = st.slider(
            "On a scale of 1 to 5, how accurate was the processed information?",
            min_value=1,
            max_value=5,
            value=3,
            help="Rate the accuracy of the extracted assessment, plan, and key findings."
        )
        
        # Text area for additional comments
        additional_comments = st.text_area(
            "Any additional comments or suggestions for improvement?",
            placeholder="Please share any specific feedback about the analysis, missing information, or suggestions for improvement...",
            height=100
        )
        
        # Email input for follow-up
        email = st.text_input(
            "Optional: Enter your email if you'd like us to follow up",
            placeholder="your.email@example.com",
            help="We'll only use this to follow up on your feedback if needed."
        )
        
        # Submit button
        submitted = st.form_submit_button("Submit Feedback", type="primary")
        
        if submitted:
            # Collect feedback data
            feedback_data = {
                "document_id": selected_doc['id'],
                "document_name": selected_doc['name'],
                "summary_helpful": summary_helpful,
                "accuracy_rating": accuracy_rating,
                "additional_comments": additional_comments,
                "email": email,
                "feedback_timestamp": datetime.now().isoformat(),
                "user_session": st.session_state.get('session_id', 'anonymous')
            }
            
            # Show success message
            st.success("✅ Thank you for your feedback! Your input helps us improve our AI analysis.")
            
            # Display collected feedback (for demonstration)
            st.markdown("#### Feedback Summary:")
            st.json(feedback_data)
            
            # TODO: Database Integration
            st.info("""
            **Note for Production:** This feedback should be saved to a database.
            
            **Implementation Steps:**
            1. Set up Azure SQL Database or Azure Cosmos DB
            2. Create feedback table/collection with appropriate schema
            3. Use Azure App Service Application Settings for database connection strings
            4. Replace this demo display with actual database insertion
            5. Implement proper error handling and data validation
            6. Consider adding user authentication for better feedback tracking
            
            **Example Database Save Code:**
            ```python
            # Azure SQL Database example
            import pyodbc
            connection_string = os.environ.get('DATABASE_CONNECTION_STRING')
            
            # Azure Cosmos DB example  
            from azure.cosmos import CosmosClient
            cosmos_client = CosmosClient(os.environ.get('COSMOS_ENDPOINT'), 
                                       os.environ.get('COSMOS_KEY'))
            ```
            """)
    
    # Sidebar information
    with st.sidebar:
        st.header("📋 Document Info")
        st.write(f"**ID:** {selected_doc['id']}")
        st.write(f"**Category:** {selected_doc['category']}")
        st.write(f"**Processed:** {selected_doc['date_processed'].strftime('%Y-%m-%d')}")
        
        st.markdown("---")
        st.markdown("### 🎯 Analysis Metrics")
        metrics = selected_doc['metrics']
        st.progress(metrics['accuracy']/100, text=f"Accuracy: {metrics['accuracy']}%")
        st.progress(metrics['confidence']/100, text=f"Confidence: {metrics['confidence']}%")
        
        st.markdown("---")
        st.info("💡 Your feedback helps train our AI models to provide better analysis for healthcare professionals.")

if __name__ == "__main__":
    main()
