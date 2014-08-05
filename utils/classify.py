# coding: cp936
import logging, os
from decaf.scripts.imagenet import DecafNet
#import numpy as np
from sklearn.externals import joblib

logging.info('Loading classifier.')
classifer = joblib.load(os.path.join(os.path.dirname(__file__),'420.pkl'))

logging.info('Loading feature extractor.')
net = DecafNet()

def extractFeature(img, blob_name='fc6_cudanet_out'):
    assert img.shape == (256, 256, 3), 'Image should be 256*256 RGB tile'
    logging.info("Extract features.")
    net.classify(img, True)
    return net.feature(blob_name)
    
    
def classifyit(img, blob_name='fc6_cudanet_out'):
    logging.info('Classify the image.')
    x = extractFeature(img, blob_name)
    return classifer.predict(x)
    
def classifyall(X):
    return classifer.predict(X)