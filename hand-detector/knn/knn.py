import os
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

from dataset import dataset as ds


class KNN:
    def __init__ (self, neigh = 5, data_file = None, img_size = 128):
        self.neighbors = neigh
        self.IMAGE_SIZE = img_size
        if data_file is None:
            self.dataset = ds.Dataset(img_size)
        else:
            self.dataset = ds.retrieveDataset(data_file)

        self.model = KNeighborsClassifier(n_neighbors = neigh, weights = 'distance')

    def add (self, img, cmd):
        self.dataset.add(img, cmd)
        print(self.dataset.getImages().shape)
        print(self.dataset.getKeys().shape)

    def train (self):
        self.model.fit( self.dataset.getImages(), self.dataset.getKeys() )

    def enforce (self, img, cmd):
        # Add image 10 times
        for i in range(10):
            self.dataset.add(img, cmd)

    def predict (self, img):
        img = np.reshape(img, (self.IMAGE_SIZE*self.IMAGE_SIZE))
        key = self.model.predict([img])
        return key

    def save(self, filename):
        ds.saveDataset(self.dataset, filename)
