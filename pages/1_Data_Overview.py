import streamlit as st
import data_processing as dp
import visualization as viz
import pandas as pd

st.markdown("""
    <style>
    .st-emotion-cache-scp8yw {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)
st.logo("assets/logo.svg",size="large")
if "df" not in st.session_state or st.session_state.df is None:
    st.warning("Please upload a dataset on the **Home** page to proceed.")
    st.stop()

df = st.session_state.df

st.title("Data Overview")

st.header("Key Dataset Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Rows", f"{df.shape[0]:,}")
col2.metric("Total Columns", f"{df.shape[1]:,}")
col3.metric("Missing Cells", f"{df.isnull().sum().sum():,}")
size_bytes = df.memory_usage(deep=True).sum()
def format_bytes(size):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"
col4.metric("Memory Usage", format_bytes(size_bytes))



st.markdown("---")

st.header("Detailed Column Summary")
st.markdown("View data types, missing counts, unique values, and descriptive statistics.")
with st.expander("Expand to see full summary table", expanded=True):
    st.dataframe(dp.get_summary(df), width='stretch')

st.markdown("---")

st.header("Missing Data Pattern")
st.markdown("A heatmap showing where missing values are located (Red = Missing).")
viz.plot_missing_data_heatmap(df)

