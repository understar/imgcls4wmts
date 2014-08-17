# coding: cp936
import sys
import os
import gflags
import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

SAMPLES_DIRECTORY = "samples"
gflags.DEFINE_string('samples_directory', SAMPLES_DIRECTORY, 'The directory of samples.')

FLAGS = gflags.FLAGS

IMG = None
IMGS_LIST = []
LABELS = {}
CURRENT = 0
FIG = plt.subplot()

''' label infos
1 植被覆盖
2 建设用地（道路、居民地）
3 裸地
4 水体
'''
class1 = plt.axes([0.2, 0.05, 0.1, 0.075])
class2 = plt.axes([0.41, 0.05, 0.1, 0.075])
class3 = plt.axes([0.6, 0.05, 0.1, 0.075])
class4 = plt.axes([0.81, 0.05, 0.1, 0.075])

class Index:
    def label(self, event):
        global CURRENT,IMGS_LIST, LABELS, FIG, IMG
        global class1, class2, class3, class4
        #print event
        img_name = IMGS_LIST[CURRENT]
        if event.inaxes == class1:
            LABELS[img_name] = 1
        elif event.inaxes == class2:
            LABELS[img_name] = 2
        elif event.inaxes == class3:
            LABELS[img_name] = 3
        else:
            LABELS[img_name] = 4
            
        CURRENT+=1
        if CURRENT < len(IMGS_LIST):
            IMG = cv2.imread(IMGS_LIST[CURRENT])
            FIG.clear()
            FIG.imshow(IMG)
        else:
            print LABELS
            with open('labels.txt','w') as fw:
                for k,v in LABELS.items():
                    fw.writelines([k, ',', str(v), '\n'])

if __name__ == '__main__':
    gflags.FLAGS(sys.argv)
    

    for root, dirs, files in os.walk(SAMPLES_DIRECTORY):
        for f in files:
            if f[-3:] == "png":
                IMGS_LIST.append(os.path.join(root,f))
    
    #print len(IMGS_LIST)
    
    print "Enjoy the physical labor ..."
    
    callback = Index()
    
    b1 = Button(class1, 'green')
    b1.on_clicked(callback.label)
    b2 = Button(class2, 'building')
    b2.on_clicked(callback.label)
    b3 = Button(class3, 'land(uncovered)')
    b3.on_clicked(callback.label)
    b4 = Button(class4, 'water')
    b4.on_clicked(callback.label)
    
    FIG.imshow(cv2.imread(IMGS_LIST[CURRENT]))