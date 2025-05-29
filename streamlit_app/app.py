import streamlit as st

# Page Config
st.set_page_config(page_title="Redirect to Tool", page_icon="🌐", layout="centered")

# Professional CSS with light/dark theme support
st.markdown("""
<style>
:root {
    --bg-light: #ffffff;
    --bg-dark: #1f1f1f;
    --text-light: #1a1a1a;
    --text-dark: #f0f0f0;
    --subtext-light: #4b5563;
    --subtext-dark: #d1d5db;
    --primary-color: #2563eb;
    --primary-hover: #1e40af;
    --button-text: #ffffff;
    --card-radius: 14px;
    --card-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

@media (prefers-color-scheme: dark) {
    .main {
        background-color: var(--bg-dark);
        color: var(--text-dark);
    }
    .title, .subtext {
        color: var(--text-dark);
    }
}

@media (prefers-color-scheme: light) {
    .main {
        background-color: var(--bg-light);
        color: var(--text-light);
    }
    .title {
        color: var(--text-light);
    }
    .subtext {
        color: var(--subtext-light);
    }
}

.main {
    padding: 2rem;
    border-radius: var(--card-radius);
    box-shadow: var(--card-shadow);
    margin-top: 3rem;
    max-width: 700px;
    margin-left: auto;
    margin-right: auto;
}

.title {
    font-size: 2.4rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 1rem;
    font-family: 'Segoe UI', sans-serif;
}

.subtext {
    font-size: 1.1rem;
    text-align: center;
    margin-bottom: 2rem;
    font-family: 'Segoe UI', sans-serif;
    font-weight: 400;
}

.redirect-button {
    display: inline-block;
    width: 100%;
    background-color: var(--primary-color);
    color: var(--button-text) !important;
    font-size: 1.1rem;
    font-weight: 600;
    padding: 0.9rem;
    border: none;
    border-radius: 10px;
    text-align: center;
    text-decoration: none;
    transition: background 0.3s ease;
}

.redirect-button:hover {
    background-color: var(--primary-hover);
}
</style>
""", unsafe_allow_html=True)

# App content
st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown('<div class="title">AI-Portfolio Management Tool</div>', unsafe_allow_html=True)
st.markdown('<div class="subtext">Click below to launch the tool 🚀</div>', unsafe_allow_html=True)

# Redirect button
redirect_html = """
<a href="https://spontaneous-taiyaki-9a2592.netlify.app/" target="_blank" class="redirect-button">Open Tool</a>
"""
st.markdown(redirect_html, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
