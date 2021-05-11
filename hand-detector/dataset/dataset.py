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
        self.images = np.zeros((1,self.IMAGE_SIZE*self.IMAGE_SIZE), dtype=np.uint8)
        self.keys = np.empty(1, dtype=np.str)
        self.size = 0

    def add(self, img, key):
        if self.size == 0:
            self.images[0] = np.reshape(img, (self.IMAGE_SIZE*self.IMAGE_SIZE))
            self.keys[0] = key
        else :
            print("adfs")
            img = np.reshape(img, (1, self.IMAGE_SIZE*self.IMAGE_SIZE))
            self.images = np.vstack((self.images, img))
            self.keys = np.append(self.keys, key)

        self.size += 1

    def getImages(self):
        return self.images

    def getKeys(self):
        return self.keys

def saveDataset(dataset, filename):
    data_file = open(filename, 'wb')
    pickle.dump(dataset, data_file)
    data_file.close()

def retrieveDataset(filename):
    date_file = open(filename, 'rb')
    dataset = pickle.load(data_file)
    data_file.close()
    return dataset

