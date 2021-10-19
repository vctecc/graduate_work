from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from src.models import PaymentState
from src.providers import ProviderPaymentResult
from src.schemas.payment import AddPaymentSchema
from src.services import PaymentService, get_payment_auth_service, PaymentAuthenticatedService, get_payment_service
from src.schemas import NewPaymentSchema, PaymentSchema, NewPaymentResult
from src.services.payment import CustomerNotFound

router = APIRouter()


@router.post("/payments", status_code=201)
async def new_payment(
        payment: AddPaymentSchema,
        payment_service: PaymentService = Depends(get_payment_service)
):
    try:
        await payment_service.add_payment(payment)
    except CustomerNotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='Customer with given user id not found.')


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


@router.patch("/payments/update_status", )
async def update_payment_status(
        payment: PaymentSchema,
        payment_service: PaymentService = Depends(get_payment_service),
) -> None:
    await payment_service.update_status(payment)  # TODO: exception


@router.patch("/payments/{payment_id}/accept")
async def update_payment_status(
        payment_id: str,
        payment_service: PaymentService = Depends(get_payment_service),
) -> None:
    await payment_service.accept_payment(payment_id)  # TODO: exception


@router.patch("/payments/{payment_id}/error")
async def update_payment_status(
        payment_id: str,
        payment_service: PaymentService = Depends(get_payment_service),
) -> None:
    await payment_service.error_payment(payment_id)  # TODO: exception
