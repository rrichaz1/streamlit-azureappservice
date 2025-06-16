You are a senior Python and Streamlit developer. Your task is to help me build a multi-application Streamlit deployment for document management, accessible via a single Azure App Service instance. Each "app" (App1 for Assessment/Plan Extractor, App2 for Summarizer) will have its own distinct user base and a workflow of: Document List -> Document Detail View. The detail view must include a user feedback mechanism.

**Here's a breakdown of the requirements:**

**1. Overall Project Structure & Routing:**
* Create a Streamlit **multi-page app** structure.
* The root `Home.py` should serve as a **main portal/router**, allowing users to select either "App 1: Assessment/Plan Extractor" or "App 2: Summarizer".
* Each app should have its own set of pages (e.g., `pages/App1_Documents.py`, `pages/App1_Detail.py`, `pages/App2_Documents.py`, `pages/App2_Detail.py`).
* Ensure smooth navigation between the main portal and the app-specific pages using `st.switch_page()`.

**2. Document List View (for App1 and App2):**
* Each app's document list page (`App1_Documents.py`, `App2_Documents.py`) should display a categorized list of documents.
* For demonstration purposes, use **dummy data** for documents within the Python files (e.g., a list of dictionaries converted to a Pandas DataFrame). Each document should have at least `id`, `name`, `category`, `summary`, `metrics`, and `processed_info` fields.
* The Document list and documents should be stored in blob storage.
* Document names in the list should be **clickable buttons** that navigate to the corresponding detail view.
* When navigating, use **`st.session_state`** to pass the `selected_doc_id` to the detail page.
* Include a "Back to [App Name] Home" button on the document list page.


**3. Document Detail View (for App1 and App2):**
* Each app's document detail page (`App1_Detail.py`, `App2_Detail.py`) should retrieve the `selected_doc_id` from `st.session_state`.
* Display the document's `name`, `category`, `summary` (highlighted clearly), and `processed_info`.
* Provide an expandable section (`st.expander`) to view the `full_content` of the document.
* Include a "Back to [App Name] Document List" button for easy navigation.

**4. User Feedback Mechanism (within Detail View):**
* On **both** `App1_Detail.py` and `App2_Detail.py`, add a dedicated "Provide Feedback" section.
* This section should be enclosed within an **`st.form()`** to ensure atomic submission.
* Include the following feedback widgets:
    * **`st.radio`**: "Was the summary helpful and accurate?" (Options: "Yes", "No", "Partially"). Set `index=None` initially.
    * **`st.slider`**: "On a scale of 1 to 5, how accurate was the processed information?" (Default `value=3`).
    * **`st.text_area`**: "Any additional comments or suggestions for improvement?" (Include a placeholder).
    * **`st.text_input`**: "Optional: Enter your email if you'd like us to follow up."
    * **`st.form_submit_button`**: "Submit Feedback".
* Upon submission, for demonstration purposes, display a `st.success()` message and use `st.json()` to show the collected feedback data.
* **Crucially, add comments explaining where to integrate actual database saving logic (e.g., to Azure SQL Database or Azure Cosmos DB) and the importance of secure credential management via Azure App Service Application Settings.**

**5. Azure Deployment Considerations:**
* Assume the deployment environment is **Azure App Service (Linux consumption plan)**.
* The solution should be compatible with the **`streamlit run app.py --server.port 8000 --server.enableCORS false --server.enableXsrfProtection false`** startup command (or equivalent if we structure `Home.py` as the main entry).
* Emphasize using **`os.environ.get()`** for API keys or database credentials, assuming they are set as **Azure App Service Application Settings**.
* Remind me to include `streamlit` and `pandas` in `requirements.txt`.

**Agent Instructions:**

* Generate the Python code for `Home.py`, `App1_Home.py`, `pages/App1_Documents.py`, `pages/App1_Detail.py`.
* **For App2 files (`App2_Home.py`, `pages/App2_Documents.py`, `pages/App2_Detail.py`), provide clear instructions on how to create them by adapting the App1 code, highlighting key changes needed (e.g., distinct session state keys, different dummy data).** Do not generate the full code for App2 unless I ask.
* Provide a `requirements.txt` file.
* Explain the project structure clearly.
* Include comments in the code for clarity and to highlight important sections (like where to add database logic or API key access).
* Do not include actual API keys or sensitive data in the code.











