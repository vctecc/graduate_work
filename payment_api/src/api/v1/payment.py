from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from src.services import SubscriptionService, get_subscription_service
from src.schemas import Payment, Subscription
router = APIRouter()


@router.post("/create-subscription",)
async def create_subscription(
        payment: Payment,
        subscription_service: SubscriptionService = Depends(get_subscription_service)
) -> Subscription:
    return subscription_service.create(payment)


@router.post("/cancel-subscription",)
async def cancel_subscription(
        subscription_service: SubscriptionService = Depends(get_subscription_service),
) -> None:
    subscription_service.cancel()
