from dependency_injector import containers, providers

from server.entity.context import Context


class DI(containers.DeclarativeContainer):
    context = providers.Factory(
        Context,
        yaml_path="src/server/ctx.yaml"
    )
