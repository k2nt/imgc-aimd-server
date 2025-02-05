from dependency_injector import containers, providers

from server.api.controller.imgc import Resnet50Controller


class DI(containers.DeclarativeContainer):
    resnet50_controller = providers.Factory(
        Resnet50Controller
    )
