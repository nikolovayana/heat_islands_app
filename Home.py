import geemap.foliumap as geemap
import streamlit as st
from helpers import ee_authenticate

st.set_page_config(layout="wide")
ee_authenticate("json_data", "service_account")

## Home page view
# TODO  
st.html("home.html")

m = geemap.Map() 
m.to_streamlit() 