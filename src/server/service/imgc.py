from typing import List

from server.infra.image import preprocess_image_resnet
from server.infra.imgc import ImgcModel
from server.domain.entity.imgc import Classification

import numpy as np


class ImgcService:
    def classify(
            self, 
            model: ImgcModel, 
            image_bytes: bytes
    ) -> Classification:
        image_array = preprocess_image_resnet(image_bytes)
        results = model.classify(image_array)
        return results[0]
        
    def classify_batch(
            self, 
            model: ImgcModel, 
            images_bytes: List[bytes],
    ) -> List[Classification]:
        image_arrays = [preprocess_image_resnet(image_bytes) for image_bytes in images_bytes]
        batch_image_array = np.vstack(image_arrays)
        return model.classify(batch_image_array)
