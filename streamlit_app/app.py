import streamlit as st

# Page Config
st.set_page_config(page_title="Redirect to Tool", page_icon="🌐", layout="centered")

# Improved CSS supporting both dark and light themes
st.markdown("""
<style>
/* Theme-aware root variables */
:root {
    --main-bg-light: #f0f4f8;
    --main-bg-dark: #1e1e1e;
    --text-light: #333333;
    --text-dark: #f0f0f0;
    --subtext-light: #555555;
    --subtext-dark: #cccccc;
    --button-bg: #6366f1;
    --button-bg-hover: #4f46e5;
    --button-text: #ffffff;
}

@media (prefers-color-scheme: dark) {
    .main {
        background-color: var(--main-bg-dark);
        color: var(--text-dark);
    }
    .title, .subtext {
        color: var(--text-dark);
    }
}

@media (prefers-color-scheme: light) {
    .main {
        background-color: var(--main-bg-light);
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
    border-radius: 16px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.15);
    margin-top: 3rem;
}

.title {
    font-size: 2.75rem;
    font-weight: 800;
    text-align: center;
    margin-bottom: 1rem;
}

.subtext {
    font-size: 1.25rem;
    text-align: center;
    margin-bottom: 2rem;
    font-weight: 500;
}

.redirect-button {
    display: inline-block;
    width: 100%;
    background-color: var(--button-bg);
    color: var(--button-text) !important;
    font-size: 1.15rem;
    font-weight: 600;
    padding: 1rem;
    border: none;
    border-radius: 10px;
    text-align: center;
    text-decoration: none;
    transition: background 0.3s ease;
    box-shadow: 0 2px 12px rgba(0,0,0,0.2);
}

.redirect-button:hover {
    background-color: var(--button-bg-hover);
}
</style>
""", unsafe_allow_html=True)

# App content
st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown('<div class="title">Welcome to AI-PortFolio Management Tool</div>', unsafe_allow_html=True)
st.markdown('<div class="subtext">Click the button below to access the tool 🚀</div>', unsafe_allow_html=True)

# Redirect button
redirect_html = """
<a href="https://spontaneous-taiyaki-9a2592.netlify.app/" target="_blank" class="redirect-button">Go to Site</a>
"""
st.markdown(redirect_html, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
