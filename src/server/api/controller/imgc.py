from typing import List

from server.service.imgc import Resnet50Service
from server.service.image import ImageService

from server.domain.entity.imgc import Classification


class Resnet50Controller:
    def __init__(self):
        self.imgc_svc = Resnet50Service()
        self.image_svc = ImageService()

    def classify(self, image_bytes: bytes) -> Classification:
        image_array = self.image_svc.preprocess_image_resnet(image_bytes)
        return self.imgc_svc.classify(image_array)

    def classify_batch(
            self, 
            image_bytes_list: List[bytes]
    ) -> List[Classification]:
        image_array_list = []
        for image_bytes in image_bytes_list:
            image_array_list.append(
                self.image_svc.preprocess_image_resnet(image_bytes)
            )
        return self.imgc_svc.classify_batch(image_array_list)
    