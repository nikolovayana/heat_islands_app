import ee
import geemap.foliumap as geemap
import streamlit as st
from helpers import visualize, verify

st.set_page_config(layout="wide", page_icon=":fire:", page_title="Heatmap")

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

## Page Information and layout
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
    slider_val = st.slider("Select a start and end year",2013, 2024, value=(2014, 2019),\
                            help="The values should be minimum 3 years apart",)

    # Submit the form with visualize() function TODO
    submitted = st.form_submit_button("Check", on_click=visualize(selectbox_val, slider_val, m, regions))
    

if selectbox_val and verify(slider_val): 
    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        st.write("Heatmap for", selectbox_val, "for the period from",\
                str(slider_val[0]) + '-1-1 to',str(slider_val[1]) + '-1-1')
    # with col2:
        # st.button(label="Export as JPEG", type="secondary", use_container_width=True)
        # st.button(label="Export as PNG", type="secondary", use_container_width=True)

# Visualize the map after submitting the form
m.to_streamlit()