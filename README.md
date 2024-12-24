
# Heat Islands Application
### App link: https://heatislands.streamlit.app
***Streamlit*** Application for displaying Land Surface Temperature in 13 European cities as part of the SpongeCity project. It also serves as the final project for ***CS50 Introduction to Computer Science***.

# Overview
The application allows users to run ***Land Surface Temperature (LST)*** analyses using ***Google Earth Engine*** API, through a user-friendly interface provided by ***Streamlit***. Users can chose out of 13 cities, and a time-span between years 2013 and 2024 to run their LST analyses. The end result is a map of the median Land Surface Temperature for the chosen city and period. To ensure robustness of analyses a minimum period of three years is required. The analyses script is using Landsat 8 satellite images and is developed by Yana Nikolova. The graphical user interface in ***Streamlit***, on the other hand is developed by Rosen Ruev. For more advanced users, a Jupyter Notebook is provided, where the whole script can be run and adjusted with Python. For the moment the application supports only 4 of the planned 13 cities. The remaining cities will be added soon, when we receive the additional data needed. 

# Description
### Framework
For this application Streamlit was used (https://streamlit.io) because it is a high level Python framework designed for sharing machine learning and data science web apps. 

### Script Integration
Yana Nikolova's script uses ***Google Earth Engine (GEE)***, a cloud computing platform with a catalog of satellite imagery and geospatial datasets , via its Python API (https://developers.google.com/earth-engine/tutorials/community/intro-to-python-api). I am using Qiusheng Wu's Python package ***Geemap*** for interactive geospatial analysis and visualization with Google Earth Engine.

## Home.py
The homepage and the entry point of the app. It initializes the Google Earth Engine python module `ee` using the `ee_authenticate()` function imported from ***helpers.py***. The function requires a Google Earth Engine token along with other data in ***JSON*** format and a `service_account` email. Both are located in a ***secrets.toml*** file which is not pushed to the remote repository and are retrieved with `st.secrets` per ***Streamlit Documentation***. The token is provided by Google Earth Engine API in a `.json` file. After that a file called ***home.html*** is rendered by `st.html()` in which I added custom CSS animation. After the button is created to link to the ***heatmap*** page an application information is displayed by reading a Markdown file using the function `read_file` from ***helpers.py***, rendered by `st.markdown()`. 

## 1_heatmap.py
This is the page where the visualization of the analysis takes place. It is located in **/pages** directory per the ***Streamlit Documentation***. First the city variables are declared as ***FeatureCollection*** objects and put in a dictionary called  `regions` with two keys ***name*** and ***geometry***. The map is created using `geemap.Map()`. `st.html()` injects a ***HTML*** string which allows using custom CSS. In this case I am using it to center the text on the page. Empty python list `options` is declared which is then populated dynamically with the names of the cities from `regions`. `st.sidebar.form()` creates a form that has a ***selectbox*** with the names of the cities form the `options` list, a ***slider*** with two values for the years and a submit button. When the form is submited a function is called named `visualize()` imported from ***helpers.py*** where the inputs are passed as arguments along with the `regions` dictionary and the `Map` object. Then the `Map` object is rendered to Streamlit with its method `Map.to_streamlit()`

## helpers.py
***helpers.py*** contains four key functions. The first one `ee_authenticate()` used in ***Home.py*** is a decorated function with `@st.cache_data` decorator which ensures that the function is ran only once when the page is opened. The function authenticates and `ee.Initialize()` the python `ee` module. The second function is `visualize()` which is called when the form in ***1_heatmap.py*** is submitted. If a City is selected and the minimum gap (3 years) between years is correct, the function calls `analyze()` from ***geoscript.py*** with the selected ***FeatureCollection***, start and end years, and the `Map` object. The next function, `verify()`, ensures that the values from the slider input are at least 3 integers apart. Since this condition is required both in `visualize()` and in ***1_heatmap.py***, I chose to implement it as a separate function for better design and reusability. The last function `readfile()` just reads a file using `Path` from the ***pathlib*** module.

## geoscript.py 
This script contains all the geo analyses needed to obtain the Land Surface Temperature. It is implemented in a function called `analyze()` used in ***helpers.py*** which takes as arguments a region of interest, start and end year and a `Map` object. For the analyses Landsat 8 Top of Atmosphere was used. Landsat's thermal bands measure the top-of-atmosphere brightness temperature. To obtain Land Surface Temperature we need to account for the emissivity of the land surface. Here we derive pixel-level emissivity as a function of the vegetation fraction of the pixel. For this, we are calculating the Normalized Difference Vegetation Index (NDVI) from the Landsat surface reflectance data.

Disclaimer: This application includes text and code snippets from google-earth-engine.com tutorial for ADVANCED TOPICS >> HUMAN APPLICATIONS >> Heat islands done by TC Chakraborty.

## error.html
A custom error if the user's start and end year inputs are not at least 3 years apart

## home.html
It is containing the custom homepage information, with and nice CSS animation.

# Potential issues
A potential issue might be that the `Map` object is passed and modified directly by the ***geoscript.py*** which may lead to bugs in the future if unintended modifications happens. 