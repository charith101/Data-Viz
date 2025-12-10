import streamlit as st
import pandas as pd
import data_processing as dp

# Set the page configuration for the whole app
st.set_page_config(
    page_title="Data-Viz : Data visualizer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------- SESSION STATE -------------------
# Initialize session state variables
if "df" not in st.session_state:
    st.session_state.df = None
if "original_df" not in st.session_state:
    st.session_state.original_df = None
if "last_uploaded_name" not in st.session_state:
    st.session_state.last_uploaded_name = None

# A global function for pages to call when data is required
def check_data():
    if st.session_state.df is None:
        st.warning("Please upload a dataset on the **Upload Data** page to proceed.")
        st.stop()
        
# ------------------- UPLOAD PAGE (Default) -------------------
st.title("Upload Your Dataset")
st.subheader("Step 1: Choose your file")
st.markdown("### Start your analysis by uploading a file.")

uploaded_file = st.file_uploader(
    "Supported Formats: CSV, Excel (.xlsx, .xls)", 
    type=["csv", "xlsx", "xls"],
    key="file_uploader_widget"
)

if uploaded_file:
    # Check if this is a new file or if data hasn't been loaded yet
    if st.session_state.df is None or uploaded_file.name != st.session_state.last_uploaded_name:
        with st.spinner(f"Loading data from **{uploaded_file.name}**..."):
            new_df = dp.load_data(uploaded_file)
            if new_df is not None:
                st.session_state.df = new_df
                st.session_state.original_df = new_df.copy()
                st.session_state.last_uploaded_name = uploaded_file.name
                st.success("Data loaded successfully! Head over to the **Data Overview** page.")
                st.toast("Data loaded!")
                st.rerun() # Force Streamlit to refresh with new data

if st.session_state.df is not None:
    df = st.session_state.df
    st.success(f"Current Dataset: **{df.shape[0]:,}** rows × **{df.shape[1]:,}** columns")
    st.markdown("---")
    st.subheader("Data Preview")
    st.dataframe(df.head(), width='stretch')
    
