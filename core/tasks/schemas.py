from pydantic import BaseModel,Field

class Task(BaseModel):
    title: str = Field(max_length=100)
    description: str = Field(max_length=300)
    is_done: bool = Field(default=False)