import geemap.foliumap as geemap
import ee


def analyze(regionInt, start_year, end_year, m):
    ''' AUTHORS:
    Yana Nikolova (yana.nikolova@plus.ac.at)
    Rosen Ruev (rosenruev@gmail.com)


    'SCRIPT CONTENT':
    1. Import assets (shapefiles with areas of interest)
    2. User defined variables
    3. Main code with analyses
    '''
    ################################################################################################
    # 1. Import assets
    ################################################################################################
    # plovdiv = ee.FeatureCollection("projects/ee-nikolova100yana/assets/SpongeCity/02_Plovdiv")
    # pecs = ee.FeatureCollection("projects/ee-nikolova100yana/assets/SpongeCity/03_Pecs")
    # salzburg = ee.FeatureCollection("projects/ee-nikolova100yana/assets/SpongeCity/04_Salzburg")
    # chisinau = ee.FeatureCollection("projects/ee-nikolova100yana/assets/SpongeCity/01_ChisinauMunicipality")
    # ---------------------and more TO DO

    ################################################################################################
    # 2. User defined variables
    ################################################################################################
    # Area of analyses
    # regionInt = plovdiv

    # Period of analyses
    # start = '2014-01-01'
    # end = '2019-01-01'

    start = str(start_year) + '-01-01'
    end = str(end_year) + '-01-01'
    #-------------------------------------------------------------

    ##################################################################################################
    # 1. MAIN FUNCTION WITH ANALYSES
    ##################################################################################################-
    # Function containing the main code used for Land Surface Temperature analyses
    # The function's content was adapted from google-earth-engine.com
    # Chapter:      A1.5 Heat Islands
    # Checkpoint:   A15b
    # Author:       TC Chakraborty

    # Add layer and zoom to it in the map
    # m = geemap.Map(basemap='HYBRID')
    m.centerObject(regionInt,12)
    #print("regionInt",regionInt.getInfo())

    # Create a summer filter. This filter takes the range of dates of the year for which analyses will be done
    sumFilter = ee.Filter.dayOfYear(152, 243)

    # Generate a water mask.
    water = ee.Image('JRC/GSW1_0/GlobalSurfaceWater').select('occurrence')
    notWater = water.mask().Not()

    # ------------------------------------------------------------------------------
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
    .filterDate(start, end) \
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

    # 1.1. Selection of maps to be displayed

    # m.addLayer(regionInt, {}, 'City boundary')

    # Landsat brightness temperature
    #m.addLayer(thermal, { min: 295, max: 310, palette: ['blue', 'white', 'red']},'Landsat_BT')

    # Normalized Vegetation Index
    # m.addLayer(ndvi, {'min': 0, 'max': 1, 'palette': ['white', 'green', 'darkgreen']}, 'NDVI')

    # Fractional vegetation
    #m.addLayer(fv, {min: 0, max: 1, palette: ['blue', 'white', 'green']}, 'Fractional vegetation')

    # Emissivity
    #m.addLayer(em, { min: 0.98, max: 0.99, palette: ['blue', 'white', 'green']},'EMM')

    # Land Surface Temperature
    m.addLayer(lstLandsat, {'min': 25, 'max': 35, 'palette': ['blue', 'white', 'red']},'Land Surface Temperature')
    vis_params = {
    'min': 25,
    'max': 35,
    'palette': ['blue', 'white', 'red']}
    m.add_colorbar(vis_params, label ="Land Surface Temperature", layer_name="lstLandsat")
    #  -----------------------------------------------------------------------
    #  CHECKPOINT
    #  -----------------------------------------------------------------------