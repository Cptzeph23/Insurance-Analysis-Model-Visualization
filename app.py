import streamlit as st
from data_loader import load_data

st.set_page_config(page_title="Insurance Analytics", layout="wide")

df = load_data()

st.title("Insurance Analytics Dashboard")
st.write("Dataset Preview:")
st.dataframe(df.head())
