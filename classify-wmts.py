# -*- coding: utf-8 -*-

import logging, os
from landez import TilesManager
from utils.classify import classifyall, extractFeature
from skimage import io
import numpy as np

# query from the WMTS meta-data
levelsdetail = {18:(262144, 131072, 256),
                17:(131072, 65536, 256)
               }
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
# 50
tiles = tileslist(bbox=(102.7929761, 30.07529713, 102.8259933,30.12396325 ),
                  levels=[18])
# 32
#tiles = tileslist(bbox=(102.9910789, 30.2212955, 103.024096,30.26996163 ),
#                  levels=[18])


logging.getLogger().setLevel(logging.INFO)
# From a TMS tile server
# http://www.scgis.net.cn/imap/iMapServer/defaultRest/services/newtianditudom/tile/15/0/0
tm = TilesManager(tiles_url="http://www.scgis.net.cn/imap/iMapServer/defaultRest/services/newtianditudom/tile/{z}/{x}/{y}",
                  tiles_dir=".",
                  cache_scheme="wmts",
                  cache=False)
results = {}
features = []
for tile in tiles:
    tilecontent = tm.tile(tile)  # download, extract or take from cache
    with open('%s_%s_%s.png'%tile,'wb') as img:
         img.write(tilecontent)
    img = io.imread('%s_%s_%s.png'%tile)
    logging.info('Classify tile (%s_%s_%s)'%tile)
    features.append(extractFeature(img))
    os.system('del %s_%s_%s.png'%tile)
  
labels = classifyall(np.vstack(features))
results = {tile:label for tile, label in zip(tiles, labels)}

#shape=(36,25)
#labels = results.values()
#labels = np.array(labels)
#labels = labels.reshape(shape)
#imshow(labels)
#plt.colorbar()
    