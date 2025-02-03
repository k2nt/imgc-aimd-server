"""Context"""

import yaml
from pydantic import BaseModel, Field


class SLA(BaseModel):
    max_latency_ms: int = Field(
        description='Maximum request latency (milliseconds)',
        gt=0, 
    )


class ServerContext(BaseModel):
    port: int = Field(
        description='Port number for the server',
        default=3000,
    )


class AIMDBufferContext(BaseModel):
    init_capacity_num_req: int = Field(
        description='Initial buffer capacity (number of requests)',
        default=5, 
        gt=0, 
    )

    incr_amt: int = Field(
        description='AIMD incremental amount',
        default=1, 
        gt=0, 
    )

    decr_fct: float = Field(
        description='AIMD decrement factor',
        default=0.9, 
        lt=1,
        gt=0, 
    )


class Context(BaseModel):
    sla: SLA
    server: ServerContext
    aimd_buffer: AIMDBufferContext


def load_context_from_yaml(yaml_path: str) -> Context:
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)
    return Context(**data)
