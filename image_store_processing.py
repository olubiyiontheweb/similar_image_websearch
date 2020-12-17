from skimage.metrics import structural_similarity as ssim
from glob import glob
from PIL import Image
import numpy as np
import ntpath
import dhash
import cv2

from database_structure import database_migrations

IMAGE_FOLDER = "./image_store"
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
image_store_hash = dict()
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
                values = imgname, IMAGE_FOLDER, "local"
                print(values)
                db_ops.image_store_migrations()
                # TODO Abstract requests and insert from database
                db_ops.insert_operations("image_store", values)

    def request_list_of_images_in_db(self):
        # images = glob(IMAGE_FOLDER + "/*" + img_type)
        images = db_ops.request_matches("image_store")
        print("list from database" + str(images))
        self.image_store.clear()
        self.images_list.clear()
        for img in images:
            # get image name
            print("current list" + str(self.image_store))
            self.images_list["image_id"] = img[0]
            self.images_list["image_name"] = img[1]
            print("Check the values" + str(self.images_list))
            self.image_store.append(self.images_list.copy())
            print("Check the images" + str(self.image_store))

        print("We have" + str(len(self.image_store)) + "images in the store")
        print(self.image_store)
        return self.image_store

    def generate_hash(self):
        images_in_db = self.request_list_of_images_in_db()

        print(images_in_db)

        for img in images_in_db:
            image = Image.open(IMAGE_FOLDER + "\\" + img["image_name"])
            row, col = dhash.dhash_row_col(image)
            img_hash = dhash.format_hex(row, col)
            values = img_hash, img["image_id"]
            db_ops.image_store_migrations()
            print(values)
            db_ops.insert_operations("image_store_hash", values)


class compare_files:
    def __init__(self):
        # image table values to insert in database
        self.images_list = dict()
        self.image_store = list()

    def request_image_hashes(self):
        images = db_ops.request_matches("image_store_hash")
        print("list from database" + str(images))
        self.image_store.clear()
        self.images_list.clear()
        for img in images:
            # get image name
            print("current list" + str(img))
            self.images_list["image_hash"] = img[1]
            # request image name from image store database
            img_name = db_ops.conditional_request_matches(
                "image_store", img[2], "image_name", "image_id")
            self.images_list["image_name"] = img_name[0][0]
            print("Check the values" + str(self.images_list))
            self.image_store.append(self.images_list.copy())
            print("Check the images" + str(self.image_store))

        print("We have" + str(len(self.image_store)) + "images in the store")
        print(self.image_store)

        return self.image_store

    def calculate_hamming_dist(self, uploaded_hash, db_store_hash):
        i = 0
        count = 0

        while (i < len(uploaded_hash)):
            if (uploaded_hash[i] != db_store_hash[i]):
                count += 1
            i += 1
        return count

    def mean_squared_error(self, uploaded_image, db_store_image):
        # the 'Mean Squared Error' between the two images is the
        # sum of the squared difference between the two images;
        # NOTE: the two images must have the same dimension
        err = np.sum((uploaded_image.astype("float") -
                      db_store_image.astype("float"))**2)
        err /= float(uploaded_image.shape[0] * uploaded_image.shape[1])

        # return the MSE, the lower the error, the more "similar"
        # the two images are
        return err

    def structural_similarity_index(self, uploaded_image, db_store_image):
        ssim_index = ssim(uploaded_image, db_store_image)

        return ssim_index

    def convert_and_resize_compare(self, uploaded_image, db_store_image):
        # TODO: make structural similarity and mean squared error functionals

        uploaded_image = cv2.imread(uploaded_image)
        db_store_image = cv2.imread(db_store_image)

        uploaded_image = cv2.resize()
        db_store_image = cv2.resize()

        uploaded_image = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)
        db_store_image = cv2.cvtColor(db_store_image, cv2.COLOR_BGR2GRAY)

        mean_sq_error = self.mean_squared_error(uploaded_image, db_store_image)
        ssim_index = self.structural_similarity_index(uploaded_image,
                                                      db_store_image)

        return ssim_index, mean_sq_error
