"""Image classification"""

from typing import List

import keras
import numpy as np
from keras.api.applications.resnet50 import ResNet50, decode_predictions


class BaseModel:
    def __init__(self, model: keras.Model):
        self._model = model

    def predict(self, image: np.ndarray, top: int):
        return decode_predictions(self._model.predict(image), top)

    def predict_batch(self, images: List[np.ndarray], top: int):
        return decode_predictions(self._model.predict(np.vstack(images)), top)


class Resnet50Model(BaseModel):
    def __init__(self):
        super().__init__(ResNet50(weights="imagenet"))
