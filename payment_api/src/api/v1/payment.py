from fastapi import APIRouter, Depends

from src.models import PaymentState
from src.providers import ProviderPaymentResult
from src.services import PaymentService, get_payment_auth_service, PaymentAuthenticatedService, get_payment_service
from src.schemas import NewPaymentSchema, PaymentSchema, NewPaymentResult

router = APIRouter()


@router.post("/payments/new", response_model=ProviderPaymentResult, status_code=201)
async def new_payment(
        payment: NewPaymentSchema,
        payment_service: PaymentAuthenticatedService = Depends(get_payment_auth_service)
) -> NewPaymentResult:
    payment = await payment_service.new_payment(payment)
    return payment


@router.get("/payments/processing", response_model=list[PaymentSchema])
async def get_processing_payments(
        payment_service: PaymentService = Depends(get_payment_service),
) -> list[PaymentSchema]:
    processing = await payment_service.get_processing()
    return processing


@router.patch("/payments/{payment_id}/status", )
async def update_payment_status(
        payment_id: int,
        status: PaymentState,
        payment_service: PaymentService = Depends(get_payment_service),
) -> None:
    await payment_service.update_status(payment_id, status)
