"""
Mock data generators for the multipage application
"""

import pandas as pd
from datetime import datetime, timedelta
import random

def generate_app1_documents():
    """Generate mock documents for Assessment/Plan Extractor app"""
    documents = [
        {
            'id': 'doc_001',
            'name': 'Patient Assessment Report - John Doe',
            'category': 'Medical Assessment',
            'summary': 'Comprehensive assessment revealing moderate hypertension with recommended lifestyle modifications and medication review.',
            'metrics': {'accuracy': 92, 'confidence': 87, 'processing_time': 2.3},
            'processed_info': {
                'assessment': 'Hypertension Stage 1, BMI elevated',
                'plan': 'Lifestyle modifications, medication review in 6 weeks',
                'key_findings': ['Blood pressure 145/92', 'BMI 28.5', 'No diabetes indicators']
            },
            'full_content': 'Patient presents with elevated blood pressure readings over the past month. Current medications include lisinopril 10mg daily. Lifestyle factors include sedentary work, high sodium diet. Recommendations include dietary modifications, exercise program, and medication adjustment.',
            'date_processed': datetime.now() - timedelta(days=1)
        },
        {
            'id': 'doc_002',
            'name': 'Cardiology Assessment - Sarah Johnson',
            'category': 'Specialist Consultation',
            'summary': 'Cardiology consultation reveals stable angina with need for stress testing and medication optimization.',
            'metrics': {'accuracy': 95, 'confidence': 91, 'processing_time': 1.8},
            'processed_info': {
                'assessment': 'Stable angina, possible CAD',
                'plan': 'Stress test, optimize medications, cardiac rehabilitation',
                'key_findings': ['Chest pain on exertion', 'Normal resting ECG', 'Family history of CAD']
            },
            'full_content': 'Patient reports chest pain during moderate exercise. ECG shows normal sinus rhythm. Echocardiogram reveals normal left ventricular function. Stress testing recommended to evaluate for coronary artery disease.',
            'date_processed': datetime.now() - timedelta(days=2)
        },
        {
            'id': 'doc_003',
            'name': 'Diabetes Management Plan - Michael Brown',
            'category': 'Chronic Disease Management',
            'summary': 'Diabetes management review showing good glycemic control with minor medication adjustments needed.',
            'metrics': {'accuracy': 89, 'confidence': 85, 'processing_time': 2.1},
            'processed_info': {
                'assessment': 'Type 2 DM, well controlled, HbA1c 6.8%',
                'plan': 'Continue current regimen, increase monitoring frequency',
                'key_findings': ['HbA1c 6.8%', 'No retinopathy', 'Mild peripheral neuropathy']
            },
            'full_content': 'Patient with Type 2 diabetes, diagnosed 5 years ago. Currently on metformin 1000mg BID and glipizide 5mg daily. Recent HbA1c 6.8%. Mild peripheral neuropathy present. Annual eye exam shows no retinopathy.',
            'date_processed': datetime.now() - timedelta(days=3)
        },
        {
            'id': 'doc_004',
            'name': 'Mental Health Assessment - Lisa Wang',
            'category': 'Psychiatric Evaluation',
            'summary': 'Mental health screening indicates moderate anxiety with recommendation for therapy and possible medication.',
            'metrics': {'accuracy': 88, 'confidence': 82, 'processing_time': 2.7},
            'processed_info': {
                'assessment': 'Generalized Anxiety Disorder, moderate severity',
                'plan': 'CBT referral, consider SSRI, follow-up in 4 weeks',
                'key_findings': ['GAD-7 score: 12', 'No suicidal ideation', 'Work-related stressors']
            },
            'full_content': 'Patient reports persistent worry and anxiety for the past 6 months. GAD-7 score of 12 indicates moderate anxiety. Sleep disturbances and concentration difficulties present. No history of panic attacks.',
            'date_processed': datetime.now() - timedelta(days=4)
        }
    ]
    
    return pd.DataFrame(documents)

