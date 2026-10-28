"""JobApply AI staging. Safe demo by default; secure portal only when configured."""
import streamlit as st
from secure_portal import configured, secure_portal

st.set_page_config(page_title="JobApply AI | Staging", page_icon="🤖", layout="wide", initial_sidebar_state="collapsed")
if configured():
    secure_portal()
else:
    # Existing approved visual design, no private data or credentials.
    from demo_ui import show_demo
    show_demo()
