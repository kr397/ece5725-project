import os
import numpy as np
import pickle

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier

from dataset import Dataset

#MODELS = {"knn","logreg","nb"}

class Model:
    def __init__ (self,model="knn",filename = None, img_size = 128):
       
        self.IMAGE_SIZE = img_size
        if filename is None:
            # Don't retrieve dataset, create new
            self.dataset = Dataset(img_size)
        else:
            # Retrieve dataset
            data_file = open(filename, 'rb')
            self.dataset = pickle.load(data_file)
            data_file.close()

        # Initialize model
        if(model == "logreg"):
            # Logistical Regression
            self.model = LogisticRegression(random_state=0,multi_class='multinomial')
            self.model_type = 1
        elif(model == "nb"):
            # Naive Bayes
            self.model = MultinomialNB()
            self.model_type = 2
        elif(model == "dectrees"):
            # Decision Tree
            self.model = DecisionTreeClassifier()
            self.model_type = 3
        else:
            # K-Nearest Neighbors
            self.model = KNeighborsClassifier(n_neighbors = 5, weights = 'distance')
            self.model_type = 0

    def check_dataset (self):
        if(self.model_type == 0):
            neigh = self.model.get_params()['n_neighbors']
            print( neigh )
            
            size = self.dataset.getSize()
            print( size )
            return neigh < size
        else:
            return True
            
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
        if(self.check_dataset()):
            img = np.reshape(img, (self.IMAGE_SIZE*self.IMAGE_SIZE))
            key = self.model.predict([img])
            return key
        else:
            return ""

    def save(self, filename):
        data_file = open(filename, 'wb')
        pickle.dump(self.dataset, data_file)
        data_file.close()