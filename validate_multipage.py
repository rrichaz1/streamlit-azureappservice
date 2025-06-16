#!/usr/bin/env python3
"""
Pre-deployment validation script for multipage Streamlit app
"""

import os
import sys
import importlib.util
from pathlib import Path

def validate_file_structure():
    """Validate that all required files exist"""
    print("🔍 Validating file structure...")
    
    required_files = [
        "Home.py",
        "requirements.txt",
        "startup.sh",
        ".env.example",
        "utils/config.py",
        "utils/blob_storage.py",
        "utils/mock_data.py",
        "pages/App1_Documents.py",
        "pages/App1_Detail.py",
        "pages/App2_Documents.py",
        "pages/App2_Detail.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All required files present")
    return True

def validate_python_syntax():
    """Validate Python syntax for all Python files"""
    print("🔍 Validating Python syntax...")
    
    python_files = [
        "Home.py",
        "utils/config.py",
        "utils/blob_storage.py", 
        "utils/mock_data.py",
        "pages/App1_Documents.py",
        "pages/App1_Detail.py",
        "pages/App2_Documents.py",
        "pages/App2_Detail.py"
    ]
    
    for file in python_files:
        try:
            with open(file, 'r') as f:
                compile(f.read(), file, 'exec')
        except SyntaxError as e:
            print(f"❌ Syntax error in {file}: {e}")
            return False
        except Exception as e:
            print(f"❌ Error validating {file}: {e}")
            return False
    
    print("✅ All Python files have valid syntax")
    return True

def validate_imports():
    """Test that all imports work correctly"""
    print("🔍 Validating imports...")
    
    # Add utils to path
    sys.path.append('utils')
    
    try:
        from mock_data import generate_app1_documents, generate_app2_documents
        from config import AppConfig
        
        # Test mock data generation
        app1_docs = generate_app1_documents()
        app2_docs = generate_app2_documents()
        
        if len(app1_docs) == 0 or len(app2_docs) == 0:
            print("❌ Mock data generation failed")
            return False
            
        # Test config
        config = AppConfig.get_app_config()
        if not config:
            print("❌ Config loading failed")
            return False
            
        print("✅ All imports and data generation work correctly")
        return True
        
    except Exception as e:
        print(f"❌ Import validation failed: {e}")
        return False

def validate_environment():
    """Check environment setup"""
    print("🔍 Validating environment...")
    
    if not os.path.exists('.env'):
        if not os.path.exists('.env.example'):
            print("❌ Neither .env nor .env.example found")
            return False
        else:
            print("⚠️  .env file not found, but .env.example exists")
            print("   Create .env from .env.example for local development")
    else:
        print("✅ .env file found")
    
    return True

def main():
    print("=" * 50)
    print("🚀 MULTIPAGE STREAMLIT APP VALIDATION")
    print("=" * 50)
    print()
    
    all_valid = True
    
    # Run all validations
    validations = [
        validate_file_structure,
        validate_python_syntax,
        validate_imports,
        validate_environment
    ]
    
    for validation in validations:
        if not validation():
            all_valid = False
        print()
    
    # Final result
    if all_valid:
        print("🎉 ALL VALIDATIONS PASSED!")
        print("✅ App is ready for deployment")
        print()
        print("Next steps:")
        print("1. Test locally: ./run_local.sh")
        print("2. Deploy to Azure: ./deploy.sh")
    else:
        print("❌ VALIDATION FAILED!")
        print("Please fix the issues above before deploying")
        sys.exit(1)

if __name__ == "__main__":
    main()
