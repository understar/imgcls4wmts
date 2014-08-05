# -*- coding: cp936-*-
__author__ = 'shuaiyi'

import numpy as np
import calc_tsne as tsne
import matplotlib.pyplot as plt

NEW = True

if NEW:
    data = np.loadtxt('420_X.txt', delimiter=',')
    X = tsne.calc_tsne(data)
else:
    Xmat,LM,costs=tsne.readResult()
    X=tsne.reOrder(Xmat,LM)
    
labels = np.loadtxt('420_Y.txt', delimiter=',')
plt.scatter(X[:,0], X[:,1], 20, labels)
plt.colorbar()
plt.show()
