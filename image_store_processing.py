import os
from glob import glob
import ntpath

IMAGE_FOLDER = ".\image_store"
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
image_store = list()
image_store_hash = dict()


class compare_files:

    #def __init__(self):
    #    self.image_store_hash = dict()

    def load_images(self):
        for img_type in ALLOWED_EXTENSIONS:
            images = glob(IMAGE_FOLDER + "/*" + img_type)
            for img in images:
                imgname = ntpath.basename(img)
                image_store.append(imgname)

        print("We have" + str(len(image_store)) + "images in the store")
        return image_store

    def generate_hash():
        print("Hello")
