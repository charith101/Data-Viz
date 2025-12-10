import streamlit as st
import pandas as pd
import numpy as np

st.markdown("""
    <style>
    .st-emotion-cache-scp8yw {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)
st.logo("assets/logo.svg",size="large")
@st.cache_data
def load_data(uploaded_file):
    """Loads data from a file, supports CSV and Excel."""
    if uploaded_file is None:
        return None
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, low_memory=False)
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        else:
            st.error("Unsupported file type. Please use CSV or Excel.")
            return None
            
        return df.convert_dtypes()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def get_summary(df):
    """Generates a detailed summary DataFrame of the input DataFrame."""
    if df is None or df.empty:
        return pd.DataFrame()
    
    summary = pd.DataFrame({
        'Column': df.columns,
        'Type': df.dtypes.astype(str),
        'Non-Null': df.count().values,
        'Missing': df.isnull().sum().values,
        '% Missing': (df.isnull().sum() / len(df) * 100).round(2),
        'Unique': df.nunique().values,
    })
    
    numerical_cols = df.select_dtypes(include=np.number).columns
    if not numerical_cols.empty:
        desc = df[numerical_cols].describe().T.reset_index()
        desc.rename(columns={'index': 'Column'}, inplace=True)
        summary = pd.merge(summary, desc[['Column', 'mean', 'std', 'min', 'max']], 
                           on='Column', how='left')
    
    return summary.set_index('Column')

def clean_missing(df, strategy, cols):
    """Handles missing values based on the selected strategy."""
    if not cols:
        st.info("No columns selected for missing value imputation.")
        return df.copy()

    df_cleaned = df.copy()
    
    if strategy == "drop_rows":
        before = len(df_cleaned)
        df_cleaned.dropna(subset=cols, inplace=True)
        st.success(f"Dropped {before - len(df_cleaned)} rows with missing values in selected columns.")
    
    elif strategy in ["mean", "median"]:
        for col in cols:
            if pd.api.types.is_numeric_dtype(df_cleaned[col]):
                fill_value = df_cleaned[col].mean() if strategy == "mean" else df_cleaned[col].median()
                df_cleaned[col].fillna(fill_value, inplace=True)
            else:
                st.warning(f"Skipping **{col}**: {strategy} only applies to numerical columns.")
        st.success(f"Filled missing values in numerical columns using **{strategy}**.")
        
    elif strategy == "mode":
        for col in cols:
            fill_value = df_cleaned[col].mode().iloc[0] if not df_cleaned[col].mode().empty else "Unknown"
            df_cleaned[col].fillna(fill_value, inplace=True)
        st.success("Filled missing values in selected columns using **mode**.")
        
    return df_cleaned

def remove_outliers_iqr(df, cols):
    """Removes outliers using the Interquartile Range (IQR) method."""
    if not cols:
        st.info("No numerical columns selected for outlier removal.")
        return df.copy()

    df_cleaned = df.copy()
    initial_len = len(df_cleaned)
    
    for col in cols:
        if pd.api.types.is_numeric_dtype(df_cleaned[col]):
            Q1 = df_cleaned[col].quantile(0.25)
            Q3 = df_cleaned[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            
            df_cleaned = df_cleaned[(df_cleaned[col] >= lower) & (df_cleaned[col] <= upper)]
        else:
            st.warning(f"Skipping **{col}**: IQR method only applies to numerical columns.")

    removed_rows = initial_len - len(df_cleaned)
    if removed_rows > 0:
        st.success(f"Removed **{removed_rows}** outlier rows across selected numerical columns.")
    else:
        st.info("No outliers removed based on the IQR method for the selected columns.")
        
    return df_cleaned