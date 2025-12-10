import streamlit as st
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

st.title("Univariate Plots")
st.markdown("Analyze the distribution of a single column.")

num_cols = df.select_dtypes(include='number').columns.tolist()
cat_cols = [c for c in df.columns if c not in num_cols]

st.header("Numerical Analysis")

if not num_cols:
    st.info("No numerical columns available for plotting.")
else:
    col_num = st.selectbox("Select Numerical Column", num_cols, key="univar_num_col")
    
    plot_type_num = st.radio(
        "Select Plot Type", 
        ["Histogram & Box Plot", "Box Plot (Individual)"], 
        key="num_plot_type",
        horizontal=True
    )
    
    if plot_type_num == "Histogram & Box Plot":
        viz.plot_histogram(df, col_num)
    elif plot_type_num == "Box Plot (Individual)":
        viz.plot_box_plot(df, col_num)

st.markdown("---")

st.header("Categorical Analysis")

if not cat_cols:
    st.info("No categorical columns available for plotting.")
else:
    col_cat = st.selectbox("Select Categorical Column", cat_cols, key="univar_cat_col")
    
    plot_limit = st.slider(
        "Max Categories to Display", 
        min_value=5, 
        max_value=50, 
        value=15, 
        step=5,
        key="cat_limit"
    )
    
    viz.plot_bar_chart_categorical(df, col_cat, limit=plot_limit)