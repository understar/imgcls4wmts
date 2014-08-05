# -*- coding: cp936-*-
__author__ = 'shuaiyi'

import logging, random
import numpy as np
import calc_tsne as tsne
import matplotlib.pyplot as plt
from features import dataset as ds

logging.getLogger().setLevel(logging.INFO)

NEW = False

if NEW:
    data = np.loadtxt('420_X.txt', delimiter=',')
    X = tsne.calc_tsne(data)
else:
    logging.info('Loading t_SNE results.')
    Xmat,LM,costs=tsne.readResult()
    X=tsne.reOrder(Xmat,LM)
    
logging.info('Loading data and labels.')    
data = np.loadtxt('420_X.txt', delimiter=',')
labels = np.loadtxt('420_Y.txt', delimiter=',')

logging.info('Loading samples (image path).')
data_path = "E:/Classification_service/Labelsamples/labels.txt"
samples = ds(data_path)

from skimage import io
from matplotlib.offsetbox import OffsetImage, AnnotationBbox 

ax = plt.subplot(111)
logging.info('Generating picture scatter')
for i in range(len(samples.X)):
    if random.randint(0,10) >= 5:
        img_path = ds.getImg_path(data_path, samples.X[i][0])
        logging.info('Processing %s'%img_path)
        xy = (X[i,0],X[i,1])
        arr_sam = io.imread(img_path) 
    
        imagebox = OffsetImage(arr_sam, zoom=0.1) 
        ab = AnnotationBbox(imagebox, xy, 
                            xycoords='data', 
                            pad=0, 
                            )
        ax.add_artist(ab) 


ax.grid(True)
ax.set_xlim(-60, 60)
ax.set_ylim(-60, 60)
plt.scatter(X[:,0], X[:,1], 20, labels)
plt.draw()
plt.show()