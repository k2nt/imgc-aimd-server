from typing import List

from server.infra.imgc import ImgcModel, Resnet50Model
from server.domain.entity.imgc import Classification

import numpy as np


class ImgcService:
    def __init__(self, model: ImgcModel):
        self._model = model

    def classify(
            self, 
            image_array: np.ndarray
    ) -> Classification:
        results = self._model.classify(image_array)
        return results[0]
        
    def classify_batch(
            self, 
            image_arrays: List[np.ndarray],
    ) -> List[Classification]:
        batch_image_array = np.vstack(image_arrays)
        return self._model.classify(batch_image_array)


class Resnet50Service(ImgcService):
    def __init__(self):
        super().__init__(Resnet50Model())
