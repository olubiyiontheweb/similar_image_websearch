import os
from glob import glob
import ntpath

from database_structure import database_migrations

IMAGE_FOLDER = ".\image_store"
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
image_store_hash = dict()

table_values = list()
db_ops = database_migrations()


class preprocess:
    def __init__(self):
        # image table values to insert in database
        self.images_list = dict()
        self.image_store = list()

    def load_images_into_to_db(self):
        for img_type in ALLOWED_EXTENSIONS:
            images = glob(IMAGE_FOLDER + "/*" + img_type)
            for img in images:
                imgname = ntpath.basename(img)
                # image_store.append(imgname)
                self.images_list["image_name"] = imgname
                self.images_list["storage_location"] = IMAGE_FOLDER
                self.images_list["storage_service"] = "local"
                print(self.images_list)
                db_ops.image_store_migrations()
                db_ops.insert_operations("image_store", self.images_list)

    def request_list_of_images_in_db(self):
        #images = glob(IMAGE_FOLDER + "/*" + img_type)
        images = db_ops.request_matches()
        print(images)
        for img in images:
            # get image name
            imgname = img[1]
            print(imgname)
            self.image_store.append(imgname)

        print("We have" + str(len(self.image_store)) + "images in the store")
        return self.image_store


class compare_files:
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
