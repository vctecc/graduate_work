from fastapi import APIRouter, Depends

from src.services import PaymentService, get_payment_auth_service, PaymentAuthenticatedService, get_payment_service
from src.schemas import NewPaymentSchema, PaymentSchema

router = APIRouter()


@router.post("/payments", status_code=201)
async def create_subscription(
        payment: NewPaymentSchema,
        payment_service: PaymentAuthenticatedService = Depends(get_payment_auth_service)
):
    await payment_service.create(payment)


@router.get("/payments", response_model=list[PaymentSchema])
async def cancel_subscription(
        payment_service: PaymentService = Depends(get_payment_service),
) -> list[PaymentSchema]:
    return await payment_service.get_processing()
