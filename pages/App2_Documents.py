"""
App 2: Document Summarizer - Document List View
"""

import streamlit as st
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from mock_data import generate_app2_documents
from config import AppConfig

def main():
    st.set_page_config(
        page_title="Document Summarizer - Documents",
        page_icon="📄",
        layout="wide"
    )
    
    # Initialize session state for app2
    if 'app2_documents' not in st.session_state:
        st.session_state.app2_documents = generate_app2_documents()
    
    st.title("📄 Document Summarizer")
    st.markdown("### Document List")
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("🏠 Back to Portal", type="secondary"):
            st.switch_page("Home.py")
    
    st.markdown("---")
    
    # Load documents
    documents_df = st.session_state.app2_documents
    
    # Display document categories
    categories = documents_df['category'].unique()
    selected_category = st.selectbox("Filter by Category:", ["All Categories"] + list(categories))
    
    # Filter documents if category is selected
    if selected_category != "All Categories":
        filtered_docs = documents_df[documents_df['category'] == selected_category]
    else:
        filtered_docs = documents_df
    
    st.markdown(f"**Showing {len(filtered_docs)} documents**")
    
    # Display documents in a grid layout
    for idx, row in filtered_docs.iterrows():
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"**{row['name']}**")
                st.write(f"📁 {row['category']}")
                st.write(f"📝 {row['summary'][:100]}...")
                
            with col2:
                # Display metrics
                st.metric("Readability", f"{row['metrics']['readability']}%")
                st.metric("Compression", f"{row['metrics']['compression_ratio']:.1%}")
                
            with col3:
                st.write("")  # Spacing
                if st.button(f"View Summary", key=f"view_{row['id']}", type="primary"):
                    st.session_state.selected_doc_id = row['id']
                    st.switch_page("pages/App2_Detail.py")
                
                # Show processing date
                st.caption(f"Processed: {row['date_processed'].strftime('%Y-%m-%d')}")
        
        st.markdown("---")
    
    # Sidebar information
    with st.sidebar:
        st.header("📊 App 2 Statistics")
        
        total_docs = len(documents_df)
        avg_readability = documents_df['metrics'].apply(lambda x: x['readability']).mean()
        avg_compression = documents_df['metrics'].apply(lambda x: x['compression_ratio']).mean()
        
        st.metric("Total Documents", total_docs)
        st.metric("Avg Readability", f"{avg_readability:.1f}%")
        st.metric("Avg Compression", f"{avg_compression:.1%}")
        
        st.markdown("---")
        st.markdown("### Categories")
        for category in categories:
            count = len(documents_df[documents_df['category'] == category])
            st.write(f"• {category}: {count}")
        
        st.markdown("---")
        st.info("💡 Click 'View Summary' to see the full document summary and provide feedback.")

if __name__ == "__main__":
    main()
