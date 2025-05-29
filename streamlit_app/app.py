import streamlit as st

# Page Config
st.set_page_config(page_title="Redirect to Tool", page_icon="🌐", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f0f4f8;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
    }
    .title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #333;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .subtext {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .redirect-button {
        display: block;
        width: 100%;
        background-color: #4285F4;
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        padding: 1rem;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        text-align: center;
        text-decoration: none;
        transition: background 0.3s;
    }
    .redirect-button:hover {
        background-color: #357ae8;
    }
    </style>
""", unsafe_allow_html=True)

# App content
st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown('<div class="title">Welcome to AI-PortFolio Management Tool</div>', unsafe_allow_html=True)
st.markdown('<div class="subtext">Click the button below to the Page 🚀</div>', unsafe_allow_html=True)

# Redirect button
redirect_html = """
<a href="https://spontaneous-taiyaki-9a2592.netlify.app/" target="_blank" class="redirect-button">Go to Site</a>
"""
st.markdown(redirect_html, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
