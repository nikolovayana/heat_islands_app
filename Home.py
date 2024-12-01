import streamlit as st
import geemap.foliumap as geemap

st.set_page_config(layout="wide")

st.write("Hi")

m = geemap.Map()
m.to_streamlit()
