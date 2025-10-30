import streamlit as st
from utils import data_prep
from snowflake.snowpark.context import get_active_session

def network_page(session=None):
    """Main function to handle the network incident prediction page"""

    if session is None:
        session = get_active_session()
    
    try:
        st.title("🌐 Network Incident Prediction Tool")
        
        st.write("""
                **Welcome to the Network Incident Prediction Platform!** ⚡  

                Wondering if the network might face an outage soon?  
                This intelligent tool analyzes key network conditions and predicts the likelihood of an incident within the next hour.  

                Simply enter the network details below, and the system will instantly show whether an outage is likely.  
                It’s fast, insightful, and designed to help you take action before problems occur, keeping operations smooth and reliable.  
                 """)

        data_prep.dt_prep(session=session)

    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        st.error("Please refresh the page and try again")
