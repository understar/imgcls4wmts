# coding: cp936
import logging, os, random
from skimage import io
import numpy as np

data_path = "E:/Classification_service/Labelsamples/labels.txt"

#def writeFeatures_labels(FEATURES, file_name):
#    f_X = open(file_name + '_X', 'w')
#    f_L = open(file_name + '_Y', 'w')
#    for feature in FEATURES:
#        f_L.writelines(feature['label'] + '\n')
#        f_X.writelines(feature['feature'].ravel().tolist().append('\n'))
#    f_X.close()
#    f_L.close()

class dataset(object):
    X=[]
    FEATURES=[]
    def __init__(self, path):
        logging.info("Loading dataset.")
        self.PATH = path
        with open(path, 'r') as f:
            # d = {key: value for (key, value) in iterable}
            self.X = [tuple(line.strip().split(',')) for line in f.readlines()]
         
    @staticmethod
    def getImg_path(data_path, record_path):
        return os.path.join(os.path.dirname(data_path),record_path)
    
    def onesample(self):
        index = random.randint(0,len(self.X))
        return self.X[index]
        
    def getsample(self, index):
        return self.X[index]
        
    def extractFeatures(self, net, blob_name):
        logging.info("Extract features.")
        for record in self.X:
            print "Extract %s" % record[0]
            img = io.imread(self.getImg_path(self.PATH, record[0]))
            # img = net.oversample(img,True) # center only
            # print net._net.predict(data = img).keys()
            net.classify(img, True)
            feature = net.feature(blob_name)
            self.FEATURES.append({\
                "name":record[0],\
                "feature":feature,\
                "label":record[1]})
        #return net._net.predict()[blob_name]
    
    def writeFeatures_labels(self, file_name):
        logging.info('Saving the features and labels.')
        labels = []
        features = []
        for feature in self.FEATURES:
            labels.append(int(feature['label']))
            features.append(feature['feature'].ravel())
        labels = np.array(labels)
        features = np.array(features)
        np.savetxt(file_name + '_X.txt', features, delimiter=',')
        np.savetxt(file_name + '_Y.txt', labels, delimiter=',')
          
if __name__ == "__main__":
    """A simple demo showing how to run decafnet."""
    from decaf.util import visualize
    from decaf.scripts.imagenet import DecafNet
    logging.getLogger().setLevel(logging.INFO)
    net = DecafNet()
    data = dataset(data_path)
    data.extractFeatures(net, 'fc6_cudanet_out')
    data.writeFeatures_labels('420')
    
    #import cv2
    #print 'prediction:', net.top_k_prediction(scores, 5)
    #visualize.draw_net_to_file(net._net, 'decafnet.png')
    #print 'Network structure written to decafnet.png'