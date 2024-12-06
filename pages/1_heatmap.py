import ee
import geemap.foliumap as geemap
import streamlit as st
from helpers import visualize, ee_authenticate

st.set_page_config(layout="wide")
ee_authenticate()
# ee.Initialize()

## Global variables TODO
plovdiv = ee.FeatureCollection("projects/ee-nikolova100yana/assets/SpongeCity/02_Plovdiv")
pecs = ee.FeatureCollection("projects/ee-nikolova100yana/assets/SpongeCity/03_Pecs")
salzburg = ee.FeatureCollection("projects/ee-nikolova100yana/assets/SpongeCity/04_Salzburg")
chisinau = ee.FeatureCollection("projects/ee-nikolova100yana/assets/SpongeCity/01_ChisinauMunicipality")

regions = [
    {"name": "Salzburg", "geometry": salzburg},
    {"name": "Plovdiv", "geometry": plovdiv},
    {"name": "Pecs", "geometry": pecs},
    {"name": "Chisinau", "geometry": chisinau}
]

# Initialize the map
m = geemap.Map(basemap='HYBRID')

## Page Information and legend
# TODO  
st.html("<h2 style='text-align: center'>Choose a city from the sidebar</h2>")


## Creating the sidebar widgets
# Selectbox options
options = []
for region in regions:
    options.append(region["name"])

# Create a form with all the widgets
with st.sidebar.form("options", border=False):
    # Implementing selectbox
    selectbox_val = st.selectbox(label="City", options=options, placeholder="Choose a city", index=None)

    # Implementing slider and other widgets TODO

    # Submit the form with visualize() function TODO
    submitted = st.form_submit_button("Check", on_click=visualize(selectbox_val, m, regions))
if selectbox_val:
    st.write("Heatmap for", selectbox_val)

# Visualize the map after submitting the form
m.to_streamlit()