from pydantic import BaseModel


class PaidFacility(BaseModel):
    user_id: str
    provider_user_id: str
    payment_amount: float