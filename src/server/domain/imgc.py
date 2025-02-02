import io

import numpy as np
from PIL import Image
from keras.api.preprocessing import image
from keras.api.applications.resnet import preprocess_input


def preprocess_image_resnet(raw_img) -> np.ndarray:
    img = Image.open(io.BytesIO(raw_img)).resize((224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return preprocess_input(img_array)
