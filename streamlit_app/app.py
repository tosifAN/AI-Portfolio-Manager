import streamlit as st

# Page Config
st.set_page_config(page_title="Redirect to Tool", page_icon="🌐", layout="centered")

# App content using native Streamlit
st.title("AI-Portfolio Management Tool")
st.markdown("### Click below to launch the tool 🚀")

# Center the button using container and spacing
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("Open Tool"):
        st.markdown("[Click here if not redirected](https://spontaneous-taiyaki-9a2592.netlify.app/)", unsafe_allow_html=True)
        st.experimental_rerun()  # Optional: simulate a redirect behavior
