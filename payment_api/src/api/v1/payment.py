from fastapi import APIRouter, Depends

from src.services import PaymentService, get_payment_auth_service, PaymentAuthenticatedService, get_payment_service
from src.schemas import NewPaymentSchema, PaymentSchema

router = APIRouter()


@router.post("/payments", status_code=201)
async def create_subscription(
        payment: NewPaymentSchema,
        payment_service: PaymentAuthenticatedService = Depends(get_payment_auth_service)
) -> None:
    await payment_service.create(payment)


@router.get("/payments/processing", response_model=list[PaymentSchema])
async def processing_payments(
        payment_service: PaymentService = Depends(get_payment_service),
) -> list[PaymentSchema]:
    return await payment_service.get_processing()


@router.patch("/payments/<payment_id>", )
async def cancel_subscription(
        payment_id: str,
        status: str,
        payment_service: PaymentService = Depends(get_payment_service),
) -> None:
    await payment_service.update_status(payment_id, status)
