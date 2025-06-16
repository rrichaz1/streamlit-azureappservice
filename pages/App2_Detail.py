"""
App 2: Document Summarizer - Document Detail View with Feedback
"""

import streamlit as st
import sys
import os
import json
from datetime import datetime

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from mock_data import generate_app2_documents, get_document_by_id

def main():
    st.set_page_config(
        page_title="Document Summarizer - Document Detail",
        page_icon="📄",
        layout="wide"
    )
    
    # Initialize session state for app2
    if 'app2_documents' not in st.session_state:
        st.session_state.app2_documents = generate_app2_documents()
    
    # Check if document ID is in session state
    if 'selected_doc_id' not in st.session_state:
        st.error("No document selected. Please go back to the document list.")
        if st.button("🔙 Back to Document List"):
            st.switch_page("pages/App2_Documents.py")
        return
    
    # Load the selected document
    documents_df = st.session_state.app2_documents
    selected_doc = get_document_by_id(documents_df, st.session_state.selected_doc_id)
    
    if selected_doc is None:
        st.error("Document not found.")
        if st.button("🔙 Back to Document List"):
            st.switch_page("pages/App2_Documents.py")
        return
    
    st.title("📄 Document Summarizer")
    st.markdown("### Document Summary & Analysis")
    
    # Navigation buttons
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🔙 Back to Document List", type="secondary"):
            st.switch_page("pages/App2_Documents.py")
    
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
        st.markdown("### 📊 Analysis Metrics")
        metrics = selected_doc['metrics']
        st.metric("Readability Score", f"{metrics['readability']}%")
        st.metric("Compression Ratio", f"{metrics['compression_ratio']:.1%}")
        st.metric("Key Concepts", metrics['key_concepts'])
    
    # Processed Information
    st.markdown("### 🔍 Document Analysis")
    processed_info = selected_doc['processed_info']
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Main Topics:**")
        for topic in processed_info['main_topics']:
            st.write(f"• {topic}")
        
        st.markdown("**Methodology:**")
        st.write(processed_info['methodology'])
        
    with col2:
        st.markdown("**Key Insights:**")
        for insight in processed_info['key_insights']:
            st.write(f"• {insight}")
    
    # Full content in expandable section
    with st.expander("📄 View Full Document Content"):
        st.write(selected_doc['full_content'])
    
    st.markdown("---")
    
    # User Feedback Section
    st.markdown("### 💬 Provide Feedback")
    st.markdown("Help us improve our document summarization by providing your feedback on this analysis.")
    
    # Feedback form
    with st.form("feedback_form_app2"):
        st.markdown("#### Rate the Summary Quality")
        
        # Radio button for summary helpfulness
        summary_helpful = st.radio(
            "Was the summary helpful and accurate?",
            options=["Yes", "No", "Partially"],
            index=None,
            help="Please evaluate if the AI-generated summary accurately captures the document's key information."
        )
        
        # Slider for accuracy rating
        accuracy_rating = st.slider(
            "On a scale of 1 to 5, how accurate was the processed information?",
            min_value=1,
            max_value=5,
            value=3,
            help="Rate the accuracy of the extracted topics, insights, and analysis."
        )
        
        # Text area for additional comments
        additional_comments = st.text_area(
            "Any additional comments or suggestions for improvement?",
            placeholder="Please share any specific feedback about the summary quality, missing information, or suggestions for improvement...",
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
                "app_type": "document_summarizer",
                "summary_helpful": summary_helpful,
                "accuracy_rating": accuracy_rating,
                "additional_comments": additional_comments,
                "email": email,
                "feedback_timestamp": datetime.now().isoformat(),
                "user_session": st.session_state.get('session_id', 'anonymous')
            }
            
            # Show success message
            st.success("✅ Thank you for your feedback! Your input helps us improve our document summarization.")
            
            # Display collected feedback (for demonstration)
            st.markdown("#### Feedback Summary:")
            st.json(feedback_data)
            
            # TODO: Database Integration
            st.info("""
            **Note for Production:** This feedback should be saved to a database.
            
            **Implementation Steps:**
            1. Set up Azure SQL Database or Azure Cosmos DB for feedback storage
            2. Create feedback table/collection with schema for document summarizer feedback
            3. Use Azure App Service Application Settings for secure database credentials
            4. Replace this demo display with actual database insertion logic
            5. Implement proper error handling and data validation
            6. Consider adding user authentication for better feedback tracking
            7. Add analytics dashboard for feedback monitoring
            
            **Security Considerations:**
            - Store database connection strings in Azure App Service Application Settings
            - Use managed identities where possible for Azure resource access
            - Implement input validation and sanitization
            - Add rate limiting for feedback submissions
            """)
    
    # Sidebar information
    with st.sidebar:
        st.header("📄 Document Info")
        st.write(f"**ID:** {selected_doc['id']}")
        st.write(f"**Category:** {selected_doc['category']}")
        st.write(f"**Processed:** {selected_doc['date_processed'].strftime('%Y-%m-%d')}")
        
        st.markdown("---")
        st.markdown("### 🎯 Analysis Metrics")
        metrics = selected_doc['metrics']
        st.progress(metrics['readability']/100, text=f"Readability: {metrics['readability']}%")
        st.progress(metrics['compression_ratio'], text=f"Compression: {metrics['compression_ratio']:.1%}")
        
        st.markdown("---")
        st.info("💡 Your feedback helps improve our AI summarization algorithms for better document analysis.")

if __name__ == "__main__":
    main()
