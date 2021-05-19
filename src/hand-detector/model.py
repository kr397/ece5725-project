""" 
ECE 5725 Spring 2021
Final Project

PiDog
Aryaa Pai (avp34) and Krithik Ranjan (kr397)

Model class to handle ML for hand gesture classification. 
""" 

# Import global libraries
import os
import numpy as np
import pickle
# Sci-kit learn models
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
# Open CV
import cv2
# Import local modules
from dataset import Dataset

""" 
Model
Class to encapsulate ML models for hand gesture classification.

IMAGE_SIZE: constant for image size
model: model object from sklearn (KNeighbors Classifier, Logistic Regression, Multinomial Naive Bayes, Decision Tree)
model_type: identifier of the type of model
dataset: dataset object 
"""
class Model:
    """ 
    Constructor
    Default set to KNN, 128-size image, and create new dataset
    """
    def __init__ (self,model="knn",filename = None, img_size = 128):
       
        self.IMAGE_SIZE = img_size

        # Initialize model
        if(model == "logreg"):
            # Logistical Regression
            self.model = LogisticRegression(random_state=0,multi_class='multinomial',solver='newton-cg')
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

        if filename is None:
            # Don't retrieve dataset, create new
            self.dataset = Dataset(img_size)
        else:
            # Retrieve dataset
            data_file = open(filename, 'rb')
            self.dataset = pickle.load(data_file)
            data_file.close()
            # Fit the older model
            self.model.fit( self.dataset.getImages(), self.dataset.getKeys() )
            
    """ 
    add(img, cmd)
    Add new image with its command to dataset
    img: image
    cmd: command
    """
    def add (self, img, cmd):
        self.dataset.add(img, cmd)
        # Print for confirmation
        print(self.dataset.getKeys())

    """ 
    train()
    Function to train the model
    """
    def train (self):
        self.model.fit( self.dataset.getImages(), self.dataset.getKeys() )

    """ 
    enforce(img, cmd)
    Function for enforcement of correct classification by adding the element
    to dataset multiple times
    img: image
    cmd: command
    """
    def enforce (self, img, cmd):
        # Add image 10 times
        for i in range(10):
            self.dataset.add(img, cmd)

    """ 
    predict(img)
    Function to obtain the classification of the imput image
    img: image
    """
    def predict (self, img):
        try:
            # Predict and return associated command
            img = np.reshape(img, (self.IMAGE_SIZE*self.IMAGE_SIZE))
            key = self.model.predict([img])
            return key[0]
        except:
            # Dataset is not big enough to predict
            return ""

    """ 
    save(filename)
    Function to save the current dataset to file
    filename: name of the file
    """
    def save(self, filename):
        data_file = open(filename, 'wb')
        pickle.dump(self.dataset, data_file)
        data_file.close()