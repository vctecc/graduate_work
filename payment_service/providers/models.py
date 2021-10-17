from pydantic import BaseModel, validator

from models.payment import PaymentState


class PaymentIntent(BaseModel):
    id: str
    amount: int
    customer: str
    status: PaymentState = ''

    @validator('status', pre=True)
    def set_status(cls, v):
        if v == 'succeeded':
            return PaymentState.PAID
        elif v == 'canceled':
            return PaymentState.CANCELED
        else:
            return PaymentState.ERROR
