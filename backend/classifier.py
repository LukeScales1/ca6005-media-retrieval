from datetime import datetime

import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import InceptionResNetV2
from tensorflow.keras.applications.inception_resnet_v2 import preprocess_input


IMAGENET_LABELS = {
    "filename": "ImageNetLabels.txt",
    "url": "https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt"
}


class Classifier:
    def __init__(self):
        self.model = InceptionResNetV2(weights='imagenet', input_shape=(299, 299, 3))
        self.img_dims = (299, 299)
        self.labels = self.fetch_labels()

    @staticmethod
    def fetch_labels():
        labels_path = tf.keras.utils.get_file(IMAGENET_LABELS["filename"], IMAGENET_LABELS["url"])
        imagenet_labels = np.array(open(labels_path).read().splitlines())
        return imagenet_labels[1:]  # remove first "background" label

    def get_predictions_from_url(self, img_url, class_name=None):
        if class_name is None:
            class_name = "test"
        timestamp = datetime.now().timestamp()
        img_path = tf.keras.utils.get_file(f"{class_name}-{timestamp}", origin=img_url)  # need new filename each time
        img = tf.keras.preprocessing.image.load_img(
            img_path, target_size=self.img_dims
        )
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)
        img_processed = preprocess_input(img_array)

        prediction = self.model.predict(img_processed)
        score = tf.nn.softmax(prediction[0])

