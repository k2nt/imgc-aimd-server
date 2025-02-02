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


class Config(BaseModel):
    port: int = Field(
        default=3000, 
        ge=1024, 
        le=65535, 
        description="Port number for the server"
    )


class Context(BaseModel):
    sla: SLA

    def __init__(self, yaml_path: str):
        with open(yaml_path, "r") as f:
            data = yaml.safe_load(f)
        super().__init__(**data)
