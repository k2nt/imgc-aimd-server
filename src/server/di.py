from dependency_injector import containers, providers

from server.domain.entity.context import Context
from server.api.controller.imgc import Resnet50Controller


class DI(containers.DeclarativeContainer):
    context = providers.Factory(
        Context,
        yaml_path="src/server/ctx.yaml"
    )

    resnet50_service = providers.Factory(
        Resnet50Controller
    )
