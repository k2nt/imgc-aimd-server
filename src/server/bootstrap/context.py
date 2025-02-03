"""Context"""

import yaml
from pydantic import BaseModel, Field


class SLA(BaseModel):
    max_req_latency_ms: int = Field(
        gt=0, 
        description="Maximum request latency (milliseconds)"
    )
    init_buffer_size_num_req: int = Field(
        default=5, 
        gt=0, 
        description="Initial buffer size (number of requests)"
    )


class ServerContext(BaseModel):
    port: int = Field(
        default=3000,
        description="Port number for the server"
    )


class Context(BaseModel):
    sla: SLA
    server: ServerContext


def load_context_from_yaml(yaml_path: str) -> Context:
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)
    return Context(**data)
