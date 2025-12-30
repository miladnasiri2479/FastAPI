from pydantic import BaseModel, Field, field_validator

class ExpenseSchema(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        description="type name  is string"
    )
    
    amount: float = Field(
        ...,
        gt=0,
        description="amount cant lt 0"
    )
    

    @field_validator("name")
    def name_must_be_str_and_not_empty(cls, v):
        if not isinstance(v, str):
            raise ValueError("name input type not string")
        if not v.strip():  
            raise ValueError("name input cant null")
        return v.strip()
    

    @field_validator("amount")
    def round_amount(cls, v):
        return round(v, 2)
