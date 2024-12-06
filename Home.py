import geemap.foliumap as geemap
import streamlit as st
from helpers import ee_authenticate

st.set_page_config(layout="wide")

## Home page view
# TODO  
st.html("home.html")

ee_authenticate()
m = geemap.Map() 
m.to_streamlit() 