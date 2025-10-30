import pandas as pd
import streamlit as st
from utils import dash_sup

def dashboard_page():
    st.title("📊 Network Incident Dashboard")
    st.markdown("<br>", unsafe_allow_html=True)

    dash_sup.show_model_metrics()
    dash_sup.show_feature_importance()
    dash_sup.show_outage_distribution()