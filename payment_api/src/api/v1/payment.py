from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from src.providers import ProviderPaymentResult
from src.schemas import NewPaymentResult, NewPaymentSchema, PaymentSchema
from src.schemas.payment import (AddPaymentSchema, PaymentCancel,
                                 UpdatePaymentSchema)
from src.services.payment import (PaymentAuthenticatedService, PaymentService,
                                  get_payment_auth_service,
                                  get_payment_service)

router = APIRouter()


@router.post("/payments/new",
             response_model=ProviderPaymentResult,
             status_code=201,
             description='Проведение платежа с клиента.')
async def new_payment(
        payment: NewPaymentSchema,
        payment_service: PaymentAuthenticatedService = Depends(get_payment_auth_service)
) -> NewPaymentResult:
    payment = await payment_service.new_payment(payment)
    return payment


@router.post("/payments",
             status_code=201,
             description='Создание платежа из других сервисов.')
async def add_payment(
        payment: AddPaymentSchema,
        payment_service: PaymentService = Depends(get_payment_service)
):
    await payment_service.add_payment(payment)


@router.patch("/payments/cancel/")
async def cancel_payment(
        cancel_info: PaymentCancel,
        payment_service: PaymentService = Depends(get_payment_service),
) -> None:
    await payment_service.cancel(cancel_info)  # TODO: exception


@router.get("/payments/processing", response_model=list[PaymentSchema])
async def get_processing_payments(
        payment_service: PaymentService = Depends(get_payment_service),
) -> list[PaymentSchema]:
    processing = await payment_service.get_processing()
    return processing


@router.patch("/payments/update_status", )
async def update_payment_status(
        payment: UpdatePaymentSchema,
        payment_service: PaymentService = Depends(get_payment_service),
) -> None:
    await payment_service.update_status(payment)  # TODO: exception

