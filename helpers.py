import streamlit as st
from geoscript import main

def visualize(selectbox, m, regions):
    if selectbox == None:
        return
    
    st.write(selectbox)

    for region in regions:
        if selectbox.lower() == region["name"].lower():
            main(region["geometry"], m)