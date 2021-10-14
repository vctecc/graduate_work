from http import HTTPStatus
from typing import List, Optional

from core import User, get_current_user
from fastapi import APIRouter, Depends, HTTPException, Query
from schemas import PaymentInfoIn, Subscription
from services import UserSubscriptionService, get_user_subscription_service

from .error_messag import ACTIVE_SUBSCRIPTION_NOT_FOUND

service_router = APIRouter()


@service_router.get("/subscription", response_model=Subscription, status_code=200)
async def get_subscription_for_payment(
        user: User = Depends(get_current_user),
        service: UserSubscriptionService = Depends(get_user_subscription_service)
) -> Subscription:

    subscription = await service.get(user.id)
    if not subscription:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=ACTIVE_SUBSCRIPTION_NOT_FOUND)

    return subscription
