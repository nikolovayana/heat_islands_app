import geemap.foliumap as geemap
import streamlit as st
import ee
from pathlib import Path
from geoscript import analyze


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
 

# Visualize the data
def visualize(selectbox: str , slider, m, regions: dict):
    """
    Takes the input of the user, dictionary of feature 
    collections and a basemap and pass the right feature collection
    the basemap to the analyze() function to run analysis on 
    satellite remote sensing data

    Args:
        selectbox (str): selectbox input return value
        slider (Any): two integers from the slider input return value
        m (Any): folium basemap
        regions (dict): dictionary from feature collections
    """
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
 
 
def verify(values):
    """
    Takes two values and check if they are 3 or more
    integers apart

    Args:
        values : two values in a list, set or tuple

    Returns:
        bool: True if the values are 3 integers apart, otherwise False
    """
    if values[1] - values[0] < 3:
        return False
    return True


def read_file(file):
    return Path(file).read_text()