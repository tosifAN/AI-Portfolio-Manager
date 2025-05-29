import streamlit as st

# Set page configuration
st.set_page_config(page_title="AI Portfolio Manager", layout="centered")

# Add custom CSS to center content
st.markdown("""
    <style>
        .centered-title {
            text-align: center;
            font-size: 2.5em;
            font-weight: bold;
            margin-top: 20px;
        }
        .centered-text {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 70vh;
            font-size: 1.5em;
        }
    </style>
""", unsafe_allow_html=True)

# Display centered title
st.markdown('<div class="centered-title">AI Portfolio Manager</div>', unsafe_allow_html=True)

# Display centered message
st.markdown('<div class="centered-text">Migrating from Streamlit to ReactJS to handle the I/O voice efficiently</div>', unsafe_allow_html=True)
