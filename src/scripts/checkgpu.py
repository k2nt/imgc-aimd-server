"""Check that Tensorflow is correctly using GPU

For MacOS remember to install tensorflow-metal to make use of Apple Silicon GPU
"""
import tensorflow as tf


print("Tensorflow version:", tf.__version__)
devices = tf.config.list_physical_devices()
print("Devices: ", devices)

gpus = tf.config.list_physical_devices('GPU')
if gpus:
    details = tf.config.experimental.get_device_details(gpus[0])
    print("GPU details: ", details)