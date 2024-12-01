import geemap.foliumap as geemap
import streamlit as st

st.set_page_config(layout="wide")

st.write("Hii")

m = geemap.Map()
m.to_streamlit()
