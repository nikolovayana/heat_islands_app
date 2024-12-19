import geemap.foliumap as geemap
import streamlit as st
import ee
from geoscript import analyze

# Visualize the data
def visualize(selectbox, slider, m, regions):
    if selectbox == None:
        return
    
    if not verify(slider):
        st.html("error.html")
        return

    start_year = slider[0]
    end_year = slider[1]

    # Pass the selected city's geometry to geoscript.main
    for region in regions:
        if selectbox.lower() == region["name"].lower():
           analyze(region["geometry"], start_year, end_year, m)
    
    return


# Authenticate Google Earth Engine
@st.cache_data
def ee_authenticate(token, service_account):
    """_summary_
        Google Earth Engine token authentication and initialization
    Args:
        token_name (Any): Google Earth Engine token in JSON format received by the
          Google Earth Engine API services
        service_account (Any): The email that is connected to your Google Earth Engine account
    """
    service_account = service_account
    credentials = ee.ServiceAccountCredentials(service_account, key_data=token)
    ee.Initialize(credentials)
    return 

def verify(values):
    if values[1] - values[0] < 3:
        return False
    return True