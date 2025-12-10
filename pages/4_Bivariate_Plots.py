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

st.title("Bivariate & Multivariate Plots")
st.markdown("Explore relationships between two or more variables.")

num_cols = df.select_dtypes(include='number').columns.tolist()
cat_cols = [c for c in df.columns if c not in num_cols]

tab1, tab2, tab3, tab4 = st.tabs(["Scatter Plot", "Grouped Box Plot", "Density Heatmap", "Correlation"])

with tab1:
    st.header("Scatter Plot (Numerical vs Numerical)")
    if len(num_cols) < 2:
        st.info("Need at least two numerical columns.")
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            x = st.selectbox("X-axis", num_cols, key="bivar_x")
        with col2:
            y_options = [c for c in num_cols if c != x]
            y = st.selectbox("Y-axis", y_options, key="bivar_y")
        with col3:
            color_options = ["None"] + cat_cols
            color_by = st.selectbox("Color by (Category)", color_options, key="bivar_color")
        
        color_by_col = None if color_by == "None" else color_by
        viz.plot_scatter(df, x, y, color_by_col)

with tab2:
    st.header("Grouped Box Plot (Numerical vs Categorical)")
    if not num_cols or not cat_cols:
        st.info("Need at least one numerical and one categorical column.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            num_col_box = st.selectbox("Numerical Value (Y-axis)", num_cols, key="box_num")
        with col2:
            cat_col_box = st.selectbox("Grouping Category (X-axis)", cat_cols, key="box_cat")
            
        viz.plot_box_plot(df, num_col_box, cat_col_box)

with tab3:
    st.header("2D Density Heatmap")
    st.markdown("Useful for visualizing the concentration of data points in dense scatter plots.")
    if len(num_cols) < 2:
        st.info("Need at least two numerical columns.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            x_den = st.selectbox("X-axis (Density)", num_cols, key="den_x")
        with col2:
            y_den = st.selectbox("Y-axis (Density)", [c for c in num_cols if c != x_den], key="den_y")
            
        viz.plot_density_heatmap(df, x_den, y_den)

with tab4:
    st.header("Correlation Heatmap & Pair Plot")
    
    st.subheader("Numerical Correlation Heatmap")
    viz.plot_correlation_heatmap(df)
    
    st.markdown("---")
    
    st.subheader("Pair Plot (Up to 5 Numerical Columns)")
    st.markdown("Warning: Can be slow on large datasets!")
    
    if len(num_cols) >= 2:
        if st.button("Generate Pair Plot", key="show_pair_plot_btn"):
            with st.spinner("Generating Pair Plot... (800px tall)"):
                viz.plot_pairplot(df)
    else:
        st.info("Need at least two numerical columns for a Pair Plot.")