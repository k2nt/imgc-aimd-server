import io

import numpy as np
from PIL import Image as PILImage
from keras.api.applications.resnet import preprocess_input


def preprocess_image_resnet(image_bytes: bytes) -> np.ndarray:
    image = PILImage.open(io.BytesIO(image_bytes))
    image = image.resize((224, 224))
    image_array = np.array(image)
    image_array = np.expand_dims(image_array, axis=0)
    return preprocess_input(image_array)
