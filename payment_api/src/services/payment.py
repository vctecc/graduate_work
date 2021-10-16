from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.auth import auth
from src.db.session import get_db
from src.models import Payment, PaymentState, Customer
from src.providers import AbstractProvider, ProviderPayment, get_default_provider
from src.schemas import NewPaymentSchema, NewPaymentResult
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

    async def get_customer(self) -> Customer:
        customer = await self.db.execute(
            select(
                Customer.id, Customer.customer_id
            ).where(
                Customer.user_id == self.user_id
            )
        )
        customer = customer.first()
        if not customer:
            provider_customer = await self.provider.create_customer()
            customer = Customer(
                user_id=self.user_id,
                customer_id=provider_customer.id,
            )
            self.db.add(customer)
            await self.db.commit()

        return customer

    async def new_payment(self, payment: NewPaymentSchema) -> NewPaymentResult:

        customer = await self.get_customer()
        product = await self.subscriptions.get_product(payment.product)

        provider_payment = ProviderPayment(
            amount=product.price,
            currency=payment.currency,
            customer=customer.customer_id
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
        processing_payments = await self.db.execute(
            select(
                Payment.customer_id, Payment.invoice_id, Payment.status
            ).where(
                Payment.status == PaymentState.PROCESSING
            )
        )
        return processing_payments.all()

    async def update_status(self, payment_id, status: PaymentState):
        payment = await self.get(payment_id)
        payment.status = status
        await self.db.commit()

    async def accept_payment(self, payment_id):
        await self.update_status(payment_id, PaymentState.PAID)


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
