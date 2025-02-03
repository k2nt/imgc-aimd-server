from typing import List

from server.infra.image import preprocess_image_resnet
from server.infra.imgc import ImgcModel, Resnet50Model
from server.domain.entity.imgc import Classification

import numpy as np


class ImgcService:
    def __init__(self, model: ImgcModel):
        self._model = model

    def classify(
            self, 
            image_bytes: bytes
    ) -> Classification:
        image_array = preprocess_image_resnet(image_bytes)
        results = self.model.classify(image_array)
        return results[0]
        
    def classify_batch(
            self, 
            images_bytes: List[bytes],
    ) -> List[Classification]:
        image_arrays = [preprocess_image_resnet(image_bytes) for image_bytes in images_bytes]
        batch_image_array = np.vstack(image_arrays)
        return self.model.classify(batch_image_array)


class Resnet50Service:
    def __init__(self):
        super().__init__(Resnet50Model())
