import numpy as np
import pickle

# KEY ENCODING
# GO: 0
# BACK: 1
# RIGHT: 2
# LEFT: 3

class Dataset:
    def __init__ (self, img_size):
        self.IMAGE_SIZE = img_size
        self.images = np.zeros((1,self.IMAGE_SIZE,self.IMAGE_SIZE), dtype=np.uint8)
        self.keys = np.zeros(1)

        self.size = 0

    def add(self, img, cmd):
        key = getKey( cmd )

        if self.size == 0:
            self.images[0] = img
            self.keys[0] = key
        else :
            np.vstack((self.images, [img]))
            np.append(self.keys, key)
    
    def getImages(self):
        return self.images

    def getKeys(self):
        return self.keys

def getKey( command ):
    pairing = {'go':0, 'back':1, 'right':2, 'left':3}
    return pairing[command]

def getCommand( key ):
    pairing = {0:'go', 1:'back', 2:'right', 3:'left'}
    return pairing[key]

def saveDataset(dataset, filename):
    data_file = open(filename, 'wb')
    pickle.dump(dataset, data_file)
    data_file.close()

def retrieveDataset(filename):
    date_file = open(filename, 'rb')
    dataset = pickle.load(data_file)
    data_file.close()
    return dataset

