import ee 
from ee_plugin import Map


#AUTHORS:
Yana Nikolova (yana.nikolova@plus.ac.at)
Rosen Ruev (rruev@gmail.com)


'SCRIPT CONTENT':
1. Main function with analyses
2. Import assets (shapefiles with areas of interes)
3. App User Interface 

##################################################################################################
# 1. MAIN FUNCTION WITH ANALYSES
##################################################################################################-
# Function containing the main code used for Land Surface Temperature analyses
# The function's content was adapted from google-earth-engine.com
# Chapter:      A1.5 Heat Islands
# Checkpoint:   A15b
# Author:       TC Chakraborty

def run_main(region, start, end):

    # Add layer and zoom to it in the map
    m.centerObject(regionInt,12)
    #print("regionInt",regionInt.getInfo())

    # MODIS section
    #--------------------------------------------------------------------------
    # Load MODIS image collection from the Earth Engine data catalog.
    modisLst = ee.ImageCollection('MODIS/006/MYD11A2')

    # Select the band of interest (in this case: Daytime LST).
    landSurfTemperature = modisLst.select('LST_Day_1km')

    # Create a summer filter.
    sumFilter = ee.Filter.dayOfYear(152, 243)

    # Filter the date range of interest using a date filter.
    lstDateInt = landSurfTemperature \
    .filterDate(start,end ).filter(sumFilter)

    # Take pixel-wise mean of all the images in the collection.
    lstMean = lstDateInt.mean()

    # Multiply each pixel by scaling factor to get the LST values.
    lstFinal = lstMean.multiply(0.02)

    # Generate a water mask.
    water = ee.Image('JRC/GSW1_0/GlobalSurfaceWater').select(
    'occurrence')
    notWater = water.mask().Not()

    # Clip data to region of interest, convert to degree Celsius, and mask water pixels.
    lstNewHaven = lstFinal.clip(regionInt).subtract(273.15) \
    .updateMask(notWater)


    ################
    #  CHECKPOINT MODIS SECTION  #
    ################

    # LANDSAT SECTION
    #--------------------------------------------------------------------------------
    # Function to filter out cloudy pixels.
    def cloudMask(cloudyScene):
        # Add a cloud score band to the image.
        scored = ee.Algorithms.Landsat.simpleCloudScore(cloudyScene)

        # Create an image mask from the cloud score band and specify threshold.
        mask = scored.select(['cloud']).lte(10)

        # Apply the mask to the original image and return the masked image.
        return cloudyScene.updateMask(mask)


    # Load the collection, apply cloud mask, and filter to date and region of interest.
    col = ee.ImageCollection('LANDSAT/LC08/C02/T1_TOA') \
    .filterBounds(regionInt) \
    .filterDate('2014-01-01', '2019-01-01') \
    .filter(sumFilter) \
    .map(cloudMask)

    print('Landsat collection', col.getInfo())

    # Generate median composite.
    image = col.median()

    # Select thermal band 10 (with brightness temperature).
    thermal = image.select('B10') \
    .clip(regionInt) \
    .updateMask(notWater)


    # Calculate Normalized Difference Vegetation Index (NDVI)
    # from Landsat surface reflectance.
    ndvi = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
    .filterBounds(regionInt) \
    .filterDate('2014-01-01', '2019-01-01') \
    .filter(sumFilter) \
    .median() \
    .normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI') \
    .clip(regionInt) \
    .updateMask(notWater)


    # Find the minimum and maximum of NDVI.  Combine the reducers
    # for efficiency (single pass over the data).
    minMax = ndvi.reduceRegion(
    reducer=ee.Reducer.min().combine(
    reducer2=ee.Reducer.max(),
    sharedInputs=True
    ),
    geometry=regionInt,
    scale=30,
    maxPixels=1e9
    )
    print('minMax', minMax.getInfo())

    min = ee.Number(minMax.get('NDVI_min'))
    max = ee.Number(minMax.get('NDVI_max'))

    # Calculate fractional vegetation.
    fv = ndvi.subtract(min).divide(max.subtract(min)).rename('FV')


    # Emissivity calculations.
    a = ee.Number(0.004)
    b = ee.Number(0.986)
    em = fv.multiply(a).add(b).rename('EMM').updateMask(notWater)


    # Calculate LST from emissivity and brightness temperature.
    lstLandsat = thermal.expression(
    '(Tb/(1 + (0.001145* (Tb / 1.438))*log(Ep)))-273.15', {
        'Tb': thermal.select('B10'),
        'Ep': em.select('EMM')
    }).updateMask(notWater)

    # 1.1. Selection of maps to be desplayed

    # m.addLayer(regionInt, {}, 'City boundary')

    # MODIS.
    # m.addLayer(lstNewHaven, {palette: ['blue', 'white', 'red']min: 25,max: 38},'LST_MODIS')

    # Landsat brightness temperature
    #m.addLayer(thermal, { min: 295, max: 310, palette: ['blue', 'white', 'red']},'Landsat_BT')

    # Normalized Vegetation Index
    m.addLayer(ndvi, {'min': 0, 'max': 1, 'palette': ['white', 'green', 'darkgreen']}, 'NDVI')

    # Fractional vegetaion
    #m.addLayer(fv, {min: 0, max: 1, palette: ['blue', 'white', 'green']}, 'Fractional vegetation')

    # Emissivity
    #m.addLayer(em, { min: 0.98, max: 0.99, palette: ['blue', 'white', 'green']},'EMM')

    # Land Surface Temperature
    m.addLayer(lstLandsat, {'min': 25, 'max': 35, 'palette': ['blue', 'white', 'red']},'Land Surface Temperature')


    #  -----------------------------------------------------------------------
    #  CHECKPOINT
    #  -----------------------------------------------------------------------



