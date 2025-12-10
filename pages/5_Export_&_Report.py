import streamlit as st
import data_processing as dp
import pandas as pd
import io

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

st.title("Export & Final Report")
st.header("Download Cleaned Data")
st.markdown("Download your current, cleaned dataset in your preferred format.")

col1, col2 = st.columns(2)

with col1:
    st.download_button(
        "Download as CSV",
        df.to_csv(index=False).encode('utf-8'),
        "cleaned_data.csv",
        "text/csv",
        key="download_csv_btn"
    )

with col2:
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False, engine='openpyxl')
    excel_buffer.seek(0)
    
    st.download_button(
        "Download as Excel (.xlsx)",
        data=excel_buffer,
        file_name="cleaned_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="download_excel_btn"
    )

st.markdown("---")

st.header("Final Data Report Summary")

final_rows = df.shape[0]
original_rows = st.session_state.original_df.shape[0] if st.session_state.original_df is not None else final_rows
rows_removed = original_rows - final_rows
missing_remaining = df.isnull().sum().sum()

col_a, col_b, col_c = st.columns(3)
col_a.metric("Original Rows", f"{original_rows:,}")
col_b.metric("Final Rows", f"{final_rows:,}")
col_c.metric("Rows Removed (Cleaned)", f"{rows_removed:,}", delta=f"{rows_removed:,} removed")

st.markdown(f"""
#### Current Data State:
* **Total Columns:** {df.shape[1]:,}
* **Total Missing Cells (Remaining):** {missing_remaining:,}
* **Data Types Used:** {len(df.dtypes.unique()):,} unique types
""")

with st.expander("Show Final Detailed Data Summary"):
    st.dataframe(dp.get_summary(df), width='stretch')

st.markdown("---")
st.caption("Thank you for using Data-Viz Pro!")