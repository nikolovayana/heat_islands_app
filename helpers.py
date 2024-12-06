from geoscript import main

# Visualize the data
def visualize(selectbox, m, regions):
    if selectbox == None:
        return

    # Pass the selected city's geometry to geoscript.main
    for region in regions:
        if selectbox.lower() == region["name"].lower():
           main(region["geometry"], m)