# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 10:41:47 2014

@author: shuaiyi
"""
import logging
from landez import TilesManager

down = False
# for tianditu-sichuan
def tileslist(bbox, levels):
    if len(bbox) != 4:
        print "Wrong format of bounding box."
    xmin, ymin, xmax, ymax = bbox
    if abs(xmin) > 180 or abs(xmax) > 180 or \
       abs(ymin) > 90 or abs(ymax) > 90:
        print "Some coordinates exceed [-180,+180], [-90, 90]."

    if xmin >= xmax or ymin >= ymax:
        print "Bounding box format is (xmin, ymin, xmax, ymax)"

    ll0 = (xmin, ymax)  # left top
    ll1 = (xmax, ymin)  # right bottom

    levelsdetail = {18:(262144, 131072, 256),
                    17:(131072, 65536, 256)
                   }
    l = []
    for z in levels:
        width = levelsdetail[z][0]
        height = levelsdetail[z][1]
        # tilesize = levelsdetail[z][2]

        for y in range(int((ll0[0]+180)/(360.0/width)),
                       int((ll1[0]+180)/(360.0/width)+1)):
            for x in range(int((90-ll0[1])/(180.0/height)),
                           int((90-ll1[1])/(180.0/height)+1)):
                l.append((z, x, y))
    return l

tiles = tileslist(bbox=(102.9910789, 30.2212955, 103.024096,30.26996163 ),
                  levels=[18])

if down:
    logging.basicConfig(level = logging.DEBUG)
    # From a TMS tile server
    # http://www.scgis.net.cn/imap/iMapServer/defaultRest/services/newtianditudom/tile/15/0/0
    tm = TilesManager(tiles_url="http://www.scgis.net.cn/imap/iMapServer/defaultRest/services/newtianditudom/tile/{z}/{x}/{y}",
                      tiles_dir=".",
                      cache_scheme="wmts",
                      cache=False)
    count = len(tiles)
    for tile in tiles:
        tilecontent = tm.tile(tile)  # download, extract or take from cache
        with open('%s_%s_%s.png'%tile,'wb') as img:
            img.write(tilecontent)
        print "Cache %s finish ..." % count
        count -= 1                  
else:
    from PIL import Image
    import numpy as np
    a = np.array(tiles)
    _, gmaxx, gmaxy = a.max(0)
    _, gminx, gminy = a.min(0)
    _,w,h = a.max(0)-a.min(0) + 1   
    # image size
    img_size = ( h * 256, w * 256 )
    large_img = Image.new('RGB', img_size)
    
    
    idx_y = 0
    for gy in range(gminy, gmaxy+1):
        idx_x = 0
        for gx in range(gminx, gmaxx+1):
            img = Image.open( '18_%s_%s.png'%( gx, gy )  ) 
            print 'Processing %s ,%s tile...' %(gx,gy)
            large_img.paste( img, ( idx_y * 256, idx_x * 256 ))
            idx_x = idx_x + 1
        idx_y = idx_y + 1
        
    large_img.save( '32.png' )