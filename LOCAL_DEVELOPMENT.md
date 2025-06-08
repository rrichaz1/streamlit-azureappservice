# 🏠 Local Development Guide

## 🚀 **Quick Start (Recommended)**

Since you already have a `.env` file with your Azure Storage connection string, you can run the app immediately:

```bash
# Option 1: Use the automated script
./run_local.sh

# Option 2: Manual run
streamlit run app.py
```

The app will automatically:
- ✅ Load your `.env` file
- ✅ Connect to Azure Blob Storage  
- ✅ Display the dashboard at http://localhost:8501

## 📋 **Prerequisites**

### 1. **Python Environment**
```bash
# Make sure you're in the virtual environment
# (You should see (.venv) in your prompt)

# If not, activate it:
source .venv/bin/activate
```

### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3. **Environment Variables**
Your `.env` file already contains:
```env
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;...
```

## 🛠️ **Running the App**

### **Method 1: Automated Script (Easiest)**
```bash
./run_local.sh
```
This script will:
- ✅ Check for `.env` file
- ✅ Install dependencies
- ✅ Run syntax checks
- ✅ Start the Streamlit server

### **Method 2: Direct Streamlit Command**
```bash
streamlit run app.py
```

### **Method 3: Custom Port**
```bash
streamlit run app.py --server.port 8502
```

### **Method 4: Development Mode (Auto-reload)**
```bash
streamlit run app.py --server.runOnSave true
```

## 🌐 **Accessing the App**

Once running, open your browser to:
- **Local URL**: http://localhost:8501
- **Network URL**: http://[your-ip]:8501

## 🔧 **Development Tips**

### **Live Reloading**
Streamlit automatically reloads when you save changes to your Python files.

### **Debug Mode**
Add debug prints in your code:
```python
import streamlit as st

st.write("Debug: Data loaded successfully")
st.write("Debug: DataFrame shape:", df.shape)
```

### **Testing Specific Features**
```bash
# Test blob storage connection
python -c "from blob_storage import create_blob_manager; from config import AppConfig; config = AppConfig.get_azure_storage_config(); blob_manager = create_blob_manager(config['storage_account_name'], config['container_name']); print('✅ Connection successful' if blob_manager.check_blob_exists(config['blob_name']) else '❌ Connection failed')"
```

### **Check Environment Variables**
```bash
# Verify your .env file is loaded
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Azure Storage:', 'Found' if os.getenv('AZURE_STORAGE_CONNECTION_STRING') else 'Not found')"
```

## 🐛 **Troubleshooting**

### **Common Issues:**

1. **Module not found errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **Port already in use**
   ```bash
   streamlit run app.py --server.port 8502
   ```

3. **Azure Storage connection issues**
   - Check your `.env` file has the correct connection string
   - Verify the storage account and container exist

4. **Streamlit not found**
   ```bash
   # Make sure you're in the virtual environment
   source .venv/bin/activate
   pip install streamlit
   ```

### **Debug Commands:**
```bash
# Check Python path
which python

# Check installed packages
pip list | grep streamlit

# Verify .env file
cat .env

# Test Azure connection
python -c "from azure.storage.blob import BlobServiceClient; import os; from dotenv import load_dotenv; load_dotenv(); print('Testing connection...'); client = BlobServiceClient.from_connection_string(os.getenv('AZURE_STORAGE_CONNECTION_STRING')); print('✅ Success')"
```

## 🔄 **Development Workflow**

1. **Start the app**: `./run_local.sh`
2. **Make changes** to your Python files
3. **Save** - Streamlit auto-reloads
4. **Test** in browser
5. **When ready**: Use `./deploy.sh` to deploy to Azure

## 📂 **File Structure for Local Dev**
```
streamlit-app/
├── .env                 # 🔑 Your environment variables (LOCAL ONLY)
├── app.py              # 🎨 Main Streamlit app
├── blob_storage.py     # ☁️  Azure Blob operations  
├── config.py           # ⚙️  Configuration management
├── run_local.sh        # 🏃‍♂️ Local development script
├── deploy.sh          # 🚀 Deployment script
└── requirements.txt    # 📦 Dependencies
```

## 🔒 **Security Note**
Your `.env` file is already in `.gitignore` to prevent accidentally committing secrets to git. Keep it that way! ✅

---

**Happy coding! 🎉** Your local development environment is now ready to go!
