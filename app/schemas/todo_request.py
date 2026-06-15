from typing import Optional
from pydantic import BaseModel, Field

class TodoRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool = Field()

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Do dishes",
                "description": "Mom is very angry at me right now.",
                "priority": 5,
                "complete": False
            }
        }
    }