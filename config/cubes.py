import pandas as pd
import numpy as np

#from sqlcollect import gettable


def makeCubes(table,region,side=5,energyRelease=False):


    #table = table

    # Force the results into float type
    latitude = [float(item) for item in table['latitude']]
    longitude = [float(item) for item in table['longitude']]
    depth = [float(item) for item in table['depth']]
    magnitude = [float(item) for item in table['magnitude']]

    # Create cubes indexes for all the dimensions
    # ------------------------------------------

    # Set min max for the dimensions
    minLat = min(latitude)
    maxLat = max(latitude)
    minLong = min(longitude)
    maxLong = max(longitude)
    minDepth = min(depth)
    maxDepth = max(depth)

    region = region
    # Find the number of cubes, given the size of the cube in km ( previously inputted )
    # Depending on region, the size of one degree lat/long differs:

    # IN VRANCEA 1 deg Lat = 111km / 1 deg Long = 79km
    if region=='vrancea' or region=='romania':
        longitudeInKm = 79

    # IN CALI 1 deg Lat = 111km / 1 deg Long = 94km
    if region=='california':
        longitudeInKm = 94

    # IN ITALY 1 deg Lat = 111km / 1 deg Long = 84km
    if region=='italy':
        longitudeInKm = 84

    # IN JAPAN 1 deg Lat = 111km / 1 deg Long = 91km
    if region=='japan':
        longitudeInKm = 91


    x = round((maxLat-minLat)*111 / side)
    y = round((maxLong-minLong)*longitudeInKm / side)
    z = round((maxDepth-minDepth) / side)

    # Create cubes indexes for all the dimensions 
    xLatitude = [int(np.floor((i-minLat)*x/(maxLat-minLat))+1) for i in latitude]
    yLongitude = [int(np.floor((i-minLong)*y/(maxLong-minLong))+1) for i in longitude]
    zDepth = [int(np.floor((i-minDepth)*z/(maxDepth-minDepth))+1) for i in depth]
    cubeIndex=[]
    # and a general cubeindex for graph formation
    for i in range(len(xLatitude)):
        cubeIndex.append(int(str(xLatitude[i])+str(yLongitude[i])+str(zDepth[i])))
        #cubeIndex.append((xLatitude[i]-1)*x+(yLongitude[i]-1)*y+zDepth[i])

    table['xLatitude']=xLatitude
    table['yLongitude']=yLongitude
    table['zDepth']=zDepth

    table['cubeIndex']=cubeIndex

    
    # Input coordinates of every cubeIndex
    cubeLatitude=[round(minLat + (side/111)*(i-1+1/2),4) for i in xLatitude]
    cubeLongitude=[round(minLong + (side/longitudeInKm)*(i-1+1/2),4) for i in yLongitude]
    cubeDepth=[round(minDepth + (side)*(i-1+1/2),4) for i in zDepth]

    table['cubeLatitude']=cubeLatitude
    table['cubeLongitude']=cubeLongitude
    table['cubeDepth']=cubeDepth


    # if energyReleas = True, add a column with the energy release converted from magnitude 
    if energyRelease:
        energyRelease=[np.power(10, 5.24 + 1.44*i) for i in magnitude]

        table['energyRelease']=energyRelease

    return table