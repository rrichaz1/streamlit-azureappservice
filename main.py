import streamlit as st
import google.generativeai as genai
import os

# Configure the Google Gemini API (get your key from Azure App Settings)
GEMINI_API_KEY = os.environ.get("GOOGLE_API_KEY") # Or st.secrets["GOOGLE_API_KEY"] if using secrets.toml for local dev

if not GEMINI_API_KEY:
    st.error("Google API Key not found. Please set it as an environment variable or in .streamlit/secrets.toml")
else:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro') # Or 'gemini-1.5-flash' for faster, cheaper inference

    st.title('Streamlit LLM Experimentation')

    user_input = st.text_area("Enter your prompt:")

    if st.button("Generate Response"):
        if user_input:
            try:
                with st.spinner("Generating..."):
                    # For chat-like interactions, use start_chat()
                    # For single turn prompts, use generate_content()
                    response = model.generate_content(user_input)
                    st.write("---")
                    st.write("### LLM Response:")
                    st.write(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a prompt.")