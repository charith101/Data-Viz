import streamlit as st
import visualization as viz

st.set_page_config(page_title="Data-Viz", layout="wide")

st.title("Data-Viz: Project Setup")
st.write("Main App Running...")

viz.show_test_chart()