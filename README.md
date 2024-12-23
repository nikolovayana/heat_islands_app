
# Heat Islands Application
### App link: https://heatislands.streamlit.app
***Streamlit*** Application for displaying heat island effect in 13 european cities as part of the SpongeCity project. It is also used as a final project for ***CS50 Introduction to Computer Science***.

# Overview
The application allows the user to interact in a user friendly way with Google Earth Engine script that runs analyses for heat island effect in cities. The script is developed by my partner for this project Yana Nikolova. For the moment the application allows only 4 of the 13 cities but soon when I receive the additional information needed, all cities will be added as well. Also the user can specify the time span for the analyses between the years 2013 and 2024.

# Description
For this application I decided to use Streamlit https://streamlit.io/ because it is a python high level framework that is designed to share machine learning and data science web apps. Yana's script is using Google Earth Engine, a cloud computing platform with catalog of satellite imagery and geospatial datasets , through its Python API https://developers.google.com/earth-engine/tutorials/community/intro-to-python-api and I am using Qiusheng Wu's python package "Geemap" for interactive geospatial analysis and visualization with Google Earth Engine.

## Home.py
The homepage and the entry point of the app. It initializes the Google Earth Engine python module `ee` with the `ee_authenticate()` function imported from ***helpers.py*** which takes as arguments a Google Earth Engine token along with other data in ***JSON*** format and a `service_account` email. Both are located in a ***secrets.toml*** file which is not pushed to the remote repository and are retrieved with `st.secrets` per ***Streamlit Documentation***. The token is provided by Google Earth Engine API in a `.json` file. After that a file called ***home.html*** is rendered by `st.html()`

## 1_heatmap.py
This is the page where the visualization of the analysis takes place. It is located in **/pages** directory per the ***Streamlit Documentation***. First it declares the city variables which are all ***FeatureCollection*** and puts them in a dictionary called  `regions` with two keys ***name*** and ***geometry***. The map is initialized using `geemap.Map()`. `st.html()` injects a ***HTML*** string which allows using custom CSS. In this case I am using it to center the text on the page. Empty python list `options` is declared which is then populated dynamically with the names of the cities from `regions`. `st.sidebar.form()` creates a form that has a ***selectbox*** with the names of the cities form the `options` list, a ***slider*** with two values for the years and a submit button. When the form is submited a function is called named `visualize()` imported from ***helpers.py*** where the inputs are passed as arguments along with the `regions` dictionary and the `Map` object. Then the `Map` object is rendered to Streamlit with its method `Map.to_streamlit()`

## helpers.py
In ***helpers.py*** three functions are declared. The first one `ee_authenticate()` used in ***Home.py*** is a decorated function with `@st.cache_data` decorator which ensures that the function is ran only once when the page is opened. The function authenticates and `ee.Initialize()` the python `ee` module. The second function is `visualize()` which is called when the form in ***1_heatmap.py*** is submitted. If a City is selected and the start and end year have 3 years gap between them the function passes the chosen ***FeatureCollection*** along with start and end year and the `Map` object to `analyze()` function imported from ***geoscript.py*** which modifies the `Map`. The last function, `verify()`, ensures that the values from the slider input are at least 3 integers apart. Since this condition is required both in `visualize()` and in ***1_heatmap.py***, I chose to implement it as a separate function for better design and reusability.

## geoscript.py 
This is the script developed by my partner for this project Yana Nikolova which is inplemented in a function called `analyze()` used in ***helpers.py*** which takes as arguments a region of interest, start and end year and a `Map` object. Then proceeds to analyze using the LANDSAT satellite the temperature of the pixels and visualizing the heat islands in the area of interest.

## error.html
A custom error if user's start and end year inputs are not 3 years apart

## home.html
It is containing the custom homepage information, with and nice CSS animation.

# Potential issues
One potential issue might be that the `Map` object is passed and modified directly by the geoscript which may lead to some bugs in the future. 