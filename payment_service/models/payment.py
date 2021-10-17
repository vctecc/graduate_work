from pydantic import BaseModel


class Payment(BaseModel):
    id: str
    customer_id: str
    invoice_id: str
    status: str
