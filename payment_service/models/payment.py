from pydantic import BaseModel


class Payment(BaseModel):
    id: str
    user_id: str
    provider_user_id: str
    payment_amount: float
    status: str