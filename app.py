import streamlit as st
import pandas as pd
from blob_storage import create_blob_manager
from config import AppConfig

# Get configuration
config = AppConfig.get_azure_storage_config()
app_config = AppConfig.get_app_config()

# Initialize blob storage manager
blob_manager = create_blob_manager(
    config["storage_account_name"], 
    config["container_name"]
)

@st.cache_data
def load_data_from_blob():
    """Load CSV data from Azure Blob Storage"""
    try:
        df = blob_manager.download_csv_as_dataframe(config["blob_name"])
        return df
    except Exception as e:
        st.error(f"Error loading data from blob storage: {str(e)}")
        return None

def main():
    st.title(app_config["title"])
    st.write(app_config["description"])
    
    # Sidebar for additional info
    with st.sidebar:
        st.header("📊 Dashboard Info")
        st.write(f"**Storage Account:** {config['storage_account_name']}")
        st.write(f"**Container:** {config['container_name']}")
        st.write(f"**Data File:** {config['blob_name']}")
        st.write(f"**Environment:** {AppConfig.get_environment()}")
        
        # Check blob availability
        try:
            if blob_manager.check_blob_exists(config["blob_name"]):
                st.success("✅ Data file found")
            else:
                st.error("❌ Data file not found")
        except Exception as e:
            st.warning(f"⚠️ Unable to check blob status: {str(e)}")
    
    # Load data
    with st.spinner('Loading data from Azure Blob Storage...'):
        df = load_data_from_blob()
    
    if df is not None:
        st.success(f"✅ Successfully loaded {len(df)} records from blob storage!")
        
        # Display basic info
        st.subheader("📈 Dataset Overview")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Records", len(df))
        with col2:
            st.metric("Total Columns", len(df.columns))
        with col3:
            st.metric("Average Salary", f"${df['Salary'].mean():,.0f}")
        with col4:
            st.metric("Departments", df['Department'].nunique())
        
        # Display the data
        st.subheader("👥 Employee Data")
        st.dataframe(df, use_container_width=True)
        
        # Show some basic analytics
        st.subheader("📊 Analytics")
        
        tab1, tab2, tab3 = st.tabs(["Department Analysis", "Location Analysis", "Salary Analysis"])
        
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Employees by Department**")
                dept_counts = df['Department'].value_counts()
                st.bar_chart(dept_counts)
            with col2:
                st.write("**Average Salary by Department**")
                dept_salary = df.groupby('Department')['Salary'].mean().sort_values(ascending=False)
                st.bar_chart(dept_salary)
        
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Employees by City**")
                city_counts = df['City'].value_counts()
                st.bar_chart(city_counts)
            with col2:
                st.write("**Average Salary by City**")
                city_salary = df.groupby('City')['Salary'].mean().sort_values(ascending=False)
                st.bar_chart(city_salary)
        
        with tab3:
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Salary Distribution**")
                # Create salary bins for better visualization
                salary_bins = pd.cut(df['Salary'], bins=5, precision=0)
                salary_counts = salary_bins.value_counts().sort_index()
                st.bar_chart(salary_counts)
            with col2:
                st.write("**Age vs Salary**")
                # Create a proper scatter plot data structure
                age_salary_df = df[['Age', 'Salary']].copy()
                st.line_chart(age_salary_df.set_index('Age'))
        
        # Show raw data option
        with st.expander("🔍 View Raw Data"):
            st.dataframe(df, use_container_width=True)
            
            # Download button
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download data as CSV",
                data=csv,
                file_name='employee_data.csv',
                mime='text/csv'
            )
    else:
        st.error("Failed to load data. Please check the blob storage configuration.")
        
        with st.expander("🔧 Troubleshooting"):
            st.write("**Common Issues:**")
            st.write("1. Ensure the Azure Storage Account exists")
            st.write("2. Verify the container 'data' exists")
            st.write("3. Check that 'sample_data.csv' is uploaded to the container")
            st.write("4. Confirm the App Service has proper permissions to access storage")
            st.write("5. Check if AZURE_STORAGE_CONNECTION_STRING is properly configured")
            
            # Show available blobs for debugging
            try:
                st.write("**Available blobs in container:**")
                blobs = blob_manager.list_blobs()
                if blobs:
                    for blob in blobs:
                        st.write(f"- {blob}")
                else:
                    st.write("No blobs found in container")
            except Exception as e:
                st.write(f"Could not list blobs: {str(e)}")

if __name__ == "__main__":
    main()
