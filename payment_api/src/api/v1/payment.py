from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from src.providers.schemas import ProviderPaymentResult
from src.schemas.payment import (
    NewPaymentSchema, PaymentSchema,
    AddPaymentSchema, PaymentCancel, UpdatePaymentSchema,
)
from src.services.exceptions import PaymentNotFound
from src.services.payment import (
    PaymentAuthenticatedService, PaymentService,
    get_payment_auth_service, get_payment_service,
)

router = APIRouter()


@router.post(
    "/payments/new",
    status_code=201,
    response_model=ProviderPaymentResult,
    description='Проведение платежа с клиента.',
)
async def new_payment(
        payment: NewPaymentSchema,
        payment_service: PaymentAuthenticatedService = Depends(get_payment_auth_service),
) -> ProviderPaymentResult:
    return await payment_service.new_payment(payment)


@router.post(
    "/payments",
    status_code=201,
    description='Создание платежа из других сервисов.',
)
async def add_payment(
        payment: AddPaymentSchema,
        payment_service: PaymentService = Depends(get_payment_service),
):
    await payment_service.add_payment(payment)


@router.post(
    "/payments/cancel/",
    status_code=200,
    description='Возврат денег пользователю.',
)
async def cancel_payment(
        cancel_info: PaymentCancel,
        payment_service: PaymentService = Depends(get_payment_service),
) -> None:
    try:
        await payment_service.cancel(cancel_info)
    except PaymentNotFound:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Payment not found.',
        )


@router.get(
    "/payments/processing",
    response_model=list[PaymentSchema],
    description='Получение отправленных в провайдер платежей.',
)
async def get_processing_payments(
        payment_service: PaymentService = Depends(get_payment_service),
) -> list[PaymentSchema]:
    return await payment_service.get_processing()


@router.patch(
    "/payments/update_status",
    status_code=200,
    description='Обновление статуса платежа.',
)
async def update_payment_status(
        payment: UpdatePaymentSchema,
        payment_service: PaymentService = Depends(get_payment_service),
) -> None:
    try:
        await payment_service.update_status(payment)
    except PaymentNotFound:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Payment not found.',
        )
