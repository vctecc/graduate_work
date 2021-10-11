from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
import stripe

from src.core.auth import auth
from src.db.session import get_db
from src.models.payments import Payment, PaymentState
from src.schemas import Subscription, CustomerSchema, PaymentSchema, NewPaymentSchema
from src.models import Customer


class PaymentAuthenticatedService(object):

    def __init__(self, db: Session, user_id: str):
        self.db = db
        self.user_id = user_id

    async def get_create_customer(self) -> Customer:
        customer_db = await self.db.execute(
            select(
                Customer.provider_id
            ).where(
                Customer.user_id == self.user_id
            )
        ).all()

        if not customer_db:
            customer = stripe.Customer.create()
            customer_db = Customer(
                user_id=self.user_id,
                provider_id=customer.stripe_id
            )
            self.db.add(customer_db)
            await self.db.commit()

        return customer_db

    async def create(self, payment: NewPaymentSchema):
        customer = await self.get_create_customer()

        invoice = stripe.Invoice.create(
            customer=customer.provider_id,
            items=[{
                'product': payment.product,
                'price': payment.price,
            }],
        )

        customer_db = Payment(
            customern=customer.id,
            provider_id=invoice.stripe_id,
            status=PaymentState.PROCESSING
        )
        self.db.add(customer_db)
        await self.db.commit()


class PaymentService(object):

    def __init__(self, db: Session):
        self.db = db

    async def get(self, payment_id):
        return await self.db.get(payment_id)

    async def get_processing(self) -> list[Payment]:
        return await self.db.execute(
            select(
                Payment.provider_id, Payment.status, Payment.customer_id
            ).where(
                Payment.status == PaymentState.PROCESSING
            )
        ).all()

    async def update_status(self, payment_id, status):
        payment = await self.get(payment_id)
        payment.status = status
        await self.db.commit()


def get_payment_auth_service(
        db: Session = Depends(get_db),
        user_id: str = Depends(auth),
):
    return PaymentAuthenticatedService(db, user_id)


def get_payment_service(
        db: Session = Depends(get_db),
):
    return PaymentService(db)
