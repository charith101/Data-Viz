import streamlit as st
import data_processing as dp
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

st.title("Clean & Transform")
tab1, tab2, tab3 = st.tabs(["Handle Missing Values", "Remove Outliers (IQR)", "Reset Data"])

with tab1:
    st.header("Handle Missing Values")
    st.markdown("Select columns and a strategy to impute or drop missing data.")
    
    missing = df.isnull().sum()
    missing_cols = missing[missing > 0].index.tolist()
    
    if not missing_cols:
        st.success("No missing values in the current dataset!")
    else:
        st.info(f"Columns with missing values: **{len(missing_cols)}**")
        
        cols = st.multiselect(
            "Select columns to process", 
            missing_cols, 
            default=missing_cols, 
            key="missing_cols_select"
        )
        
        strategy_options = {
            "Drop Rows": "drop_rows",
            "Fill with Mean (Numerical only)": "mean",
            "Fill with Median (Numerical only)": "median",
            "Fill with Mode (All types)": "mode"
        }
        
        selected_strategy_name = st.selectbox(
            "Select Imputation/Drop Strategy", 
            list(strategy_options.keys()), 
            key="missing_strategy_select"
        )
        strategy = strategy_options[selected_strategy_name]
        
        if st.button("Apply Cleaning Operation", type="primary", key="apply_cleaning_btn"):
            cleaned = dp.clean_missing(df, strategy, cols)
            st.session_state.df = cleaned
            st.toast("Cleaning applied successfully!")
            st.rerun()

with tab2:
    st.header("Remove Outliers (IQR Method)")
    st.markdown("Identify and remove extreme values in numerical columns using the Interquartile Range (IQR) method.")
    
    num_cols = df.select_dtypes(include='number').columns.tolist()
    if not num_cols:
        st.info("No numerical columns found to check for outliers.")
    else:
        cols_outlier = st.multiselect(
            "Select numerical columns to clean", 
            num_cols, 
            default=num_cols, 
            key="outlier_cols_select"
        )
        if st.button("Remove Outliers", type="primary", key="remove_outliers_btn"):
            cleaned = dp.remove_outliers_iqr(df, cols_outlier)
            st.session_state.df = cleaned
            st.toast("Outlier removal applied!")
            st.rerun()

with tab3:
    st.header("Reset Data")
    st.markdown("Revert your dataset to the state right after the initial upload.")
    
    if st.button("Reset to Original Data", type="secondary", key="reset_data_btn"):
        if st.session_state.original_df is not None:
            st.session_state.df = st.session_state.original_df.copy()
            st.success("Data reset to original state!")
            st.toast("Dataset reset!")
            st.rerun()
        else:
            st.error("Original data not found. Please re-upload.")

st.markdown("---")
st.subheader("Current Data Snapshot")
st.data_editor(df.head(10), width='stretch')