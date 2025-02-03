from pydantic import BaseModel


class Classification(BaseModel):
    label: str
    confidence: float
