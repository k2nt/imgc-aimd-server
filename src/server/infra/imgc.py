from typing import List

import keras
import numpy as np
from keras.api.applications.resnet50 import ResNet50, decode_predictions

from server.domain.entity.imgc import Classification


class ImgcModel:
    def __init__(self, model: keras.Model):
        self._model = model

    def classify(self, image_array: np.ndarray) -> List[Classification]:
        decoded = decode_predictions(self._model.predict(image_array), top=1)

        classifications = []
        for pred in decoded:
            _, label, confidence = pred[0]
            classifications.append(Classification(label=label, confidence=confidence))

        return classifications


class Resnet50Model(ImgcModel):
    def __init__(self):
        super().__init__(ResNet50(weights="imagenet"))
