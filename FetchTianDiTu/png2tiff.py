import gdal,  osr
import numpy as np

levelsdetail = {18:(262144, 131072, 256),
                17:(131072, 65536, 256)
               }

def lat_lon2index(lat, lon, level): # top left corner
    width = levelsdetail[level][0]
    height = levelsdetail[level][1]
    # tilesize = levelsdetail[z][2]
    return int((lat+180)/(360.0/width)),int((90-lon)/(180.0/height))

def array2raster(newRasterfn,rasterOrigin,pixelWidth,pixelHeight,array):
    # attention: band*rows*cols 
    cols = array.shape[2]
    rows = array.shape[1]
    originX = rasterOrigin[0]
    originY = rasterOrigin[1]

    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(newRasterfn, cols, rows, 3, gdal.GDT_Byte) # single band 8bit
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
 
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromEPSG(4326) #wgs84?
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    
    outRaster.GetRasterBand(1).WriteArray(array[0,:,:][::-1])# flip it!!!
    outRaster.GetRasterBand(2).WriteArray(array[1,:,:][::-1])
    outRaster.GetRasterBand(3).WriteArray(array[2,:,:][::-1])
#    for i in range(1,4):
#        # the band sequence? rgb bgr?
#        print 'Processing band %s' % i
#        outband = outRaster.GetRasterBand(i)
#        outband.WriteArray(array[i-1,:,:])
    outRaster.FlushCache()


def main(newRasterfn,rasterOrigin,pixelWidth,pixelHeight,array):
    reversed_arr = array # [::-1] # reverse array so the tif looks like the array
    array2raster(newRasterfn,rasterOrigin,pixelWidth,pixelHeight,reversed_arr) # convert array to raster

if __name__ == "__main__":
    pixelWidth = 5.36441802978516E-06  # query from 
    pixelHeight = 5.36441802978516E-06 # http://www.scgis.net.cn/imap/iMapServer/defaultRest/services/newtianditudom

    lat, lon = (102.7929761, 30.17262938) # 30.12396325
    col, row= lat_lon2index(lat, lon, 18)
    rasterOrigin = (-180 + col*pixelWidth*256, 90 - (row+1)*pixelWidth*256)
    newRasterfn = '34.tif'
	
    array = gdal.Open('34.png').ReadAsArray()

    main(newRasterfn,rasterOrigin,pixelWidth,pixelHeight,array)	
	
# def array_to_raster(array):
    # """Array > Raster
    # Save a raster from a C order array.

    # :param array: ndarray
    # """
    # dst_filename = '/a_file/name.tiff'


    # # You need to get those values like you did.
    # x_pixels = 16  # number of pixels in x
    # y_pixels = 16  # number of pixels in y
    # PIXEL_SIZE = 3  # size of the pixel...        
    # x_min = 553648  
    # y_max = 7784555  # x_min & y_max are like the "top left" corner.
    # wkt_projection = 'a projection in wkt that you got from other file'

    # driver = gdal.GetDriverByName('GTiff')

    # dataset = driver.Create(
        # dst_filename,
        # x_pixels,
        # y_pixels,
        # 1,
        # gdal.GDT_Float32, )

    # dataset.SetGeoTransform((
        # x_min,    # 0
        # PIXEL_SIZE,  # 1
        # 0,                      # 2
        # y_max,    # 3
        # 0,                      # 4
        # -PIXEL_SIZE))  

    # dataset.SetProjection(wkt_projection)
    # dataset.GetRasterBand(1).WriteArray(array)
    # dataset.FlushCache()  # Write to disk.
    # return dataset, dataset.GetRasterBand(1)  #If you need to return, remenber to return  also the dataset because the band don`t live without dataset.