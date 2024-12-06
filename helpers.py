import geemap.foliumap as geemap
import streamlit as st
import ee
from google.oauth2 import service_account
from ee import oauth
from geoscript import main

# Visualize the data
def visualize(selectbox, m, regions):
    if selectbox == None:
        return

    # Pass the selected city's geometry to geoscript.main
    for region in regions:
        if selectbox.lower() == region["name"].lower():
           main(region["geometry"], m)


# Authenticate Google Earth Engine
@st.cache_data
def ee_authenticate():
    geemap.ee_initialize(token_name='private_key')
    return 'success'