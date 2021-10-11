from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
import stripe

from src.core.auth import auth
from src.db.session import get_db
from src.schemas import Subscription, CustomerSchema
from src.models import Customer


class SubscriptionService(object):

    def __init__(self, db: Session, user_id: str):
        self.db = db
        self.user_id = user_id

    async def get_create_customer(self) -> CustomerSchema:
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

        return CustomerSchema(customer_db)

    async def create(self, payment) -> Subscription:
        price_id = payment.priceId

        customer = self.get_create_customer()

        subscription = stripe.Subscription.create(
            customer=customer.provider_id,
            items=[{
                'price': price_id,
            }],
            payment_behavior='default_incomplete',
            expand=['latest_invoice.payment_intent'],
        )
        return Subscription(subscriptionId=subscription.id,
                            clientSecret=subscription.latest_invoice.payment_intent.client_secret)

    async def cancel(self, user_id):
        subscription = self.get_user_subscription(user_id)
        stripe.Subscription.delete(subscription.subscriptionId)


def get_subscription_service(
        db: Session = Depends(get_db),
        user_id: str = Depends(auth),
):
    return SubscriptionService(db, user_id)
