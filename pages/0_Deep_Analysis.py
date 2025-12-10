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
if "df" not in st.session_state or st.session_state.df is None:
    st.warning("Please upload a dataset on the Home page to proceed.")
    st.stop()


df = st.session_state.df.copy()

st.title("Deep Analysis & Inspection")
st.markdown("Explore your data with filtering, specific column metrics, and custom aggregations.")


with st.expander("Column Display Settings"):
    all_cols = df.columns.tolist()
    selected_cols = st.multiselect(
        "Select Columns to Display",
        all_cols,
        default=all_cols,
        help="Remove columns to declutter the table view."
    )

st.subheader("1. Interactive Data Explorer")

search_query = st.text_input(
    "Global Search", 
    placeholder="Type to search across all columns...",
    help="Filters rows where ANY column matches the text."
)

if search_query:
    mask = df.astype(str).apply(
        lambda x: x.str.contains(search_query, case=False, na=False)
    ).any(axis=1)
    filtered_df = df[mask]
else:
    filtered_df = df

display_df = filtered_df[selected_cols] if selected_cols else filtered_df

row_count = display_df.shape[0]
col_count = display_df.shape[1]

st.markdown(f"**Showing {row_count:,} rows and {col_count:,} columns**")

st.dataframe(
    display_df, 
    width='stretch', 
    height=400
)

st.markdown("---")

st.subheader("2. Quick Column Metrics")
st.markdown("Select a column to analyze statistics based on the filtered data above.")

if not display_df.empty:
    target_col = st.selectbox("Select Column to Analyze", display_df.columns)

    if target_col:
        col_data = display_df[target_col]
        col_type = col_data.dtype

        m1, m2, m3, m4 = st.columns(4)

        if pd.api.types.is_numeric_dtype(col_type):
            avg = col_data.mean()
            med = col_data.median()
            mn = col_data.min()
            mx = col_data.max()
            std = col_data.std()
            
            m1.metric("Average", f"{avg:,.2f}")
            m2.metric("Median", f"{med:,.2f}")
            m3.metric("Min / Max", f"{mn:,.0f} / {mx:,.0f}")
            m4.metric("Std Dev", f"{std:,.2f}")
            
            with st.expander("Show Distribution (Mini-Chart)"):
                st.bar_chart(col_data.value_counts(bins=10).sort_index())

        else:
            unique_count = col_data.nunique()
            most_freq = col_data.mode()[0] if not col_data.mode().empty else "N/A"
            most_freq_count = col_data.value_counts().iloc[0] if not col_data.empty else 0
            missing = col_data.isnull().sum()

            m1.metric("Unique Values", f"{unique_count:,}")
            m2.metric("Most Frequent", str(most_freq))
            m3.metric("Freq Count", f"{most_freq_count:,}")
            m4.metric("Missing Values", f"{missing:,}")

            with st.expander("Show Top 10 Categories"):
                st.table(col_data.value_counts().head(10))
else:
    st.warning("No data available in current filter to analyze.")

st.markdown("---")

st.subheader("3. Grouping & Aggregation")
st.markdown("Create a pivot view to summarize data.")

if not display_df.empty:
    c1, c2, c3 = st.columns(3)
    
    cat_cols = display_df.select_dtypes(exclude='number').columns.tolist()
    num_cols = display_df.select_dtypes(include='number').columns.tolist()
    
    with c1:
        group_col = st.selectbox("Group By (Category)", cat_cols if cat_cols else display_df.columns, key="grp_col")

    with c2:
        agg_col = st.selectbox("Calculate Value (Numerical)", num_cols if num_cols else display_df.columns, key="agg_col")
        
    with c3:
        agg_func = st.selectbox("Function", ["mean", "sum", "count", "min", "max", "std"], key="agg_func")
        
    if st.button("Generate Summary Table"):
        try:
            grouped_df = display_df.groupby(group_col)[agg_col].agg(agg_func).reset_index()
            
            grouped_df.columns = [group_col, f"{agg_func.title()} of {agg_col}"]
            
            sort_col = grouped_df.columns[1]
            grouped_df = grouped_df.sort_values(by=sort_col, ascending=False)
            
            st.dataframe(grouped_df, width='stretch')
            
        except Exception as e:
            st.error(f"Could not group data: {e}. Try selecting different columns.")
else:
    st.info("Upload data to use aggregation tools.")