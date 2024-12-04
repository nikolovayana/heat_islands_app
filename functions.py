import streamlit as st

## Implement the main function with the gee code TODO
def main():
    pass

## Visualize function
def visualize(selectbox, m, regions):
    if selectbox == None:
        return
    
    st.write(selectbox)

    for region in regions:
        if selectbox.lower() == region.name:
            m.setCenter(region.E, region.N, 12)

