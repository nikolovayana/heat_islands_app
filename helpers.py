import geemap.foliumap as geemap
import streamlit as st
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
def ee_authenticate(token_name=st.secrets["EARTHENGINE_TOKEN"]):
    geemap.ee_initialize(token_name=token_name)