def generate_app2_documents():
    """Generate mock documents for Document Summarizer app"""
    documents = [
        {
            'id': 'sum_001',
            'name': 'Research Paper - AI in Healthcare',
            'category': 'Academic Research',
            'summary': 'Comprehensive review of artificial intelligence applications in healthcare, focusing on diagnostic imaging and predictive analytics.',
            'metrics': {'readability': 85, 'compression_ratio': 0.15, 'key_concepts': 12},
            'processed_info': {
                'main_topics': ['Machine Learning in Diagnostics', 'Clinical Decision Support', 'Predictive Analytics'],
                'key_insights': ['AI improves diagnostic accuracy by 23%', '78% reduction in false positives', 'Cost savings of $2.1B annually'],
                'methodology': 'Systematic literature review of 156 papers'
            },
            'full_content': 'This systematic review examines the current state and future potential of artificial intelligence in healthcare. We analyzed 156 peer-reviewed papers published between 2019-2024, focusing on clinical applications of machine learning, deep learning, and natural language processing. Key findings include significant improvements in diagnostic accuracy, particularly in radiology and pathology.',
            'date_processed': datetime.now() - timedelta(days=1)
        },
        {
            'id': 'sum_002',
            'name': 'Financial Report Q3 2024',
            'category': 'Business Documentation',
            'summary': 'Quarterly financial performance showing 15% revenue growth with strong performance in digital services segment.',
            'metrics': {'readability': 78, 'compression_ratio': 0.12, 'key_concepts': 8},
            'processed_info': {
                'main_topics': ['Revenue Growth', 'Digital Transformation', 'Market Expansion'],
                'key_insights': ['15% YoY revenue growth', 'Digital services up 32%', 'EBITDA margin improved to 18%'],
                'methodology': 'Standard financial analysis and market comparison'
            },
            'full_content': 'Q3 2024 financial results demonstrate continued strong performance across all business segments. Total revenue reached $2.4B, representing 15% year-over-year growth. Digital services segment showed exceptional performance with 32% growth, driven by cloud adoption and AI solutions.',
            'date_processed': datetime.now() - timedelta(days=2)
        },
        {
            'id': 'sum_003',
            'name': 'Policy Document - Remote Work Guidelines',
            'category': 'Corporate Policy',
            'summary': 'Updated remote work policy establishing flexible work arrangements with performance metrics and collaboration requirements.',
            'metrics': {'readability': 92, 'compression_ratio': 0.18, 'key_concepts': 6},
            'processed_info': {
                'main_topics': ['Flexible Work Arrangements', 'Performance Management', 'Team Collaboration'],
                'key_insights': ['Up to 3 days remote per week', 'Mandatory team meetings twice weekly', 'Quarterly performance reviews'],
                'methodology': 'Policy analysis and requirement extraction'
            },
            'full_content': 'This policy establishes guidelines for remote work arrangements to support work-life balance while maintaining productivity and team cohesion. Employees may work remotely up to 3 days per week with manager approval. All remote workers must participate in mandatory team meetings and maintain regular communication.',
            'date_processed': datetime.now() - timedelta(days=3)
        },
        {
            'id': 'sum_004',
            'name': 'Technical Specification - API Documentation',
            'category': 'Technical Documentation',
            'summary': 'RESTful API specification for user management system with authentication, CRUD operations, and rate limiting.',
            'metrics': {'readability': 73, 'compression_ratio': 0.22, 'key_concepts': 15},
            'processed_info': {
                'main_topics': ['Authentication', 'CRUD Operations', 'Rate Limiting', 'Error Handling'],
                'key_insights': ['OAuth 2.0 implementation', '1000 requests/hour limit', 'JSON-based responses'],
                'methodology': 'API specification analysis and endpoint documentation'
            },
            'full_content': 'This document provides comprehensive API documentation for the user management system. The API implements OAuth 2.0 for authentication and provides full CRUD operations for user accounts. Rate limiting is set at 1000 requests per hour per API key. All responses are JSON-formatted with standardized error codes.',
            'date_processed': datetime.now() - timedelta(days=4)
        }
    ]
    
    return pd.DataFrame(documents)

def get_document_by_id(documents_df, doc_id):
    """Retrieve a specific document by ID"""
    doc = documents_df[documents_df['id'] == doc_id]
    if not doc.empty:
        return doc.iloc[0]
    return None
