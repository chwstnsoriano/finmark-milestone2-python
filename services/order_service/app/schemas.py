from pydantic import BaseModel, Field


class OrderCreate(BaseModel):
    customer_name: str = Field(
        min_length=1,
        max_length=120,
    )
    customer_email: str = Field(
        min_length=3,
        max_length=255,
    )
    client_type: str = Field(
        min_length=1,
        max_length=80,
    )
    service_id: int = Field(gt=0)
    order_notes: str = Field(
        default="",
        max_length=1000,
    )