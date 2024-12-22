import streamlit as st
from helpers import ee_authenticate, read_file


st.set_page_config(layout="wide", page_icon=':fire:', page_title="Home")

json_data = st.secrets["json_data"]
service_account = st.secrets["service_account"]
ee_authenticate(json_data, service_account)

## Home page view
# TODO  
st.html("home.html")

if st.button("heatmap :thermometer:", type="primary", use_container_width=True):
    st.switch_page("pages/1_heatmap.py")

markdown = read_file("home.md")
st.markdown(markdown) 