import os
import time

import numpy as np
from PIL import Image
from keras.api.applications.resnet50 import ResNet50, decode_predictions, preprocess_input
from keras.api.preprocessing import image


model = ResNet50(weights='imagenet')


def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"{func.__name__} executed in {end_time - start_time:.6f} seconds")
        return result
    return wrapper


# Function to preprocess an image
def preprocess_image(img: Image.Image):
    img = img.resize((224, 224))  # Resize image to 224x224
    img_array = image.img_to_array(img)  # Convert to array
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = preprocess_input(img_array)  # Normalize for ResNet50
    return img_array


# Function to classify an image
def classify_image(img_path: str):
    img = Image.open(img_path).convert("RGB")  # Open image and convert to RGB
    img_array = preprocess_image(img)
    preds = model.predict(img_array)  # Make predictions
    decoded_preds = decode_predictions(preds, top=1)[0]  # Decode top 3 predictions

    # Print results
    for i, (imagenet_id, label, score) in enumerate(decoded_preds):
        print(f"{i + 1}: {label} ({score:.4f})")


# Function to classify a batch of images
@timing_decorator
def classify_batch(image_folder):
    image_arrays = []
    image_paths = []

    # Load and preprocess each image in the folder
    for img_name in os.listdir(image_folder):
        img_path = os.path.join(image_folder, img_name)
        try:
            img = Image.open(img_path).convert("RGB")
            image_arrays.append(preprocess_image(img))
            image_paths.append(img_path)
        except Exception as e:
            print(f"Error loading {img_path}: {e}")

    if not image_arrays:
        print("No valid images found.")
        return

    # Stack images into a batch
    batch_array = np.vstack(image_arrays)

    # Predict for the entire batch
    predictions = model.predict(batch_array)

    # Decode predictions
    decoded_preds = decode_predictions(predictions, top=3)

    print("AAAA", decoded_preds)

    # Print results
    for i, img_path in enumerate(image_paths):
        print(f"Predictions for {img_path}:")
        for j, (imagenet_id, label, score) in enumerate(decoded_preds[i]):
            print(f"  {j + 1}: {label} ({score:.4f})")
        print("=" * 50)


@timing_decorator
def classify_sequential(image_folder):
    for img_name in os.listdir(image_folder):
        img_path = os.path.join(image_folder, img_name)
        classify_image(img_path)


SINGLE_DATASET_FOLDER = "/Users/khainguyen/Documents/work/lass/adaptive-batching/code/imgc-aimd-server-datasets/single"
CIFAR_100_DATASET_FOLDER = "/Users/khainguyen/Documents/work/lass/adaptive-batching/code/imgc-aimd-server-datasets/cifar-100-python"
CAT_DATASET_FOLDER = "/Users/khainguyen/Documents/work/lass/adaptive-batching/code/imgc-aimd-server-datasets/animal/animals/animals/cat"
ANIMAL_RANDOM_DATASET_FOLDER = "/Users/khainguyen/Documents/work/lass/adaptive-batching/code/imgc-datasets/animal/animals/animals/cat"

classify_batch(ANIMAL_RANDOM_DATASET_FOLDER)
# classify_sequential(ANIMAL_RANDOM_DATASET_FOLDER)
