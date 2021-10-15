from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.auth import auth
from src.db.session import get_db
from src.models.payments import Payment, PaymentState
from src.providers import AbstractProvider, ProviderPayment, ProviderPaymentResult, get_default_provider
from src.schemas import NewPaymentSchema, CustomerSchema
from src.schemas.payment import NewPaymentResult
from src.services.subscriptions import SubscriptionService, get_subscriptions_service


class NotFound(BaseException):
    ...


class PaymentAuthenticatedService(object):

    def __init__(
            self,
            db: Session,
            user_id: str,
            provider: AbstractProvider,
            subscriptions: SubscriptionService,
    ):
        self.db = db
        self.user_id = user_id
        self.provider = provider
        self.subscriptions = subscriptions

    async def get_customer(self) -> CustomerSchema:
        customer = await self.subscriptions.get_customer(self.user_id)
        if not customer:
            customer = await self.provider.create_customer()

        return customer

    async def new_payment(self, payment: NewPaymentSchema) -> NewPaymentResult:

        customer = await self.get_customer()
        price = await self.subscriptions.get_product_price(payment.product)

        provider_payment = ProviderPayment(
            amount=price,
            currency=payment.currency,
            customer=customer.id
        )
        invoice = await self.provider.create_payment(provider_payment)

        payment_db = Payment(
            customer_id=customer.id,
            invoice_id=invoice.id,
            status=PaymentState.PROCESSING
        )
        self.db.add(payment_db)
        await self.db.commit()

        return NewPaymentResult(id=invoice.id, client_secret=invoice.client_secret)


class PaymentService(object):

    def __init__(self, db: Session):
        self.db = db

    async def get(self, payment_id: int) -> Payment:
        return await self.db.get(Payment, payment_id)

    async def get_processing(self) -> list[Payment]:
        proccessing_payments = await self.db.execute(
            select(
                Payment.customer_id, Payment.invoice_id, Payment.status
            ).where(
                Payment.status == PaymentState.PROCESSING
            )
        )
        return proccessing_payments.all()

    async def update_status(self, payment_id, status: PaymentState):
        payment = await self.get(payment_id)
        payment.status = status
        await self.db.commit()


def get_payment_auth_service(
        db: Session = Depends(get_db),
        user_id: str = "",
        provider: AbstractProvider = Depends(get_default_provider),
        subscriptions: SubscriptionService = Depends(get_subscriptions_service)
):
    return PaymentAuthenticatedService(
        db=db,
        user_id=user_id,
        provider=provider,
        subscriptions=subscriptions
    )


def get_payment_service(
        db: Session = Depends(get_db),
):
    return PaymentService(db)