################################################################################################
# 2. Import assets
################################################################################################

plovdiv = ee.FeatureCollection("projects/ee-nikolova100yana/assets/SpongeCity/02_Plovdiv")
pecs = ee.FeatureCollection("projects/ee-nikolova100yana/assets/SpongeCity/03_Pecs")
salzburg = ee.FeatureCollection("projects/ee-nikolova100yana/assets/SpongeCity/04_Salzburg")
chisinau = ee.FeatureCollection("projects/ee-nikolova100yana/assets/SpongeCity/01_ChisinauMunicipality")
# ---------------------and more TO DO

# 1. User parameters   ---------------------------------------
# 1.1. Define an empty aoi variable, that will contain whatever the user selects in the UI
regionInt

# -----------------------TO DO
# Set description which will be the title of exported results
#description = ''

#------------------------------------------------------------TO DO
# 1.2. Define periods for (seasonal) composites:
# Whole year
start = '2019-11-20'
end = '2024-11-20'
#-------------------------------------------------------------

########################################################################################
# 3. APP USER INTERFACE
########################################################################################

regions = ["Chisinau","Plovdiv","Salzburg","Pecs"]
regionsReal = [
{'name': "Chisinau", 'geometry': chisinau},
{'name': "Plovdiv", 'geometry': plovdiv},
{'name': "Salzburg", 'geometry': salzburg},
{'name': "Pecs", 'geometry': pecs}
]

#/ Dropdown select menu for areas of interest
aoiSelector = ui.Select(
items=regions,
#value='Salzburg',
placeholder='Select a region',
style={
    width='190px',
},

def func_nor(selected) =
    fori in range(0, regionsReal.length, 1) =
if (regionsReal[i].name == selected) =
                    # TO DO add function that cleans all previos layers from the map
                    regionInt = regionsReal[i].geometry
                    print("Selected region",regionsReal[i].geometry.getInfo())
                    run_main(regionInt, start, end)



onChange=func_nor









)


# SLider
sliderStartDate = ui.Slider(
style={
    width='190px',
}
)

# SLider
sliderEndDate = ui.Slider(
style={
    width='190px',
}
)

labelTitle = ui.Label(
value='Heat City Mapper',
style={fontSize='24px',height='50px', fontWeight='bold'}
)

labelDescrib = ui.Label(
value="This web application will allow users to explore Land Surface Temperature and Heat Islands in a chosen city for a chosen time-frame. It is based on Landsat thermal bands. The app is part of SpongeCity project. It is still in development and curruntly only Land Surface Temperature is shown. Also only four of the 12 project's pilot sites are curruntly available. ",
style={fontSize='18px'}
)

labelAoi=ui.Label(
value='Select an Area of Interest (more partner areas will be added)',
style={fontSize='16px',height='50px', fontWeight='bold'}
)

labelDate = ui.Label(
value='Select start and end year for analyses (coming soon)',
style={fontSize='16px', height='50px', fontWeight='bold'
}
)

labelLegend = ui.Label(
value='Color Legend (coming soon)',
style={fontSize='16px', height='50px', fontWeight='bold'
}
)

# White panel to contain widgets
panel = ui.Panel(
widgets=[
labelTitle,
labelDescrib,
labelAoi,
aoiSelector,
labelDate,
sliderStartDate,
sliderEndDate,
labelLegend
],
layout=ui.Panel.Layout.flow('vertical'),
style={width='500px'}
)

ui.root.add(panel)

# #m.add(slider)

# # Create a panel with vertical flow layout.
# panel = ui.Panel(
#   layout=ui.Panel.Layout.flow('vertical'),
#   style={width='400px'}
# })

# label=ui.Label(
#   value='Select a Region of Interest =',
# })

# panel.add(label)
# panel.add(yearSelector)
# panel.add(slider)

# ui.root.add(panel)

m