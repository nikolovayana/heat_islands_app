import geemap.foliumap as geemap
import streamlit as st

st.set_page_config(layout="wide")

## Home page view
# TODO  
st.html("home.html")

m = geemap.Map(basemap='HYBRID')
m.to_streamlit() 