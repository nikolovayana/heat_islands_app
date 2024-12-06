import ee
import geemap.foliumap as geemap
import streamlit as st
# from helpers import ee_authenticate

st.set_page_config(layout="wide")

## Home page view
# TODO  
st.html("home.html")

credentials = st.secrets["EARTHENGINE_TOKEN"]
ee.Initialize(credentials)

m = geemap.Map() 
m.to_streamlit() 