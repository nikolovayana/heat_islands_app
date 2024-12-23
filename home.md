### Deriving Land Surface Temperature from Landsat

Disclaimer: This application includes text and code snippets from google-earth-engine.com tutorial for ADVANCED TOPICS >> HUMAN APPLICATIONS >> Heat islands done by TC Chakraborty

Chapter:      A1.5 Heat Islands
Checkpoint:   A15b
Author:       TC Chakraborty

Landsat's thermal bands use the thermal infrared longwave radiation to measure the top-of-atmosphere brightness temperature.(Reiners et al. 2023) Brightness temperature is the temperature equivalent of the infrared radiation escaping the top of the atmosphere, assuming the Earth to be a black body. It is not the same as the land surface temperature (LST), which requires accounting for atmospheric absorption and re-emission, as well as the emissivity of the land surface. The surface emissivity (ε) of a material is the effectiveness with which it can emit thermal radiation compared to a black body at the same temperature and can range from 0 (for a perfect reflector) to 1 (for a perfect absorber and emitter). Since the thermal radiation captured by satellites is a function of both LST and ε, you need to accurately prescribe or estimate ε to get to the correct LST. One way to derive pixel-level emissivity is as a function of the vegetation fraction of the pixel (Malakar et al. 2018). For this, we are calculating the Normalized Difference Vegetation Index (NDVI) from the Landsat surface reflectance data.

It's important to note that Landsat is a polar-orbiting satelllite and it can only provide instantaneous measurements, which do not represent the daily progress of the LST. Thus it is very important to keep in mind the time of image acquisition which might not correspond to the hottest time of the day. Furthurmore, since Landsat images are acquired once every 16 days, this means that the hottest day of the year might nor be captured. 