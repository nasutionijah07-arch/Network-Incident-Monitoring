# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Get the current credentials
session = get_active_session()


# Adjusting the page
st.set_page_config(
    page_title="Network Incident Prediction", 
    page_icon="🌐", 
    layout='wide'
)

def main():
    # Load external CSS
    def load_css():
        with open("assets/styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Load external JS
    def load_js(current_page):
        with open("assets/scripts.js") as f:
            js_code = f.read().replace("{{CURRENT_PAGE}}", current_page)
            st.markdown(f"<script>{js_code}</script>", unsafe_allow_html=True)

    # Initialize session state for page navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "📈 Prediction"

    # Navigation options
    nav_options = [
        "📈 Prediction",
        "📊 Dashboard",
    ]

    # Load CSS
    load_css()

    # Sidebar navigation
    with st.sidebar:
        st.markdown(
            '<div class="sidebar-title">🌐 Network Prediction</div>', 
            unsafe_allow_html=True
        )
        
        for option in nav_options:
            if st.button(option, key=option):
                st.session_state.current_page = option
                st.rerun()

    # Load JS with current page
    load_js(st.session_state.current_page)

    # Page display logic
    if st.session_state.current_page == "📈 Prediction":
        from app.network import network_page
        network_page(session=session)
    else:
        from custom_pages.dash import dashboard_page
        dashboard_page()

if __name__ == "__main__":
    main()