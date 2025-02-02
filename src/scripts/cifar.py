import pickle

import tensorflow as tf
import numpy as np
from keras.api.applications.resnet50 import preprocess_input, decode_predictions


# Function to load CIFAR-100 from a pickle file
def load_cifar100_pickle(file_path):
    with open(file_path, 'rb') as f:
        data = pickle.load(f, encoding='bytes')  # Load as a dictionary

    # Extract images and labels
    x = data[b'data']  # Image data
    y = np.array(data[b'fine_labels'])  # Fine labels

    # Reshape images from (N, 3072) → (N, 32, 32, 3)
    x = x.reshape(-1, 3, 32, 32)
    x = x.transpose(0, 2, 3, 1)
    return x, y


def load_label_names(file_path):
    with open(file_path, "rb") as f:
        label_names = pickle.load(f, encoding="bytes")[b'fine_label_names']
        label_names = [name.decode("utf-8") for name in label_names]  # Decode bytes to strings
    return label_names


# Function to preprocess CIFAR-100 images for ResNet-50
def preprocess_cifar100_images(images):
    resized_images = np.array([tf.image.resize(img, (224, 224)).numpy() for img in images])  # Resize each image
    return preprocess_input(resized_images)  # Normalize images for ResNet-50
