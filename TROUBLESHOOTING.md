# 🐛 Common Streamlit Errors and Fixes

## Error: `st.histogram()` doesn't exist

### Problem
```python
AttributeError: module 'streamlit' has no attribute 'histogram'
```

### Root Cause
`st.histogram()` is not a valid Streamlit function. This is a common confusion with other plotting libraries.

### ✅ Solution
Use one of these alternatives:

#### Option 1: Bar Chart with Binned Data
```python
# Create salary bins for histogram-like visualization
salary_bins = pd.cut(df['Salary'], bins=5, precision=0)
salary_counts = salary_bins.value_counts().sort_index()
st.bar_chart(salary_counts)
```

#### Option 2: Use Plotly/Altair with st.plotly_chart()
```python
import plotly.express as px

fig = px.histogram(df, x='Salary', bins=10)
st.plotly_chart(fig)
```

#### Option 3: Simple Value Counts
```python
st.bar_chart(df['Salary'].value_counts().sort_index())
```

## Other Common Streamlit Chart Issues

### 1. Scatter Plot Data Structure
```python
# ❌ Wrong
st.scatter_chart(df, x='Age', y='Salary')

# ✅ Correct
age_salary_df = df[['Age', 'Salary']].copy()
st.line_chart(age_salary_df.set_index('Age'))
```

### 2. Chart Data Format
```python
# ✅ Most Streamlit charts expect:
# - Series or DataFrame
# - For line/area charts: index as x-axis, columns as series
# - For bar charts: index as categories, values as heights
```

## Deployment Best Practices

### Always Test Locally First
```bash
# Set environment variables
export AZURE_STORAGE_CONNECTION_STRING="your_connection_string"

# Run locally
streamlit run app.py

# Test specific functionality before deploying
```

### Check Syntax Before Deployment
```bash
python -m py_compile app.py blob_storage.py config.py
```

### Use Proper Error Handling
```python
try:
    # Your chart code
    st.bar_chart(data)
except Exception as e:
    st.error(f"Chart error: {str(e)}")
    st.write("Debug info:", data.head() if hasattr(data, 'head') else str(data))
```

## Streamlit Chart Reference

### Available Chart Functions
- `st.line_chart()`
- `st.area_chart()`
- `st.bar_chart()`
- `st.pyplot()` (for matplotlib)
- `st.plotly_chart()` (for plotly)
- `st.altair_chart()` (for altair)
- `st.map()` (for maps)

### NOT Available
- `st.histogram()` ❌
- `st.scatter_chart()` ❌ (use st.line_chart or plotly)
- `st.boxplot()` ❌ (use plotly)
