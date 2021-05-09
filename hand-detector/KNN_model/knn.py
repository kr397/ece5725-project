import os
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

import dataset as ds

class KNN:
    def __init__ (self, neigh = 5, data_file = None, img_size = 128):
        self.neighbors = neigh
        
        if data_file is None:
            self.dataset = ds.Dataset(img_size)
        else:
            self.dataset = ds.retrieveDataset(data_file)

        self.model = KNeighborsClassifier(n_neighbors = neigh, weights = 'distance')

    def add (self, img, cmd):
        self.dataset.add(img, cmd)

    def train ():
        self.model.fit( self.dataset.getImages(), self.dataset.getKeys() )

    def enforce (self, img, cmd):
        # Add image 10 times
        for i in range(10):
            self.dataset.add(img, cmd)

    def predict (self, img):
        key = self.model.predict([img])
        return ds.getCommand(key)
