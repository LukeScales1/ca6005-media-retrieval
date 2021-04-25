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
        self.labels = self.fetch_labels(labels_to_fix={"cock": "cockerel", "drake": "drake duck"})

    @staticmethod
    def fetch_labels(labels_to_fix: dict = None):
        labels_path = tf.keras.utils.get_file(IMAGENET_LABELS["filename"], IMAGENET_LABELS["url"])
        imagenet_labels = np.array(open(labels_path).read().splitlines())
        imagenet_labels = imagenet_labels[1:]  # remove first "background" label
        if labels_to_fix is not None:
            for k in labels_to_fix.keys():
                fix_index = list(imagenet_labels).index(k)
                imagenet_labels[fix_index] = labels_to_fix[k]

        return imagenet_labels

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
        # score = tf.nn.softmax(prediction[0])
        return prediction

    @staticmethod
    def get_image_class_relevance(label_index, prediction):
        """This ranking will be used to sort images by relevance with 1 being the most relevant."""
        for i in range(5):
            results = tf.math.in_top_k(
                [label_index], prediction, i, name=None
            )
            if results[0]:
                return i
        return 10  # return 10 if not in top 5 - will be easier to sort or filter

    def get_relevance_score(self, class_name, img_url):
        label_index = list(self.labels).index(class_name)
        prediction = self.get_predictions_from_url(img_url, class_name)
        return self.get_image_class_relevance(label_index, prediction)
