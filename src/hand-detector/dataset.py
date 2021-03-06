import numpy as np

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
            self.keys = np.append(self.keys, key)
            self.keys = self.keys[1:]
        else :
            img = np.reshape(img, (1, self.IMAGE_SIZE*self.IMAGE_SIZE))
            self.images = np.vstack((self.images, img))
            self.keys = np.append(self.keys, key)

        self.size += 1

    def getSize(self):
        return self.size

    def getImages(self):
        return self.images

    def getKeys(self):
        return self.keys

