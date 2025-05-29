import streamlit as st

# Page Config
st.set_page_config(page_title="Redirect to Tool", page_icon="🌐", layout="centered")

# Title and subtitle
st.title("AI-Portfolio Management Tool")
st.markdown("### Click the button below to launch the tool 🚀")

# Centered layout using columns
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.link_button("Open Tool", "https://spontaneous-taiyaki-9a2592.netlify.app/")
