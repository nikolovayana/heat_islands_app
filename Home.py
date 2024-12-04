import ee
import geemap.foliumap as geemap
import streamlit as st
# from sqlalchemy import create_engine, text, select, Table, MetaData
from helpers import visualize

st.set_page_config(layout="wide")
ee.Initialize()

## Global variables
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
# Add the database to the code
# engine = create_engine(st.secrets.connections.project_db.url)
# metadata = MetaData()
# coordinates = Table("coordinates", metadata, autoload_with=engine)

## Testing the secrets for the API
# st.write(st.secrets)
# st.write(st.secrets.get("connections", {}).get("project_db"))

# Initialize the map
m = geemap.Map(basemap='HYBRID')

## Main page view
# TODO  
st.write("Hi")


## Creating the sidebar widgets
# Selectbox options
options = ["Salzburg", "Plovdiv", "Pecs", "Chisinau"]

# Query the database for all coordinates, convert them to dicts and add them to a list
# with engine.connect() as conn:
#     table = conn.execute(select(coordinates))
#     regions = []
#     for row in table:
#         regions.append(row._mapping)

# Create a form with all the widgets
with st.sidebar.form("options", border=False):
    # Implementing selectbox
    selectbox_val = st.selectbox(label="City", options=options, placeholder="Choose a city", index=None)

    # Implementing slider and other widgets TODO

    # Submit the form with visualize() function TODO
    submitted = st.form_submit_button("Check", on_click=visualize(selectbox_val, m, regions))

# Visualize the map after submitting the form
m.to_streamlit()