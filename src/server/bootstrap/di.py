from dependency_injector import containers, providers

from server.api.controller.imgc import Resnet50Controller
from server.infra.aimd_buffer import AIMDBuffer


class DI(containers.DeclarativeContainer):
    resnet50_controller = providers.Factory(
        Resnet50Controller
    )

    aimd_buffer = providers.Factory(
        AIMDBuffer
    )
