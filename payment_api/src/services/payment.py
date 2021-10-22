from fastapi import Depends
from sqlalchemy import select, update, desc
from sqlalchemy.orm import Session

from src.core.auth import auth
from src.db.session import get_db
from src.models import Payment, PaymentState, Customer
from src.providers import AbstractProvider, ProviderPayment, get_default_provider
from src.providers.schemas import ProviderPaymentCancel
from src.schemas.payment import AddPaymentSchema, NewPaymentSchema, NewPaymentResult, PaymentSchema, PaymentCancel
from src.schemas.subscriptions import SubscriptionSchema
from src.services.subscriptions import SubscriptionService, get_subscriptions_service


class NotFound(BaseException):
    ...


class CustomerNotFound(BaseException):
    ...


class PaymentNotFound(BaseException):
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
                Customer.id, Customer.provider_customer_id
            ).where(
                Customer.user_id == self.user_id
            )
        )
        customer = customer.first()
        if not customer:
            provider_customer = await self.provider.create_customer()
            customer = Customer(
                user_id=self.user_id,
                provider_customer_id=provider_customer.id,
            )
            self.db.add(customer)
            await self.db.flush()

        return customer

    async def new_payment(self, payment: NewPaymentSchema) -> NewPaymentResult:
        customer = await self.get_customer()
        product = await self.subscriptions.get_product(payment.product)

        provider_payment = ProviderPayment(
            amount=product.price,
            currency=payment.currency,
            customer=customer.provider_customer_id
        )
        invoice = await self.provider.new_payment(provider_payment)

        payment_db = Payment(
            customer_id=customer.id,
            invoice_id=invoice.id,
            product_id=product.id,
            status=PaymentState.PROCESSING
        )
        self.db.add(payment_db)
        await self.db.commit()

        return NewPaymentResult(id=invoice.id, client_secret=invoice.client_secret)


class PaymentService(object):

    def __init__(
            self,
            db: Session,
            provider: AbstractProvider,
            subscriptions: SubscriptionService,
    ):
        self.db = db
        self.provider = provider
        self.subscriptions = subscriptions

    async def get_payment(self, payment_id: int) -> Payment:
        return await self.db.get(Payment, payment_id)

    async def get_payment_by_invoice_id(self, invoice_id: str) -> Payment:
        payment = await self.db.execute(
            select(
                Payment.id,
                Payment.status,
                Payment.product_id,
                Customer.user_id,
            ).outerjoin(
                Customer, Payment.customer_id == Customer.id
            ).where(
                Payment.invoice_id == invoice_id
            )
        )
        if not payment:
            raise PaymentNotFound

        return payment.first()

    async def get_last_payment(self, customer_id: int) -> Payment:
        payment = await self.db.execute(
            select(
                Payment.id,
                Payment.invoice_id,
            ).where(
                Payment.customer_id == customer_id
            ).order_by(desc(Payment.id))
        )
        if not payment:
            raise PaymentNotFound

        return payment.first()

    async def get_customer(self, user_id: str) -> Customer:
        customer = await self.db.execute(
            select(
                Customer.id, Customer.provider_customer_id
            ).where(
                Customer.user_id == user_id
            )
        )

        if not customer:
            raise CustomerNotFound

        return customer.first()

    async def add_payment(self, payment: AddPaymentSchema):
        customer = await self.get_customer(payment.user_id)

        provider_payment = ProviderPayment(
            amount=payment.amount,
            currency=payment.currency,
            customer=customer.provider_customer_id
        )
        invoice = await self.provider.create_payment(provider_payment)
        # TODO: что если отправим на платеж и тут упадем?

        payment_db = Payment(
            customer_id=customer.id,
            invoice_id=invoice.id,
            product_id=payment.product_id,
            status=PaymentState.PROCESSING,
        )
        self.db.add(payment_db)
        await self.db.commit()

    async def get_processing(self) -> list[PaymentSchema]:
        processing_payments = await self.db.execute(
            select(
                Payment.id,
                Payment.invoice_id,
                Payment.product_id,
                Payment.status,
                Customer.user_id,
            ).outerjoin(
                Customer, Payment.customer_id == Customer.id
            ).where(
                Payment.status == PaymentState.PROCESSING
            )
        )
        return processing_payments.all()

    async def update_status(self, payment: PaymentSchema):
        payment_db = await self.get_payment(payment.id)
        payment_db.status = payment.status

        if payment.status == PaymentState.PAID:
            subscription = SubscriptionSchema(
                user_id=payment.user_id,
                product_id=payment.product_id,
            )
            await self.subscriptions.add_subscription(subscription)

        await self.db.commit()

    async def accept_payment(self, invoice_id):
        await self.db.execute(
            update(
                Payment
            ).values(
                status=PaymentState.PAID
            ).where(
                Payment.invoice_id == invoice_id
            )
        )

        payment = await self.get_payment_by_invoice_id(invoice_id)
        subscription = SubscriptionSchema(
            user_id=payment.user_id,
            product_id=payment.product_id,
        )
        await self.subscriptions.add_subscription(subscription)
        await self.db.commit()

    async def error_payment(self, invoice_id):
        await self.db.execute(
            update(
                Payment
            ).values(
                status=PaymentState.PAID
            ).where(
                Payment.invoice_id == invoice_id
            )
        )
        await self.db.commit()

    async def cancel(self, cancel_info: PaymentCancel):

        customer = await self.get_customer(cancel_info.user_id)
        payment = await self.get_last_payment(customer.id)

        provider_cancel = ProviderPaymentCancel(
            amount=cancel_info.amount,
            currency=cancel_info.currency,
            customer=customer.provider_customer_id,
            payment=payment.invoice_id
        )
        await self.provider.cancel(provider_cancel)


def get_payment_auth_service(
        db: Session = Depends(get_db),
        user_id: str = "",
        provider: AbstractProvider = Depends(get_default_provider),
        subscriptions: SubscriptionService = Depends(get_subscriptions_service),
):
    return PaymentAuthenticatedService(
        db=db,
        user_id=user_id,
        provider=provider,
        subscriptions=subscriptions
    )


def get_payment_service(
        db: Session = Depends(get_db),
        provider: AbstractProvider = Depends(get_default_provider),
        subscriptions: SubscriptionService = Depends(get_subscriptions_service),
):
    return PaymentService(
        db=db,
        provider=provider,
        subscriptions=subscriptions
    )
