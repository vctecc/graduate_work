from http import HTTPStatus

from core import User, get_current_user
from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.subscription import SubscriptionPreview
from app.services.subscription import SubscriptionService, get_subscription_service

from .error_messag import ACTIVE_SUBSCRIPTION_NOT_FOUND

user_router = APIRouter()


@user_router.get("/subscription", response_model=SubscriptionPreview, status_code=200)
async def get_subscription(
        user: User = Depends(get_current_user),
        service: SubscriptionService = Depends(get_subscription_service)
) -> SubscriptionPreview:

    subscription = await service.get(user.id)
    if not subscription:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=ACTIVE_SUBSCRIPTION_NOT_FOUND)

    return subscription


@user_router.delete("/subscription", status_code=200)
async def cancel_subscription(
    user: User = Depends(get_current_user),
    service: SubscriptionService = Depends(get_subscription_service)
):
    subscription = await service.cancel(user.id)
    if not subscription:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=ACTIVE_SUBSCRIPTION_NOT_FOUND)


@user_router.get("/payment_method", response_model=SubscriptionPreview, status_code=200)
async def get_payment_method(
        user: User = Depends(get_current_user),
        service: SubscriptionService = Depends(get_subscription_service)
) -> SubscriptionPreview:

    subscription = await service.get(user.id)
    if not subscription:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=ACTIVE_SUBSCRIPTION_NOT_FOUND)

    return subscription
