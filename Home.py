import streamlit as st
import pandas as pd
import data_processing as dp

st.set_page_config(
    page_title="Data-Viz : Data visualizer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .st-emotion-cache-scp8yw {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

if "df" not in st.session_state:
    st.session_state.df = None
if "original_df" not in st.session_state:
    st.session_state.original_df = None
if "last_uploaded_name" not in st.session_state:
    st.session_state.last_uploaded_name = None

def check_data():
    if st.session_state.df is None:
        st.warning("Please upload a dataset on the **Upload Data** page to proceed.")
        st.stop()
        

st.title("Data-Viz")
st.logo("assets/logo.svg",size="large")
st.subheader("Upload Your Dataset")
st.markdown("##### Start your analysis by uploading a file.")

uploaded_file = st.file_uploader(
    "Supported Formats: CSV, Excel (.xlsx, .xls)", 
    type=["csv", "xlsx", "xls"],
    key="file_uploader_widget"
)

if uploaded_file:
    if st.session_state.df is None or uploaded_file.name != st.session_state.last_uploaded_name:
        with st.spinner(f"Loading data from **{uploaded_file.name}**..."):
            new_df = dp.load_data(uploaded_file)
            if new_df is not None:
                st.session_state.df = new_df
                st.session_state.original_df = new_df.copy()
                st.session_state.last_uploaded_name = uploaded_file.name
                st.success("Data loaded successfully! Head over to the **Data Overview** page.")
                st.toast("Data loaded!")
                st.rerun() 

if st.session_state.df is not None:
    df = st.session_state.df
    st.success(f"Current Dataset: **{df.shape[0]:,}** rows × **{df.shape[1]:,}** columns")
    st.markdown("---")
    st.subheader("Data Preview")
    st.markdown("First 5 rows.")
    st.dataframe(df.head(), width='stretch')
    
