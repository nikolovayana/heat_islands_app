import geemap.foliumap as geemap
import streamlit as st
import ee
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
# @st.cache_data
def ee_authenticate(token_name, service_account):
    service_account = service_account
    credentials = ee.ServiceAccountCredentials(service_account, key_data=token_name)
    ee.Initialize(credentials)